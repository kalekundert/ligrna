#!/usr/bin/env python

import pytest
from sgrna_sensor import *

def test_complements():
    assert complement('ACUG') == 'UGAC'
    assert reverse_complement('ACUG') == 'CAGU'

def test_find_middlemost():
    # Test a few simple cases.
    assert find_middlemost('G', '(G)') == [(0,0)]
    assert find_middlemost('AG', '(G)') == [(1,0)]
    assert find_middlemost('AGA', '(G)') == [(1,1)]

    # Make sure the middlemost group is found, not the middlemost start.
    assert find_middlemost('GGGAGGGA', 'GGG(A)') == [(3,4)]

    # If there is a tie, the leftmost match will be returned.
    assert find_middlemost('AGGA', '([G])') == [(1,2)]
    assert find_middlemost('AGGAA', '([G])') == [(2,2)]
    assert find_middlemost('AAGGA', '([G])') == [(2,2)]

    # If multiple groups exist, use whichever one matches.
    assert find_middlemost('GGGGG', '(A)|(G)') == [(2,2)]

    # If multiple matches are requested, make sure they are all found.
    assert find_middlemost('GGGGG', '(G)', 2) == [(2,2), (1,3)]
    assert find_middlemost('GGGGG', '(G)', 3) == [(2,2), (1,3), (3,1)]

    # Find overlapping patterns.
    assert find_middlemost('GGGGG', 'G(G)') == [(2,2)]

    # Raise a ValueError if the pattern isn't found.
    with pytest.raises(ValueError):
        find_middlemost('GGGGGG', '(A)')
    with pytest.raises(ValueError):
        find_middlemost('GGAGGG', '(A)', 2)
    
    # Test some "real life" cases.
    assert find_middlemost('AGGGA', '([GU])') == [(2,2)]
    assert find_middlemost('ACGACGU', '[AU](.)[CG]') == [(4,2)]

