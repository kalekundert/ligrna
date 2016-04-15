#!/usr/bin/env python3

"""\
Calculate how many unique library members remain in each step of a screen.  
This information can inform how long and how accurate sorting steps should be.

Usage:
    unique_variants.py <protocol> [options]
    unique_variants.py <num_items> <num_picked>... [options]

Arguments:
    <protocol>
        A YAML-formatted file describing all the steps in a library screen.  
        The number of individuals kept after each step is specified.
        
    <num_items>
        The theoretical complexity of the library being picked from.

    <num_picked>
        The number of individuals you picked from the library.

Options:
    -e --event-rate <evt_sec>
        Report how long it would take to screen '--fraction-wanted' of the 
        entire library on the BD FACSAria II with the given event rate.  The 
        fact that some cells will be double-counted and that some cells won't 
        survive sorting will be accounted for.  Note that you should think of 
        event rate as a proxy for sorting accuracy.

    -f --fraction-wanted <percent>  [default: 95]
        If you specified '--event-rate', what fraction of the library do you 
        want to screen?  63% corresponds to 1x coverage, roughly speaking.

    -s --survival-rate <percent>  [default: 60]
        If you specified '--event-rate', what fraction of cells survive 
        sorting?  I've measured this in two ways (plating and flow cytometry) 
        and gotten ~60% by both metrics.  However, it may be that you could 
        optimize conditions to increase cell viability.
"""

from pprint import pprint
inf = float('inf')

def fraction_picked(num_items, num_picked):
    return 1 - ((num_items - 1) / num_items)**num_picked

def unique_items(num_items, num_picked):
    return num_items * fraction_picked(num_items, num_picked)

def sort_time(num_items, fraction_wanted, event_rate=10000, survival_rate=0.6):
    import numpy as np
    import scipy.stats

    # Predict how efficient the sorting will be.  I've observed that the linear 
    # correlation between event rate and sorting efficiency is pretty good, 
    # although the efficiency also fluctuates by ~10% depending on how common 
    # the cells you're sorting for are.

    if event_rate < 0:
        raise ValueError('The event rate must be positive, not {}.'.format(event_rate))

    event_rates_to_efficiencies = {
        47668: 0.08, # 20160331_optimize_sorting_speed
        26166: 0.42,
         9575: 0.73,
         3098: 0.90,
        49921: 0.06,
        26267: 0.39,
         9961: 0.72,
         3233: 0.90,
        53380: 0.10,
        30071: 0.49,
        10233: 0.81,
         2917: 0.91,
        53380: 0.16,
        30071: 0.57,
        10233: 0.84,
         2917: 0.94,
         1135: 0.96, # 20160414_screen_rb
         1348: 0.96,
    }

    event_rates = np.array(list(event_rates_to_efficiencies.keys()))
    efficiencies = np.array(list(event_rates_to_efficiencies.values()))
    m, b, _, _, _ = scipy.stats.linregress(event_rates, efficiencies)
    efficiency = m * event_rate + b

    # Calculate how long it will take to collect the given fraction of the 
    # library, accounting for the fact that some cells will be double-counted 
    # and some cells won't survive sorting.

    counting = np.log(1 - fraction_wanted) / np.log((num_items - 1) / num_items)
    inv_min = survival_rate * efficiency * event_rate * 60
    sort_time = int(counting / inv_min)
    return '{}h{:02d}'.format(sort_time // 60, sort_time % 60)

def cast_to_number(x):
    try:
        return int(x)
    except:
        return eval(x)

def percent(x, precision=2):
    return '{1:.{0}f}%'.format(precision, 100 * step.fraction_picked)

def scientific_notation(x, precision=2):
    from math import log10
    exponent = int(log10(x))
    mantissa = x / 10**exponent
    mantissa_str = '{0:.{1}f}'.format(mantissa, precision)

    # Handle the corner case where the mantissa rounds up to 10, in which case 
    # we should increment the exponent by one.
    if mantissa_str.startswith('10'):
        exponent += 1
        mantissa /= 10
        mantissa_str = '{0:.{1}f}'.format(mantissa, precision)

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
        # If the specific number of items wasn't specified, return None.
        if self._num_items is None:
            return None

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

        return cast_to_number(self._num_items)

    @property
    def num_picked(self):
        return cast_to_number(self._num_picked)

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
        return cast_to_number(self._num_sampled)



def steps_from_yaml(path):
    import yaml

    with open(path) as file:
        records = yaml.load(file)

    steps = []

    for record in records:
        num_items = steps[-1] if steps else None

        if 'picked' in record:
            num_picked = record['picked']
            step = PickStep(num_items, num_picked)
        elif 'sorted' in record:
            num_picked, num_sampled = record['sorted'].split(' of ')
            step = SortStep(num_items, num_picked, num_sampled) 
        else:
            raise SyntaxError("Every step must specify either 'picked' or 'sorted'.")

        step.name = record.get('step', '')
        steps.append(step)

    return steps

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
        steps = steps_from_yaml(args['<protocol>'])

    table = []
    for step in steps:
        row = []
        table.append(row)

        if any(x.name for x in steps):
            row.append(step.name)

        row.append(scientific_notation(step.unique_items))
        row.append(percent(step.fraction_picked))

        if args['--event-rate']:
            row.append(sort_time(
                step.unique_items,
                eval(args['--fraction-wanted']) / 100,
                eval(args['--event-rate']),
                eval(args['--survival-rate']) / 100,
            ))

    print(tabulate.tabulate(table, tablefmt='plain'))




