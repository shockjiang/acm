finp = "../results/offset-stat.txt"
with open(finp) as fin:
    for line in fin.readlines():
        dt = line.split()
        print dt[1]