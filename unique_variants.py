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
    -i --int
        Report the number of unique library members as full-precision integers.  
        By default, these numbers are rounded and reported using scientific 
        notation.

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

import re, numpy as np
from nonstdlib import *
from pprint import pprint
inf = float('inf')

def fraction_picked(num_items, num_picked):
    return 1 - ((num_items - 1) / num_items)**num_picked

def unique_items(num_items, num_picked):
    return num_items * fraction_picked(num_items, num_picked)

def sort_efficiency(event_rate):
    """
    Predict the efficiency of the sort, meaning the number of cells that are 
    actually charged and sorted divided by the number of events that are 
    just detected.  I've observed that the linear correlation between event 
    rate and sorting efficiency is pretty good, although the efficiency also 
    fluctuates by ~10% depending on how common the desired cells are.
    """
    import scipy.stats

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
    return m * event_rate + b

def sort_time(num_items, fraction_wanted, event_rate=10000, survival_rate=0.6):
    """
    Calculate how long it will take to collect the given fraction of the 
    library, accounting for the fact that some cells will be double-counted 
    and some cells won't survive sorting.
    """
    counting = np.log(1 - fraction_wanted) / np.log((num_items - 1) / num_items)
    return int(counting / items_sorted(1, event_rate, survival_rate))

def items_sorted(sort_time, event_rate=10000, survival_rate=0.6):
    """
    Return the number of cells that can be sorted in the given amount of time, 
    accounting for the fact that not all cells survive sorting and that the 
    sorter will decline to sort cells in certain (usually crowded) conditions.
    """
    true_event_rate = event_rate * sort_efficiency(event_rate) * survival_rate
    return 60 * cast_to_minutes(sort_time) * true_event_rate

def cast_to_number(x):
    try:
        return int(x)
    except:
        return eval(x)

def cast_to_minutes(x):
    if isinstance(x, int):
        return x

    parsed_time = re.match('(\d+)h(\d+)?', x)
    if not parsed_time:
        raise ValueError("can't interpret '{}' as a time.".format(x))

    hours = parsed_time.group(1)
    minutes = parsed_time.group(2) or 0

    return 60 * int(hours) + int(minutes)

def percent(x, precision=2):
    return '{0:{1}.{2}f}%'.format(100 * x, precision + 4, precision)

def hours_and_minutes(x):
    return '{}h{:02d}'.format(x // 60, x % 60)


class Step:

    @property
    def unique_items(self):
        raise NotImplementedError

    @property
    def fraction_picked(self):
        raise NotImplementedError

    @property
    def previous_step(self):
        raise NotImplementedError


class UniqueStep(Step):

    def __init__(self, unique_items, previous_step=None):
        self._unique_items = unique_items
        self._previous_step = previous_step

    @property
    def unique_items(self):
        return cast_to_number(self._unique_items)

    @property
    def fraction_picked(self):
        if self.previous_step is None:
            return 1
        else:
            return self.unique_items / self.previous_step.unique_items

    @property
    def previous_step(self):
        return self._previous_step


class PickStep(Step):

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
    import os, yaml

    with open(path) as file:
        records = yaml.load(file)

    steps = []

    for record in records:
        previous_step = steps[-1] if steps else None

        if 'unique' in record:
            unique_items = record['unique']
            step = UniqueStep(unique_items, previous_step)

        elif 'picked' in record:
            num_picked = record['picked']
            step = PickStep(previous_step, num_picked)

        elif 'sorted' in record:
            count_syntax = re.match('(.*) of (.*)', record['sorted'])
            percent_syntax = re.match('(.*)% for (.*) at (.*) evt/sec', record['sorted'])

            if count_syntax:
                num_picked, num_sampled = count_syntax.groups()

            elif percent_syntax:
                percent_kept = cast_to_number(percent_syntax.group(1)) / 100
                sort_time = cast_to_minutes(percent_syntax.group(2))
                event_rate = cast_to_number(percent_syntax.group(3))
                num_sampled = items_sorted(sort_time, event_rate)
                num_picked = percent_kept * num_sampled

            else:
                raise SyntaxError("can't understand '{}'.".format(record['sorted']))
                
            step = SortStep(previous_step, num_picked, num_sampled) 

        elif 'from' in record:
            import_path = os.path.join(os.path.dirname(path), record['from'])
            for step in steps_from_yaml(import_path):
                if step.name != record['step']:
                    steps.append(step)
                else:
                    break

        else:
            raise SyntaxError("Every step must specify 'unique', 'picked', 'sorted', or 'from'.")

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

        if args['--int']:
            row.append(int(step.unique_items))
        else:
            row.append(sci(step.unique_items))

        row.append(percent(step.fraction_picked))

        if args['--event-rate']:
            row.append(hours_and_minutes(sort_time(
                step.unique_items,
                eval(args['--fraction-wanted']) / 100,
                eval(args['--event-rate']),
                eval(args['--survival-rate']) / 100,
            )))

    print(tabulate.tabulate(table, tablefmt='plain'))




