#!/usr/bin/env python3

import jinja2
import subprocess
from pathlib import Path

def render_template(path, context, template_dir='.'):
    loader = jinja2.FileSystemLoader(template_dir)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(f'{path}.jinja')
    template.stream(**context).dump(path)

def render_latex(path, context, template_dir='.'):
    render_template(path)
    latex(path)

def render_latex_table(path, context):
    path = Path(path)
    render_template(f'{path.stem}_tabular.tex', context)

    if not path.exists():
        with path.open('w') as file:
            file.write(r"""\documentclass{article}

\usepackage{fontspec}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{multicol}
\usepackage{multirow}

\setmainfont{Liberation Sans}

\newcommand\ligrnaF{ligRNA\textsuperscript{+}}
\newcommand\ligrnaB{ligRNA\textsuperscript{−}}

\begin{document}

\begin{table}
\centering
\input{%s_tabular}
\end{table}

\end{document}
""" % path.stem)

    latex(path)

def latex(path):
    subprocess.run(['xelatex', '--halt-on-error', str(path)])

