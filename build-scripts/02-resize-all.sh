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


newdir=resized/
olddir=keep/

mkdir -p "$newdir"

cd "$olddir"


imgfiles=$(find . -type f -regextype posix-egrep -regex ".*\.(JPG|png)$"  -printf "%f\n")
echo $imgfiles
cd ..


convertmax=16
converting=0
for imgfile in $imgfiles; do
  echo $imgfile
  if [ $converting -eq 8 ]; then
    converting=0
    wait
  else
    echo $converting
    converting=$((converting+1))
  fi
  convert -resize 256x256\! "$olddir""$imgfile" "$newdir""$imgfile" &
done
