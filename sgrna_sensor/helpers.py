#!/usr/bin/env python3

def molecular_weight(name, polymer='rna'):
    from . import from_name
    return from_name(name).mass(polymer)

def reverse(sequence):
    return sequence[::-1]

def complement(sequence):
    complements = {
            'A': 'U',
            'C': 'G',
            'G': 'C',
            'U': 'A',
    }
    return ''.join(complements[x] for x in sequence)

def reverse_complement(sequence):
    return reverse(complement(sequence))

def find_middlemost(seq, pattern, num_matches=1):
    """
    Find all occurrences of the given pattern in the given sequence and return 
    the index of the middlemost one.  The pattern must include at least one 
    parenthetical group.  The start of the group will be the value used to 
    calculate the middlemost match.
    """
    import regex as re
    matches = [x for x in re.finditer(pattern, seq, overlapped=True)]

    if len(matches) < num_matches:
        raise ValueError("'{}' found fewer that {} time(s) in '{}'".format(
            pattern, num_matches, seq))

    # Find every index matched by the pattern.  If the pattern has multiple 
    # capturing groups, iterate to find the one that matches.

    indices = []
    for match in matches:
        i, group = -1, 0
        while i < 0:
            group += 1
            i = match.start(group)
        indices.append(i)

    # Sort the list of indices by how close they are to the middle of the given 
    # sequence.

    dist_to_middle = lambda i: abs(i - (len(seq)-1) / 2)
    indices.sort(key=dist_to_middle)
    return [(i, len(seq) - i - 1) for i in indices[:num_matches]]


