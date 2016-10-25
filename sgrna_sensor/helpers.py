#!/usr/bin/env python3

def reverse(sequence):
    return sequence[::-1]

def rna_complement(sequence):
    complements = {
            'A': 'U',
            'C': 'G',
            'G': 'C',
            'U': 'A',
    }
    return ''.join(complements[x] for x in sequence)

complement = rna_complement

def rna_reverse_complement(sequence):
    return reverse(rna_complement(sequence))

reverse_complement = rna_reverse_complement

def dna_complement(sequence):
    complements = {
            'A': 'T',
            'C': 'G',
            'G': 'C',
            'T': 'A',
    }
    return ''.join(complements[x] for x in sequence)

def dna_reverse_complement(sequence):
    return reverse(dna_complement(sequence))

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

def clamp(x, low, hi):
    return min(max(x, low), hi)

def library_size(sequence):
    library_size = 1
    num_possibilities = {
            'A': 1, 'G': 1, 'C': 1, 'T': 1, 'U': 1,
            'R': 2, 'Y': 2, 'M': 2, 'K': 2, 'S': 2, 'W': 2,
            'H': 3, 'B': 3, 'V': 3, 'D': 3,
            'N': 4,
    }

    for letter in sequence.upper():
        library_size *= num_possibilities[letter]

    return library_size

