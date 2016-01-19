def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.strip('\r\n') + '\n' + content)


line = open("./Data/1.txt", "r").readline()
decisions = len(line.split(",")) - 3
objectives = 3

header = ",".join(["$" + str(i) for i in xrange(decisions)] + ["$<"+str(i) for i in xrange(objectives)])

from os import listdir
folder = "./Data/"
files = [folder + f for f in listdir(folder)]
for file in files:
    line_prepender(file, header)
