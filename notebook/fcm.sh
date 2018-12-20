#!/usr/bin/env zsh
set -euo pipefail
IFS=$'\n\t'

function fcm () {(
    # Run one of the flow cytometry data analysis scripts, and infer the 
    # correct directories for all the arguments.  This is meant to make it 
    # easier to run these analysis scripts from my lab notebook without having 
    # to be proper about all the paths.
    #
    # Usage:
    #    fcm <script name> <yaml file> [<other args>...]
    #
    # Examples:
    #    $ source fcm.sh
    #    $ fcm fold_change 20170824_multiplex_controls.yml
    #    $ fcm fold_change 20170824_multiplex_controls.yml -O9x13
    #    $ fcm bar_chart 20170824_multiplex_controls.yml -o '$_bar_plot.svg'

    # If the user didn't specify an output path, tell the analysis script to 
    # create an SVG file named after the data being plotted, instead of opening 
    # up an interactive graph.
    grep -q -- -o <<<"$@" && o='' || o='-o$.svg'

    # Run the analysis with the corrected script and data file paths.
    fcm=$(realpath ~/sgrna/flow_cytometry)
    $fcm/$1.py $fcm/data/$2 "${@:3}" $o
)}

function join_by { local IFS="$1"; shift; echo "$*"; }

function vienna () {
    slug=$(join_by _ "$@")
    sgrna_sensor -rc --color always "$@" | aha -b -s > $slug.html
    wkhtmltopdf $slug.html $slug.pdf 2> /dev/null
    pdf2svg $slug.pdf $slug.svg
    inkscape $slug.svg --verb FitCanvasToDrawing --verb FileSave --verb FileQuit
    rm $slug.html $slug.pdf
}


