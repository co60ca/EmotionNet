from pathlib import Path
import sys
import re
import csv

from enum import Enum

class ReaderMode(Enum):
    none = 0
    train = 1
    test = 2

def to_csv(filename):
    p = Path(filename)
    if not p.exists() or p.is_dir():
        print("Filename " + filename + " is not a valid file or is a dir")
        return False

    with p.open() as f:
        pattern = re.compile("Starting Optimization")
        # Find the Starting Optimization line
        while True:
            line = f.readline()
            if pattern.search(line) is not None:
                break
        # Find the next iteration or testing
        patterntrain = re.compile("Iteration ([0-9]+), loss = ([0-9e\-\.]+)")
        patterntesting = re.compile("Iteration ([0-9]+), Testing net")
        patternlr = re.compile("Iteration [0-9]+, lr = ([0-9e\-\.]+)")

        # Pattern test/train
        patternto = re.compile("(Train|Test) net output #([0-9]+): (\S+) = ([0-9e\-\.]+)")
        mode = ReaderMode.none
        result = None
        learningrate = 0.01

        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["iteration", "learningrate", "train/testing", "output", "value"])
        while True:
            line = f.readline()
            #print(line)
            if line is "":
                return

            resultstr = patterntrain.search(line)
            if resultstr:
                itera = resultstr.group(1)
                mode = ReaderMode.train
                continue

            resultste = patterntesting.search(line)
            # Testing line
            if resultste:
                itera = resultste.group(1)
                mode = ReaderMode.test
                continue

            resultlr = patternlr.search(line)
            if resultlr:
                learningrate = resultlr.group(1)

            if mode is not ReaderMode.none:
                result = patternto.search(line)
            # Training line
            if result:
                if mode is ReaderMode.train:
                    writer.writerow([itera, learningrate, "train", result.group(3), result.group(4)])
                else:
                    writer.writerow([itera, learningrate, "testing", result.group(3), result.group(4)])

to_csv(sys.argv[1])
