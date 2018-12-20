#!/usr/bin/env zsh
set -euo pipefail
source ../fcm.sh

fcm fold_change 20170824_multiplex_controls.yml -o '$_traces.svg' -O9x13.5
fcm bar_chart 20170824_multiplex_controls.yml
fcm bar_chart 20170828_mockup_multiplex_time_course_3mx.yml -q gfp -o '$_gfp.svg' --inkscape
fcm bar_chart 20170828_mockup_multiplex_time_course_3mx.yml -q rfp -o '$_rfp.svg' --inkscape
fcm bar_chart 20170828_mockup_multiplex_time_course_theo_3mx.yml -q gfp -o '$_gfp.svg' --inkscape
fcm bar_chart 20170828_mockup_multiplex_time_course_theo_3mx.yml -q rfp -o '$_rfp.svg' --inkscape

fcm fold_change 20170831_multiplex_timecourse_theo_3mx.yml

