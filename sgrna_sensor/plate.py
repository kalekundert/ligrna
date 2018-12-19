#!/usr/bin/env python3

# - Need to handle multiple plates
#   - Each plate can be, but doesn't have to be, associated with a path
#
# - Return data frame:
#   - Index: row, column
#     - plate: apo
#     - path: 20181002_qpcr_expt.xlsx
#     - row: 0
#     - row_abc: A
#     - col: 0
#     - col_123: 1
#     - well: A1
#
#   - Columns: all fields
#
# - Tiling?

def recursive_merge(config, defaults, overwrite=False):
    for key, default in defaults.items():
        if isinstance(default, dict):
            layout.setdefault(key, {})
            recursive_merge(layout[key], default)
        else:
            if overwrite or key not in layout:
                layout[key] = default


def load_plate(toml_path):
    """\
    Parse a TOML-formatted configuration file defining how each well in a 
    particular plate should be interpreted.
    
    Below is a list of the keys that are understood in the configuration file:

    'xlsx_path' [string]
        The path to the XLSX file containing the plate reader data, relative to 
        the configuration file itself.  If not specified, this script will look 
        for a file with the same name as the configuration file, but the 
        '.xlsx' extension, e.g. 'abc.xlsx' if the config file is 'abc.toml'.

    'template' [string]
        The path to another TOML file that should be interpreted as containing 
        default values for all possible settings.

    'notes' [string]
        A string that will be printed every time the file is visualized.  This 
        is meant to reminder the user of any details relating to this 
        particular experiment (e.g. mistakes) that might affect interpretation 
        of the data.

    The following keys relate to particular wells.  Each of these keys can be 
    specified in any of four kinds of block: [well.A1], [row.A], [col.1], and 
    [plate].  The [well] block allows values to be set for individual wells ('A1' 
    in this example).  The [row] and [col] blocks allow values to be set for 
    whole rows and columns ('A' and '1' in these examples).  The [plate] block 
    allows values to be set for the whole plate.  The same value can be set 
    multiple times, in which case the value from the most specific block will 
    take precedence.

    """
    import toml
    import itertools
    from pathlib import Path

    def recursive_merge(layout, defaults, overwrite=False):
        for key, default in defaults.items():
            if isinstance(default, dict):
                layout.setdefault(key, {})
                recursive_merge(layout[key], default)
            else:
                if overwrite or key not in layout:
                    layout[key] = default

    def do_load_paths(toml_path, expected_ext='.xlsx'):
        toml_path = Path(toml_path).resolve()
        layout = toml.load(str(toml_path))

        # Resolve the path(s) to actual data.
        if 'path' in layout and 'paths' in layout:
            raise ValueError(f"{toml_path} specifies both 'path' and 'paths'")

        elif 'path' in layout:
            path = toml_path.parent / layout['path']
            layout['paths'] = {'default': path}

        elif 'paths' in layout:
            layout['paths'] = {
                    toml_path.parent / x
                    for x in layout['paths']
            }
        else:
            default_path = toml_path.with_suffix(expected_ext)
            if default_path.exists():
                layout['paths'] = {'default': default_path}

        # Include a remote file if one is specified.  
        if 'template' in layout:
            layout['template'] = toml_path.parent / layout['template']
            template = do_load_paths(layout['template'])
            recursive_merge(layout, template)

        return layout

    layout = do_load_paths(toml_path)

    # Apply any row or column defaults.
    if 'well' not in layout:
        layout['well'] = {}

    rows = layout.get('row', {})
    cols = layout.get('col', {})

        # Create new wells implied by the 'row' and 'col' blocks.
    for row, col in itertools.product(rows, cols):
        layout['well'].setdefault(f'{row}{col}', {})

        # Update any existing wells.
    for well in layout.get('well', {}):
        row, col = well[:1], well[1:]
        recursive_merge(layout['well'][well], rows.get(row, {}))
        recursive_merge(layout['well'][well], cols.get(col, {}))

    # Apply any plate-wide defaults.
    layout.setdefault('plate', {}),
    for well in layout.get('well', {}):
        recursive_merge(layout['well'][well], layout['plate'])

    # If the experiment has any notes, print them out.
    if 'notes' in layout:
        print(toml_path)
        print(layout['notes'].strip())
        print()

    return layout

def rows_cols_from_dict(config, label=None):
    # Create wells dictionary from dictionary.  The following keys are used to 
    # fill out wells:
    #
    # [row]
    # [irow]
    # [col]
    # [icol]
    # [well]

    wells = layout.get('well', {})
    meta = layout.get('meta', {})
    rows = layout.get('row', {})
    irows = layout.get('irow', {})
    cols = layout.get('col', {})
    icols = layout.get('icol', {})

    # Fill in everything from the template.
    if 'defaults' in meta:
        config = 

    # Create new wells implied by the 'row' and 'col' blocks.
    for row, col in itertools.product(rows, cols):
        key = well_from_row_col(row, col)
        wells.setdefault(key, {})

    for irow, col in itertools.product(irows, cols):
        key = well_from_irow_col(irow, col)
        wells.setdefault(key, {})

    if row, icol in itertools.product(rows, icols):
        key = well_from_row_icol(row, icol)
        wells.setdefault(key, {})
    
    # Update any existing wells.
    for key in wells:
        row, col = row_col_from_well(well)
        irow, icol = irow_icol_from_well(well)

        recursive_merge(wells[key], rows.get(row, {}))
        recursive_merge(wells[key], cols.get(col, {}))
        recursive_merge(wells[key], irows.get(irow, {}))
        recursive_merge(wells[key], icols.get(icol, {}))

    
    

def well_from_row_col(row, col):
    return f'{row}{col}'

def well_from_irow_col(irow, col):
    ii, j = ints_from_row_col(irow, col)
    i = interleave(ii, j)
    return well_from_ints(i, j)

def well_from_row_icol(row, icol):
    i, jj = ints_from_row_col(row, icol)
    j = interleave(jj, i)
    return well_from_ints(i, j)

def well_from_ints(i, j):
    return well_from_row_col(
            row_from_int(i),
            col_from_int(j),
    )


def interleave(a, b):
    """
    `a` is the index being interleaved (e.g. row or column).  `b` is the 
    straight index in the opposite dimension (e.g. column or row).
    """
    d = 1 - 2 * (b % 2)
    return a + d

def inverse_interleave(a, b):
    """
    Given a coordinate where `a` has been interleaved and `b` hasn't, return 
    the value that `a` would have at `b=0`.
    """
    if a % 2 == 0:
        return a + b % 2
    else:
        return a - (b+1) % 2


def int_from_row(row):
    return ord(row.upper()) - ord('A')

def int_from_col(col):
    return int(col) - 1

def ints_from_row_col(row, col):
    return int_from_row(row), int_from_col(col)


def row_from_int(i):
    return string.ascii_uppercase[i]

def col_from_int(j):
    return str(j + 1)

def row_col_from_ints(i, j):
    return row_from_int(i), col_from_int(j)


def row_col_from_well(well):
    return well[:1], well[1:]

def irow_icol_from_well(well):
    row, col = row_col_from_well(well)
    i, j = ints_from_row_col(row, col)
    ii = inverse_interleave(i, j)
    jj = inverse_interleave(j, i)
    return row_col_from_ints(ii, jj)


def index_from_well(well):
    row, col = well[:1], well[1:]
    return dict(
            well=key,
            row=row,
            col=col,
            row_0=int_from_row(row),
            col_0=int_from_col(col),
    )


def dotted_label(label, x):
    return f'{label}.{x}' if label else x


