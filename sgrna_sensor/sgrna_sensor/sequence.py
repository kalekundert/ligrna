#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections, re, nonstdlib, six

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
        tokens = re.findall('[a-zA-Z0-9]+', self.name)
        return '{}({})'.format(tokens[0], ','.join(tokens[1:]))

    @property
    def underscore_name(self):
        tokens = re.findall('[a-zA-Z0-9]+', self.name)
        return '_'.join(tokens)

    @property
    def slash_name(self):
        tokens = re.findall('[a-zA-Z0-9]+', self.name)
        return '/'.join(tokens)

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



