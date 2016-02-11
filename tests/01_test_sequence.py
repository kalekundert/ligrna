#!/usr/bin/env python

import pytest
from sgrna_sensor import *

def test_domain_class():
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

    domain.append('UU')
    assert domain.seq == 'GACAUU'

    domain.prepend('UU')
    assert domain.seq == 'UUGACAUU'

def test_construct_class():
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
    for i, domain in enumerate(expected_domains):
        assert dave.domain_from_index(i) == domain
        assert dave.index_from_domain(domain[0].name, domain[1]) == i
    for i, domain in enumerate(reversed(expected_domains), 1):
        assert dave.domain_from_index(-i) == domain
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


