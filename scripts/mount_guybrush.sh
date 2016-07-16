#!/usr/bin/env sh

sshfs -o follow_symlinks guybrush:sgrna/addapt/results/ results
sshfs -o follow_symlinks guybrush:sgrna/addapt/figures/ figures
