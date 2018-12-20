#!/usr/bin/env zsh

alias same='python -c "import sys; print(sys.argv[1] == sys.argv[2])"'

echo test same
same abc abc

echo test different
same abc def

echo Linear_MS2_sgRNA_Vector-Forward
same gtccacgtctcaagcatttccataggctccgccccc \
     gtccacgtctcaagcatttccataggctccgccccc

echo Linear_MS2_sgRNA_Vector-Reverse
same taccacgtctcatcagaacgccagcaacgcgg \
     taccacgtctcatcagaacgccagcaacgcgg

echo sgRNA_Transcriptional_Unit-Forward-CORR
same taccacgtctcactgaTTGACAGCTAGCTCAGTCCTAGGT \
     taccacgtctcactgaTTGACAGCTAGCTCAGTCCTAGGT

echo sgRNA_Transcriptional_Unit-Reverse-CORR
same gtccacgtctcatgctGTTCACCGACAAACAACAGATAAAACGAAAG \
     gtccacgtctcatgctGTTCACCGACAAACAACAGATAAAACGAAAG





