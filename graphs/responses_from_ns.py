#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import latexify


XLABEL = "Timeline (by seconds) or Requests Sending Frequency"
YLABEL = "Load (percentage)"
TITLE = None #"Select the Best Name Server (NS)"
YLIMIT = (None, 1)
LABELS = ["NS-1", "NS-2", "NS-3"]
COLORS = ["#2b83ba", "#abdda4", "#fdae61", "#d7191c", "#ffffbf"]

YLIMIT2 = (None, None)

DATASET_NUM = len(LABELS)

#for bar
BAR_WIDTH = 200
#BAR_GAP = 1000

#for line
LINE_STYLE = "o-"
LINE_WIDTH = 1

def run(suffix, fig_size):
    xs = []
    ys1 = []
    ys2 = []
    ys3 = []
    yss = [ys1, ys2, ys3]

    DATA_FILE = "data/responses-from-ns%s.txt" %(suffix)
    OUT_FILE = 'pdfs/responses-from-ns%s-%s.pdf' %(suffix, fig_size)

    print "load data file %s" %(DATA_FILE)
    lines = open (DATA_FILE, "r").readlines()
    for line in lines:
        if line.startswith("#"):
            continue
        items = line.split()
        if len(items) < 2:
            print "the record is wrong: %" %(line)
        xs.append(items[0])
        ys1.append(items[1])
        if len(items) == 2:
            ys2.append(0)
            ys3.append(0)
        if len(items) == 3:
            ys2.append(items[2])
            ys3.append(0)
        if len(items) == 4:
            ys2.append(items[2])
            ys3.append(items[3])

    plt.clf()
    ax = plt.gca()
    localVars = locals()    
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
    if "YLABEL" in localVars and YLABEL != None:
        plt.ylabel(YLABEL)
    
    
    plt.grid()

    Total = 600.0

    ax.yaxis.get_major_formatter().set_scientific(True)
    ax.yaxis.get_major_formatter().set_powerlimits((0, 1))

    for i in range(DATASET_NUM):
        ys = yss[i]
        ys = [float(y)/Total for y in ys]
        label = LABELS[i]
        color = COLORS[i]
        l,  = plt.plot(xs, ys, LINE_STYLE, markersize=1, linewidth=LINE_WIDTH, color=color, label=label)
    #plt.legend(loc="center left")

    el = mpatches.Ellipse((22, 570/Total), 7, 80/Total, alpha=0.2, color="y")
    ax.add_artist(el)
    el = mpatches.Ellipse((52, 320/Total), 7, 80/Total, alpha=0.2, color="y")
    ax.add_artist(el)

    ax.annotate("",
                xy=(30, 420/Total), xycoords='data',
                xytext=(24, 0.9), textcoords='data',
                arrowprops=dict(arrowstyle="<-",
                                connectionstyle="arc3"),
                )
    ax.annotate("",
                xy=(40, 390/Total), xycoords='data',
                xytext=(50, 350/Total), textcoords='data',
                arrowprops=dict(arrowstyle="<-",
                                connectionstyle="arc3"),
                )
    plt.text(23, 400/Total, "Detect Loss", bbox=dict(facecolor='y', alpha=0.10))



    el = mpatches.Ellipse((23, 55/Total), 7, 80/Total, alpha=0.2, color='b')
    plt.gca().add_artist(el)
    el = mpatches.Ellipse((54, 20/Total), 7, 80/Total, alpha=0.2, color='b')
    ax.add_artist(el)
    ax.annotate("",
                xy=(40, 90/Total), xycoords='data',
                xytext=(25, 0.10), textcoords='data',
                arrowprops=dict(arrowstyle="<-",
                                connectionstyle="arc3"),
                )
    ax.annotate("",
                xy=(50, 90/Total), xycoords='data',
                xytext=(55, 0.1), textcoords='data',
                arrowprops=dict(arrowstyle="<-",
                                connectionstyle="arc3"),
                )
    plt.text(35, 100/Total, "Select NS", bbox=dict(facecolor='b', alpha=0.10))

    plt.text(91, 0.91, "NS-1", color='r')
    plt.text(91, 0.54, "NS-2", color='r')
    plt.text(91, 0.35, "NS-3", color='r')

    plt.savefig(OUT_FILE)
    print "save figure to %s" %(OUT_FILE)
    #plt.show()

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
