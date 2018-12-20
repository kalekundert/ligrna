#!/usr/bin/env python3

"""\
Count how many cells were successfully transformed via electroporation.

This is a fairly brittle script meant to help with a calculation I frequently 
make.  When I do an electro-transformation, I plate up to four dilutions: 10⁻³, 
10⁻⁴, 10⁻⁵, 10⁻⁶.  This script takes the number of colony-forming units (CFUs) 
from each plate and converts that into the number of transformants.  It also 
reports a weighted average, based on the number of counts at each level, which 
I treat as the true number of transformants.

Usage:
    count_transformed_cells.py <cfus>... [options]

Options:
    -p --plate-volume <μL>          [default: 20]
        The volume of cells that were plated for each dilution.  By default 
        this is 20 μL, which is a good amount for titering 16 measurements on a 
        single plate.
        
    -r --recovery-volume <μL>       [default: 1000]
        The total volume of recovered cells.  By default, this is 1 mL, which 
        is the amount of SOC I typically add after electroporation.  However, 
        the volume should technically also include the volume of the competent 
        cells (50-100 μL) and the volume of the added DNA (1-5 μL).
"""

from attr import attrs, attrib
from numpy import array, arange, average
from nonstdlib import sci
from pprint import pprint

default_dilutions = (200 / 2) * (200 / 20)**arange(4)

def count_transformants(recover_uL, plate_uL, num_cfus, *, dilutions=None):
    if dilutions is None:
        dilutions = default_dilutions

    num_cfus, dilutions = discard_lawns(num_cfus, dilutions)
    num_transformants = dilutions * num_cfus * recover_uL / plate_uL
    ii = num_transformants > 0
    return average(num_transformants[ii], weights=1/dilutions[ii])

def discard_lawns(all_cfus, all_dilutions):
    num_cfus = []
    dilutions = []
    lawn = 'x', '-', 'lawn'

    for cfu, dilution in zip(all_cfus, all_dilutions):
        if cfu not in lawn:
            num_cfus.append(cfu)
            dilutions.append(dilution)

    return array(num_cfus), array(dilutions)

def parse_library(library, size=None):
    import sgrna_sensor

    if size is not None:
        return library, size
    elif isinstance(library, str):
        library_name = library
        library_seq = sgrna_sensor.from_name(library_name).seq
        library_size = sgrna_sensor.library_size(library_seq)
    else:
        library_name, library_size = library

    return library_name, library_size

def evaluate_coverage(library_size, num_transformants):
    from unique_variants import unique_items
    num_unique_transformants = unique_items(library_size, num_transformants)
    percent_coverage = num_unique_transformants / library_size
    fold_coverage = num_transformants / library_size
    return num_unique_transformants, percent_coverage, fold_coverage


class TransformationTable:
    """
    Calculate efficiencies for one more more transformations and display the 
    results in a table.

    A list of tuples should be provided to describe each transformation.  Each 
    tuple should contain four values:

    - The name of the library.  This may be a string or a tuple.  If it's a 
      string, it is assumed to be the name of an sgRNA sensor library, and the 
      size of that library will be used when calculating coverage data.  If 
      it's a tuple, the first item should be the name of the library, and the 
      second should be it's size.

    - The volume of cells recovered, in μL.  1000 μL would be a typical value.

    - The volume of cells plated, in μL.  40 μL would be a typical value.

    - A list of the number of colonies counted.  The first item in the list 
      should correspond the greatest dilution, the second to the second 
      greatest, and so on.  If you get to a point where there are too many 
      colonies to count, just end the list.

      The default dilutions are four 10x dilutions starting from 10⁻³.  If you 
      diluted your cells differently, either change the `default_dilutions` 
      global variable or construct a TransformationTable object and set its 
      `dilutions` attribute.
    """

    @attrs
    class Row:
        library_name = attrib()
        recover_uL = attrib()
        plate_uL = attrib()
        num_cfus = attrib()
        num_transformants = attrib()
        num_unique_transformants = attrib()
        percent_coverage = attrib()
        fold_coverage = attrib()

    def __init__(self, *data, **kwargs):
        self.results = []
        self.dilutions = kwargs.get('dilutions', default_dilutions)
        self.add_rows(*data)

    def __reprhtml__(self):
        num_cfu_cols = max(len(row.num_cfus) for row in self.results)
        cfu_col_headers = ''.join(
                f'<th style="text-align:right"># cfu/{sci(x, exp_only=True)}</th>'
                for x in self.dilutions[0:num_cfu_cols])

        html = ('<table>'
                '<tr>'
                '<th style="text-align:left">Library</th>'
                '<th style="text-align:right">Recover (μL)</th>'
                '<th style="text-align:right">Plate (μL)</th>'
                f'{cfu_col_headers}'
                '<th style="text-align:right"># Transformants</th>'
                '<th style="text-align:right"># Unique</th>'
                '<th style="text-align:right">Coverage (%)</th>'
                '<th style="text-align:right">Coverage (fold)</th>'
                '</tr>')

        def get(list, i, default):
            try: return list[i]
            except IndexError: return default

        for row in self.results:
            cfu_cells = ''.join(
                    f'<td style="text-align:right">{get(row.num_cfus, i, "lawn")}</td>'
                    for i in range(num_cfu_cols))
            html += ('<tr>'
                    f'<td style="text-align:left">{row.library_name}</td>'
                    f'<td style="text-align:right">{row.recover_uL}</td>'
                    f'<td style="text-align:right">{row.plate_uL}</td>'
                    f'{cfu_cells}'
                    f'<td style="text-align:right">{sci(row.num_transformants)}</td>'
                    f'<td style="text-align:right">{int(round(row.num_unique_transformants))}</td>'
                    f'<td style="text-align:right">{row.percent_coverage * 100:.2f}%</td>'
                    f'<td style="text-align:right">{row.fold_coverage:.2f}x</td>'
                    '</tr>')

        html += '</table>'
        return html

    _repr_html_ = __reprhtml__

    def add_rows(self, *data):
        for library_name, recover_uL, plate_uL, num_cfus in data:
            self.add_row(library_name, recover_uL, plate_uL, num_cfus)

    def add_row(self, library, recover_uL, plate_uL, num_cfus):
        num_transformants = count_transformants(
                recover_uL, plate_uL, num_cfus, dilutions=self.dilutions)
        library_name, library_size = parse_library(library)
        num_unique, percent_coverage, fold_coverage = evaluate_coverage(
                library_size, num_transformants)
        row = self.Row(
                library_name, recover_uL, plate_uL, num_cfus,
                num_transformants, num_unique, percent_coverage, fold_coverage)
        self.results.append(row)


record_transformants = TransformationTable


if __name__ == '__main__':
    import docopt
    from pylab import *

    args = docopt.docopt(__doc__)
    cfus = array([eval(n) for n in args['<cfus>']])
    plate_volume = float(args['--plate-volume'])
    recovery_volume = float(args['--recovery-volume'])
    dilutions = (200 / 2) * (200 / 20)**arange(len(cfus))
    transformants = recovery_volume * dilutions * (cfus / plate_volume)
    num_data = len(cfus[cfus != 0])

    print('Dilution  # CFU  # transformants')
    print('========  =====  ===============')
    for i in range(len(cfus)):
        if cfus[i] > 0:
            print('1e-{:<5d}  {:>5d}  {:>14.2e}'.format(
                i + 3,
                cfus[i],
                transformants[i],
            ))

    if num_data > 1:
        idx = transformants > 0
        print("Weighted average: {:13.2e}".format(
            np.average(transformants[idx], weights=1/dilutions[idx])))

