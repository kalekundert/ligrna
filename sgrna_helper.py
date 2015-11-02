#!/usr/bin/env python3

import nonstdlib
import collections
import random

class Sequence:
    """
    Abstract base class that represents a sequence that's associated with a 
    name and provides some convenience functions to query that sequence.  How 
    the sequence is stored is actually left up to the subclasses, which have to 
    reimplement the 'seq' property to return the sequence in question.
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, sequence):
        """
        Return whether or not two sequences are equal.  Sequence object can 
        either be compared to each other or to strings.
        """
        try:
            return self.seq == sequence.seq
        except AttributeError:
            return self.seq == sequence

    def __hash__(self):
        """
        Hash the sequence based on its location in memory.
        """
        from builtins import id
        return id(self)

    def __len__(self):
        """
        Return the length of the sequence.
        """
        return len(self.seq)

    def __iter__(self):
        """
        Iterate through the nucleotides in this sequence.
        """
        yield from self.seq

    def __getitem__(self, index):
        """
        Return the nucleotide at the given index.
        """
        return self.seq[index]

    @property
    def seq(self):      # (pure virtual)
        """
        Return the sequence represented by this object.  This is a pure virtual 
        method and must be reimplemented by subclasses.
        """
        raise NotImplementedError

    @property
    def dna(self):
        """
        Return the DNA version of the sequence.  This simply replaces U with T.
        """
        return self.seq.replace('U', 'T')

    @property
    def rna(self):
        """
        Return the RNA version of the sequence.  This simply replaces T with U.
        """
        return self.seq.replace('T', 'U')

    @property
    def indices(self):
        """
        Iterate through the indices of the nucleotides in this sequence.
        """
        return range(len(self))

    def mass(self, polymer='rna'):
        """
        Calculate the mass of this sequence for the given type of polymer.  
        This calculation assumes that the terminal phosphates have been 
        replaced with alcohol groups, which is the case for most oligos.
        """
        sequence = self.seq.upper()

        a = sequence.count('A')
        c = sequence.count('C')
        g = sequence.count('G')
        t = u = sequence.count('T') + sequence.count('U')

        if polymer == 'rna':
            return (a * 329.2) + (u * 306.2) + (c * 305.2) + (g * 345.2) + 159
        elif polymer == 'dna':
            return ((a + t) * 617.4) + ((g + c) * 618.4) - 124
        elif polymer == 'ssdna':
            return (a * 313.2) + (t * 304.2) + (c * 289.2) + (g * 329.2) - 62
        else:
            raise ValueError("unknown polymer type: '{}'".format(polymer))


class Construct (Sequence):
    """
    A interesting or useful sequence composed of parts that can be individually 
    modified without unduly affecting the rest of the sequence.
    """

    Attachment = collections.namedtuple(
            'Attachment', 'start_domain start_index end_domain end_index construct')
    BasePair = collections.namedtuple(
            'BasePair', 'domain_i i domain_j j')
    FoldEvaluation = collections.namedtuple(
            'FoldEvaluation', 'base_pairs_kept base_pairs_lost unpaired_bases_kept unpaired_bases_lost')

    def __init__(self, name='', domains=None):
        super().__init__(name)
        if domains is None:
            domains = []
        if isinstance(domains, Domain):
            domains = [domains]
        self._domains = domains
        self._attachments = dict()
        self._expected_base_pairs = set()
        self._expected_unpaired_bases = set()

    def __repr__(self):
        return 'Construct("{}")'.format(self.name)

    def __str__(self):
        return self.format()

    def __getitem__(self, key):
        if isinstance(key, str):
            domains = self.domains_from_name(key)
            if len(domains) == 1:
                return domains[0]
            else:
                raise KeyError("{} domains named '{}'.".format(len(domains), key))
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, construct):
        self.attach(construct, *key)

    def __add__(self, other):
        construct = Construct()
        construct += self
        construct += other
        return construct

    def __iadd__(self, other):
        self.append(other)
        return self

    @property
    def function_name(self):
        factory, arguments = parse_name(self.name)
        return '{}({})'.format(factory, ','.join(str(x) for x in arguments))

    @property
    def underscore_name(self):
        import re
        return re.sub('[^a-zA-Z0-9]+', '_', self.name).strip('_')

    @property
    def slash_name(self):
        import re
        return re.sub('[^a-zA-Z0-9]+', '/', self.name).strip('/')

    @property
    def seq(self):
        return ''.join(
                iter.domain.seq[iter.rel_start:iter.rel_end]
                for iter in self._iterate_domains())

    @property
    def constraints(self):
        return ''.join(
                iter.domain.constraints[iter.rel_start:iter.rel_end]
                for iter in self._iterate_domains())

    def domain_from_index(self, index):
        """
        Return the domain that includes the given index.
        """

        if index < 0:
            index += len(self)

        for iter in self._iterate_domains():
            if iter.start <= index < iter.end:
                return iter.domain, iter.rel_index(index)

        raise IndexError('index out of range')

    def domains_from_name(self, *names):
        domains = [x for x in self._domains if x.name in names]
        for attachment in self._attachments.values():
            domains += attachment.construct.domains_from_name(*names)
        return domains

    def format(self, dna=False, rna=False, start=None, end=None, pad=False, labels=False, color='auto'):
        sequence = ''

        if start is None: start = 0
        if end is None: end = len(self)

        for iter in self._iterate_domains():
            rel_start = nonstdlib.clamp(
                    iter.rel_index(start),
                    iter.rel_start,
                    iter.rel_end,
            )
            rel_end = nonstdlib.clamp(
                    iter.rel_index(end),
                    iter.rel_start,
                    iter.rel_end,
            )
            sequence += iter.domain.format(
                    dna=dna,
                    rna=rna,
                    start=rel_start,
                    end=rel_end,
                    color=color,
            )

        if labels: sequence = "5'-{}-3'".format(sequence)
        if pad: sequence = (start or 0) * ' ' + sequence

        return sequence

    def show(self, *args, **kwargs):
        print(self.format(*args, **kwargs))

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def append(self, sequence):
        """
        Add the given sequence onto the end of this construct.

        Parameters
        ----------
        sequence: Domain or Construct
            The sequence to add to this construct.  If a domain is given, it 
            will simply be added.  If a construct is given, the domains and 
            attachments from that construct will be read from the given 
            construct and inserted into this one.  Both construct will end up 
            with references to the same domain objects, but changes to one 
            construct won't affect the other.
        """
        self._add_sequence(-1, sequence)

    def prepend(self, sequence):
        """
        Add the given sequence onto the beginning of this construct.

        Parameters
        ----------
        sequence: Domain or Construct
            The sequence to add to this construct.  If a domain is given, it 
            will simply be added.  If a construct is given, the domains and 
            attachments from that construct will be read from the given 
            construct and inserted into this one.  Both construct will end up 
            with references to the same domain objects, but changes to one 
            construct won't affect the other.
        """
        self._add_sequence(0, sequence)

    def remove(self, *domains):
        """
        Remove the specified domain(s) from the construct.

        Parameters
        ----------
        *domains: str or Domain
            The domains to remove.

        sequence: Domain or Construct
            The sequence to add to this construct.  If a domain is given, it 
            will simply be added.  If a construct is given, the domains and 
            attachments from that construct will be read from the given 
            construct and inserted into this one.  Both construct will end up 
            with references to the same domain objects, but changes to one 
            construct won't affect the other.
        """
        for domain in domains:
            self._remove_sequence(domain)

    def replace(self, domain, sequence):
        """
        Remove the specified domain and replace it with the given sequence.

        Parameters
        ----------
        domain: str or Domain
            The domain to remove.
        """
        index = self._remove_sequence(domain)
        self._add_sequence(index, sequence)

    def attach(self, construct, start_domain, start_index, end_domain, end_index):
        """
        Insert a construct into one of the domains comprising this construct, 
        possibly replacing some of that domain.

        Parameters
        ----------
        construct: Construct
            The construct to attach.  Note that what is stored is a reference 
            to the given construct, so changes to that object will be reflected 
            by this one.

        start_domain, end_domain: str or Domain
            The domain into which the new sequence will be inserted.  You can 
            either provide the name or the domain or the domain object itself.  
            If you provide a name, there must be only one domain with that name 
            in the construct.
            
        start_index, end_index: int
            The index (relative to the domain) where the attachment will start.  
            As usual in python, think of this as indexing the spaces between 
            the nucleotides.
            
        Be aware that this method is fundamentally different that append(), 
        prepend(), and remove().  Those methods manage a flat list of domains 
        that you can think of as the "base layer" of the construct.  This 
        method attaches constructs (not domains) that float on top of that 
        layer and form a more tree-like structure.  Having attachments float on 
        top of the base construct makes it easy to move them around, which is 
        an important feature of this class.

        To simplify things, attachments cannot span domains.  That is, each 
        attachment can only occlude parts of one domain at a time.  This 
        shouldn't be an issue so long as you take care to compose your 
        constructs from functionally separate domains.
        """
        if isinstance(start_domain, str):
            start_domain = self[start_domain]
        if start_domain not in self._domains:
            raise ValueError("no '{}' domain in '{}'.".format(start_domain, self.name))

        if isinstance(end_domain, str):
            end_domain = self[end_domain]
        if end_domain not in self._domains:
            raise ValueError("no '{}' domain in '{}'.".format(end_domain, self.name))

        if start_index is ...:
            start_index = 0
        if start_index not in start_domain.attachment_sites:
            raise ValueError("Position {} of domain {} is not an attachment site.".format(start_index, start_domain.name))

        if end_index is ...:
            end_index = len(end_domain)
        if end_index not in end_domain.attachment_sites:
            raise ValueError("Position {} of domain {} is not an attachment site.".format(end_index, end_domain.name))

        self._attachments[start_domain] = self.Attachment(
                start_domain, start_index, end_domain, end_index, construct)

    def unattach(self, construct):
        """
        Remove the specified attachment from the construct.

        Parameters
        ----------
        construct: Construct
            The construct to unattach from this one.  If this construct has 
            been attached more than once, all the copies will be removed.
        """
        self._attachments = {
                k: a for k, a in self._attachments.items()
                if a.construct is not construct
        }

    def reattach(self, construct, start_domain, start_index, end_domain, end_index):
        """
        Reposition an attachment within a domain.

        Parameters
        ----------
        domain: str or Domain
            The domain containing the attachment that will be repositioned.

        start: int
            The new start index for the attachment.

        end: int
            The new end index for the attachment.

        If you want to move an attachment into a new domain, you can't use this 
        method.  Instead use unattach() followed by attach().
        """
        self.unattach(construct)
        self.attach(construct, start_domain, start_index, end_domain, end_index)

    def _iterate_domains(self):
        """
        Iterate over all the domains that make up this construct (even those 
        from attachments) and indicate how each one should be indexed to 
        properly assemble the whole construct.

        This method is very important because it provides an easy-to-use 
        interface for methods that want to read data from the construct.  The 
        actual data structures that make up the construct are designed to be 
        easy to modify, but they are not especially easy to work with.  This 
        function takes the easy-to-modify data and converts it into an 
        easy-to-use iterator.  That way we get the best of both worlds!
        """

        class DomainIter:
            # Indices refer to positions between the nucleotides, as usual for 
            # slices in python.

            def __init__(self, domain, cursor, rel_start, rel_end):
                self.domain = domain
                self.start = cursor
                self.rel_start = rel_start
                self.rel_end = rel_end

            def __repr__(self):
                return ('DomainIter('
                            'domain={0.domain!r}, '
                            'start={0.start}, '
                            'rel_start={0.rel_start}, '
                            'rel_end={0.rel_end})'.format(self))
            @property
            def len(self):
                return self.rel_end - self.rel_start

            @property
            def end(self):
                return self.start + self.len

            def rel_index(self, index):
                return index - self.start + self.rel_start

        domain_cursor = 0
        index_cursor = 0
    
        while domain_cursor < len(self._domains):
            domain = self._domains[domain_cursor]

            # If this domain doesn't have anything attached to it, then we can 
            # just yield the whole thing right away.

            if domain not in self._attachments:
                yield DomainIter(domain, index_cursor, 0, len(domain))
                index_cursor += len(domain)

            # If this domain does have something attached to it, then we need 
            # to carefully yield only the parts of it that aren't covered by 
            # the attachment.

            else:
                attachment = self._attachments[domain]

                # Yield whatever fraction of this domain comes before the 
                # attachment.

                yield DomainIter(domain,
                        index_cursor, 0, attachment.start_index)
                index_cursor += attachment.start_index

                # Yield the domains in the attachment itself by recursively 
                # calling this method.

                for domain_iter in attachment.construct._iterate_domains():
                    domain_iter.start += index_cursor
                    yield domain_iter
                index_cursor += len(attachment.construct)

                # Skip domains until we reach the one where the attachment 
                # ends.

                while domain is not attachment.end_domain:
                    domain_cursor += 1
                    domain = self._domains[domain_cursor]

                # Yield whatever fraction of that domain comes after the 
                # attachment.

                yield DomainIter(domain,
                        index_cursor, attachment.end_index, len(domain))
                index_cursor += len(domain) - attachment.end_index

            domain_cursor += 1

    def _add_sequence(self, position, sequence):
        if position < 0:
            position += len(self)
        if position > len(self):
            raise IndexError('index out of range')

        if isinstance(sequence, Construct):
            self._domains[position:position] = sequence._domains
            self._attachments.update(sequence._attachments)
        elif isinstance(sequence, Domain):
            self._domains.insert(position, sequence)
        else:
            raise ValueError("can't combine 'Construct' and '{}'".format(sequence.__class__.__name__))

    def _remove_sequence(self, domain):
        if isinstance(domain, str):
            domain = self[domain]

        idx = self._domains.index(domain)
        self._domains.remove(domain)
        self._attachments = {
                k: a for k, a in self._attachments.items()
                if a.start_domain is not domain and a.end_domain is not domain
        }
        return idx


class Domain (Sequence):
    """
    A mutable sequence that can be used to compose larger constructs.
    """

    def __init__(self, name, sequence, style=None, mutable=False):
        super().__init__(name)
        self._sequence = sequence
        self._attachment_sites = []
        self._constraints = None
        self.construct = None
        self.style = style
        self.mutable = mutable

    def __repr__(self):
        return 'Domain("{}", "{}")'.format(self.name, self.seq)

    def __str__(self):
        return self.format()

    def __len__(self):
        return len(self.seq)

    def __setitem__(self, index, sequence):
        if isinstance(index, slice):
            start, stop = index.start, index.stop
        else:
            start, stop = index, index + 1
        self.seq = self.seq[:start] + sequence + self.seq[stop:]

    def __delitem__(self, index):
        self[index] = ''

    @property
    def seq(self):
        return self._sequence

    @seq.setter
    def seq(self, sequence):
        if not self.mutable:
            raise AssertionError("domain '{}' is not mutable.".format(self.name))
        if self._constraints and len(self._constraints) != len(sequence):
            raise ValueError("sequence doesn't match constraints")
        self._sequence = sequence

    @property
    def constraints(self):
        return self._constraints or '.' * len(self)

    @constraints.setter
    def constraints(self, constraints):
        if constraints and len(constraints) != len(self):
            raise ValueError("constraints don't match sequence")
        self._constraints = constraints

    @property
    def attachment_sites(self):
        return self._attachment_sites 

    @attachment_sites.setter
    def attachment_sites(self, sites):
        if sites == 'anywhere':
            sites = range(len(self) + 1)
        sites = list(sites)
        if any(x < 0 or x > len(self) for x in sites):
            raise ValueError('index out of range')
        self._attachment_sites = sites

    def format(self, dna=False, rna=False, start=None, end=None, color='auto'):
        if dna: sequence = self.dna
        elif rna: sequence = self.rna
        else: sequence = self.seq

        if start is None: start = 0
        if end is None: end = len(self)
        sequence = sequence[start:end]
            
        # The style can either be ("color", "weight") or just "color".  If no 
        # weight is given, it is assumed to be normal.

        style = self.style or 'normal'
        if isinstance(style, str):
            style = style, 'normal'

        return nonstdlib.color(sequence, *style, when=color)

    def show(self, *args, **kwargs):
        print(self.format(*args, **kwargs))

    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    def mutate(self, index, mutation):
        self[index] = mutation

    def insert(self, index, insert):
        self[index:index] = insert

    def replace(self, start, end, insert):
        self[start:end] = insert

    def delete(self, start, end):
        self[start:end] = ''



def from_name(name, **kwargs):
    from inspect import getargspec

    construct = Construct()
    names = []

    for factory, args in parse_name(name):
        if factory not in globals():
            raise ValueError("No designs named '{}'.".format(factory))

        factory = globals()[factory]
        argspec = getargspec(factory)
        known_kwargs = {k:v for k,v in kwargs.items() if k in argspec.args}
        fragment = factory(*args, **known_kwargs)
        names.append(fragment.name)
        construct += fragment

    construct.name = '+'.join(x for x in names if x)
    return construct

def parse_name(name):
    import re

    def cast_if_necessary(x):
        try: return int(x)
        except: return x


    name = name.strip()
    sub_names = []

    if not name:
        raise ValueError("Can't parse empty name.")

    for sub_name in name.split('+'):
        tokens = re.findall('[a-zA-Z0-9]+', sub_name)
        factory = tokens[0]
        arguments = [cast_if_necessary(x) for x in tokens[1:]]
        sub_names.append((factory, arguments))

    return sub_names

def make_name(factory, *args):
    return factory + '(' + ','.join(str(x) for x in args) + ')'

def molecular_weight(name, polymer='rna'):
    return from_name(name).mass(polymer)

def complement(sequence):
    complements = str.maketrans('ACUG', 'UGAC')
    return sequence.translate(complements)

def reverse_complement(sequence):
    return complement(sequence[::-1])


def t7_promoter(source='briner'):
    """
    Return the sequence for the T7 promoter.

    Parameters
    ----------
    source: 'briner', 'igem'
        Specify which T7 sequence to use.  All the sequences are similar, but 
        different sequences may give better or worse transcription.
    """
    if source == 'igem':
        # The "T7 consensus -10 and rest" sequence from IGEM:
        # http://parts.igem.org/Promoters/Catalog/T7
        sequence = 'TAATACGACTCACTATA'

    elif source == 'briner':
        # The T7 sequence used by Briner et al. (2014):
        sequence = 'TATAGTAATAATACGACTCACTATAG'

    else:
        raise ValueError("Unknown T7 sequence: '{}'".format(source))

    return Construct(
            '{} t7'.format(source),
            Domain('t7', sequence))

def manual(*sequences):
    from itertools import cycle

    if len(sequences) == 1:
        colors = 'white',
    else:
        colors = 'magenta', 'red', 'yellow', 'green', 'cyan', 'blue'

    return Construct('manual', [
        Domain('.', seq, style=color)
        for seq, color in zip(sequences, cycle(colors))
    ])

def spacer(name='aavs'):
    """
    Return the specified spacer sequence.

    Parameters
    ----------
    target: 'rfp', 'aavs', 'vegfa'
        The sequence to target.
    """
    if name == 'rfp':
        sequence = 'GGAACUUUCAGUUUAGCGGUCU'
    elif name == 'aavs':
        sequence = 'GGGGCCACTAGGGACAGGAT'
    elif name == 'vegfa':
        sequence = 'GGGTGGGGGGAGTTTGCTCC'
    elif name == 'klein1':
        sequence = 'GGGCACGGGCAGCTTGCCCG'
    elif name == 'klein2':
        sequence = 'GTCGCCCTCGAACTTCACCT'
    else:
        raise ValueError("Unknown spacer: '{}'".format(name))

    spacer = Domain('spacer', sequence)
    spacer.style = 'yellow'

    return Construct(name, spacer)

def dna_to_cut(target='aavs'):
    """
    Return the specified target sequence.

    Parameters
    ----------
    target: 'rfp', 'aavs', 'vegfa'
        The sequence to return.
    """
    if target == 'aavs':
        return Construct('aavs', Domain('target', 
            'CCCCGTTCTCCTGTGGATTCGGGTCACCTCTCACTCCTTTCATTTGGGCA'
            'GCTCCCCTACCCCCCTTACCTCTCTAGTCTGTGCTAGCTCTTCCAGCCCC'
            'CTGTCATGGCATCTTCCAGGGGTCCGAGAGCTCAGCTAGTCTTCTTCCTC'
            'CAACCCGGGCCCCTATGTCCACTTCAGGACAGCATGTTTGCTGCCTCCAG'
            'GGATCCTGTGTCCCCGAGCTGGGACCACCTTATATTCCCAGGGCCGGTTA'
            'ATGTGGCTCTGGTTCTGGGTACTTTTATCTGTCCCCTCCACCCCACAGTG'
            'GGGCCACTAGGGACAGGATTGGTGACAGAAAAGCCCCATCCTTAGGCCTC'
            'CTCCTTCCTAGTCTCCTGATATTGGGTCTAACCCCCACCTCCTGTTAGGC'
            'AGATTCCTTATCTGGTGACACACCCCCATTTCCTGGAGCCATCTCTCTCC'
            'TTGCCAGAACCTCTAAGGTTTGCTTACGATGGAGCCAGAGAGGAT'))
    else:
        raise ValueError("Unknown target: '{}'".format(target))

def repeat(name, length, pattern='UUUCCC'):
    """
    Construct a repeating sequence using the given pattern.

    Oct 31, 2015: After having read some more of the literature, especially 
    Rhiju's EteRNA papers, I've realized that poly-A is a more common 
    "unstructured" linker sequence.

    Parameters
    ----------
    length: int
        Indicate how long the final sequence should be.

    pattern: str
        Provide the basic unit that should be repeated to make the sequence.
    """
    sequence = pattern * (1 + length // len(pattern))
    return Domain(name, sequence[:length])

def aptamer(ligand, piece='whole'):
    """
    Construct aptamer sequences.

    Parameters
    ----------
    ligand: 'theo'
        Specify the aptamer to generate.  Right now only the theophylline 
        aptamer is known.

    piece: 'whole', '5', '3', or 'splitter'
        Specify which part of the aptamer to generate.  The whole aptamer 
        is returned by default, but each aptamer can be broken into a 
        5' half, a 3' half, and a splitter between those halves.  

    Returns
    -------
    aptamer: Construct
        The returned construct is given constraints, which can be used to force 
        RNAfold to approximate a ligand bound state.
    """

    # Get the right sequence for the requested aptamer.

    if ligand in ('th', 'theo', 'theophylline'):
        name = 'theo aptamer'
        sequence_pieces   = 'AUACCAGCC', 'GAAA', 'GGCCCUUGGCAG'
        constraint_pieces = '(((((.(((', '....', ')))....)))))'
    else:
        raise ValueError("no aptamer for '{}'".format(ligand))

    # Define the domains that make up the aptamer.

    aptamer_5 = Domain("aptamer/5'", sequence_pieces[0])
    aptamer_S = Domain("splitter", sequence_pieces[1])
    aptamer_3 = Domain("aptamer/3'", sequence_pieces[2])

    aptamer_5.constraints = constraint_pieces[0]
    aptamer_S.constraints = constraint_pieces[1]
    aptamer_3.constraints = constraint_pieces[2]

    aptamer_5.style = 'white', 'bold'
    aptamer_S.style = 'white', 'bold'
    aptamer_3.style = 'white', 'bold'

    aptamer_S.mutable = True

    # Assemble the aptamer domains into a single construct and return it.

    construct = Construct('aptamer')

    if piece == 'whole':
        construct += aptamer_5
        construct += aptamer_S
        construct += aptamer_3
    elif str(piece) == '5':
        construct += aptamer_5
    elif piece == 'splitter':
        construct += aptamer_S
    elif str(piece) == '3':
        construct += aptamer_3
    else:
        raise ValueError("must request 'whole', '5', '3', or 'splitter' piece of aptamer, not {}.".format(piece))

    return construct

def aptamer_insert(ligand, linker_len=0, splitter_len=0, repeat_factory=repeat,
        num_aptamers=1):

    insert = aptamer(ligand)

    # If multiple aptamers were requested, build them around the central one.

    for i in range(1, num_aptamers):
        insert.replace('splitter', aptamer(ligand))

    # If a splitter was requested, insert it into the middle of the aptamer.

    if splitter_len != 0:
        insert.replace('splitter', repeat_factory('splitter', splitter_len))

    # Add a linker between the aptamer and the sgRNA.

    try: linker_len_5, linker_len_3 = linker_len
    except TypeError: linker_len_5 = linker_len_3 = linker_len

    insert.prepend(repeat_factory("linker/5'", linker_len_5))
    insert.append(repeat_factory("linker/3'", linker_len_3))

    return insert

def serpentine_insert(ligand, target_seq, target_end, turn_seq='GAAA',
        num_aptamers=1):

    if not target_seq:
        raise ValueError('target_seq cannot be empty')

    domains = [
            Domain('target', target_seq),
            Domain('turn', turn_seq),
            Domain('latch', reverse_complement(target_seq)),
            aptamer_insert(ligand, num_aptamers=num_aptamers),
            Domain('decoy', target_seq),
    ]

    if target_end == '3':
        domains.reverse()

    return Construct('serpentine', domains)

def circle_insert(ligand, target_seq, target_end, num_aptamers=1):
    if not target_seq:
        raise ValueError('target_seq cannot be empty')

    domains = [
            Domain('target', target_seq),
            Domain('decoy', target_seq),
            aptamer_insert(ligand, num_aptamers=num_aptamers),
            Domain('latch', reverse_complement(target_seq)),
    ]

    if target_end == '3':
        domains.reverse()

    return Construct('circle', domains)


def wt_sgrna(target=None):
    """
    Return the wildtype sgRNA sequence, without a spacer.

    The construct is composed of 3 domains: stem, nexus, and hairpins.  The 
    stem domain encompasses the lower stem, the bulge, and the upper stem.  
    Attachments are allowed pretty much anywhere, although it would be prudent 
    to restrict this based on the structural biology of Cas9 if you're planning 
    to make random attachments.
    """
    sgrna = Construct('wt sgrna')

    if target is not None:
        sgrna += spacer(target)

    sgrna += Domain('stem', 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU')
    sgrna += Domain('nexus', 'AAGGCUAGUCCGU')
    sgrna += Domain('hairpins', 'UAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC')
    sgrna += Domain('tail', 'UUUUUU')

    sgrna['stem'].style = 'green'
    sgrna['nexus'].style = 'red'
    sgrna['hairpins'].style = 'blue'

    sgrna['stem'].attachment_sites = 'anywhere'
    sgrna['nexus'].attachment_sites = range(2, 12)
    sgrna['hairpins'].attachment_sites = 'anywhere'

    return sgrna

def dead_sgrna(target=None):
    """
    Return the sequence for the negative control sgRNA.

    This sequence has two mutations in the nexus region that prevent the sgRNA 
    from folding properly.  These mutations were described by Briner et al.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = 'dead sgrna'

    sgrna['nexus'].mutable = True
    sgrna['nexus'].mutate(2, 'C')
    sgrna['nexus'].mutate(3, 'C')
    sgrna['nexus'].mutable = False

    return sgrna

def fold_upper_stem(N, linker_len=0, splitter_len=0, num_aptamers=1, small_molecule='theo', target='aavs'):
    """
    Insert the aptamer into the upper stem region of the sgRNA.

    The upper stem region of the sgRNA is very tolerant to mutation.  In the 
    natural CRISPR/Cas system, this stem is actually where the two strands of  
    guide RNA (crRNA and tracrRNA) come together.

    Parameters
    ----------
    N: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.  The aptamer will be inserted 
        between the two ends of the stem.

    linker_len: int
        Indicate how many bases should separate the aptamer from the upper 
        stem.  The linker sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    splitter_len: int
        Indicate how many bases should separate the 3' half of the aptamer from 
        the 5' half.  The splitter sequence will have the same pattern as the 
        linker (see above).

    num_aptamers: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    Returns
    -------
    sgRNA: Construct
    """

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    if num_aptamers != 1:
        args = N, linker_len, splitter_len, num_aptamers
    elif splitter_len != 0:
        args = N, linker_len, splitter_len
    else:
        args = N, linker_len
    if target != 'aavs':
        args = args + ('s='+target,)
    if small_molecule != 'theo':
        args = args + ('a='+small_molecule,)

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('us', *args)
    sgrna.attach(
            aptamer_insert(
                small_molecule,
                linker_len=linker_len,
                splitter_len=splitter_len,
                num_aptamers=num_aptamers,
            ),
            'stem', 8 + N,
            'stem', 20 - N,
    )
    return sgrna

def fold_lower_stem(N, linker_len=0, splitter_len=0, small_molecule='theo', target='aavs'):
    """
    Insert the aptamer into the lower stem region of the sgRNA.

    Parameters
    ----------
    N: int
        Indicate how many of the 6 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 6, although in practice I only 
        expect to use values greater than 4 or 5.  Shorter than that and you'll 
        almost certainly interfere with normal Cas9 binding.

    linker_len: int
        Indicate how many base pairs should separate the aptamer from the upper 
        stem.  The linker sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    splitter_len: int
        Indicate how many bases should separate the 3' half of the aptamer from 
        the 5' half.  The splitter sequence will have the same pattern as the 
        linker (see above).

    Returns
    -------
    sgRNA: Construct
    """

    if not 0 <= N <= 6:
        raise ValueError("Location for lower stem insertion must be between 0 and 6, not {}.".format(N))

    if splitter_len != 0:
        args = N, linker_len, splitter_len
    else:
        args = N, linker_len
    if target != 'aavs':
        args = args + ('s='+target,)
    if small_molecule != 'theo':
        args = args + ('a='+small_molecule,)

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('ls', *args)
    sgrna.attach(
            aptamer_insert(
                small_molecule,
                linker_len=linker_len,
                splitter_len=splitter_len,
            ),
            'stem', 0 + N,
            'stem', 30 - N,
    )
    return sgrna

def fold_nexus(linker_len=0, small_molecule='theo', target='aavs'):
    """
    Insert the aptamer into the nexus region of the sgRNA.

    The nexus is a short (2 bp) stem connected by 5 residues with irregular 
    secondary structure.  Briner et al. (2014) and Nishimasu et al. (2014) both 
    studied how mutations to this area can affect binding, but the results 
    aren't easy to rationalize.  Either one of the stem base pairs, but not 
    both, can be mutated to AU (both are naturally GC) without affecting 
    function.  Mutations were also made to 4 of the 5 positions with irregular 
    structure (sometimes in conjunction with mutations elsewhere that weren't 
    obviously compensatory) and all of those mutants were functional.
    
    My takeaway is that replacing the 5 irregular residues with the aptamer and 
    a variable length linker might be a good strategy.  For now, I'm going to 
    neglect the possibility of keeping any of the 5 irregular nexus residues.  
    There are of course many ways to do that, but no reason to think that one 
    would be more promising that any other.

    Parameters
    ----------
    linker_len: int
        Indicate how many base pairs should separate the aptamer from the nexus 
        region stem.  The linker sequence will have a UUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    args = (linker_len,)
    if target != 'aavs':
        args = args + ('s='+target,)
    if small_molecule != 'theo':
        args = args + ('a='+small_molecule,)

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('nx', linker_len)
    sgrna.attach(
            aptamer_insert(
                small_molecule,
                linker_len=linker_len,
                repeat_factory=lambda name, length: repeat(name, length, 'U'),
            ),
            'nexus', 4,
            'nexus', 9,
    )
    return sgrna
    
def fold_nexus_2(N, M, splitter_len=0, num_aptamers=1, small_molecule='theo', target='aavs'):
    """
    Insert the aptamer into the nexus region of the sgRNA.

    This design strategy expands upon the original fold_nexus() function, 
    which produced promising initial hits.  This strategy allows more control 
    over where the aptamer is inserted, by having the user specify the number 
    of nucleotides to keep (N and M) on both sides of the nexus.  This strategy 
    also places the repeat sequence inside the aptamer rather than around it, 
    and allows for more than one aptamer to be chained together.

    Parameters
    ----------
    N: int
        The number of base pairs to keep on the 5' side of the nexus, starting 
        from the base of the hairpin at position 53.

    M: int
        The number of base pairs to keep on the 3' side of the nexus, starting 
        from the base of the hairpin at position 61.

    splitter_len: int
        The number of base pairs to insert into the middle of the aptamer.  The 
        linker will have the sequence 'UCGUCG...', which was chosen because it 
        has very low complementarity with the rest of the design.

    num_aptamers: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    Returns
    -------
    sgRNA: Construct
    """

    # Make sure the arguments have reasonable values.

    min_splitter_len = len(aptamer('theo', 'splitter'))

    if not 0 <= N <= 4:
        raise ValueError("nxx: N must be between 0 and 4, not {}".format(N))
    if not 0 <= M <= 5:
        raise ValueError("nxx: M must be between 0 and 5, not {}".format(N))
    if 0 < splitter_len <= min_splitter_len:
        raise ValueError("nxx: splitter_len must be longer than {} (the natural linker length).".format(min_splitter_len))
    if num_aptamers < 1:
        raise ValueError("nxx: Must have at least 1 aptamer")

    # Figure out what to name the construct.  Make an effort to exclude 
    # arguments that the user didn't actually specify from the name.

    if num_aptamers != 1:
        args = N, M, splitter_len, num_aptamers
    elif splitter_len != 0:
        args = N, M, splitter_len
    else:
        args = N, M
    if target != 'aavs':
        args = args + ('s='+target,)
    if small_molecule != 'theo':
        args = args + ('a='+small_molecule,)

    # Create and return the construct using a helper function.

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('nxx', *args)
    sgrna.attach(
            aptamer_insert(
                small_molecule,
                splitter_len=splitter_len,
                num_aptamers=num_aptamers,
            ),
            'nexus', 2 + N,
            'nexus', 11 - M,
    )
    return sgrna

def replace_hairpins(N, small_molecule='theo', target='aavs'):
    """
    Remove a portion of the 3' terminal hairpins and replace it with the 
    aptamer.
    
    Parameters
    ----------
    N: int
        Indicate how much of the 3' terminal hairpins should be kept, with the 
        counting starting at position 63.  An N of 33 therefore specifies that 
        the whole sgRNA should be kept (excluding the poly-U tail) and that the 
        aptamer should simply be added onto the end.  Values larger than 33 
        specify that a linker should be inserted between the sgRNA and the 
        aptamer.  Values smaller than 33 specify that some residues should be 
        truncated from the 3' end of the sgRNA.  The expected range for this 
        parameter is roughly 17-33.

    Returns
    -------
    sgRNA: Construct
        The specified construct will be returned, with a hexa-uracil tail will 
        added to the end for the benefit of the T7 polymerase.
    """
    args = (N,)
    if target != 'aavs':
        args = args + ('s='+target,)
    if small_molecule != 'theo':
        args = args + ('a='+small_molecule,)

    design = wt_sgrna(target)
    design.name = make_name('hp', *args)

    domain_len = len(design['hairpins'])
    insertion_site = min(N, domain_len)
    linker_len = max(0, N - domain_len), 0

    design.attach(
            aptamer_insert(small_molecule, linker_len=linker_len),
            'hairpins', insertion_site,
            'hairpins', ...,
    )
    return design

def induce_dimerization(half, N, small_molecule='theo', target='aavs'):
    """
    Split the guide RNA into its two naturally occurring halves, and use the 
    aptamer to bring those halves together in the presence of the ligand.  The 
    aptamer replaces some or all of the upper stem.  We have already observed 
    that an sgRNA with the upper stem fully replaced by the theophylline 
    aptamer is fully functional, so the design should work if the ligand 
    successfully induces dimerization.

    Parameters
    ----------
    half: 5 or 3
        Indicate which half of the split construct to return.  '5' and '3' 
        refer to the 5' and 3' halves, respectively.

    N: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.

    Returns
    -------
    sgRNA: Construct
    """

    # Make sure the arguments make sense.

    half = str(half)
    N = int(N)

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    args = half, N
    if target != 'aavs':
        args = args + ('s='+target,)
    if small_molecule != 'theo':
        args = args + ('a='+small_molecule,)

    # Construct and return the requested sequence.

    design = Construct()
    design.name = make_name('id', *args)
    wt = wt_sgrna(target)

    if half == '5':
        design += wt['spacer']
        design += wt['stem']
        design.attach(
                aptamer(small_molecule, '5'),
                'stem', 8 + N, 'stem', ...,
        )
    elif half == '3':
        design += wt
        design.attach(
                aptamer(small_molecule, '3'),
                'stem', ..., 'stem', 20 - N,
        )
    else:
        raise ValueError("Half for induced dimerization must be either 5 (for the 5' half) or 3 (for the 3' half), not '{}'.".format(half))

    return design

def serpentine_bulge(N):
    """
    Sequester the bulge in a non-productive hairpin when the ligand isn't 
    present.  The bulge is an interesting target because it doesn't have to be 
    there, but if it is there it must be unpaired and it must have its wildtype 
    sequence.  This design uses the two adenosines that are naturally in the 
    bulge to construct a tetraloop that caps the non-productive hairpin.  Below 
    is an ASCII-art schematic of the design, along with an example sequence:

       ┌──────────┐ ┌───────────┐ ┌────┐ ┌────────────┐ ┌─────┐ ┌──────────┐ 
    5'─┤lower stem├─┤  bulge''  ├─┤theo├─┤   bulge'   ├─┤bulge├─┤lower stem├─3'
       └──────────┘ └───────────┘ └────┘ └────────────┘ └─────┘ └──────────┘ 
        GUUUUAga     UCGU(UAAAAU)  ...   (GUUUUA)AC-GA   AA-GU   UAAAAU
                                                   └───────┘
                                                   tetraloop

    The length of the non-productive hairpin can be extended by including bases 
    from the lower stem, as shown in parentheses.  Mutations can be made in the 
    bulge', bulge'', and lower stem regions to tune the balance between the 
    "on" and "off" states.  The bulge itself is never changed.

    Parameters
    ----------
    N: int
        Indicate how long the non-productive hairpin should be.  Must be 
        between 2 and 7.  The first two bases in the hairpin come from the 
        bulge, and subsequent bases come from the lower stem.

    Returns
    -------
    sgRNA: Construct
    """
    if not 2 <= N <= 7:
        raise ValueError("sb(N): N must be between 2 and 7")

    sense = 'GUUAAAAU'[:N]
    antisense = 'GUUAAAAU'[:N]

    insert = make_serpentine_insert('GUUAAAAU', '3', num_aptamers=num_aptamers)
    insert["bulge''"].append('UC')

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('sb', N)

    #target = sgrna['stem'][
    #sgrna.attach(
            #insert, 'stem', ???, 'stem', ???,
    #)
    return sgrna

def circle_bulge():
    pass


## Abbreviations
wt = wt_sgrna
dead = dead_sgrna
fu = us = fold_upper_stem
fl = ls = fold_lower_stem
fn = nx = fold_nexus
fnx = nxx = fold_nexus_2
hp = replace_hairpins
id = induce_dimerization

t7 = t7_promoter
th = theo = lambda: aptamer('theo')
aavs = lambda: dna_to_cut('aavs')


def test_domain_class():
    import pytest

    domain = Domain('Alice', 'ACTG')

    assert domain.name == 'Alice'
    assert domain.seq == 'ACTG'
    assert domain.dna == 'ACTG'
    assert domain.rna == 'ACUG'
    assert domain.indices == range(4)
    assert domain.mass('rna') == 1444.8
    assert domain.mass('dna') == 2347.6
    assert domain.mass('ssdna') == 1173.8
    assert domain.copy().seq == domain.seq
    assert len(domain) == 4
    assert domain[0] == 'A'
    assert domain[1] == 'C'
    assert domain[2] == 'T'
    assert domain[3] == 'G'
    assert domain[1:3] == 'CT'
    assert domain.constraints == '....'
    assert domain.attachment_sites == []
    assert domain.format(color='never') == 'ACTG'

    for i, base in enumerate(domain):
        assert base == domain[i]

    with pytest.raises(ValueError):
        domain.constraints = '.'

    domain.constraints = '.(.)'
    assert domain.constraints == '.(.)'

    domain.attachment_sites = range(len(domain))
    assert domain.attachment_sites == [0, 1, 2, 3]

    with pytest.raises(AssertionError):
        domain.seq = 'AAAA'

    domain.mutable = True
    domain.constraints = None

    domain.seq = 'GTCA'
    assert domain.seq == 'GTCA'

    domain[1] = 'A'
    assert domain.seq == 'GACA'

    domain[1] = 'TATA'
    assert domain.seq == 'GTATACA'

    domain[1:3] = 'CT'
    assert domain.seq == 'GCTTACA'

    domain[1:3] = 'GCGC'
    assert domain.seq == 'GGCGCTACA'

    del domain[5]
    assert domain.seq == 'GGCGCACA'

    del domain[1:5]
    assert domain.seq == 'GACA'

    domain.mutate(1, 'A')
    assert domain.seq == 'GACA'

    domain.insert(2, 'TTT')
    assert domain.seq == 'GATTTCA'

    domain.replace(2, 5, 'GG')
    assert domain.seq == 'GAGGCA'

    domain.delete(2, 4)
    assert domain.seq == 'GACA'

def test_construct_class():
    import pytest

    ## Test making a one domain construct.

    bob = Construct('Bob')
    bob += Domain('A', 'AAAAAA')

    assert bob.seq == 'AAAAAA'
    assert bob.seq == bob.copy().seq
    assert bob.format(color='never') == bob.seq
    assert bob.constraints == 6 * '.'
    assert len(bob) == 6

    with pytest.raises(KeyError):
        bob['not a domain']

    for i, expected_nucleotide in enumerate(bob.seq):
        assert bob[i] == expected_nucleotide

    ## Test making a two domain construct.

    bob += Domain('C', 'CCCCCC')

    assert bob.seq == 'AAAAAACCCCCC'
    assert bob.seq == bob.copy().seq
    assert bob.format(color='never') == bob.seq
    assert bob.constraints == 12 * '.'
    assert len(bob) == 12

    ## Test appending one construct onto another.

    carol = Construct('Carol')
    carol += Domain('G', 'GGGGGG')
    carol = carol + bob

    assert carol.seq == 'GGGGGGAAAAAACCCCCC'
    assert carol.constraints == 18 * '.'
    assert len(carol) == 18

    carol.prepend(Domain('T', 'TTTTTT'))

    assert carol.seq == 'TTTTTTGGGGGGAAAAAACCCCCC'
    assert carol.constraints == 24 * '.'
    assert len(carol) == 24

    carol.replace('G', Domain('CG', 'CGCGCG'))

    assert carol.seq == 'TTTTTTCGCGCGAAAAAACCCCCC'
    assert carol.constraints == 24 * '.'
    assert len(carol) == 24

    carol.remove('CG')

    assert carol.seq == 'TTTTTTAAAAAACCCCCC'
    assert carol.constraints == 18 * '.'
    assert len(carol) == 18

    ## Test attaching one construct into another.

    dave = Construct('Dave')
    dave += Domain('G', 'GGGGGG')
    dave += Domain('T', 'TTTTTT')
    dave['G'].attachment_sites = 0, 3, 6
    dave['T'].attachment_sites = 0, 3, 6

    with pytest.raises(ValueError):
        dave.attach(bob, 'G', 0, 'T', 5)
    with pytest.raises(ValueError):
        dave.attach(bob, 'G', 1, 'T', 6)
    with pytest.raises(KeyError):
        dave.attach(bob, '?', 0, 'T', 6)

    dave.attach(bob, 'G', 0, 'G', 3)

    assert dave.seq == 'AAAAAACCCCCCGGGTTTTTT'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 21 * '.'
    assert len(dave) == 21

    dave.reattach(bob, 'G', 3, 'G', 6)

    assert dave.seq == 'GGGAAAAAACCCCCCTTTTTT'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 21 * '.'
    assert len(dave) == 21

    dave.reattach(bob, 'G', 0, 'G', 6)

    assert dave.seq == 'AAAAAACCCCCCTTTTTT'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 18 * '.'
    assert len(dave) == 18

    dave.reattach(bob, 'G', 0, 'T', 0)

    assert dave.seq == 'AAAAAACCCCCCTTTTTT'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 18 * '.'
    assert len(dave) == 18

    dave.reattach(bob, 'G', 0, 'T', 6)

    assert dave.seq == 'AAAAAACCCCCC'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 12 * '.'
    assert len(dave) == 12

    dave.reattach(bob, 'G', 6, 'T', 0)

    assert dave.seq == 'GGGGGGAAAAAACCCCCCTTTTTT'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 24 * '.'
    assert len(dave) == 24

    dave.reattach(bob, 'G', 6, 'T', 6)

    assert dave.seq == 'GGGGGGAAAAAACCCCCC'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 18 * '.'
    assert len(dave) == 18

    dave.reattach(bob, 'G', 3, 'T', 3)

    assert dave.seq == 'GGGAAAAAACCCCCCTTT'
    assert dave.format(color='never') == dave.seq
    assert dave.constraints == 18 * '.'
    assert len(dave) == 18

    ## Test removing a domain with an attached construct.

    dave_copy = dave.copy()
    dave_copy.remove('G')
    assert dave_copy.seq == 'TTTTTT'

    dave_copy = dave.copy()
    dave_copy.remove('T')
    assert dave_copy.seq == 'GGGGGG'

    ## Test accessing domains by index.

    expected_domains = [
            (dave['G'], 0),
            (dave['G'], 1),
            (dave['G'], 2),
            (dave['A'], 0),
            (dave['A'], 1),
            (dave['A'], 2),
            (dave['A'], 3),
            (dave['A'], 4),
            (dave['A'], 5),
            (dave['C'], 0),
            (dave['C'], 1),
            (dave['C'], 2),
            (dave['C'], 3),
            (dave['C'], 4),
            (dave['C'], 5),
            (dave['T'], 3),
            (dave['T'], 4),
            (dave['T'], 5),
    ]
    for index, domain in enumerate(expected_domains):
        assert dave.domain_from_index(index) == domain
    for index, domain in enumerate(reversed(expected_domains), 1):
        assert dave.domain_from_index(-index) == domain
    with pytest.raises(IndexError):
        dave.domain_from_index(len(dave))

    ## Test changing the sequence of a domain.

    bob['A'].mutable = True
    bob['A'].seq = 'AAAA'

    assert bob.seq == 'AAAACCCCCC'
    assert carol.seq == 'TTTTTTAAAACCCCCC'
    assert dave.seq == 'GGGAAAACCCCCCTTT'

    ## Test adding constraints to a domain.

    bob['A'].constraints = '(())'

    assert bob.constraints == '(())......'
    assert carol.constraints == '......(())......'
    assert dave.constraints == '...(()).........'


def test_from_name():
    equivalent_constructs = [
            from_name('us(4)'),
            from_name('us(4,0)'),
            from_name('us(4, 0)'),
            from_name('us 4'),
            from_name('us 4 0'),
            from_name('us/4'),
            from_name('us/4/0'),
            from_name('us-4'),
            from_name('us-4-0'),
            from_name('us_4'),
            from_name('us_4_0'),
    ]

    for construct in equivalent_constructs:
        assert construct.seq == equivalent_constructs[0].seq

def test_complements():
    assert complement('ACUG') == 'UGAC'
    assert reverse_complement('ACUG') == 'CAGU'

def test_t7_promoter():
    import pytest

    with pytest.raises(ValueError): t7_promoter('not a promoter')

    assert t7_promoter() == 'TATAGTAATAATACGACTCACTATAG'
    assert t7_promoter('igem') == 'TAATACGACTCACTATA'

def test_aptamer():
    import pytest

    with pytest.raises(ValueError): aptamer('unknown ligand')
    with pytest.raises(ValueError): aptamer('theo', 'unknown piece')

    assert aptamer('theo').seq == 'AUACCAGCCGAAAGGCCCUUGGCAG'

def test_spacer():
    import pytest

    with pytest.raises(ValueError): spacer('not a spacer')

    assert spacer('aavs') == 'GGGGCCACTAGGGACAGGAT'
    assert spacer('rfp') == 'GGAACUUUCAGUUUAGCGGUCU'
    assert spacer('vegfa') == 'GGGTGGGGGGAGTTTGCTCC'

def test_repeat():
    assert repeat('dummy', 1) == 'U'
    assert repeat('dummy', 2) == 'UU'
    assert repeat('dummy', 3) == 'UUU'
    assert repeat('dummy', 4) == 'UUUC'
    assert repeat('dummy', 5) == 'UUUCC'
    assert repeat('dummy', 6) == 'UUUCCC'
    assert repeat('dummy', 7) == 'UUUCCCU'

def test_serpentine_insert():
    assert serpentine_insert('theo', 'G', '3') == 'GAUACCAGCCGAAAGGCCCUUGGCAGCGAAAG'
    assert serpentine_insert('theo', 'G', '5') == 'GGAAACAUACCAGCCGAAAGGCCCUUGGCAGG'
    assert serpentine_insert('theo', 'GUUAAAAU', '3') == 'GUUAAAAUAUACCAGCCGAAAGGCCCUUGGCAGAUUUUAACGAAAGUUAAAAU'
    assert serpentine_insert('theo', 'GUUAAAAU', '5') == 'GUUAAAAUGAAAAUUUUAACAUACCAGCCGAAAGGCCCUUGGCAGGUUAAAAU'
    assert serpentine_insert('theo', 'GUAC', '3', turn_seq='UAA') == 'GUACAUACCAGCCGAAAGGCCCUUGGCAGGUACUAAGUAC'
    assert serpentine_insert('theo', 'GUAC', '3', num_aptamers=2) == 'GUACAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGGUACGAAAGUAC'

def test_circle_insert():
    assert circle_insert('theo', 'G', '3') == 'CAUACCAGCCGAAAGGCCCUUGGCAGGG'
    assert circle_insert('theo', 'G', '5') == 'GGAUACCAGCCGAAAGGCCCUUGGCAGC'
    assert circle_insert('theo', 'AUGC', '3') == 'GCAUAUACCAGCCGAAAGGCCCUUGGCAGAUGCAUGC'
    assert circle_insert('theo', 'AUGC', '5') == 'AUGCAUGCAUACCAGCCGAAAGGCCCUUGGCAGGCAU'
    assert circle_insert('theo', 'AUGC', '3', num_aptamers=2) == 'GCAUAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAUGCAUGC'

def test_wt_sgrna():
    assert from_name('wt') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('wt(aavs)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_dead_sgrna():
    assert from_name('dead').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAACCCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_upper_stem():
    import pytest

    with pytest.raises(ValueError): from_name('us(5)')

    assert from_name('us(4)') == from_name('us(4,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAAUACCAGCCGAAAGGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(2)') == from_name('us(2,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCAUACCAGCCGAAAGGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0)') == from_name('us(0,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,7)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAUAUACCAGCCGAAAGGCCCUUGGCAGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,7)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCUGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,7)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCUUUCCCUGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,0,2)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_lower_stem():
    import pytest

    with pytest.raises(ValueError): from_name('ls(7)')

    assert from_name('ls(6,0)') == from_name('ls(6)') == 'GGGGCCACTAGGGACAGGATGUUUUAAUACCAGCCGAAAGGCCCUUGGCAGUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(5,0)') == from_name('ls(5)') == 'GGGGCCACTAGGGACAGGATGUUUUAUACCAGCCGAAAGGCCCUUGGCAGAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,0)') == from_name('ls(0)') == 'GGGGCCACTAGGGACAGGATAUACCAGCCGAAAGGCCCUUGGCAGAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(6,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(6,7)') == 'GGGGCCACTAGGGACAGGATGUUUUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,1)') == 'GGGGCCACTAGGGACAGGATUAUACCAGCCGAAAGGCCCUUGGCAGUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,7)') == 'GGGGCCACTAGGGACAGGATUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_nexus():
    assert from_name('nx(0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nx(1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGUAUACCAGCCGAAAGGCCCUUGGCAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nx(6)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGUUUUUUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_nexus_2():
    import pytest

    with pytest.raises(ValueError): from_name('nxx(5,0)')
    with pytest.raises(ValueError): from_name('nxx(0,6)')
    with pytest.raises(ValueError): from_name('nxx(0,0,4)')
    with pytest.raises(ValueError): from_name('nxx(0,0,5,0)')

    assert from_name('nxx(0,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAAUACCAGCCGAAAGGCCCUUGGCAGGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(1,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGAUACCAGCCGAAAGGCCCUUGGCAGCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(2,2)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(2,3)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,5)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,6)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,7)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCUGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,8)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCUUGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,0,2)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,0,3)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,10,2)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCUUUCCCUUUCGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_replace_hairpins():
    assert from_name('hp(0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(18)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(33)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(39)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(49)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCUUUCCCUUUCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'

def test_induce_dimerization():
    import pytest

    with pytest.raises(ValueError): from_name('id(0,0)')
    with pytest.raises(ValueError): from_name('id(hello,0)')
    with pytest.raises(ValueError): from_name('id(3,5)')
    with pytest.raises(ValueError): from_name('id(3,hello)')

    assert from_name('id(5,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCC'
    assert from_name('id(5,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGAUACCAGCC'
    assert from_name('id(5,2)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCAUACCAGCC'
    assert from_name('id(5,3)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUACCAGCC'
    assert from_name('id(5,4)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAAUACCAGCC'

    assert from_name('id(3,0)') == 'GGGGCCACTAGGGACAGGATGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,1)') == 'GGGGCCACTAGGGACAGGATGGCCCUUGGCAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,2)') == 'GGGGCCACTAGGGACAGGATGGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,3)') == 'GGGGCCACTAGGGACAGGATGGCCCUUGGCAGAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,4)') == 'GGGGCCACTAGGGACAGGATGGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'


if __name__ == '__main__':
    import sys, pytest
    pytest.main(sys.argv)
