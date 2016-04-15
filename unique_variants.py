#!/usr/bin/env python3

"""\
Usage:
    unique_variants.py <protocol> [options]
    unique_variants.py <num_items> <num_picked>... [options]

Options:
    -f --fraction
    -n --count
    -t --sort-time <percent,time> [default: ??]
    -T --sort-times-below <percent,time> [default: 3h]
    -e --event-rate <evt_sec> [default: 10000]
"""

"""
-T 2h
-t 2h
-t 120m
-t 99%
-T 99%
"""

from pprint import pprint

def fraction_picked(num_items, num_picked):
    return 1 - ((num_items - 1) / num_items)**num_picked

def unique_items(num_items, num_picked):
    return num_items * fraction_picked(num_items, num_picked)

def cast_to_int(x):
    try:
        return int(x)
    except:
        return int(eval(x))

def percent(x, precision=2):
    return '{1:.{0}f}%'.format(precision, 100 * step.fraction_picked)

def scientific_notation(x, precision=2):
    from math import log10
    exponent = int(log10(x))
    mantissa = x / 10**exponent
    superscripts = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    superscript_exponent = str(exponent).translate(superscripts)
    return '{1:.{0}f}×10{2}'.format(precision, mantissa, superscript_exponent)


class PickStep:

    def __init__(self, num_items, num_picked, name=None):
        self.name = None
        self._num_items = num_items
        self._num_picked = num_picked

    def __repr__(self):
        return 'PickStep(num_picked={0.num_picked})'.format(self)

    @property
    def num_items(self):
        # If there was a selection step before this one, see how many unique 
        # items it yielded.
        try:
            return self._num_items.unique_items
        except AttributeError:
            pass

        # If the number of items is the name of an sgRNA design, count the 
        # number of variable positions in that design and raise 4 to that power 
        # to get the number of sequences theoretically in that library.
        try:
            import sgrna_sensor
            design = sgrna_sensor.from_name(self._num_items)
            return 4 ** design.dna.upper().count('N')
        except:
            pass

        # If none of these conditions apply, return the underlying attribute, 
        # converted to a number (e.g. via ``eval`` for strings) if necessary.

        return cast_to_int(self._num_items)

    @property
    def num_picked(self):
        return cast_to_int(self._num_picked)

    @property
    def unique_items(self):
        if self._num_items is None:
            return self.num_picked
        else:
            return unique_items(self.num_items, self.num_picked)

    @property
    def fraction_picked(self):
        if self._num_items is None:
            return 1
        else:
            return fraction_picked(self.num_items, self.num_picked)

    @property
    def previous_step(self):
        if isinstance(self._num_items, PickStep):
            return self._num_items


class SortStep(PickStep):

    def __init__(self, num_items, num_picked, num_sampled, name=None):
        super().__init__(num_items, num_picked, name)
        self._num_sampled = num_sampled

    def __repr__(self):
        return 'SortStep(num_picked={0.num_picked}, num_sampled={0.num_sampled})'.format(self)

    @property
    def num_items(self):
        return super().num_items * self.num_picked / self.num_sampled

    @property
    def num_sampled(self):
        return cast_to_int(self._num_sampled)



def parse_num_file(path):
    with open(path) as file:
        blocks = file.read().strip().split('\n\n')

    all_steps = []
    last_step_with_indent = {-1: None}

    for block in blocks:
        leading_space = len(block) - len(block.lstrip())
        indent = leading_space // 2
        last_step = last_step_with_indent[indent-1]

        *labels, num_picked = [x.strip() for x in block.splitlines()]
        label = '\n'.join(labels)

        if 'of' not in num_picked:
            step = PickStep(last_step, num_picked)
        else:
            num_picked, num_sampled = num_picked.split(' of ')
            step = SortStep(last_step, num_picked, num_sampled)

        all_steps.append(step)
        last_step_with_indent[indent] = step

    return all_steps

def most_recent(steps):
    most_recent = steps[:]
    for step in steps:
        try: most_recent.remove(step.previous_step)
        except ValueError: pass
    return most_recent


if __name__ == '__main__':
    import docopt, yaml, tabulate
    args = docopt.docopt(__doc__)
    steps = []

    if args['<num_items>']:
        steps = [
                PickStep(args['<num_items>'], num_picked)
                for num_picked in args['<num_picked>']
        ]

    if args['<protocol>']:
        steps = parse_num_file(args['<protocol>'])
        steps = most_recent(steps)

    table = []
    for step in steps:
        row = []
        table.append(row)

        if args['--count']:
            row.append(scientific_notation(step.unique_items))
        if args['--fraction']:
            row.append(percent(step.fraction_picked))
        if args['--sort-time']:
            raise NotImplementedError
        if args['--sort-times-below']:
            raise NotImplementedError

    print(tabulate.tabulate(table, tablefmt='plain'))




# Parse yaml file, pick nodes to report, report fraction/num unique for each.
#
#
# Problem: This is really a tree.  For example, I'm using the same MG1655 
# transformation for lots of sorts.  For another, I collected two "dead" 
# populations from the same culture.  When I branch like this, I have to 
# duplicate everything up to the branch point.

# How do I know which numbers to show?  By default, show all leaves?  Allow 
# user to select nodes by partial string match.  Also allow the user to show 
# all leaves below nodes matched by a partial string.

