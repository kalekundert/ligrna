import re, nonstdlib
import numpy as np
import pandas as pd

class Parser:

    def __init__(self, expt):
        self.expt = expt

    def parse_row(self, row):
        raise NotImplementedError


class NullParser(Parser):

    def parse_row(self, row):
        pass

class HeaderParser(Parser):

    header_keys = {
            'Software Version',
            'Experiment File Path:',
            'Protocol File Path:',
            'Plate Number',
            'Date',
            'Time',
            'Reader Type:',
            'Reader Serial Number:',
            'Reading Type',
            'Procedure Details',
            'Plate Type',
    }

    def parse_row(self, row):
        key = row[0].value
        value = row[1].value

        if key in self.header_keys:
            attr = nonstdlib.name_from_title(key)
            setattr(self.expt, attr, value)

        
class ReadParser(Parser):

    def parse_row(self, row):
        indent = row[0].value
        key = row[1].value
        read_pattern = re.compile('(?:Blank Read \d:)?(\d+)')

        if indent is not None:
            return
        if key is None:
            return
        if key == 'Well':
            self.wells = [x.value for x in row[2:] if x.value]
            return
        
        read_match = read_pattern.match(str(key))
        if read_match:
            wavelength = int(read_match.group(1))
            reads = {
                    k: x.value
                    for k,x in zip(self.wells, row[2:])
                    if x.value != '?????'
            }
            self.expt.reads[wavelength] = reads
            setattr(self.expt, f'reads_{wavelength}', reads)

class KineticParser(Parser):

    def parse_row(self, row):
        title = row[0].value
        key = row[1].value

        if title is not None:
            self.wavelength = int(title.split(':')[-1])
            self.attr = f'kinetic_{self.wavelength}'
            self.kinetic = []

        if key == 'Time':
            self.header = ['minutes'] + [x.value for x in row[2:]]

        elif key is not None:
            reads = [x.value for x in row[2:]]
            if reads:
                minutes = 60 * key.hour + key.minute
                self.kinetic.append([minutes] + reads)

        if key is None and self.kinetic:
            df = pd.DataFrame(self.kinetic, columns=self.header)
            df[df == '?????'] = np.nan
            df = df.dropna(axis='columns', how='all')
            df = df.dropna(axis='rows', how='any')
            self.expt.kinetic[self.wavelength] = df
            setattr(self.expt, self.attr, df)



class BetaGalExperiment:

    def __init__(self, path):
        from openpyxl import load_workbook

        self.reads = {}
        self.kinetic = {}

        wb = load_workbook(path)
        ws = wb.active
        parser = HeaderParser(self)

        for row in ws.rows:
            key = row[0].value

            if key == 'Results':
                parser = ReadParser(self)

            if isinstance(key, str) and key.startswith('Blank Read'):
                parser = KineticParser(self)

            parser.parse_row(row)

    def __str__(self):
        lines = ['BetaGalExperiment']
        for attr, value in self.__dict__.items():
            if attr.startswith('_'):
                continue
            if attr.startswith('kinetic'):
                lines += [f'  {attr}:', f'{value}']
            else:
                lines += [f'  {attr + ":":25s} {value}']
        return '\n'.join(lines)



