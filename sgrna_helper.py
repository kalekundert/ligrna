#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections, contextlib, random
import nonstdlib, six

class Sequence (object):
    """
    Abstract base class that represents a sequence that's associated with a 
    name and provides some convenience functions to query that sequence.  How 
    the sequence is stored is actually left up to the subclasses, which have to 
    reimplement the 'seq' property to return the sequence in question.
    """

    def __init__(self, name):
        self.name = name
        self.doc = ""

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
        return hash(self.seq)

    def __len__(self):
        """
        Return the length of the sequence.
        """
        return len(self.seq)

    def __iter__(self):
        """
        Iterate through the nucleotides in this sequence.
        """
        for x in self.seq: yield x

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
        Sequence.__init__(self, name)
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
        if isinstance(key, six.string_types):
            domains = self.domains_from_name(key)
            if len(domains) == 1:
                return domains[0]
            else:
                raise KeyError("{} domains named '{}'.".format(len(domains), key))
        else:
            return Sequence.__getitem__(self, key)

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
        factory, arguments = parse_name(self.name)[0]
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
        return str(''.join(
                iter.domain.seq[iter.rel_start:iter.rel_end]
                for iter in self._iterate_domains()))

    @property
    def constraints(self):
        return str(''.join(
                iter.domain.constraints[iter.rel_start:iter.rel_end]
                for iter in self._iterate_domains()))

    @property
    def expected_fold(self):
        return str(''.join(
                iter.domain.expected_fold[iter.rel_start:iter.rel_end]
                for iter in self._iterate_domains()))

    def domains_from_name(self, *names):
        """
        Return a list of all the domains in this construct (or any of its 
        attached constructs) with the given name.  
        """
        domains = [x for x in self._domains if x.name in names]
        for attachment in self._attachments.values():
            domains += attachment.construct.domains_from_name(*names)
        return domains

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

    def index_from_domain(self, domain, rel_index):
        """
        Return the absolute index of the given index of the given domain.  If 
        more than one domain has the same name, only returned value will be for 
        the first.
        """
        for iter in self._iterate_domains():
            if iter.domain.name == domain:
                return iter.abs_index(rel_index)

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
        if isinstance(start_domain, six.string_types):
            start_domain = self[start_domain]
        if start_domain not in self._domains:
            raise ValueError("no '{}' domain in '{}'.".format(start_domain, self.name))

        if isinstance(end_domain, six.string_types):
            end_domain = self[end_domain]
        if end_domain not in self._domains:
            raise ValueError("no '{}' domain in '{}'.".format(end_domain, self.name))

        if start_index == '...':
            start_index = 0
        if start_index not in start_domain.attachment_sites:
            raise ValueError("Position {} of domain {} is not an attachment site.".format(start_index, start_domain.name))

        if end_index == '...':
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

            def abs_index(self, rel_index):
                return self.start + rel_index - self.rel_start

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
        if isinstance(domain, six.string_types):
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

    def __init__(self, name, sequence, style=None, mutable=True):
        Sequence.__init__(self, name)
        self._sequence = sequence
        self._attachment_sites = []
        self._constraints = None
        self._expected_fold = None
        self.construct = None
        self.style = style
        self.mutable = mutable

    def __hash__(self):
        from six.moves.builtins import id
        return hash(id(self))

    def __eq__(self, other):
        return self.seq == other

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
        if self._constraints is not None:
            self.constraints = self.constraints[:start] + '.' * len(sequence) + self.constraints[stop:]
        if self._expected_fold is not None:
            self.expected_fold = self.expected_fold[:start] + '.' * len(sequence) + self.expected_fold[stop:]

    def __delitem__(self, index):
        self[index] = ''

    @property
    def seq(self):
        return str(self._sequence)

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
    def expected_fold(self):
        return self._expected_fold or '.' * len(self)

    @expected_fold.setter
    def expected_fold(self, expected_fold):
        if expected_fold and len(expected_fold) != len(self):
            raise ValueError("expected_fold doesn't match sequence")
        self._expected_fold = expected_fold

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
        if isinstance(style, six.string_types):
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

    def append(self, sequence):
        N = len(self)
        self[N:N] = sequence

    def prepend(self, sequence):
        self[0:0] = sequence

    def replace(self, start, end, insert):
        self[start:end] = insert

    def delete(self, start, end):
        self[start:end] = ''



def from_name(name, **kwargs):
    import re, inspect

    name = name.strip()
    if not name:
        raise ValueError("Can't parse empty name.")

    tokens = re.findall('[a-zA-Z0-9]+', name)

    # If the first token is a name recognized by the aptamer() function, then 
    # it specifies the aptamer to use.  Otherwise the theophylline aptamer is 
    # assumed.

    try:
        aptamer(tokens[0])
    except ValueError:
        ligand = 'theo'
    else:
        ligand = tokens.pop(0)

    if 'ligand' not in kwargs:
        kwargs['ligand'] = ligand

    # The first token after the (optional) aptamer specifies the factory 
    # function to use and must exist in the global namespace. 

    try:
        factory = globals()[tokens[0]]
    except KeyError:
        raise ValueError("No designs named '{}'.".format(tokens[0]))

    # All further tokens are arguments.  Arguments that look like integers need 
    # to be casted to integers.

    def cast_if_necessary(x):  # (no fold)
        try: return int(x)
        except: return x

    args = [cast_if_necessary(x) for x in tokens[1:]]

    # Use keyword arguments passed into this function if the factory knows how 
    # to handle them.  Silently ignore the arguments otherwise.

    argspec = inspect.getargspec(factory)
    known_kwargs = {k:v for k,v in kwargs.items() if k in argspec.args}

    return factory(*args, **known_kwargs)

def make_name(factory, *args):
    return factory + '(' + ','.join(str(x) for x in args if str(x)) + ')'

def molecular_weight(name, polymer='rna'):
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
        sequence = 'GGAACTTTCAGTTTAGCGGTCT'
    elif name == 'aavs':
        sequence = 'GGGGCCACTAGGGACAGGAT'
    elif name == 'vegfa':
        sequence = 'GGGTGGGGGGAGTTTGCTCC'
    elif name in ('k1', 'klein1'):
        sequence = 'GGGCACGGGCAGCTTGCCCG'
    elif name == ('k2', 'klein2'):
        sequence = 'GTCGCCCTCGAACTTCACCT'
    else:
        raise ValueError("Unknown spacer: '{}'".format(name))

    spacer = Domain('spacer', sequence)
    spacer.style = 'white'

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
        constraint_pieces = '.(.((((((', '....', ')))...))).).'

    elif ligand in ('3mx', '3-methylxanthine'):
        # Soukup, Emilsson, Breaker. Altering molecular recognition of RNA 
        # aptamers by allosteric selection. J. Mol. Biol. (2000) 298, 623-632.
        sequence_pieces   = 'AUACCAGCC', 'GAAA', 'GGCCAUUGGCAG'
        constraint_pieces = '.(.((((((', '....', ')))...))).).'

    elif ligand in ('tet', 'tetracycline'):
        # Weigand, Suess. Tetracycline aptamer-controlled regulation of pre- 
        # mRNA splicing in yeast. Nucl. Acids Res. (2007) 35 (12): 4179-4185.
        name = 'tet aptamer'
        sequence_pieces   = 'GGCCUAAAACAUACCAGAU', 'GAAA', 'GUCUGGAGAGGUGAAGAAUACGACCACCUAGGCC'
        constraint_pieces = '(((((........((((((', '....', '))))))..(((((...........))))))))))'

    else:
        raise ValueError("no aptamer for '{}'".format(ligand))

    # Define the domains that make up the aptamer.

    aptamer_5 = Domain("aptamer/5'", sequence_pieces[0])
    aptamer_S = Domain("splitter", sequence_pieces[1])
    aptamer_3 = Domain("aptamer/3'", sequence_pieces[2])

    aptamer_5.constraints = constraint_pieces[0]
    aptamer_S.constraints = constraint_pieces[1]
    aptamer_3.constraints = constraint_pieces[2]

    aptamer_5.style = 'yellow', 'bold'
    aptamer_S.style = 'yellow', 'bold'
    aptamer_3.style = 'yellow', 'bold'

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

def complementary_switch(target_seq):
    switch_domain = Domain('switch', reverse_complement(target_seq))
    on_domain = Domain('on', target_seq)
    off_domain = Domain('off', target_seq)
    return switch_domain, on_domain, off_domain

def wobble_switch(target_seq, favor_cutting, num_mutations=1):
    # Find all the positions where a wobble base pair could be made, i.e. all 
    # the positions in the "off" sequence that are either G or U.

    if favor_cutting:
        switch_domain = Domain('switch', reverse_complement(target_seq))
        for i, I in find_middlemost(target_seq, '([GU])', num_mutations):
            mutation = {'G':'U','U':'G'}[target_seq[i]] 
            switch_domain.mutate(I, mutation)
        on_domain = Domain('on', reverse_complement(switch_domain.seq))

    else:
        on_domain = Domain('on', target_seq)
        for i, I in find_middlemost(target_seq, '([AC])', num_mutations):
            mutation = {'C':'U','A':'G'}[target_seq[i]] 
            on_domain.mutate(i, mutation)
        switch_domain = Domain('switch', reverse_complement(target_seq))

    return switch_domain, on_domain, Domain('off', target_seq)

def mismatch_switch(target_seq, favor_cutting):
    middlemost = find_middlemost(target_seq, '[AU](.)[GC]|[GC](.)[AU]')
    mutations = {'A':'C','C':'C','G':'A','U':'C'}

    if favor_cutting:
        switch_domain = Domain('switch', reverse_complement(target_seq))
        for i, I in middlemost:
            switch_domain.mutate(I, mutations[target_seq[i]])
        on_domain = Domain('on', reverse_complement(switch_domain.seq))

    else:
        on_domain = Domain('on', target_seq)
        for i, I in middlemost:
            on_domain.mutate(i, mutations[complement(target_seq[i])])
        switch_domain = Domain('switch', reverse_complement(target_seq))

    return switch_domain, on_domain, Domain('off', target_seq)

def bulge_switch(target_seq, favor_cutting, bulge_seq='A'):
    i = len(target_seq) // 2
    
    if favor_cutting:
        switch_domain = Domain('switch', reverse_complement(target_seq))
        switch_domain.insert(i, bulge_seq)
        on_domain = Domain('on', reverse_complement(switch_domain.seq))

    else:
        on_domain = Domain('on', target_seq)
        on_domain.insert(i, bulge_seq)
        switch_domain = Domain('switch', reverse_complement(target_seq))

    return switch_domain, on_domain, Domain('off', target_seq)

def tunable_switch(target_seq, tuning_strategy=''):
    """
    Return three domains that comprise a switch.  The first domain ("switch") 
    is a sequence that can base pair with either of the two following domains, 
    the second domain ("on") is what the first should bind in the "on" state, 
    and the third domain ("off") is what the first should bind in the "off" 
    state.  
    
    By default, "switch" is perfectly complementary with both "on" and "off", 
    so it doesn't have a preference for one over the other.  You can tune the 
    switch by weakening the interactions it makes with one of its partners so 
    that it will prefer the other.  The tuning_strategy parameter specifies how 
    this should be done.  Each strategy is a 2-3 letter string.  The first 
    letter specifies what kind of mutation to make:

        w: Insert a wobble (GU) base pair.
        m: Insert a one nucleotide mismatch (1x1).
        b: Insert a one nucleotide bulge (1x0).

    Wobble base pairs are weaker perturbations and are only expected to shift 
    the equilibrium by a factor of 10.  Mismatches and bulges are stronger and 
    are both expected to shift the equilibrium by a factor of 100.

    The second letter specifies which state to weaken:
    
        x: More cutting, weaken the off state.
        o: Less cutting, weaken the on state.
    
    The meaning of the third letter depends on the chosen strategy (i.e. the 
    first letter):

        w: [0-9]+: Make the specified number of wobble mutations.
        b: g: Make the bulge a G instead on an A.  This should lead to a 
           slightly stronger activating effect.
    """

    if not tuning_strategy:
        return complementary_switch(target_seq)

    if tuning_strategy[0] not in 'wmb':
        raise ValueError("Tuning strategy must be one of 'wmb', not '{}'.".format(tuning_strategy[0]))
    if tuning_strategy[1] not in 'xo':
        raise ValueError("Desired tuning effect must be one of 'xo', not '{}'".format(tuning_strategy[1]))

    favor_cutting = True if tuning_strategy[1] == 'x' else False

    if tuning_strategy[0] == 'w':
        num_mutations = int(tuning_strategy[2:] or 1)
        return wobble_switch(target_seq, favor_cutting, num_mutations)
    if tuning_strategy[0] == 'm':
        return mismatch_switch(target_seq, favor_cutting)
    if tuning_strategy[0] == 'b':
        bulge_seq = 'G' if tuning_strategy == 'bxg' else 'A'
        return bulge_switch(target_seq, favor_cutting, bulge_seq)

def serpentine_insert(ligand, target_seq, target_end, tuning_strategy='',
        turn_seq='GAAA', num_aptamers=1):

    if not target_seq:
        raise ValueError('target_seq cannot be empty')

    switch_domain, on_domain, off_domain = tunable_switch(
            target_seq, tuning_strategy)

    domains = [
            Domain('turn', turn_seq),
            switch_domain,
            aptamer_insert(ligand, num_aptamers=num_aptamers),
            on_domain,
    ]

    if target_end == '3':
        domains.reverse()
        i, j = 0, 2
    else:
        i, j = 1, 3

    domains[i].expected_fold = '(' * len(domains[i])
    domains[j].expected_fold = ')' * len(domains[j])

    return Construct('serpentine', domains)

def circle_insert(ligand, target_seq, target_end, tuning_strategy='',
        num_aptamers=1):

    if not target_seq:
        raise ValueError('target_seq cannot be empty')

    switch_domain, on_domain, off_domain = tunable_switch(
            target_seq, tuning_strategy)

    domains = [
            on_domain,
            aptamer_insert(ligand, num_aptamers=num_aptamers),
            switch_domain,
    ]

    if target_end == '3':
        domains.reverse()

    domains[0].expected_fold = '(' * len(domains[0])
    domains[2].expected_fold = ')' * len(domains[2])
    
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

    sgrna['stem'].expected_fold = '((((((..((((....))))....))))))'
    sgrna['hairpins'].expected_fold = '.....((((....)))).((((((...))))))'

    sgrna['stem'].style = 'green'
    sgrna['nexus'].style = 'red'
    sgrna['hairpins'].style = 'blue'

    sgrna['stem'].attachment_sites = 'anywhere'
    sgrna['nexus'].attachment_sites = 'anywhere'
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

def fold_upper_stem(N, linker_len=0, splitter_len=0, num_aptamers=1, ligand='theo', target='aavs'):
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
    if ligand != 'theo':
        args = args + ('a='+ligand,)

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('us', *args)
    sgrna.attach(
            aptamer_insert(
                ligand,
                linker_len=linker_len,
                splitter_len=splitter_len,
                num_aptamers=num_aptamers,
            ),
            'stem', 8 + N,
            'stem', 20 - N,
    )
    return sgrna

def fold_lower_stem(N, linker_len=0, splitter_len=0, ligand='theo', target='aavs'):
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
    """

    if not 0 <= N <= 6:
        raise ValueError("Location for lower stem insertion must be between 0 and 6, not {}.".format(N))

    if splitter_len != 0:
        args = N, linker_len, splitter_len
    else:
        args = N, linker_len
    if target != 'aavs':
        args = args + ('s='+target,)
    if ligand != 'theo':
        args = args + ('a='+ligand,)

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('ls', *args)
    sgrna.attach(
            aptamer_insert(
                ligand,
                linker_len=linker_len,
                splitter_len=splitter_len,
            ),
            'stem', 0 + N,
            'stem', 30 - N,
    )
    return sgrna

def fold_nexus(linker_len=0, ligand='theo', target='aavs'):
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
    """

    args = (linker_len,)
    if target != 'aavs':
        args = args + ('s='+target,)
    if ligand != 'theo':
        args = args + ('a='+ligand,)

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('nx', linker_len)
    sgrna.attach(
            aptamer_insert(
                ligand,
                linker_len=linker_len,
                repeat_factory=lambda name, length: repeat(name, length, 'U'),
            ),
            'nexus', 4,
            'nexus', 9,
    )
    return sgrna
    
def fold_nexus_2(N, M, splitter_len=0, num_aptamers=1, ligand='theo', target='aavs'):
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
    if ligand != 'theo':
        args = args + ('a='+ligand,)

    # Create and return the construct using a helper function.

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('nxx', *args)
    sgrna.attach(
            aptamer_insert(
                ligand,
                splitter_len=splitter_len,
                num_aptamers=num_aptamers,
            ),
            'nexus', 2 + N,
            'nexus', 11 - M,
    )
    return sgrna

def fold_hairpin(H, N, A=1, ligand='theo', target='aavs'):
    """
    Replace either of the hairpins with the aptamer.  Briner et al. showed that 
    the sgRNA is at least somewhat sensitive to the distance between the nexus 
    and the hairpins, so unfolding the first hairpin may be a successful way to 
    create a sensor.  They also showed that the sgRNA is very sensitive to the 
    removal of both hairpins, but not so much to the removal of just the first.  
    They didn't try removing just the second, but it's not unreasonable to 
    think that that might be a viable way to control the sgRNA.  

    Briner et al. also didn't try changing the sequence of either hairpins, so 
    I'm just assuming that they can be freely changed as long as the base 
    pairing is maintained.  In the crystal structure, the first hairpin is not 
    interacting with Cas9 at all and the second hairpin is unresolved, so I 
    think this assumption is reasonable.  It's also worth noting that the first 
    hairpin is solvent exposed, so it should be able to sterically accommodate 
    the aptamer.

    Parameters
    ----------
    H: int
        Which hairpin to replace.  Must be either 1 or 2.  Replacing the second 
        hairpin may not be a good idea, because it think it's part of the T7 
        terminator, but I can still test it in vitro.  Worst case is that it 
        won't work as expected in vivo.

    N: int
        Indicate how many of the wildtype base pairs should be preserved.  
        This parameters must be between 0 and the number of wildtype base 
        pairs, which is 4 for the first hairpin and 6 for the second.  The 
        aptamer will be inserted between the two ends of the stem.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    ligand: str
        Which aptamer to insert into the sgRNA.  Must be one of the strings 
        accepted by the aptamer() function.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    if H not in (1, 2):
        raise ValueError("fh(H,N): H must be either 1 or 2")

    max_N = (4 if H == 1 else 6)
    if not 0 <= N <= max_N:
        raise ValueError("fh(H,N): N must be between 0 and {}".format(max_N))

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('fh', H, N)
    sgrna.attach(
            aptamer_insert(ligand, num_aptamers=A),
            'hairpins',  5 + N if H == 1 else 18 + N,
            'hairpins', 17 - N if H == 1 else 33 - N,
    )
    return sgrna

def replace_hairpins(N, ligand='theo', target='aavs'):
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
    if ligand != 'theo':
        args = args + ('a='+ligand,)

    design = wt_sgrna(target)
    design.name = make_name('hp', *args)

    domain_len = len(design['hairpins'])
    insertion_site = min(N, domain_len)
    linker_len = max(0, N - domain_len), 0

    design.attach(
            aptamer_insert(ligand, linker_len=linker_len),
            'hairpins', insertion_site,
            'hairpins', '...',
    )
    return design

def induce_dimerization(half, N, target='aavs', ligand='theo'):
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
    """

    # Make sure the arguments make sense.

    half = str(half)
    N = int(N)

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    args = half, N
    if target != 'aavs':
        args = args + ('s='+target,)
    if ligand != 'theo':
        args = args + ('a='+ligand,)

    # Construct and return the requested sequence.

    design = Construct()
    design.name = make_name('id', *args)
    wt = wt_sgrna(target)

    if half == '5':
        design += wt['spacer']
        design += wt['stem']
        design.attach(
                aptamer(ligand, '5'),
                'stem', 8 + N, 'stem', '...',
        )
    elif half == '3':
        design += wt
        design.attach(
                aptamer(ligand, '3'),
                'stem', '...', 'stem', 20 - N,
        )
    else:
        raise ValueError("Half for induced dimerization must be either 5 (for the 5' half) or 3 (for the 3' half), not '{}'.".format(half))

    return design

def serpentine_bulge(N, tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Sequester the bulge in a non-productive hairpin when the ligand isn't 
    present.  The bulge is an interesting target because it doesn't have to be 
    there, but if it is there it must be unpaired and it must have its wildtype 
    sequence.  This design uses the two adenosines that are naturally in the 
    bulge to construct a tetraloop that caps the non-productive hairpin.  Below 
    is an ASCII-art schematic of the design, along with an example sequence:

       ┌──────────┐┌───────────┐┌────┐┌────────────┐┌─────┐┌──────────┐ 
    5'─┤lower stem├┤  bulge''  ├┤theo├┤   bulge'   ├┤bulge├┤lower stem├─3'
       └──────────┘└───────────┘└────┘└────────────┘└─────┘└──────────┘ 
        GUUUUAga    UCGU(UAAAAU) ...  (GUUUUA)AC-GA  AA-GU  UAAAAU
                                                 └────┘
                                                tetraloop

    The length of the non-productive hairpin can be extended by including bases 
    from the lower stem, as shown in parentheses.  Mutations can be made in the 
    bulge', bulge'', and lower stem regions to tune the balance between the 
    "on" and "off" states.  The bulge itself is never changed.

    Parameters
    ----------
    N: int
        Indicate how long the non-productive hairpin should be.  It can't be 
        shorter than 2 base pairs.  The first two bases in the hairpin come 
        from the bulge, and subsequent bases come from the lower stem.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    if N < 2:
        raise ValueError("sb(N): N must be 2 or greater")

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('sb', N, tuning_strategy)
    sgrna.attach(
            serpentine_insert(
                ligand,
                wt_sgrna()['stem'][22:22+N], '3',
                tuning_strategy, num_aptamers=A,
            ),
            'stem', 8,
            'stem', 22,
    )
    sgrna['on'].prepend('UC')

    return sgrna

def serpentine_lower_stem(tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Sequester the nexus in base pairs with the lower stem in the absence of the 
    ligand.  This design is based off two ideas:
    
    1. That disrupting the nexus will be an effective way to deactivate the 
       sgRNA, because the nexus seems to be very sensitive to mutation.

    2. That the lower stem can be modified to have some complementarity with 
       the nexus, because the exact sequence of the lower stem seems to be 
       important, so long as it does actually form a stem.
    
    This design is named "serpentine_lower_stem" because it uses applies the 
    "serpentine" strategy to the lower stem region of the sgRNA.  A schematic 
    of this strategy is shown below.  The "serpentine" pattern is formed 
    because nexus' can base pair either with nexus or nexus''.  Note that the 
    length of the serpentine pattern is fixed at four base pairs, because the 
    length of the lower stem must be six base pairs (and two base pairs are 
    required to form the tetraloop).

       ┌───────┐┌──┐┌────┐┌────┐┌──────┐┌───────┐ 
    5'─┤nexus''├┤GA├┤theo├┤AAGU├┤nexus'├┤ nexus ├─3'
       └───────┘└──┘└────┘└────┘└──────┘└───────┘ 
        UC-GGCU  GA  ...   AAGU  AGCC-GA AA-GGCU
                                      └───┘
                                    tetraloop
    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = make_name('sl', tuning_strategy)
    sgrna.attach(
            serpentine_insert(
                ligand,
                'GGCU', '3',
                tuning_strategy,
                num_aptamers=A,
            ),
            'stem', 0,
            'nexus', 2,
    )
    sgrna['on'].prepend('UC')
    sgrna['on'].append('GA')
    sgrna['switch'].prepend('AAGU')
    return sgrna

def serpentine_lower_stem_around_nexus(tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Use the lower stem to extend the nexus stem in the absence of the aptamer 
    ligand.  This design is based of the idea that the sgRNA is very sensitive 
    to the length of the nexus stem and that the bases in the lower stem can be 
    freely mutated to complement the region just beyond the nexus stem.  The 
    extended stem will have a bulge because there is a short AA linker between 
    the lower stem and the nexus, and the length of the complementary region 
    will be fixed at 6 base pairs because the lower stem cannot be lengthened 
    or shortened.  A schematic of this design is shown below:

       ┌──────┐┌──┐┌────┐┌────┐┌──────┐┌──┐┌─────────┐┌──────┐ 
    5'─┤  on  ├┤GA├┤theo├┤AAGU├┤switch├┤AA├┤  nexus  ├┤ off  ├─3'
       └──────┘└──┘└────┘└────┘└──────┘└──┘└─────────┘└──────┘ 
        GUUAUC  GA  ...   AAGU  GAUAAC  AA  GGCUAGUCC  GUUAUC
    
    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = make_name('slx', tuning_strategy)
    sgrna.attach(
            serpentine_insert(
                ligand,
                'GUUAUC', '3',
                tuning_strategy,
                turn_seq='',
                num_aptamers=A,
            ),
            'stem', '...',
            'stem', '...',
    )
    sgrna['on'].append('GA')
    sgrna['switch'].prepend('AAGU')
    return sgrna

def serpentine_hairpin(N, tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Sequester the 3' end of the nexus in base pairs with the 5' strand of the 
    first hairpin in the absence of aptamer ligand.  This design is based on 
    the fact that proper nexus folding is required for sgRNA function and the 
    assumption that the sequence of the first hairpin can be changed if its 
    base pairing is maintained.  Briner et al. didn't actually test any point
    mutations in the first hairpin, but they did find that the whole hairpin 
    can be deleted so long as a two residue spacer is added to maintain the 
    positioning of the second hairpin.

       ┌────────────┐┌────┐┌──────┐┌────┐┌───────┐ 
    5'─┤   nexus    ├┤turn├┤nexus'├┤theo├┤nexus''├─3'
       └────────────┘└────┘└──────┘└────┘└───────┘ 
        GGCUAGUCCGUU  AUCA  AACG... ...   ...CGUU
    
    Parameters
    ----------
    N: int
        The length of the complementary region to insert, and also the length 
        of the first hairpin.  The hairpin is naturally 4 base pairs long, but 
        it's solvent exposed so in theory you can make it as long as you want.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    if not 4 <= N <= 14:
        raise ValueError("sh(N): N must be between 4 and 14")

    sgrna = wt_sgrna(target)
    sgrna.name = make_name('sh', N, tuning_strategy)
    sgrna.attach(
            serpentine_insert(
                ligand,
                wt_sgrna().seq[44-N:44], '5',
                tuning_strategy,
                turn_seq='AUCA', # ANYA
                num_aptamers=A,
            ),
            'hairpins', 1,
            'hairpins', 17,
    )
    return sgrna

def circle_bulge(tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Extend the lower stem hairpin through the bulge when the small molecule is 
    absent.  This design is based off the fact that "straightening" the bulge 
    (i.e. mutating both side so they can base pair) completely eliminates Cas9 
    activity.  Note that this design unconditionally removes the 5' part of the 
    bulge, which has the sequence 'GA'.  In wildtype sgRNA, this mutation does
    not have a significant effect.  

    This design is named "circle_bulge" because it uses the "circle" strategy 
    to sequester the bulge region of the sgRNA.  A schematic of this strategy 
    is shown below.  The circle is formed when bulge' binds to either bulge'' 
    or bulge.  The sgRNA is only active when bulge is unpaired, and ligand 
    binding by the aptamer should encourage this conformation.

       ┌──────────┐┌──────┐┌────┐┌───────┐┌─────┐┌──────────┐ 
    5'─┤lower stem├┤bulge'├┤theo├┤bulge''├┤bulge├┤lower stem├─3'
       └──────────┘└──────┘└────┘└───────┘└─────┘└──────────┘ 
        GUUUUA      ACUU    ...   AAGU     AAGU   UAAAAU

    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = make_name('cb', tuning_strategy)
    sgrna.attach(
            circle_insert(
                ligand, 'AAGU', '3',
                tuning_strategy, num_aptamers=A,
            ),
            'stem', 6,
            'stem', 20,
    )
    return sgrna

def circle_bulge_combo(tuning_strategy, combo_strategy, combo_arg=None, A=1, ligand='theo', target='aavs'):
    """
    Combine the circle bulge design with orthogonal designs.  The idea is to 
    increase fold activation, possibly at the expense of affinity, by requiring 
    two switches to turn on.  Only a select set of orthogonal designs, known to 
    be functional on their own, can be combined with 'cb'.  This set includes 
    most of the 'slx' and 'sh' families of designs.

    Parameters
    ----------
    tuning_strategy: str
        A string specifying which mutation(s) to make in the 'cb' switch.

    combo_strategy: str
        A string specifying which design to integrate into 'cb'. Either 'slx' 
        or 'sh'.
        
    combo_arg:
        Arguments to the orthogonal design.  What's expected depends on the 
        value of 'combo_strategy'.
    """
    sgrna = circle_bulge(tuning_strategy)
    sgrna.name = make_name('cb', tuning_strategy, combo_strategy, combo_arg)

    # Serpentine the lower stem around the nexus.  This code isn't done by 
    # making an attachment, like all the other designs are, because its 
    # attachment would overlap with circle bulge.  Instead, the on and switch 
    # domains are directly mutated into the existing stem domain.

    if combo_strategy == 'slx':
        L = len(sgrna['stem'])
        switch_domain, on_domain, off_domain = tunable_switch(
                'GUUAUC', combo_arg or 'wo')
        sgrna['stem'].replace(0, 6, on_domain.seq)
        sgrna['stem'].replace(L-6, L, switch_domain.seq)

    # Serpentine the first hairpin.  This code is copied verbatim from the sh() 
    # function.

    elif combo_strategy == 'sh':
        if combo_arg is None:
            raise ValueError("The 'sh' combo strategy requires an argument.")
        sgrna.attach(
                serpentine_insert(
                    ligand,
                    wt_sgrna().seq[44-combo_arg:44], '5',
                    '',
                    turn_seq='AUCA', # ANYA
                    num_aptamers=A,
                ),
                'hairpins', 1,
                'hairpins', 17,
        )
    else:
        raise ValueError("unsupported strategy: '{}'".format(strategy))

    return sgrna

def circle_lower_stem(tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Sequester the 5' half of the nexus in base pairs with the 5' half of the 
    lower stem in the absence of aptamer ligand.  This strategy is based on  
    the fact that the nexus must be natively folded for the sgRNA to function 
    and that the specific sequence in the lower stem doesn't matter as long as 
    it's well base paired.

    This is an application of the "circle" strategy, which is known as "strand 
    displacement" in the literature.  The 5' half of the lower stem (nexus') 
    can either base pair with the 3' half of the lower stem (nexus'') or the 5' 
    half of the nexus.  The former is the active state and the latter is the 
    inactive state.  When the aptamer binds its ligand, that should encourage 
    the formation of the active state.  A schematic of the design strategy is 
    shown below:

       ┌──────┐┌──┐┌────┐┌────┐┌───────┐┌─────┐ 
    5'─┤nexus'├┤AG├┤theo├┤AAGU├┤nexus''├┤nexus├─3'
       └──────┘└──┘└────┘└────┘└───────┘└─────┘ 
        AGCCUU  AG  ...   AAGU  AAGGCU   AAGGCU 

    Note that the length of the nexus' and nexus'' sequences must be six, 
    because the length of the lower stem cannot change.  Currently, the 
    sequence is also fixed to match the start of the nexus (AAGGCU), but this 
    doesn't have to be the case.  Sliding this sequence in the 3' direction 
    could also yield viable designs.

    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = make_name('cl', tuning_strategy)
    sgrna.attach(
            circle_insert(
                ligand, 'AAGGCU', '3',
                tuning_strategy, num_aptamers=A,
            ),
            'stem', 0,
            'stem', '...',
    )
    sgrna['switch'].append('GA')
    sgrna['on'].prepend('AAGU')
    return sgrna

def circle_hairpin(N, tuning_strategy='', A=1, ligand='theo', target='aavs'):
    """
    Move the nexus closer to the hairpins in the absence of the aptamer's 
    ligand.  This design is supported by the fact that inserting one residue 
    into the region between the nexus and the hairpins substantially reduces 
    sgRNA function.  Briner et al. didn't try to remove residues from this 
    region, but it seems reasonable to expect that doing so would also be 
    quite deleterious.
    
    This is an application of the "circle" strategy, which is known as "strand 
    displacement" in the literature.  The 5' half of the first hairpin (ruler') 
    can either base pair with the 3' half of the same hairpin (ruler'') or the 
    region between the nexus and the hairpin (ruler).  The former is the 
    active state and the latter is the inactive state.  When the aptamer binds 
    its ligand, that should encourage the formation of the active state.  A 
    schematic of the design strategy is shown below:

       ┌──────┐┌───────┐┌────┐┌──────┐ 
    5'─┤ruler ├┤ruler''├┤theo├┤ruler'├─3'
       └──────┘└───────┘└────┘└──────┘ 
        ..AUCA  ..AUCA   ...   UGAU..  

    Parameters
    ----------
    N: int
        The length of the complementary region to insert, and also the length 
        of the first hairpin.  The hairpin is naturally 4 base pairs long, but 
        it's solvent exposed so in theory you can make it as long as you want.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = make_name('ch', N, tuning_strategy)
    sgrna.attach(
            circle_insert(
                ligand,
                wt_sgrna().seq[48-N:48], '5',
                tuning_strategy,
                num_aptamers=A),
            'hairpins', 5,
            'hairpins', 17,
    )
    return sgrna


## Abbreviations
wt = wt_sgrna
dead = dead_sgrna
fu = us = fold_upper_stem
fl = ls = fold_lower_stem
fx = nx = fold_nexus
fxx = nxx = fold_nexus_2
fh = fold_hairpin
hp = replace_hairpins
id = induce_dimerization
sb = serpentine_bulge
sl = serpentine_lower_stem
slx = serpentine_lower_stem_around_nexus
sh = serpentine_hairpin
cb = circle_bulge
cbc = circle_bulge_combo
cl = circle_lower_stem
ch = circle_hairpin

t7 = t7_promoter
th = theo = lambda: aptamer('theo')
aavs = lambda: dna_to_cut('aavs')

## sgRNA Fragments
# Provided to make it easier to assemble test cases.
#
# AUACCAGCCGAAAGGCCCUUGGCAG
#
# GGGGCCACTAGGGACAGGAT
# GUUUUA
# GA
# GCUAGAAAUAGC
# AAGU
# UAAAAU
# AA
# GGCUAGUCC
# GUUAUCA
# ACUUGAAAAAGU
# GGCACCGAGUCGGUGCUUUUUU'


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

    assert from_name('cb') == cb()
    assert from_name('cb/wo') == cb('wo')
    assert from_name('theo/cb') == cb()
    assert from_name('tet/cb') == cb(ligand='tet')

def test_complements():
    assert complement('ACUG') == 'UGAC'
    assert reverse_complement('ACUG') == 'CAGU'

def test_find_middlemost():
    import pytest

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

def test_t7_promoter():
    import pytest

    with pytest.raises(ValueError): t7_promoter('not a promoter')

    assert t7_promoter() == 'TATAGTAATAATACGACTCACTATAG'
    assert t7_promoter('igem') == 'TAATACGACTCACTATA'

def test_aptamer():
    import pytest

    with pytest.raises(ValueError): aptamer('unknown ligand')
    with pytest.raises(ValueError): aptamer('theo', 'unknown piece')

    assert aptamer('theo') == 'AUACCAGCCGAAAGGCCCUUGGCAG'

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

def test_complementary_switch():
    assert complementary_switch('AUGC') == ('GCAU', 'AUGC', 'AUGC')

def test_wobble_switch():
    assert wobble_switch('AAGCC', True) == ('GGUUU', 'AAACC', 'AAGCC')
    assert wobble_switch('AAUCC', True) == ('GGGUU', 'AACCC', 'AAUCC')
    assert wobble_switch('GGCUU', False) == ('AAGCC', 'GGUUU', 'GGCUU')
    assert wobble_switch('GGAUU', False) == ('AAUCC', 'GGGUU', 'GGAUU')
    assert wobble_switch('AAGGCC', True, 2) == ('GGUUUU', 'AAAACC', 'AAGGCC')
    assert wobble_switch('AAUUCC', True, 2) == ('GGGGUU', 'AACCCC', 'AAUUCC')
    assert wobble_switch('GGCCUU', False, 2) == ('AAGGCC', 'GGUUUU', 'GGCCUU')
    assert wobble_switch('GGAAUU', False, 2) == ('AAUUCC', 'GGGGUU', 'GGAAUU')

def test_mismatch_switch():
    # Test all the different nucleotides to mismatch with.
    assert mismatch_switch('GGAAA', True) == ('UUCCC', 'GGGAA', 'GGAAA')
    assert mismatch_switch('GGCAA', True) == ('UUCCC', 'GGGAA', 'GGCAA')
    assert mismatch_switch('GGGAA', True) == ('UUACC', 'GGUAA', 'GGGAA')
    assert mismatch_switch('GGUAA', True) == ('UUCCC', 'GGGAA', 'GGUAA')
    assert mismatch_switch('GGAAA', False) == ('UUUCC', 'GGCAA', 'GGAAA')
    assert mismatch_switch('GGCAA', False) == ('UUGCC', 'GGAAA', 'GGCAA')
    assert mismatch_switch('GGGAA', False) == ('UUCCC', 'GGCAA', 'GGGAA')
    assert mismatch_switch('GGUAA', False) == ('UUACC', 'GGCAA', 'GGUAA')

    # Test all the different AU/GC contexts.
    assert mismatch_switch('AACCC', True) == ('GGCUU', 'AAGCC', 'AACCC')
    assert mismatch_switch('AACGG', True) == ('CCCUU', 'AAGGG', 'AACGG')
    assert mismatch_switch('CCCAA', True) == ('UUCGG', 'CCGAA', 'CCCAA')
    assert mismatch_switch('CCCUU', True) == ('AACGG', 'CCGUU', 'CCCUU')
    assert mismatch_switch('GGCAA', True) == ('UUCCC', 'GGGAA', 'GGCAA')
    assert mismatch_switch('GGCUU', True) == ('AACCC', 'GGGUU', 'GGCUU')
    assert mismatch_switch('UUCCC', True) == ('GGCAA', 'UUGCC', 'UUCCC')
    assert mismatch_switch('UUCGG', True) == ('CCCAA', 'UUGGG', 'UUCGG')

def test_bulge_switch():
    assert bulge_switch('GGAA', True) == ('UUACC', 'GGUAA', 'GGAA')
    assert bulge_switch('GGAA', True, 'G') == ('UUGCC', 'GGCAA', 'GGAA')
    assert bulge_switch('GGAA', True, 'AA') == ('UUAACC', 'GGUUAA', 'GGAA')
    assert bulge_switch('UUCC', False) == ('GGAA', 'UUACC', 'UUCC')

def test_tunable_switch():
    import pytest

    assert tunable_switch('AUGC') == complementary_switch('AUGC')
    assert tunable_switch('AUGC', 'wx') == wobble_switch('AUGC', True)
    assert tunable_switch('AUGC', 'wo') == wobble_switch('AUGC', False)
    assert tunable_switch('AUGC', 'mx') == mismatch_switch('AUGC', True)
    assert tunable_switch('AUGC', 'mo') == mismatch_switch('AUGC', False)
    assert tunable_switch('AUGC', 'bx') == bulge_switch('AUGC', True)
    assert tunable_switch('AUGC', 'bxg') == bulge_switch('AUGC', True, 'G')
    assert tunable_switch('AUGC', 'bo') == bulge_switch('AUGC', False)

    with pytest.raises(ValueError):
        tunable_switch('AUGC', 'hello')
    with pytest.raises(ValueError):
        tunable_switch('AUGC', 'wxg')

def test_serpentine_insert():
    assert serpentine_insert('theo', 'G', '3') == 'GAUACCAGCCGAAAGGCCCUUGGCAGCGAAA'
    assert serpentine_insert('theo', 'G', '5') == 'GAAACAUACCAGCCGAAAGGCCCUUGGCAGG'
    assert serpentine_insert('theo', 'GUUAAAAU', '3') == 'GUUAAAAUAUACCAGCCGAAAGGCCCUUGGCAGAUUUUAACGAAA'
    assert serpentine_insert('theo', 'GUUAAAAU', '5') == 'GAAAAUUUUAACAUACCAGCCGAAAGGCCCUUGGCAGGUUAAAAU'
    assert serpentine_insert('theo', 'GUAC', '3', turn_seq='UAA') == 'GUACAUACCAGCCGAAAGGCCCUUGGCAGGUACUAA'
    assert serpentine_insert('theo', 'GUAC', '3', num_aptamers=2) == 'GUACAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGGUACGAAA'

def test_circle_insert():
    assert circle_insert('theo', 'G', '3') == 'CAUACCAGCCGAAAGGCCCUUGGCAGG'
    assert circle_insert('theo', 'G', '5') == 'GAUACCAGCCGAAAGGCCCUUGGCAGC'
    assert circle_insert('theo', 'AUGC', '3') == 'GCAUAUACCAGCCGAAAGGCCCUUGGCAGAUGC'
    assert circle_insert('theo', 'AUGC', '5') == 'AUGCAUACCAGCCGAAAGGCCCUUGGCAGGCAU'
    assert circle_insert('theo', 'AUGC', '3', num_aptamers=2) == 'GCAUAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAUGC'

def test_wt_sgrna():
    assert from_name('wt') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('wt(aavs)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_dead_sgrna():
    assert from_name('dead') == 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAACCCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

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

def test_fold_hairpin():
    import pytest

    with pytest.raises(ValueError): from_name('fh(0,0)')
    with pytest.raises(ValueError): from_name('fh(3,0)')
    with pytest.raises(ValueError): from_name('fh(1,5)')
    with pytest.raises(ValueError): from_name('fh(2,7)')

    assert from_name('fh(1,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAUACCAGCCGAAAGGCCCUUGGCAGGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('fh(1,4)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUAUACCAGCCGAAAGGCCCUUGGCAGAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('fh(2,0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('fh(2,6)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAUACCAGCCGAAAGGCCCUUGGCAGCGGUGCUUUUUU'

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

def test_serpentine_bulge():
    import pytest

    with pytest.raises(ValueError): from_name('sb(1)')

    assert from_name('sb(2)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAUCGUAUACCAGCCGAAAGGCCCUUGGCAGACGAAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('sb(8)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAUCGUUAAAAUAUACCAGCCGAAAGGCCCUUGGCAGAUUUUAACGAAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_lower_stem():
    assert from_name('sl') == 'GGGGCCACTAGGGACAGGATUCGGCUGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUAGCCGAAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_lower_stem_around_nexus():
    assert from_name('slx') == 'GGGGCCACTAGGGACAGGATGUUAUCGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUGAUAACAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_serpentine_hairpin():
    import pytest

    with pytest.raises(ValueError): from_name('sh(3)')
    with pytest.raises(ValueError): from_name('sh(15)')

    assert from_name('sh(4)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGAUACCAGCCGAAAGGCCCUUGGCAGCGUUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('sh(14)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGGACUAGCCUUAUACCAGCCGAAAGGCCCUUGGCAGAAGGCUAGUCCGUUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_bulge():
    assert from_name('cb') == 'GGGGCCACTAGGGACAGGATGUUUUAACUUAUACCAGCCGAAAGGCCCUUGGCAGAAGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_bulge_combo():
    assert from_name('cbc/wo/slx/wo').seq == 'GGGGCCACTAGGGACAGGATGUUGUCACUUAUACCAGCCGAAAGGCCCUUGGCAGAGGUAAGUGAUAACAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('cbc/wo/sh/5') == 'GGGGCCACTAGGGACAGGATGUUUUAACUUAUACCAGCCGAAAGGCCCUUGGCAGAGGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('cbc/wo/sh/7') == 'GGGGCCACTAGGGACAGGATGUUUUAACUUAUACCAGCCGAAAGGCCCUUGGCAGAGGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAAACGGACAUACCAGCCGAAAGGCCCUUGGCAGGUCCGUUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_lower_stem():
    assert from_name('cl') == 'GGGGCCACTAGGGACAGGATAGCCUUGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUAAGGCUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_circle_hairpin():
    import pytest

    with pytest.raises(ValueError): from_name('sh(3)')
    with pytest.raises(ValueError): from_name('sh(19)')

    assert from_name('ch(4)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAUCAAUACCAGCCGAAAGGCCCUUGGCAGUGAUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ch(18)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAAAGGCUAGUCCGUUAUCAAUACCAGCCGAAAGGCCCUUGGCAGUGAUAACGGACUAGCCUUGGCACCGAGUCGGUGCUUUUUU'


if __name__ == '__main__':
    import sys, pytest
    pytest.main(sys.argv)
