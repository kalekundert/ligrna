#!/usr/bin/env python

import pytest
from sgrna_sensor import *

def test_from_name():
    with pytest.raises(ValueError):
        from_name('')
    with pytest.raises(ValueError):
        from_name('nosuchdesign')

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

    assert from_name('cb') == cb()
    assert from_name('cb/wo') == cb('wo')
    assert from_name('theo/cb') == cb()
    assert from_name('tet/cb') == cb(ligand='tet')

def test_wt_sgrna():
    assert from_name('wt') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'UAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC' 'UUUUUU'

def test_dead_sgrna():
    assert from_name('dead') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AACCCUAGUCCGU' 'UAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC' 'UUUUUU'

def test_liu_sgrna():
    assert from_name('gfp/liu').dna == 'CATCTAATTCAACAAGAATTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTGTTGAATTAGATGATACCACGCGAAAGCGCCTTGGCAGCATCTAATTTTTTTT'
    assert from_name('gfp2/liu').dna == 'AGTAGTGCAAATAAATTTAAGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTATTTGCACTACTATACCACGCGAAAGCGCCTTGGCAGAGTAGTGCATTTTTT'
    assert from_name('rfp/liu').dna == 'AACTTTCAGTTTAGCGGTCTGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCGCTAAACTGAAAGTTATACCACGCGAAAGCGCCTTGGCAGAACTTTCAGTTTTTT'
    assert from_name('rfp2/liu').dna == 'TGGAACCGTACTGGAACTGCGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTCCAGTACGGTTCCAATACCACGCGAAAGCGCCTTGGCAGTGGAACCGTTTTTTT'
def test_on():
    assert from_name('on').seq == 'guuuCagagcuaUGCUGgaaaCAGCAuagcaaguuGaaauaaggcuaguccguuaucaacuugaaaaaguggcaccgagucggugcuuuuuu'.upper()

def test_off():
    assert from_name('off').seq == 'guuuCagagcuaUGCUGgaaaCAGCAuagcaaguuGaaauaacccuaguccguuaucaacuugaaaaaguggcaccgagucggugcuuuuuu'.upper()

def test_fold_upper_stem():
    with pytest.raises(ValueError):
        from_name('us(5)')

    assert from_name('us(4)') == from_name('us(4,0)') == 'GUUUUAGAGCUAAUACCAGCCGAAAGGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(2)') == from_name('us(2,0)') == 'GUUUUAGAGCAUACCAGCCGAAAGGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0)') == from_name('us(0,0)') == 'GUUUUAGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,1)') == 'GUUUUAGAGCUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,7)') == 'GUUUUAGAGCUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,1)') == 'GUUUUAGAUAUACCAGCCGAAAGGCCCUUGGCAGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,7)') == 'GUUUUAGAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,1)') == 'GUUUUAGAAUACCAGCCUGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,7)') == 'GUUUUAGAAUACCAGCCUUUCCCUGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,0,2)') == 'GUUUUAGAAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_lower_stem():
    with pytest.raises(ValueError):
        from_name('ls(7)')

    assert from_name('ls(6,0)') == from_name('ls(6)') == 'GUUUUAAUACCAGCCGAAAGGCCCUUGGCAGUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(5,0)') == from_name('ls(5)') == 'GUUUUAUACCAGCCGAAAGGCCCUUGGCAGAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,0)') == from_name('ls(0)') == 'AUACCAGCCGAAAGGCCCUUGGCAGAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(6,1)') == 'GUUUUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(6,7)') == 'GUUUUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,1)') == 'UAUACCAGCCGAAAGGCCCUUGGCAGUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,7)') == 'UUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_nexus():
    assert from_name('nx(0)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nx(1)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGUAUACCAGCCGAAAGGCCCUUGGCAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nx(6)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGUUUUUUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_nexus_2():
    with pytest.raises(ValueError):
        from_name('nxx(5,0)')
    with pytest.raises(ValueError):
        from_name('nxx(0,6)')
    with pytest.raises(ValueError):
        from_name('nxx(0,0,4)')
    with pytest.raises(ValueError):
        from_name('nxx(0,0,5,0)')

    assert from_name('nxx(0,0)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAAUACCAGCCGAAAGGCCCUUGGCAGGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(1,1)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGAUACCAGCCGAAAGGCCCUUGGCAGCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(2,2)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(2,3)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,5)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,6)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,7)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCUGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,8)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCUUGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,0,2)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,0,3)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,10,2)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCUUUCCCUUUCGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_fold_hairpin():
    with pytest.raises(ValueError):
        from_name('fh(0,0)')
    with pytest.raises(ValueError):
        from_name('fh(3,0)')
    with pytest.raises(ValueError):
        from_name('fh(1,5)')
    with pytest.raises(ValueError):
        from_name('fh(2,7)')

    assert from_name('fh(1,0)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAUACCAGCCGAAAGGCCCUUGGCAGGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('fh(1,4)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUAUACCAGCCGAAAGGCCCUUGGCAGAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('fh(2,0)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('fh(2,6)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAUACCAGCCGAAAGGCCCUUGGCAGCGGUGCUUUUUU'

def test_replace_hairpins():
    assert from_name('hp(0)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(18)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(33)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(39)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(49)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCUUUCCCUUUCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'

def test_induce_dimerization():
    with pytest.raises(ValueError):
        from_name('id(0,0)')
    with pytest.raises(ValueError):
        from_name('id(hello,0)')
    with pytest.raises(ValueError):
        from_name('id(3,5)')
    with pytest.raises(ValueError):
        from_name('id(3,hello)')

    assert from_name('id(5,0)').rna == 'GUUUUAGAAUACCAGCC'
    assert from_name('id(5,1)').rna == 'GUUUUAGAGAUACCAGCC'
    assert from_name('id(5,2)').rna == 'GUUUUAGAGCAUACCAGCC'
    assert from_name('id(5,3)').rna == 'GUUUUAGAGCUAUACCAGCC'
    assert from_name('id(5,4)').rna == 'GUUUUAGAGCUAAUACCAGCC'

    assert from_name('id(3,0)').rna == 'GGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,1)').rna == 'GGCCCUUGGCAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,2)').rna == 'GGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,3)').rna == 'GGCCCUUGGCAGAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,4)').rna == 'GGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_bulge():
    with pytest.raises(ValueError):
        from_name('sb(1)')

    assert from_name('sb(2)') == 'GUUUUAGAUCGUAUACCAGCCGAAAGGCCCUUGGCAGACGAAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('sb(8)') == 'GUUUUAGAUCGUUAAAAUAUACCAGCCGAAAGGCCCUUGGCAGAUUUUAACGAAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_lower_stem():
    assert from_name('sl') == 'UCGGCUGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUAGCCGAAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_lower_stem_around_nexus():
    assert from_name('slx') == 'GUUAUCGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUGAUAACAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_hairpin():
    with pytest.raises(ValueError):
        from_name('sh(3)')
    with pytest.raises(ValueError):
        from_name('sh(15)')

    assert from_name('sh(4)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGAUACCAGCCGAAAGGCCCUUGGCAGCGUUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('sh(14)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGGACUAGCCUUAUACCAGCCGAAAGGCCCUUGGCAGAAGGCUAGUCCGUUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_bulge():
    assert from_name('cb') == 'GUUUUAACUUAUACCAGCCGAAAGGCCCUUGGCAGAAGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_bulge_combo():
    assert from_name('cbc/wo/slx/wo').seq == 'GUUGUCACUUAUACCAGCCGAAAGGCCCUUGGCAGAGGUAAGUGAUAACAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('cbc/wo/sh/5') == 'GUUUUAACUUAUACCAGCCGAAAGGCCCUUGGCAGAGGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('cbc/wo/sh/7') == 'GUUUUAACUUAUACCAGCCGAAAGGCCCUUGGCAGAGGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGGACAUACCAGCCGAAAGGCCCUUGGCAGGUCCGUUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_lower_stem():
    assert from_name('cl') == 'AGCCUUGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUAAGGCUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_hairpin():
    with pytest.raises(ValueError):
        from_name('sh(3)')
    with pytest.raises(ValueError):
        from_name('sh(19)')

    assert from_name('ch(4)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAUCAAUACCAGCCGAAAGGCCCUUGGCAGUGAUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ch(18)') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAAGGCUAGUCCGUUAUCAAUACCAGCCGAAAGGCCCUUGGCAGUGAUAACGGACUAGCCUUGGCACCGAGUCGGUGCUUUUUU'

def test_random_bulge():
    assert from_name('rb(4,8)').seq == 'GUUUUA' 'NNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNNNN' 'UAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('rb(5,7)').seq == 'GUUUUA' 'NNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNNN' 'UAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('rb(6,6)').seq == 'GUUUUA' 'NNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNN' 'UAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_random_nexus():
    assert from_name('rx(6,6)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AA' 'NNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNN' 'GU' 'UAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC' 'UUUUUU'

def test_random_hairpin():
    assert from_name('rh(6,6)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(6,5)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(6,4)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(5,6)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(5,5)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(5,4)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(4,6)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(4,5)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('rh(4,4)').seq == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU' 'AAGGCUAGUCCGU' 'U' 'NNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'NNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'

def test_protein_binding_hairpin():
    assert from_name('ph/0').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GUUAUCA' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/1').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GUUAUCN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/2').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GUUAUNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/3').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GUUANNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/4').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GUUNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/5').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GUNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/6').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'GNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/7').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGU' 'CC' 'NNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/8').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUAGN' 'CC' 'NNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/9').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUANN' 'CC' 'NNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/10').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CUNNN' 'CC' 'NNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/11').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'CNNNN' 'CC' 'NNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('ph/12').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNN' 'CC' 'NNNNNNN' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GGCACCGAGUCGGUGC' 'UUUUUU'

def test_modify_nexus():
    assert from_name('mx(0)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'GUUAUCA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(1)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NUUAUCA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(2)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNUAUCA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(3)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNAUCA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(4)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNUCA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(5)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNCA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(6)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNNA' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(7)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNNN' 'ACUU' 'GAAA' 'AAGU' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(8)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNNN' 'NCUU' 'GAAA' 'AAGN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(9)').seq  == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNNN' 'NNUU' 'GAAA' 'AANN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(10)').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNNN' 'NNNU' 'GAAA' 'ANNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mx(11)').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GTGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCTAC' 'NNNNNNN' 'NNNN' 'GAAA' 'NNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'

    with pytest.raises(ValueError):
        from_name('mx(12)')

def test_modify_hairpin():
    assert from_name('mh(6)').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNN' 'CC' 'NN'  'AU' 'NN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('mh(7)').seq == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNN' 'CC' 'NNN' 'AU' 'NN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'

    with pytest.raises(ValueError): from_name('mh(5)')
    with pytest.raises(ValueError): from_name('mh(8)')
def test_modify_hairpin_forward():
    assert from_name('mhf/3').dna  == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGCGGTCCCGTCATCAGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/4').dna  == 'GTTTCAGAGCTATGCTTGAAACAGCATAGCAAGTTGAAATAAGGACGAACCGTAATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/7').dna  == 'GTTTCAGAGCTTTGCTGGAAACAGCATAGCAAGTTGAAATAAGGTCTGACCAGATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/13').dna == 'GTTTCAGAGCTTTGCTGGAAACAGCATAGCAAGTTGAAATAAGGTGACACCGCATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/16').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGTGGTACCATATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/20').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGTAAACCCCTCATCAGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/21').dna == 'GTTTCAGAGCTATGCTGGAAACAGAATAGCAAGTTGAAATAAGGATCCTCCCGCATGCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/25').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGACGTCCCGCATTCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/26').dna == 'GTTTCAGAGCTATGCTGGAAACAGTATAGCAAGTTGAAATAAGGTTCGTCCGCCATTCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/30').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGGTGTCCCGTATACGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/35').dna == 'GTTTCAGAGCTATACTGGAAACAGCATAGCAAGTTGAAATAAGGGCACTCCTAATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/37').dna == 'GTTTCAGAGCATGCTGGAAACAGCATAGCAAGTTGAAATAAGGTCTTCCCCGCATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/38').dna == 'GTTTCAGAGCCATGCTGGAAACAGCATAGCAAGTTGAAATAAGGACGGTCCCGCATCCGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('mhf/41').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGACTCTCCGTATCGGCCGATACCAGCCGAAAGGCCCTTGGCAGCGACGGCACCGAGTCGGTGCTTTTTT'

def test_seqlogo_hairpin():
    assert from_name('tpp/qh/3').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGGCUAGUCCGU' 'NNNNN' 'NNN'  'UCGGGGUGCCCUUCUGCGUGAAGGCUGAGAAAUACCCGUAUCACCUGAUCUGGAUAAUGCCAGCGUAGGGAA' 'NNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('tpp/qh/4').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGGCUAGUCCGU' 'NNNNN' 'NNNN' 'UCGGGGUGCCCUUCUGCGUGAAGGCUGAGAAAUACCCGUAUCACCUGAUCUGGAUAAUGCCAGCGUAGGGAA' 'NNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('tmr/qh/3').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGGCUAGUCCGU' 'NNNNN' 'NNN'  'CCGACUGGCGAGAGCCAGGUAACGAAUG'  'NNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('tmr/qh/4').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGGCUAGUCCGU' 'NNNNN' 'NNNN' 'CCGACUGGCGAGAGCCAGGUAACGAAUG' 'NNNN' 'GGCACCGAGUCGGUGC' 'UUUUUU'

def test_sequester_uracil_59():
    assert from_name('uh/4/6').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNU' 'CC' 'NNNNNN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('uh/5/6').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNNU' 'CC' 'NNNNNN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('uh/6/6').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNNNU' 'CC' 'NNNNNN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('uh/4/7').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNU' 'CC' 'NNNNNNN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('uh/5/7').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNNU' 'CC' 'NNNNNNN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'
    assert from_name('uh/6/7').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGG' 'NNNNNNU' 'CC' 'NNNNNNN' 'GCCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGAC' 'GGCACCGAGUCGGUGC' 'UUUUUU'

def test_sequester_uracil_59_forward():
    assert from_name('tpp/uhf/8').dna == 'GTTTCAGAGCTATGCTGTAAACAGCATAGCAAGTTGAAATAAGGCGCAGTCCGTCCCTGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/30').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGCCTGTCCGTGATCAGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/37').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGGCAGGTCCGTTCCCAGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/49').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGCTAGGTCCGTTCCCGGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/66').dna == 'GTTTCAGAGCTTTGCTGGAAACAGCATAGCAAGTTGAAATAAGGCAGAGGTCCGTTCCTGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/71').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGTTCACTCCGTTCCCAGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/84').dna == 'GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGGCGAGTCCGTTCCCAGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/132').dna == 'GTTTCAGAGCTATGCTTGAAACAGCATAGCAAGTTGAAATAAGGCGCCAGTCCGTTCCTGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/135').dna == 'GTTTCAGAGCTTGCTGGAAACAGCATAGCAAGTTGAAATAAGGTTTGATCCGTTCAGGGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/160').dna == 'GTTTCAGAGCTATGCTGTAAACAGCATAGCAAGTTGAAATAAGGCCCTGTCCGCGATCAGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'
    assert from_name('tpp/uhf/174').dna == 'GTTTCAGAGCTATGCTTGAAACAGCATAGCAAGTTGAAATAAGGCTTGTCCGCGCTGGCCGTCGGGGTGCCCTTCTGCGTGAAGGCTGAGAAATACCCGTATCACCTGATCTGGATAATGCCAGCGTAGGGAACGACGGCACCGAGTCGGTGCTTTTTT'

def test_modulate_rxb_11_1():
    # Test the different bases and reverse complements.
    assert from_name('m11/ac').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGac' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'guUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/AC').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGAC' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GUUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/gu').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGgu' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'acUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/GU').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGGU' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'ACUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/hv').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGgu' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'guUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/HV').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGGU' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GUUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

    # Test different stem lengths
    assert from_name('m11').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'UACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/a').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGa' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'uUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/aa').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGaa' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'uuUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/aaa').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGaaa' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'uuuUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('m11/aaaa').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AAGUGaaaa' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'uuuuUACGU' 'UAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
def test_strand_swap_rxb_11_1():
    assert from_name('w11/1').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'CUGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCUAG' 'GUUAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('w11/2').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GAGGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCUUC' 'GUUAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('w11/3').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GUUGG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CCGAC' 'GUUAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('w11/4').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GUGCG' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'CGUAC' 'GUUAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('w11/5').rna == 'GUUUCA' 'GA' 'GCUAUGCUGGAAACAGCAUAGC' 'AAGU' 'UGAAAU' 'AA' 'GUGGC' 'AUACCAGCCGAAAGGCCCUUGGCAG' 'GCUAC' 'GUUAUCA' 'ACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
