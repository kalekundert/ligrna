#!/usr/bin/env python3

import primer3
import itertools
from sgrna_helper import reverse_complement

class Overlap:

    def __init__(self, construct, start, end):
        """
        Primers are specified by giving start and stop indices into another 
        sequence.  If the start index is less than the end index, the primer 
        will be taken directly from the associated sequence.  If the start 
        index in greater than the end index, the primer will be taken to be the 
        reverse complement of the associated sequence.
        """

        assert start != end

        self._construct = construct
        self._start = start
        self._end = end

        if start < end:
            self._sequence = construct.dna[start:end]
        else:
            self._sequence = reverse_complement(construct.dna[end:start])

        self._melting_temp = primer3.calcTm(
                self._sequence, tm_method='breslauer')

        self._gc_content = sum(x in 'GC' for x in self._sequence) / len(self)
        left_gc_count = sum(x in 'GC' for x in self._sequence[:5])
        right_gc_count = sum(x in 'GC' for x in self._sequence[-5:])
        self.has_gc_clamp = \
                (1 <= left_gc_count <= 3) and (1 <= right_gc_count <= 3)

    def __str__(self):
        return self._sequence

    def __len__(self):
        return len(self._sequence)

    @property
    def construct(self):
        return self._construct

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def length(self):
        return len(self)
    
    @property
    def sequence(self):
        return self._sequence

    @property
    def reverse_complement(self):
        return reverse_complement(self._sequence)

    @property
    def melting_temp(self):
        return self._melting_temp

    @property
    def tm(self):
        return self._melting_temp

    @property
    def gc_content(self):
        return self._gc_content

    def show(self, style=None, color='auto'):
        self.construct.show(
                style=style,
                start=min(self.start, self.end),
                end=max(self.end, self.start),
                dna=True,
                rev_com=(self.start > self.end),
                color=color,
        )


class PcrAssembly:

    def __init__(self):
        self.max_num_primers = 0
        self.min_primer_len = 40
        self.max_primer_len = 50
        self.min_overlap_len = 18
        self.max_overlap_len = 22
        self.min_overlap_tm = 52
        self.max_overlap_tm = 58
        self.max_gc_content = 0.6
        self.min_gc_content = 0.3
        self.max_tm_diff = 2.0
        self.use_color = 'auto'

    def find_primers(self, construct):
        self._construct = construct
        self._find_overlaps()
        self._find_overlap_chains()
        self._find_primer_chains()
        return self

    def print_primers(self, header_only=False):
        chains = zip(self._overlap_chains, self._primer_chains)
        num_chains = len(self._overlap_chains)
        chain_id = 1

        print('Found {} sets of primers for assembling the following construct:'.format(num_chains))
        print()
        self._construct.show(color=self.use_color)
        print()
        print('Using the following parameters:')
        print()
        print('  max_num_primers = {}'.format(self.max_num_primers))
        print('  min_primer_len = {}'.format(self.min_primer_len))
        print('  max_primer_len = {}'.format(self.max_primer_len))
        print('  min_overlap_len = {}'.format(self.min_overlap_len))
        print('  max_overlap_len = {}'.format(self.max_overlap_len))
        print('  min_overlap_tm = {}'.format(self.min_overlap_tm))
        print('  max_overlap_tm = {}'.format(self.max_overlap_tm))
        print('  max_gc_content = {}'.format(self.max_gc_content))
        print('  min_gc_content = {}'.format(self.min_gc_content))
        print('  max_tm_diff = {}'.format(self.max_tm_diff))
        print()

        if header_only or num_chains == 0:
            return

        print('─' * 79)
        print()

        for overlap_chain, primer_chain in chains:
            print("Primer Set #{}:".format(chain_id)); chain_id += 1
            print()

            for primer in primer_chain:
                primer.show(color=self.use_color)

            print()

            for i, overlap in enumerate(overlap_chain, 1):
                overlap_stats = 'Overlap {0}: Length = {1.length}, Tm = {1.tm:5.2f}°C, GC% = {1.gc_content:4.2f}'
                print(overlap_stats.format(i, overlap))

            print()

            for i, primer in enumerate(primer_chain, 1):
                primer_seqs = 'Primer {0}: Length = {1.length}, {1.sequence}'
                print(primer_seqs.format(i, primer))

            print()

            def find_expected_price():
                expected_price = 0

                for primer in primer_chain:
                    if len(primer) <= 50:
                        expected_price += 0.17 * len(primer)
                    elif len(primer) <= 60:
                        expected_price += 0.25 * len(primer)
                    elif len(primer) <= 80:
                        expected_price += 0.60 * len(primer)
                    else:
                        expected_price += 1.10 * len(primer)

                return expected_price

            print('Expected Price: ${:.2f}'.format(find_expected_price()))
            print()
            print('─' * 79)
            print()

    def _find_overlaps(self):
        # Create a data structure to hold all of the acceptable overlap 
        # regions.  Specifically, these regions must have an acceptable length 
        # and an acceptable melting temperature.  The data structure is a 2D 
        # array because later on it will be important to be able to skip to 
        # overlaps that are offset by approximately the right amount.

        self._overlaps = [[] for i in self._construct.indices]

        # For each position in the construct, find every acceptable overlap 
        # starting at that position.

        for i in self._construct.indices:
            for l in range(self.min_overlap_len, self.max_overlap_len):
                overlap = Overlap(self._construct, i, i + l)

                # Make sure the overlap has an acceptable melting temp.

                if overlap.tm < self.min_overlap_tm:
                    continue
                if overlap.tm > self.max_overlap_tm:
                    continue

                # Make sure the overlap has an acceptable GC content.

                if overlap.gc_content < self.min_gc_content:
                    continue
                if overlap.gc_content > self.max_gc_content:
                    continue

                # Make sure the overlap has a GC pair on its 3' end.

                if not overlap.has_gc_clamp:
                    continue
                
                # Add this overlap to the list of acceptable overlaps.

                self._overlaps[i].append(overlap)

    def _find_overlap_chains(self):
        self._overlap_chains = []
        self._find_overlap_chains_recurse([])

    def _find_overlap_chains_recurse(self, overlap_chain):
        primer_start = overlap_chain[-1].start if overlap_chain else 0
        min_primer_end = primer_start + self.min_primer_len
        max_primer_end = primer_start + self.max_primer_len
        min_overlap_start = max(
                min_primer_end - self.max_overlap_len,
                overlap_chain[-1].end + 1 if overlap_chain else 0)
        max_overlap_start = max_primer_end - self.min_overlap_len

        # If the end of the construct falls before the closest possible primer 
        # end, then the last primer in this chain will be too short and this 
        # chain has to be pruned.

        if min_primer_end > len(self._construct):
            return

        # If the end of the construct falls between the closest and furthest 
        # possible primer ends, then this is a viable chain.  Add it to the 
        # list of chains and return.

        if min_primer_end <= len(self._construct) <= max_primer_end:
            self._overlap_chains.append(overlap_chain)
            return

        # If the number of primers required for this chain is greater than the 
        # maximum allowable, prune the chain.

        if self.max_num_primers is not 0:
            if len(overlap_chain) + 1 >= self.max_num_primers:
                return

        def tm_matches_chain(overlap):
            for previous_overlap in overlap_chain:
                if abs(overlap.tm - previous_overlap.tm) > self.max_tm_diff:
                    return False
            return True

        for overlap_start in range(min_overlap_start, max_overlap_start):
            for overlap in self._overlaps[overlap_start]:
                if tm_matches_chain(overlap):
                    self._find_overlap_chains_recurse(overlap_chain+[overlap])

    def _find_primer_chains(self):
        self._primer_chains = []

        for overlap_chain in self._overlap_chains:
            primer_chain = []
            halfway_point = (len(overlap_chain) + 1) // 2
            previous_start = 0

            for i, overlap in enumerate(overlap_chain):

                # Decide which direction the primer should face.

                start, end = previous_start, overlap.end
                if i >= halfway_point: start, end = end, start

                # Construct the primer.

                primer = Overlap(self._construct, start, end)
                primer_chain.append(primer)
                previous_start = overlap.start

            primer = Overlap(self._construct, len(self._construct), previous_start)
            primer_chain.append(primer)
            self._primer_chains.append(primer_chain)



def design_assembly_primers(construct):
    return PcrAssembly().find_primers(construct)


