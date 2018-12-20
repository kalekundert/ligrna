#!/usr/bin/env zsh

if [ $# = 0 ]; then
    echo "Usage: ./pick_designs.sh <round> [options]"
    exit
else
    round=$1
    shift
fi

seqs=()

if [ "$round" = best ]; then
    seqs+=(
        us/0/0
        nx/0
        sh/5
        sh/7
        cb
        cb/wo
    )
fi

if [ "$round" = strategies ]; then
    seqs+=(
        wt
        dead
        us/4/6
        ls/6/2
        nx/2
        hp/17
        id/5/4
        id/3/4
        nxx/3/4
        sb/5
        sl
        slx
        sh/5
        sh/7
        cb
        cl
        ch/4                
    )
fi

if [ "$round" = 0 ] || [ "$round" = all ]; then
    seqs+=(
        wt
        dead
    )
fi

if [ "$round" = 1 ] || [ "$round" = all ]; then
    seqs+=(
        us/0/0
        us/0/1
        us/0/2
        us/0/3              
    )
fi

if [ "$round" = 2 ] || [ "$round" = all ]; then
    seqs+=(
        us/1/0
        us/1/1
        us/1/2
        us/1/3
        us/2/2
        us/2/6
        us/2/10
        us/2/14
        us/4/2
        us/4/6
        us/4/10
        us/4/14
        ls/5/0
        ls/6/0
        ls/6/2
        ls/6/4
        ls/6/6
        nx/0
        nx/1
        nx/2
        nx/3
        hp/17
        hp/18
        hp/33               
    )
fi

if [ "$round" = 3 ] || [ "$round" = all ]; then
    seqs+=(
        id/5/0
        id/3/0
        id/5/1
        id/3/1
        id/5/2
        id/3/2
        id/5/3
        id/3/3
        id/5/4
        id/3/4
        us/0/0/4
        us/0/0/12
        us/0/0/20
        us/0/0/28
        nxx/0/0
        nxx/1/1
        nxx/2/2
        nxx/2/2/10
        nxx/2/2/16
        nxx/2/2/0/2
        nxx/2/3
        nxx/2/3/10
        nxx/2/3/16
        nxx/2/3/0/2
        nxx/3/4
        nxx/3/4/10
        nxx/3/4/16
        nxx/2/4/0/2         
    )
fi

if [ "$round" = 4 ] || [ "$round" = all ]; then
    seqs+=(
        us/0/0/0/2
        us/0/0/0/3          
    )
fi

if [ "$round" = 5 ] || [ "$round" = all ]; then
    seqs+=(
        fh/1/0
        fh/2/0
        sb/2
        sb/5
        sb/8
        sl
        slx
        sh/5
        sh/7
        cb
        cl
        ch/4                
    )
fi

if [ "$round" = 6 ] || [ "$round" = all ]; then
    seqs+=(
        sb/2/bo
        sb/3
        sb/3/mo
        sb/3/bo
        sb/4
        sb/4/wo
        sb/4/mo
        sb/4/bo
        sb/5/mo
        sb/6
        sb/6/mo
        slx/wo
        slx/mx
        sh/4
        sh/4/mx
        sh/4/bx
        sh/5/mx
        sh/5/bxg
        sh/6
        sh/7/wx
        cb/wo
        cb/mo
        cb/bo
        cl/wo
        ch/5
        ch/5/wo
        ch/6
        ch/6/wo             
    )
fi

if [ "$round" = 7 ] || [ "$round" = all ]; then
    seqs+=(
        sb/6/wo
        slx/mo
        slx/bo
        sh/4/wx
        sh/5/wx
        cb/wo2
        cl/mo
        cl/bo               
    )
fi

#if [ "$round" = 8 ] || [ "$round" = all ]; then
#        cb/wo/2
#        cbc/wo/slx/wo
#        cbc/wo/sh/5
#        cbc/wo/sh/7
#        tet/cb/wo
#        3mx/cb/wo           
#fi

if [ "$round" = rb ] || [ "$round" = all ]; then
    seqs+=(
        rb/4/8
        rb/4/7
        rb/4/6
        rb/5/7
        rb/5/6
        rb/6/6
    )
fi

if [ "$round" = rx ] || [ "$round" = all ]; then
    seqs+=(
        rx/2/2
        rx/2/3
        rx/2/4
        rx/2/5
        rx/3/2
        rx/3/3
        rx/3/4
        rx/3/5
        rx/4/2
        rx/4/3
        rx/4/4
        rx/4/5
        rx/5/2
        rx/5/3
        rx/5/4
        rx/5/5
    )
fi

if [ "$round" = rh ] || [ "$round" = all ]; then
    seqs+=(
        rb/6/4
        rb/6/5
        rb/6/6
        rb/7/4
        rb/7/5
        rb/8/4
    )
fi

sgrna_sensor "$@" $seqs
