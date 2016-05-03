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


imgroot=renamed
imagelist=image-listing.txt
imagelisttest=image-listing-test.txt

maxlabel=7

listfiles=$(sort <(find renamed -type f -regextype posix-egrep -regex ".*\.(JPG|png)$"  -printf "%f\n"))

numfiles=$(echo $listfiles | wc -w)

rm "$imagelist" 2> /dev/null
rm "$imagelisttest" 2> /dev/null

count=0
kval=5 # 1/5
echo $numfiles
maxtrain=$((($numfiles * $(($kval-1))) / $kval))

testnow=false

for file in $listfiles; do
  echo $file
  label=$(echo "$file" | grep -Po _[0-9]. | grep -o [0-9])

  if [ $testnow = true ] ; then
    echo "$imgroot"/"$file"" $label" >> "$imagelisttest"
  else
    echo "$imgroot"/"$file"" $label" >> "$imagelist"
  fi

  count=$((count+1))
  if [ $count -eq $maxtrain ] ; then
    testnow=true
  fi
  if [ $count -eq $numfiles ] ; then
    exit 0
  fi
done
