#!/usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import latexify
latexify.latexify(columns=1)

def load(fn):
    inD = {}
    outI = {}
    t = 0
    with open(fn) as f:
        for line in f:
            dt = line.split()
            # print dt
            # t += 1
            # if t == 30:
            #     break
            if dt[3].startswith("dev=udp"):
                if dt[4] == "OutInterests":
                    outI[int(dt[0])] = int(dt[5])
                elif dt[4] == "InData":
                    inD[int(dt[0])] = int(dt[5])
    assert len(inD) == len(outI), "len(inD)=%d len(outI)=%d" %(len(inD), len(outI))
    keys = inD.keys()
    keys.sort()
    print keys
    t1 = map(lambda x: outI[x], keys)
    t2 = map(lambda x: inD[x], keys)
    return keys, [t1, t2]

def draw(xs, yss, of, **kwargs):
    plt.clf()
    ax = plt.gca()
    if kwargs.get("xlabel"):
        plt.xlabel(kwargs["xlabel"])
    if kwargs.get("ylabel"):
        plt.ylabel(kwargs.get("ylabel"))
    colors = kwargs.get("colors", ["#2b83ba", "#abdda4", "#fdae61", "#d7191c", "#ffffbf"])
    labels = kwargs.get("labels", ["Data-"+str(i) for i in range(10)])
    plt.grid()
    print "xs", xs
    for i in range(len(yss)):
        ys = yss[i]
        print ys
        label = labels[i]
        color = colors[i]
        l, = plt.plot(xs, ys, "-", linewidth=2.0, label=label, color=color)

    plt.legend(loc=kwargs.get("legend","lower right"))
    plt.savefig(of)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Paramenters')
    parser.add_argument('-i', '--infile', dest='inFile', type=str, nargs='?',
                        help='file path of data in')
    parser.add_argument('-o', '--outfile', dest='outFile', type=str, nargs='?',
                        help='file path of figure out')

    args = parser.parse_args()
    print "parameter: InFile=%s OutFile=%s" %(args.inFile, args.outFile)
    xs, yss = load(args.inFile)
    draw(xs, yss,args.outFile)
