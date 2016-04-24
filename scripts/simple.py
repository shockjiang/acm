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
    with open(tracefile) as fin:
        for line in fin:
            line = line.strip()
            rds = line.split()
            if rds[1] == "Node0" and rds[3] == "netDeviceFace://" and rds[4] == "InData":
                # print line
                ys1.append(float(rds[5]))
                xs.append(int(rds[int(0)]))
    yss = [ys1]
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

def group(xs, ys, args):
    group = args.group
    assert len(xs) == len(ys), "len(xs)==%d but len(ys)==%d" %(len(xs), lne(ys))
    assert len(xs) % group == 0, "len(xs)==%d but len(xs) MOD group != 0" %(len(xs))

    offsets = []
    avs = []
    mis = []
    mas = []
    xs2 = range(1, len(xs)/group)
    ths = []
    for i in xs2:
        begin = i * group
        samples = ys[begin:begin+group]
        mi = min(samples)
        ma = max(samples)
        av = float(sum(samples))/len(samples)
        r = (500.0 * i)/(500*i+650.0)
        # print samples, av/100.0, r
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
        th = math.pow(1 - t, 500*i+650)
        if args.cid == 1: #two hops
            th = math.pow(th, 2)
            # print "theory chunk received ratio: ", th
        th = th * r
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
    parser.add_argument("--id", dest="cid", type=int, nargs='?', 
                        help="id to indicate the test case", default=0)
    
    args = parser.parse_args()
    print args
    if os.path.isfile(args.inFile):
        xs, yss = extract(args.inFile)
        xs, yss = group(xs, yss[0], args)
        # draw(xs, yss, args.outFile)
    else:
        print "%s not exist" %(args.inFile)
