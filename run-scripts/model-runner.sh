#!/bin/bash
solver=$1
outputprefix=$2

mkdir -p log
mkdir -p snapshots

caffe train -solver "$solver" 2>&1 | tee log/"$outputprefix"-$(date -Iseconds).log
