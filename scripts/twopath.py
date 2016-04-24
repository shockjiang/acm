#! /usr/bin/env python
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import sys
import os.path
import latexify
latexify.latexify(columns=1)

def offsetLogger(offsets, args, outf="results/offset-stat.txt"):
    with open(outf, "a") as of:
        for offset in offsets:
            of.write("%s %f\n" %(args.outFile, offset))
    of.close()

def extract(tracefile):
    yss = []
    xs = []
    ys1 = []
    ys2 = []
    with open(tracefile) as fin:
        for line in fin:
            line = line.strip()
            rds = line.split()
            if rds[1] == "Node0" and rds[2] == "257" and rds[4] == "InData":
                # print line
                ys1.append(float(rds[5]))
                xs.append(int(rds[int(0)]))
            elif rds[1] == "Node0" and rds[2] == "256" and rds[4] == "InData":
                ys2.append(float(rds[5]))
    yss = [ys1, ys2]
    return xs, yss

def draw(xs, yss, of, **kwargs):
    plt.clf()
    ax = plt.gca()
    ax.set_xlim(xmin=0, xmax=8500)
    ax.set_ylim(ymin=0, ymax=1)
    
    colors = kwargs.get("colors", ["#2b83ba", "#abdda4", "#fdae61", "#d7191c", "#ffffbf"])
    labels = kwargs.get("labels", ["Data-"+str(i) for i in range(10)])
    plt.grid()
    # ax.yaxis.get_major_formatter().set_scientific(True)
    # ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
    ax.xaxis.get_major_formatter().set_scientific(True)
    ax.xaxis.get_major_formatter().set_powerlimits((0, 1))
    ax.xaxis.get_major_formatter().set_useOffset(True)

    plt.xlabel("Payload Size")
    plt.ylabel("G2T Ratio")
    bar_width = 250
    l = plt.bar([x-bar_width/2 for x in xs], yss[0], yerr=[yss[1], yss[2]], 
        width=bar_width, color="#4daf4a", ecolor="#ff7f00", label="Simulation")
    plt.plot(xs, yss[3], "-", linewidth=1.0, color="#e41a1c", label="Model")
    print yss[3]
    plt.legend(loc=kwargs.get("legend","upper left"))
    plt.savefig(of)
    plt.show()

def group(xs, yss, args):
    group = args.group
    assert len(xs) == len(yss[0]), "len(xs)==%d but len(ys[0])==%d" %(len(xs), lne(yss[0]))
    assert len(xs) == len(yss[1]), "len(xs)==%d but len(ys[1])==%d" %(len(xs), lne(yss[1]))
    assert len(xs) % group == 0, "len(xs)==%d but len(xs) MOD group != 0" %(len(xs))

    offsets = []
    avs = []
    mis = []
    mas = []
    xs2 = range(1, len(xs)/group)
    ths = []
    for i in xs2:
        begin = i * group
        r = (500.0 * i)/(500*i+650.0)
        ysa = yss[0][begin:begin+group]
        ysb = yss[1][begin:begin+group]
        samples = [ysa[j] + ysb[j] for j in range(group)]
        mi = min(samples)
        ma = max(samples)
        av = float(sum(samples))/len(samples)
        theav = av/100.0*r
        avs.append(theav)
        mis.append((av-mi)/100*r)
        mas.append((ma-av)/100*r)
        if args.loss == 1:
            t = 6.7e-6
        elif args.loss == 3:
            t = 2.0306e-5
        elif args.loss == 5:
            t = 3.4195e-5
        elif args.loss == 10:
            t = 7.02379e-5
        else:
            t = 0
        p1 = math.pow(1 - t, 500*i+650)
        p2 = math.pow(p1, 2)
        th = (p1*args.load + p2*(100-args.load))/100.0 * r

        ths.append(th)
        offset = abs(th - theav)/float(th)
        offsets.append(offset)
    offsetLogger(offsets, args)
    return [x*500 for x in xs2], [avs, mis, mas, ths]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Paramenters')
    parser.add_argument('-i', '--infile', dest='inFile', type=str, nargs='?',
                        help='file path of data in')
    parser.add_argument('-o', '--outfile', dest='outFile', type=str, nargs='?',
                        help='file path of figure out')
    parser.add_argument('-g', "--group", dest="group", type=int, nargs='?', 
                        default=20, help="a integer to group the results")
    parser.add_argument('-l', "--loss", dest="loss", type=float, nargs='?', 
                        default=0, help="a float to indicate the frame loss rate")
    parser.add_argument("--load", dest="load", type=int, nargs='?', 
                        default=50, help="percentage of the load of the first path")
    parser.add_argument("--id", dest="cid", type=int, nargs='?', 
                        help="id to indicate the test case", default=0)

    args = parser.parse_args()
    print args
    if os.path.isfile(args.inFile):
        xs, yss = extract(args.inFile)
        xs, yss = group(xs, yss, args)
        # draw(xs, yss, args.outFile)
    else:
        print "%s not exist" %(args.inFile)
