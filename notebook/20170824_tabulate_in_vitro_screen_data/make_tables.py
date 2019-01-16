#!/usr/bin/env python3

"""\
Summarize the results from all the in vitro rational design screens into a 
single table, which will go in the supplement.

Usage:
    make_tables.py
"""

import docopt
import jinja2
import sgrna_sensor
import pandas as pd
from enum import Enum
from sgrna_sensor import densiometry
from pprint import pprint

class Domain(Enum):
    NONE = ""
    UPPER = "Upper Stem"
    LOWER = "Lower Stem"
    NEXUS = "Nexus"
    HAIRPIN = "Hairpin"

class AlignGroup(Enum):
    CONTROL = 1
    STEMS = 2
    NEXUS = 3
    HAIRPIN = 4
    
class Strategy(Enum):
    POS_CTL = "Positive Control"
    NEG_CTL = "Negative Control"
    STEM_REP = "Stem Replacement"
    STR_DISP = "Strand displacement"
    IND_DIM = "Induced Dimerization"

class Algorithm(Enum):
    CONTROL = 1
    FOLD = 2
    CIRCLE = 3
    SERPENTINE = 4
    ZIPPER = 5

def load_rational_designs():
    df = densiometry.load_cleavage_data_from_xlsx_dir('densiometry')
    df = densiometry.calc_mean_change(df)

    df = df.apply(name_to_strategy, axis='columns')
    df['strategy'] = pd.Categorical(df.strategy, [e.value for e in Strategy])
    df['domain'] = pd.Categorical(df.domain, [e.value for e in Domain])
    df['active'] = abs(df.mean_change) > 0.15
    df['sequence'] = df.apply(name_to_sequence, axis='columns')
    #df['aligned_sequence'] = align_sequences(df.sequence)

    df = discard_modified_aptamers(df)
    df = get_pretty_sequences(df)

    priority = ['align_group', 'strategy', 'algorithm', 'domain', 'earliest_date', 'earliest_order']
    df = df.sort_values(priority).reset_index(drop=True)
    df['id'] = df.index.values + 1

    return df

def discard_controls(df):
    controls = Strategy.POS_CTL.value, Strategy.NEG_CTL.value
    return df[~df.strategy.isin(controls)]

def discard_modified_aptamers(df):

    def is_splitter(row): #
        if row.strategy == Strategy.IND_DIM.value:
            return False

        sgrna = sgrna_sensor.from_name(row.design, target='aavs')

        try:
            return sgrna['aptamer/splitter'] != 'GAAA'
        except KeyError:
            return False

    mask = df.apply(is_splitter, axis='columns')
    return df[~mask]
    #return df[mask]


def get_pretty_sequences(df):
    for i, group in df.groupby('align_group'):
        sequences = []

        # Break each sequence into domains, which will be colored and aligned 
        # separately.
        for j, row in group.iterrows():
            sequences.append(get_pretty_domains(row))

        # Make sure each sequence has the same number of domains.
        num_domains = len(sequences[0])
        try:
            for domains in sequences:
                assert len(domains) == num_domains
        except AssertionError:
            pprint(sequences)
            raise

        # Figure out how long every domain is, so that they can be aligned to 
        # constant widths.
        domain_lens = {}
        for domains in sequences:
            for i in range(num_domains):
                domain_len = len(domains[i].seq)
                domain_lens.setdefault(i, set()).add(domain_len)

        alignment_widths = {
                k: max(v)
                for k,v in domain_lens.items()
                if len(domain_lens[k]) > 1
        }

        # Render each sequence using LaTeX.
        pretty_seqs = []
        for domains in sequences:
            pretty_seq = ''
            direction = '>'

            for i in range(num_domains):
                if i in alignment_widths:
                    width = alignment_widths[i]
                    direction = '<' if direction == '>' else '>'
                    fmt = f'-{direction}{width}s'
                else:
                    fmt = 's'

                pretty_seq += r'\color{%s}' % domains[i].color
                pretty_seq += fr'\verb|{domains[i].seq:{fmt}}|'

            pretty_seqs.append(pretty_seq)

        # Add the pretty sequence back to the data frame.
        df.loc[group.index, 'pretty_sequence'] = pretty_seqs

    return df

def get_pretty_domains(row):

    def get_aptamer_start(sgrna):
        try:
            return sgrna.index_from_domain("aptamer/5'", 0)
        except KeyError:
            return sgrna.index_from_domain("aptamer", 0)

    def get_aptamer_end(sgrna):
        try:
            return sgrna.index_from_domain("aptamer/3'", 0) + len(sgrna["aptamer/3'"])
        except KeyError:
            return sgrna.index_from_domain("aptamer", 0) + len(sgrna["aptamer"])


    if row.algorithm == Algorithm.CONTROL.value:
        sgrna = sgrna_sensor.from_name(row.design, target='aavs')
        sequence = sgrna.rna
        domain_map = [
                ('ucsfblue', sgrna.index_from_domain('stem', 0)),
                ('ucsfnavy', sgrna.index_from_domain('nexus', 0)),
                ('ucsfteal', sgrna.index_from_domain('hairpins', 0)),
                ('ucsfblack', sgrna.index_from_domain('tail', 0)),
        ]

    elif row.strategy == Strategy.IND_DIM.value:
        name, n = row.design.split('/')
        sgrna_5 = sgrna_sensor.from_name(f'{name}/5/{n}', target='aavs')
        sgrna_3 = sgrna_sensor.from_name(f'{name}/3/{n}')
        divider = '    '
        len_5 = len(sgrna_5) + len(divider)

        sequence = f'{sgrna_5.rna}{divider}{sgrna_3.rna}'
        domain_map = [
                ('ucsfpurple', get_aptamer_start(sgrna_5)),
                (None, len_5 + get_aptamer_end(sgrna_3)),
                ('ucsfblue', sgrna_5.index_from_domain('stem', 0)),
                ('ucsfnavy', len_5 + sgrna_3.index_from_domain('nexus', 0)),
                ('ucsfteal', len_5 + sgrna_3.index_from_domain('hairpins', 0)),
                ('ucsfblack', len_5 + sgrna_3.index_from_domain('tail', 0)),
        ]

    else:
        sgrna = sgrna_sensor.from_name(row.design, target='aavs')
        sequence = sgrna.rna
        domain_map = [
                ('ucsfpurple', get_aptamer_start(sgrna)),
                (None, get_aptamer_end(sgrna)),
                ('ucsfblue', sgrna.index_from_domain('stem', 0)),
                ('ucsfnavy', sgrna.index_from_domain('nexus', 0)),
                ('ucsfteal', sgrna.index_from_domain('hairpins', 0)),
                ('ucsfblack', sgrna.index_from_domain('tail', 0)),
        ]

    class Domain:

        def __init__(self, seq, color): #
            self.seq = seq
            self.color = color

        def __repr__(self): #
            return f"Domain('{self.seq}', '{self.color}')"


    domains = []
    colors, indices = zip(*sorted(domain_map, key=lambda x: x[1]))
    colors, indices = list(colors), list(indices)
    colors = ['ucsfblack'] + colors
    slices = list(zip([0] + indices, indices + [len(sequence)]))

    for i in range(len(indices) + 1):
        a, b = slices[i]
        color = colors[i] or colors[i-2]
        subseq = sequence[a:b]

        domain = Domain(subseq, color)
        domains.append(domain)

    return domains


def align_sequences(seqs):
    import io
    from subprocess import run, PIPE
    from skbio.io import read, write
    from skbio.sequence import Sequence

    fasta = 'rational_designs.fa'
    seqs = (Sequence(x) for x in seqs)
    write(seqs, format='fasta', into=fasta)

    clustalo = 'clustalo', '-i', fasta
    stdout = run(clustalo, stdout=PIPE, encoding='utf8').stdout
    stdout_io = io.StringIO(stdout)
    msa = read(stdout_io, format='fasta')

    return [str(x) for x in msa]

def name_to_strategy(row):
    name = row.design

    if name in ('wt', 'on'):
        domain = Domain.NONE
        align = AlignGroup.CONTROL
        strategy = Strategy.POS_CTL
        algorithm = Algorithm.CONTROL

    elif name in ('dead', 'off'):
        domain = Domain.NONE
        align = AlignGroup.CONTROL
        strategy = Strategy.NEG_CTL
        algorithm = Algorithm.CONTROL

    elif name[0:2] == 'us':
        domain = Domain.UPPER
        align = AlignGroup.STEMS
        strategy = Strategy.STEM_REP
        algorithm = Algorithm.FOLD

    elif name[0:2] == 'ls':
        domain = Domain.LOWER
        align = AlignGroup.STEMS
        strategy = Strategy.STEM_REP
        algorithm = Algorithm.FOLD

    elif name[0:2] == 'nx':
        domain = Domain.NEXUS
        align = AlignGroup.NEXUS
        strategy = Strategy.STEM_REP
        algorithm = Algorithm.FOLD

    elif name[0:2] == 'hp':
        domain = Domain.HAIRPIN
        align = AlignGroup.HAIRPIN
        strategy = Strategy.STEM_REP
        algorithm = Algorithm.FOLD

    elif name[0:2] == 'id':
        domain = Domain.UPPER
        align = AlignGroup.STEMS
        strategy = Strategy.IND_DIM
        algorithm = Algorithm.ZIPPER

    else:
        domains = {
                'u': Domain.UPPER,
                'b': Domain.UPPER,  # "b" really means "bulge", but I'm 
                'l': Domain.LOWER,  # counting that as part of the upper stem.
                'x': Domain.NEXUS,
                'h': Domain.HAIRPIN,
        }
        align_groups = {
                'u': AlignGroup.STEMS,
                'b': AlignGroup.STEMS,
                'l': AlignGroup.STEMS,
                'x': AlignGroup.NEXUS,
                'h': AlignGroup.HAIRPIN,
        }
        strategies = {
                'f': Strategy.STEM_REP,
                'z': Strategy.IND_DIM,
                's': Strategy.STR_DISP,
                'c': Strategy.STR_DISP,
        }
        algorithms = {
                'f': Algorithm.FOLD,
                'z': Algorithm.ZIPPER,
                's': Algorithm.SERPENTINE,
                'c': Algorithm.CIRCLE,
        }
        domain = domains[name[1]]
        align = align_groups[name[1]]
        strategy = strategies[name[0]]
        algorithm = algorithms[name[0]]

    row['domain'] = domain.value
    row['align_group'] = align.value
    row['strategy'] = strategy.value
    row['algorithm'] = algorithm.value

    return row

def name_to_sequence(row):
    if row.strategy == Strategy.IND_DIM.value:
        name, n = row.design.split('/')
        sgrna_5 = sgrna_sensor.from_name(f'{name}/5/{n}', target='aavs')
        sgrna_3 = sgrna_sensor.from_name(f'{name}/3/{n}', target='aavs')
        return f'{sgrna_5.rna}&{sgrna_3.rna}'

    else:
        sgrna = sgrna_sensor.from_name(row.design, target='aavs')
        return sgrna.rna

def name_to_pretty_sequence(row):
    if row.strategy in (Strategy.POS_CTL.value, Strategy.NEG_CTL.value):
        sgrna = sgrna_sensor.from_name(row.design, target='aavs')
        sequence = sgrna.rna

        colors_from_indices = {
                sgrna.index_from_domain('stem', 0): 'ucsfblue',
                sgrna.index_from_domain('nexus', 0): 'ucsfnavy',
                sgrna.index_from_domain('hairpins', 0): 'ucsfteal',
                sgrna.index_from_domain('tail', 0): 'ucsfblack',
        }

    elif row.strategy == Strategy.IND_DIM.value:
        name, n = row.design.split('/')
        sgrna_5 = sgrna_sensor.from_name(f'{name}/5/{n}', target='aavs')
        sgrna_3 = sgrna_sensor.from_name(f'{name}/3/{n}')
        len_5 = len(sgrna_5) + 3

        sequence = f'{sgrna_5.rna} & {sgrna_3.rna}'

        colors_from_indices = {
                sgrna_5.index_from_domain('stem', 0): 'ucsfblue',
                len_5 + sgrna_3.index_from_domain('nexus', 0): 'ucsfnavy',
                len_5 + sgrna_3.index_from_domain('hairpins', 0): 'ucsfteal',
                len_5 + sgrna_3.index_from_domain('tail', 0): 'ucsfblack',
                len(sgrna_5): 'ucsflightgrey',
                len(sgrna_5) + 3: 'ucsforange',
                get_aptamer_start(sgrna_5): 'ucsforange',
                len_5 + get_aptamer_end(sgrna_3): 'ucsfblue',
        }

    else:
        sgrna = sgrna_sensor.from_name(row.design, target='aavs')
        sequence = sgrna.rna

        colors_from_indices = {
                sgrna.index_from_domain('stem', 0): 'ucsfblue',
                sgrna.index_from_domain('nexus', 0): 'ucsfnavy',
                sgrna.index_from_domain('hairpins', 0): 'ucsfteal',
                sgrna.index_from_domain('tail', 0): 'ucsfblack',
                get_aptamer_start(sgrna): 'ucsforange',
                get_aptamer_end(sgrna): None,
        }

    indices = list(reversed(sorted(colors_from_indices.keys())))
    colors = [colors_from_indices[i] for i in indices]

    for x in range(len(colors_from_indices)):
        index = indices[x]
        color = colors[x] or colors[x+2]
        sequence = insert_color(sequence, index, color)

    return r'{ \verb|' + sequence + '| }'

def insert_color(string, i, color):
    return string[:i] + r"|\color{%s}\verb|" % color + string[i:]


def make_summary_table(df):
    df = discard_controls(df)
    context = dict(df=df)

    sgrna_sensor.render_template('summary_tabular.tex', context)
    sgrna_sensor.latex('summary_table.tex')

def make_full_table(df):
    context = dict(df=df)
    sgrna_sensor.render_template('full_tabular.tex', context)
    sgrna_sensor.render_template('full_tabular_with_names.tex', context)

    sgrna_sensor.latex('full_table.tex')
    sgrna_sensor.latex('full_table_with_names.tex')


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    df = load_rational_designs()


    #make_summary_table(df)
    make_full_table(df)

