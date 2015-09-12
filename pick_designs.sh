#!/usr/bin/env sh

if [ $# = 0 ]; then
    echo "Usage: ./pick_designs.sh <round> [options]"
    exit
else
    round=$1
    shift
fi

if [ "$round" -eq 1 ]; then
    ./show_seqs.py $@       \
        us/0/0              \
        us/0/1              \
        us/0/2              \
        us/0/3              \

elif [ "$round" = 2 ]; then
    ./show_seqs.py $@       \
        us/1/0              \
        us/1/1              \
        us/1/2              \
        us/1/3              \
        us/2/2              \
        us/2/6              \
        us/2/10             \
        us/2/14             \
        us/4/2              \
        us/4/6              \
        us/4/10             \
        us/4/14             \
        ls/5/0              \
        ls/6/0              \
        ls/6/2              \
        ls/6/4              \
        ls/6/6              \
        nx/0                \
        nx/1                \
        nx/2                \
        nx/3                \
        hp/17               \
        hp/18               \
        hp/33               \

elif [ "$round" = 3 ]; then
    ./show_seqs.py $@       \
        id/5/0              \
        id/3/0              \
        id/5/1              \
        id/3/1              \
        id/5/2              \
        id/3/2              \
        id/5/3              \
        id/3/3              \
        id/5/4              \
        id/3/4              \
        us/0/0/4            \
        us/0/0/12           \
        us/0/0/20           \
        us/0/0/28           \
        nxx/0/0             \
        nxx/1/1             \
        nxx/2/2             \
        nxx/2/2/10          \
        nxx/2/2/16          \
        nxx/2/2/0/2         \
        nxx/2/3             \
        nxx/2/3/10          \
        nxx/2/3/16          \
        nxx/2/3/0/2         \
        nxx/3/4             \
        nxx/3/4/10          \
        nxx/3/4/16          \
        nxx/2/4/0/2         \

elif [ "$round" = 4 ]; then
    ./show_seqs.py $@       \
        us/0/0/0/2          \
        us/0/0/0/3          \

else
    echo "Error: round '$round' not yet defined."
fi
