#!/usr/bin/env python2

"""\
Usage:
    scorefxn.py [options] <names>...

Options:
    -x, --scorefxn SFXN      [default: mea_tree_metric]
        Specify which score function to use.
"""

import docopt, math
import RNA, sgrna_helper

def mfe_tree_metric(design, ligand_bound=False):
    ref = design.expected_fold
    mfe = design.constraints

    RNA.fold_par(design.seq, mfe, None, ligand_bound, False)

    ref_tree = RNA.make_tree(RNA.expand_Full(ref))
    mfe_tree = RNA.make_tree(RNA.expand_Full(mfe))

    return RNA.tree_edit_distance(ref_tree, mfe_tree)

def mfe_string_metric(design, ligand_bound=False):
    ref = design.expected_fold
    mfe = design.constraints

    print mfe
    RNA.fold_par(design.seq, mfe, None, ligand_bound, False)
    print ref
    print mfe

    ref_str = RNA.Make_swString(ref)
    mfe_str = RNA.Make_swString(mfe)

    return RNA.string_edit_distance(ref_str, mfe_str)

def mea_tree_metric(design, ligand_bound=False):
    ref = design.expected_fold
    mfe = design.constraints

    print mfe
    print RNA.pf_fold_par(design.seq, mfe, None, True, ligand_bound, False)
    print ref
    print mfe

    ref_tree = RNA.make_tree(RNA.expand_Full(ref))
    mfe_tree = RNA.make_tree(RNA.expand_Full(mfe))

    return RNA.tree_edit_distance(ref_tree, mfe_tree)

def mea_string_metric(design, ligand_bound=False):
    ref = design.expected_fold
    mfe = design.constraints

    RNA.pf_fold_par(design.seq, mfe, None, False, ligand_bound, False)

    ref_str = RNA.Make_swString(ref)
    mfe_str = RNA.Make_swString(mfe)

    return RNA.string_edit_distance(ref_str, mfe_str)

def active_population(design, ligand_bound=False):
    RNA.pf_fold(design.seq, None)
    bppm = RNA.export_bppm()
    print bppm
    print type(bppm)

    #s = ""
    #RNA.assign_plist_from_pr(s, bppm, len(design), 0)

    from ctypes import *
    c_double_list = POINTER(c_double)
    print c_double_list
    print int(bppm)
    print dir(bppm)
    c_bppm = c_double_list(int(bppm))

    #RNA.print_bppm(bppm)
    return 1


def calculate_fold(name):
    print name

    design = sgrna_helper.from_name(name, target=None)
    design.show()
    print design.expected_fold

    tot_e_off = RNA.pf_fold_par(design.seq, design.constraints, None, False, False, False)
    min_e_off = RNA.fold_par(design.seq, design.expected_fold, None, True, False)

    ex = ''
    for f, c in zip(design.expected_fold, design.constraints):
        ex += f if f is not '.' else c

    tot_e_on = RNA.pf_fold_par(design.seq, design.constraints, None, False, True, False)
    min_e_on = RNA.fold_par(design.seq, ex, None, True, False)

    print tot_e_off
    print min_e_off
    print tot_e_on
    print min_e_on

    kT = 0.593  # kcal/mol
    prob_off = math.exp((tot_e_off - min_e_off) / kT)
    prob_on = math.exp((tot_e_on - min_e_on) / kT)

    print
    print "Probability of active conformation in:"
    print "off ensemble:", prob_off
    print "on ensemble:", prob_on
    print
    print "Fold increase of active conformation:"
    print prob_on / prob_off
    print
    print 79 * '*'
    print


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    scorefxn = locals()[args['--scorefxn']]
    print args['--scorefxn']

    for name in args['<names>']:
        design = sgrna_helper.from_name(name, target=None)

        x_off = scorefxn(design, False)
        #x_on = scorefxn(design, True)
        #x_ratio = x_on / x_off

        #print '{name:10s} {x_ratio:.2f} ({x_on:.2f} / {x_off:.2f})'.format(**locals())
        print '{name:10s} {x_off:.2f}'.format(**locals())

    #print """\
    #This doesn't do what I want.  What I want is to get the base-pairing 
    #probability matrix (BPPM) and to calculate the probability of any structure 
    #that makes the wildtype base pairs.  This calculates the equilibrium population 
    #of the single lowest scoring structure that makes the wildtype base pairs.
    #"""
