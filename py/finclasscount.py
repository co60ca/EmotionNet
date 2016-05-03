

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


﻿# given a coutput as a CSV, the program will count the number for each image,
# the expected emotion compared to the actual classification

import csv
from array import *
print 'Enter the file: '
file = raw_input()
matrix = [[0 for x in range(8)] for y in range(8)]
with open(file, 'rb') as csvfile:
	linereader = csv.reader(csvfile, delimiter=',')
	for i, row in enumerate(linereader):
		if ('angry' in row[0].lower()):
			matrix[1][int(row[1])] += 1
		elif ('neutral' in row[0].lower()):
			matrix[0][int(row[1])] += 1
		elif ('contempt' in row[0].lower()):
			matrix[2][int(row[1])] += 1
		elif ('disgust' in row[0].lower()):
			matrix[3][int(row[1])] += 1
		elif ('fear' in row[0].lower()):
			matrix[4][int(row[1])] += 1
		elif ('happy' in row[0].lower()):
			matrix[5][int(row[1])] += 1
		elif ('sad' in row[0].lower()):
			matrix[6][int(row[1])] += 1
		elif ('surprise' in row[0].lower()):
			matrix[7][int(row[1])] += 1
		print matrix
		print '\n'
emotion = ['Neutral', 'Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise']
outfile = open(file+"-output.txt", 'w+')
i = 0
print('\n'.join([''.join(['{:4}'.format(item) for item in row])
    for row in matrix]))

print '\n'

count = 0;
outfile.write (',' + (','.join(str(x) for x in emotion)) + '\n')
for row in matrix:
	outfile.write((emotion[count] + ',' + (','.join(str(x) for x in row)))+'\n')
	count += 1
outfile.close()
