#!/usr/bin/env python2
# encoding: utf-8

from __future__ import division

import RNA, re
import numpy as np
import matplotlib.pyplot as plt
from math import *
from pylab import *
from sgrna_helper import reverse as r
from sgrna_helper import complement as c
from sgrna_helper import reverse_complement as rc

class Mutant (object):

    def __init__(self, effector, on, off, strategy=None):
        self.effector = str(effector)
        self.on = str(on)
        self.off = str(off)
        self.strategy = strategy

        # Discount if the ends aren't base paired?

        #self.on_duplex = RNA.duplexfold('GG' + self.effector + 'GG', 'CC' + self.on + 'CC')
        #self.on_base_pairs = self.on_duplex.structure[2:-2]

        #self.off_duplex = RNA.duplexfold('GG%sGG'%self.effector, 'CC%sCC'%self.off)
        #self.off_base_pairs = self.off_duplex.structure[2:-2]

        self.on_duplex = RNA.duplexfold(self.effector, self.on)
        self.on_base_pairs = self.on_duplex.structure

        self.off_duplex = RNA.duplexfold(self.effector, self.off)
        self.off_base_pairs = self.off_duplex.structure

        on_bp_5, on_bp_3 = self.on_base_pairs.split('&')
        off_bp_5, off_bp_3 = self.off_base_pairs.split('&')
        self.ends_paired = True

        if len(on_bp_5) != len(self.effector):
            self.ends_paired = False
        if on_bp_5.startswith('.') or on_bp_5.endswith('.'):
            self.ends_paired = False

        if len(on_bp_3) != len(self.on):
            self.ends_paired = False
        if on_bp_3.startswith('.') or on_bp_3.endswith('.'):
            self.ends_paired = False

        if len(off_bp_5) != len(self.effector):
            self.ends_paired = False
        if off_bp_5.startswith('.') or off_bp_5.endswith('.'):
            self.ends_paired = False

        if len(off_bp_3) != len(self.off):
            self.ends_paired = False
        if off_bp_3.startswith('.') or off_bp_3.endswith('.'):
            self.ends_paired = False

        self.dg_on = self.on_duplex.energy
        self.dg_off = self.off_duplex.energy
        self.dg = self.dg_on - self.dg_off

    def __repr__(self):
        return 'Mutant(effector={}, on={}, off={})'.format(
                self.effector, self.on, self.off)

    def __lt__(self, other):
        return self.dg < other.dg

    def __iter__(self):
        yield self.effector
        yield self.on
        yield self.off



rna_bases = 'ACGU'

def mutate(seq, i, nuc):
    return replace(seq, i, i+1, nuc)

def insert(seq, i, insert):
    return replace(seq, i, i, insert)

def remove(seq, i):
    return replace(seq, i, i+1, '')
def replace(seq, i, j, insert):
    return seq[:i] + insert + seq[j:]


def yield_mutants(off):
    for mutant in yield_all_mutants(off):
        if mutant.ends_paired:
            yield mutant

def yield_all_mutants(off):
    N = len(off)
    ideal_effector = rc(off)
    ideal_on = off

    # Return the original sequence

    yield Mutant(ideal_effector, ideal_on, off)

    # Add a mismatch to the off state by mutating a base pair in the "on" and 
    # "effector" sequences.

    for i in range(N):
        for nuc in rna_bases:
            if nuc != ideal_effector[i]:
                effector = mutate(ideal_effector, i, nuc)
                strategy = 'mismatch', ''.join(sorted((nuc, off[N-i-1])))
                yield Mutant(effector, rc(effector), off, strategy)

    # Add a mismatch to the "on" state by mutating the "on" sequence.

    for i in range(N):
        for nuc in rna_bases:
            if nuc != ideal_on[i]:
                on = mutate(ideal_on, i, nuc)
                strategy = 'mutate'
                strategy = 'mismatch', ''.join(sorted((nuc, ideal_effector[N-i-1])))
                yield Mutant(ideal_effector, on, off, strategy)

    # Add a bulge to the "off" state by inserting a base pair into the "on" and 
    # "effector" sequences.

    for i in range(1, N):
        for nuc in rna_bases:
            effector = insert(ideal_effector, i, nuc)
            strategy = 'insert',
            yield Mutant(effector, rc(effector), off, strategy)

    # Add a bulge to the "off" state the removing a base pair from the "on" and 
    # "effector" sequences.

    for i in range(N):
        effector = remove(ideal_effector, i)
        strategy = 'delete',
        yield Mutant(effector, rc(effector), off, strategy)

    # Add a bulge to the "on" state by inserting a nucleotide into the "on" 
    # sequence.

    for i in range(1, N):
        for nuc in rna_bases:
            on = insert(ideal_on, i, nuc)
            strategy = 'insert',
            yield Mutant(ideal_effector, on, off, strategy)

    # Add a bulge to the "on" state by removing a nucleotide from the "on" 
    # sequence.

    for i in range(N):
        on = remove(ideal_on, i)
        strategy = 'delete',
        yield Mutant(ideal_effector, on, off, strategy)

def plot_mutants(generator):
    mutants = []
    indices = []
    energies = []
    colors = []
    areas = []

    def pick_style(mutant):
        import tango
        radius = 5 if mutant.ends_paired else 2

        if mutant.strategy is None:
            return radius, tango.black
        if 'insert' in mutant.strategy:
            return radius, tango.grey[2]
        if 'delete' in mutant.strategy:
            return radius, tango.white

        if 'GU' in mutant.strategy:
            color = tango.blue[0]

        elif 'AC' in mutant.strategy:
            color = tango.green[0]
        elif 'AG' in mutant.strategy:
            color = tango.green[0]
        elif 'GG' in mutant.strategy:
            color = tango.green[0]
        elif 'UU' in mutant.strategy:
            color = tango.green[0]

        elif 'CC' in mutant.strategy:
            color = tango.red[0]
        elif 'CU' in mutant.strategy:
            color = tango.red[0]

        else:
            color = tango.orange[0]
            radius = 10

        return radius, color

    def print_selection(event):
        i = event.ind[0]
        mutant = mutants[i]
        print mutant.on, "(on)"
        print ''.join(reversed(mutant.effector)), "(effector)"
        print mutant.off, "(off)"
        print 'ΔG =', mutant.dg
        print mutant.on_duplex.structure
        print mutant.off_duplex.structure
        print


    for i, mutant in enumerate(generator):
        mutants.append(mutant)
        indices.append(i)
        energies.append(mutant.dg)
        radius, color = pick_style(mutant)
        colors.append(color)
        areas.append(2*pi*radius)

    scatter(indices, energies, s=areas, c=colors, picker=True)

    gcf().canvas.mpl_connect('pick_event', print_selection)


gu_pattern = re.compile('[GU]')
au_au_pattern = re.compile('[AU].[AU]')
au_gc_pattern = re.compile('[AU].[GC]|[GC].[AU]')
gc_gc_pattern = re.compile('[GC].[GC]')

au_au_mismatches = {
        'A': 'G',
        'C': 'U',
        'G': 'A',
        'U': 'C',
}
au_gc_mismatches = {
        'A': 'C',
        'C': 'C',
        'G': 'A',
        'U': 'C',
}
gc_gc_mismatches = {
        'A': 'G',
        'C': 'C',
        'G': 'A',
        'U': 'C',
}


def wobble(off, effect='x', location='center'):

    # Find all the positions where a wobble base pair could be made, i.e. all 
    # the positions in the "off" sequence that are either G or U.

    if effect == 'x':
        gu_iter = re.finditer('[GU]', off)

    elif effect == 'o':
        gu_iter = re.finditer('[AC]', off)

    else:
        raise ValueError("Unknown effect: '{}'".format(effect))

    gus = [x.start() for x in gu_iter]

    if not gus:
        raise RnaDesignError("No G or U nucleotides in input sequence.")

    # Decide where to insert the wobble base pair based on the location 
    # argument.  The default is to mutate the center-most position, but the 
    # user can choose to mutate the inner- or outer-most positions as well.

    if location == 'center':
        N = D = len(off)
        for i in gus:
            d = abs(i - N/2)
            if d < D: gu, D = i, d

    elif location == 'edge':
        # We'll assume that the edge is on the left, here.
        gu = gus[0]

    elif location == 'non-edge':
        gu = gus[-1]

    else:
        raise ValueError("Unknown location: '{}'".format(location))

    # Create "on" and "effector" sequences that will have the desired effect.
    # The effect "x" means more cutting is desired, so the interaction between 
    # the "effector" and "off" sequences has to be weakened.  The effect "o" 
    # means that less cutting is desired, so the interaction between the 
    # "effector" and "on" sequences has to be weakened.
    
    if effect == 'x':
        effector = r(mutate(c(off), gu, {'G':'U','U':'G'}[off[gu]]))
        on = rc(effector)

    elif effect == 'o':
        on = mutate(off, gu, {'C':'U','A':'G'}[off[gu]])
        effector = rc(off)

    return Mutant(effector, on, off)
    
def mismatch(off, pattern, mutations, effect='x', location='center'):
    import re

    matches = pattern.finditer(off)
    indices = [x.start() + 1 for x in matches]
    if not indices: raise RnaDesignError
    i = pick_location(location, indices, len(off))

    if effect == 'x':
        effector = rc(mutate(off, i, c(mutations[off[i]])))
        on = rc(effector)

    elif effect == 'o':
        on = mutate(off, i, mutations[c(off[i])])
        effector = rc(off)

    return Mutant(effector, on, off)

def mismatch_au_au(off, **kwargs):
    # This could be more general: find a pattern and call a function to get 
    # mutation.  Have to think about x/o strand implications, though.
    return mismatch(off, au_au_pattern, au_au_mismatches, **kwargs)

def mismatch_au_gc(off, **kwargs):
    return mismatch(off, au_gc_pattern, au_gc_mismatches, **kwargs)

def mismatch_gc_gc(off, **kwargs):
    return mismatch(off, gc_gc_pattern, gc_gc_mismatches, **kwargs)

def mismatch_center(off, effect='x'):
    i = len(off) // 2
    context = off[i-1:i+2]

    if len(off) < 3:
        raise RnaDesignError

    if au_au_pattern.match(context):
        mut_table = au_au_mismatches
    elif au_gc_pattern.match(context):
        mut_table = au_gc_mismatches
    elif gc_gc_pattern.match(context):
        mut_table = gc_gc_mismatches
    else:
        raise AssertionError

    if effect == 'x':
        effector = rc(mutate(off, i, c(mut_table[off[i]])))
        on = rc(effector)

    elif effect == 'o':
        on = mutate(off, i, mut_table[c(off[i])])
        effector = rc(off)

    return Mutant(effector, on, off)

def bulge_on(off, insert_len=1):
    on = insert(off, len(off) // 2, insert_len * 'A')
    effector = rc(off)
    return Mutant(effector, on, off)

def bulge_eff_au(off):
    effector = insert(rc(off), len(off) // 2, 'A')
    on = rc(effector)
    return Mutant(effector, on, off)

def bulge_eff_gc(off):
    effector = insert(rc(off), len(off) // 2, 'G')
    on = rc(effector)
    return Mutant(effector, on, off)


def pick_location(location, choices, N):

    if location == 'center':
        D = rv = N
        for i in choices:
            d = abs(i - N/2)
            if d < D: rv, D = i, d

    elif location == 'edge':
        # We'll assume that the edge is on the left, here.
        rv = choices[0]

    elif location == 'non-edge':
        rv = choices[-1]

    else:
        raise ValueError("Unknown location: '{}'".format(location))

    return rv
    
def test_mutants(mutant_factory, **factory_kwargs):
    for label, seq in yield_design_seqs():
        try:
            print mutant_factory(seq, **factory_kwargs)
        except RnaDesignError:
            pass


def yield_random_seqs():
    """
    Return all sequences with between 4 and 6 nucleotides, which works out to 
    4**4 + 4**5 + 4**6 = 5376 sequences.
    """
    import itertools

    for N in [4]:
        for seq in itertools.product('ACGU', repeat=N):
            yield ''.join(seq)

def yield_design_seqs():
    yield 'sb(2)', 'GU'
    yield 'sb(5)', 'GUUAA'
    yield 'sb(8)', 'GUUAAAAU'
    yield 'sl()',  'AGCC'
    yield 'slx()', 'GUUAUC'
    yield 'sh(5)', 'AACGG'
    yield 'sh(7)', 'AACGGAC'
    yield 'cb()',  'AAGU'
    yield 'cl()',  'AAGGCU'
    yield 'ch(4)', 'AUCA'


def plot_mutants(i, color, mutant_factory, **factory_kwargs):
    import tango

    def get_mutant_dg(seq):
        try:
            return mutant_factory(seq, **factory_kwargs).dg
        except RnaDesignError:
            return 0

    def print_selection(event):
        print event
        print design_labels[event.ind[0]]


    random_style = {
            'color': color,
            'marker': ',',
            'linestyle': '',
    }
    random_energies = [
            get_mutant_dg(seq)
            for seq in yield_random_seqs()
    ]
    random_indices = linspace(i-0.4, i+0.4, len(random_energies))
    plot(random_energies, random_indices, **random_style)

    design_style = {
            'color': color,
            'marker': 'o',
            'linestyle': '',
    }
    design_energies = [
            get_mutant_dg(seq)
            for label, seq in yield_design_seqs()
    ]
    design_labels = [
            label
            for label, seq in yield_design_seqs()
    ]
    design_indices = linspace(i-0.4, i+0.4, len(design_energies))
    plot(design_energies, design_indices, **design_style)

    gcf().canvas.mpl_connect('pick_event', print_selection)


class MutantPlotter:

    def __init__(self):
        self.i = 0
        self.yticks = []
        self.yticklabels = []
        self.color_i = 0
        self.color_j = 0

    def plot_mutants(self, mutant_factory, **factory_kwargs):
        plot_mutants(
                self.i, self.current_color(),
                mutant_factory, **factory_kwargs)
        self.add_ylabel(mutant_factory, **factory_kwargs)
        self.i -= 1

    def plot_all_args(self, mutant_factory):
        import tango
                    
        for effect in ('x', 'o'):
            for location in ('center', 'edge'):
                plot_mutants(
                        self.i, self.current_color(),
                        mutant_factory, effect=effect, location=location)
                self.add_ylabel(
                        mutant_factory, effect=effect, location=location)
                self.i -= 1

        self.next_color()

    def add_ylabel(self, mutant_factory, **factory_kwargs):
        ylabel = mutant_factory.__name__

        args = ', '.join(
            '{}={}'.format(k, v)
            for k, v in factory_kwargs.items()
        )

        if args:
            ylabel += ' (' + args + ')'

        self.yticks.append(self.i)
        self.yticklabels.append(ylabel)

    def current_color(self):
        import tango
        color_cycle = [
                tango.red + tango.grey[::-1],
                tango.green + tango.grey[::-1],
                tango.orange + tango.grey[::-1],
                tango.blue + tango.grey[::-1],
                tango.brown + tango.grey[::-1],
                tango.purple + tango.grey[::-1],
        ]
        color = color_cycle[self.color_i % len(color_cycle)][self.color_j]
        self.color_j += 1
        return color

    def next_color(self):
        self.color_i += 1
        self.color_j = 0


class RnaDesignError (Exception):

    def __init__(self, message=""):
        Exception.__init__(self, message)



#test_mutants(bulge_on_2)

fig, ax = plt.subplots()
p = MutantPlotter()
p.plot_all_args(wobble)
p.plot_mutants(mismatch_center, effect='x')
p.plot_mutants(mismatch_center, effect='o')
p.next_color()
p.plot_all_args(mismatch_gc_gc)
p.plot_all_args(mismatch_au_gc)
p.plot_all_args(mismatch_au_au)
p.plot_mutants(bulge_eff_au)
p.plot_mutants(bulge_eff_gc)
p.plot_mutants(bulge_on)
p.next_color()

ax2 = ax.twiny()
g_ticks = ax.get_xticks()
max_g = max(g_ticks)
kT = 0.593
max_k = int(log10(exp(max_g/kT)))
k_exps = range(-max_k, max_k+1)
k_labels = ['$\mathregular{10^{%d}}$' % k for k in k_exps]
k_ticks = [kT * log(10**k) for k in k_exps]

ax.yaxis.tick_right()
ax.set_ylim(p.i - 0.5, 1.5)
ax.set_yticks(p.yticks)
ax.set_yticklabels(p.yticklabels)

ax.set_xlabel('$\mathregular{\Delta G}$ (kcal/mol)')
ax2.set_xlabel('$\mathregular{K_{eq}}$', labelpad=13)
ax2.set_xticks(k_ticks)
ax2.set_xticklabels(k_labels)
ax2.xaxis.grid(True)

fig.subplots_adjust(left=0.06, right=0.60)
fig.set_size_inches(11, 8.5)
fig.savefig('tune_designs.pdf')
#show()
