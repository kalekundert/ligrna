#!/usr/bin/env python3

__version__ = '0.0.0'

from .components import *
from .designs import *
from .helpers import *
from .sequence import *

def from_name(name, **kwargs):
    import re, inspect

    name = name.strip()
    if not name:
        raise ValueError("Can't parse empty name.")

    tokens = re.findall('[a-zA-Z0-9]+', name)

    # If the first token matches the name of one of the known targeting 
    # sequences, use that sequence to build the design.  If the next token 
    # (which would be the first if no targeting sequence was found and the 
    # second otherwise) matches the name of one of the known ligand, use that 
    # ligand's aptamer to build the design.
    #
    # Both these fields are optional.  The default targeting sequence is "aavs" 
    # and the default ligand is "theo".

    try:
        spacer(tokens[0])
    except ValueError:
        target = 'aavs'
    else:
        target = tokens.pop(0)
    if 'target' not in kwargs:
        kwargs['target'] = target

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

def molecular_weight(name, polymer='rna'):
    return from_name(name).mass(polymer)

