#!/bin/bash


# The MIT License (MIT)
#
# Copyright (c) 2016 Maeve Kennedy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#
# This program moves subdirimages files to keep based on the emotion data
# we have available
#

subdirimages=datasets/KDEF

#Files to keep have the full subpath under subdiremotions starting with S
filestokeep=$(find "$subdirimages" -regex '.*\.JPG' | grep -P "[AB][FM]....(S|H[LR])\.JPG")

mkdir -p keep

for file in $filestokeep; do
  echo $file
  # Old without side to side
  regex='[AB][FM]..(..)(S|H[LR]).JPG'
  [[ $(basename $file) =~ $regex ]]
  typen=${BASH_REMATCH[1]}
  echo $typen
  outputname=$(basename "$file")
  outputname=$(echo "$outputname" | awk '{split($0, a, "."); print a[1] }')
  case $typen in
    NE )
    outputname2="$outputname"_0
    ;;
    AN )
    outputname2="$outputname"_1
    ;;
    DI )
    outputname2="$outputname"_3
    ;;
    AF )
    outputname2="$outputname"_4
    ;;
    HA )
    outputname2="$outputname"_5
    ;;
    SA )
    outputname2="$outputname"_6
    ;;
    SU )
    outputname2="$outputname"_7
    ;;
  esac
  cp "$file" keep/"$outputname2".JPG
done

# NE Neutral 0
# AN Angry 1
# DI Disgust 3
# AF Afraid 4
# HA Happy 5
# SA SAD 6
# SU Surprised 7


# 0=neutral, 1=anger, 2=contempt, 3=disgust, 4=fear, 5=happy, 6=sadness, 7=surprise
