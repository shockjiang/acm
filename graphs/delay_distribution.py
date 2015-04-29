#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import latexify


XLABEL = "Timeline (by seconds)"
YLABEL = "Delay (seconds)"
TITLE = None #"Delay Distibution"
YLIMIT = (None, 0.5)
XLIMIT = (0, 93)
LABELS = ["Delays"]
COLORS = ["#2b83ba", "#abdda4", "#fdae61", "#d7191c", "#ffffbf"]

YLIMIT2 = (None, None)

DATASET_NUM = len(LABELS)

#for bar
BAR_WIDTH = 200
#BAR_GAP = 1000

#for line
LINE_STYLE = "o"
LINE_WIDTH = 1

def run(suffix, fig_size):
    xs = []
    ys1 = []
    yss = [ys1]

    DATA_FILE = "data/request-delay%s.txt" %(suffix)
    OUT_FILE = 'pdfs/delay-distribution%s-%s.pdf' %(suffix, fig_size)
    OUT_FILE2 = 'pdfs/delay-distribution%s-%s.png' %(suffix, fig_size)
    print "load data file %s" %(DATA_FILE)

    cnt = 0
    lines = open (DATA_FILE, "r").readlines()
    for line in lines:
        if line.startswith("#"):
            continue

        cnt += 1
        if cnt % 10 != 1: # too many points leads to long loading delay, here sample 10 percent
            continue

        items = line.split()
        if len(items) < 2:
            print "the record is wrong: %" %(line)
        xs.append(items[0])
        ys1.append(items[1])

    plt.clf()
    ax = plt.gca()
    localVars = dict(locals())
    localVars.update(globals())

    if "YLIMIT" in localVars:
        if YLIMIT[0] != None:
            ax.set_ylim(ymin = YLIMIT[0])
        if YLIMIT[1] != None:
            ax.set_ylim(ymax = YLIMIT[1])

    if "XLIMIT" in localVars:
        if XLIMIT[0] != None:
            ax.set_xlim(xmin = XLIMIT[0])
        if YLIMIT[1] != None:
            ax.set_xlim(xmax = XLIMIT[1])

    if "TITLE" in localVars and TITLE != None:
        plt.title(TITLE)
    if "XLABEL" in localVars and XLABEL != None:
        plt.xlabel(XLABEL)
        print "xlable: ", XLABEL
    if "YLABEL" in localVars and YLABEL != None:
        plt.ylabel(YLABEL)
        print "ylabel:", YLABEL

    plt.grid()

    #ax.yaxis.get_major_formatter().set_powerlimits((0, 1))

    for i in range(DATASET_NUM):
        ys = yss[i]
        label = LABELS[i]
        color = COLORS[i]
        l,  = plt.plot(xs, ys, LINE_STYLE, markersize=0.2, linewidth=LINE_WIDTH, color="#fdae61", label=label)


    plt.axhline(y=0.02, xmin=0, xmax=0.90, ls="--", color="r", linewidth=1)
    plt.axhline(y=0.11, xmin=20.0/100, xmax=0.90, ls="--", color="r", linewidth=1)
    plt.axhline(y=0.41, xmin=50.0/100, xmax=0.90, ls="--", color="r", marker=1, linewidth=1)

    plt.text(2, 0.035, r"$RTT_{NS-1}$", color='r')
    plt.text(2, 0.125, r"$RTT_{NS-2}$", color='r')
    plt.text(28, 0.41, r"$RTT_{NS-3}$", color='r')

    plt.savefig(OUT_FILE2) #the pdf takes long time to load, png is used to debug
    plt.savefig(OUT_FILE)

    print "save figure to %s and %s" %(OUT_FILE, OUT_FILE2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Paramenters')
    parser.add_argument('-s', '--suffix', dest='suffix', type=str, nargs='?',
                        help='suffix to identity the scenaro')
    parser.add_argument("--size", dest="size", type=str, nargs='?',
                        help="the size of output figure")

    args = parser.parse_args()
    print "parameter: suffx=%s size=%s" %(args.suffix, args.size)
    fig_size = "default"
    if args.size in ["s", "small"]:
        latexify.latexify(columns=1)
        fig_size = "small"
    elif args.size in ["b", "big", "l", "large"]:
        latexify.latexify(columns=2)
        fig_size = "large"
    elif args.size in ["t", "tiny"]:
        latexify.latexify(columns=0.67)
        fig_size = "tiny"
    else:
        pass

    run(suffix=args.suffix, fig_size=fig_size)
