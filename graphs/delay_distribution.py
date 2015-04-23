#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

XLABEL = "Timeline (by seconds)"
YLABEL = "Delay (seconds)"
OUT_FILE = 'pdfs/delay-distribution.pdf'
TITLE = "Delay Distibution"
YLIMIT = (-1, 0.5)
LABELS = ["NS-1"]
COLORS = ["#2b83ba", "#abdda4", "#fdae61", "#d7191c", "#ffffbf"]

YLIMIT2 = (-1, -1)

DATASET_NUM = len(LABELS)

#for bar
BAR_WIDTH = 200
#BAR_GAP = 1000

#for line
LINE_STYLE = "o"
LINE_WIDTH = 1

xs = []
ys1 = []
yss = [ys1]

DATA_FILE = "data/request-delay.txt"
lines = open (DATA_FILE, "r").readlines()
for line in lines:
    if line.startswith("#"):
        continue
    items = line.split()
    if len(items) < 2:
        print "the record is wrong: %" %(line)
    xs.append(items[0])
    ys1.append(items[1])

plt.clf()
ax = plt.gca()
if YLIMIT[0] != -1:
    ax.set_ylim(ymin = YLIMIT[0])
if YLIMIT[1] != -1:
    ax.set_ylim(ymax = YLIMIT[1])


plt.title(TITLE)
plt.xlabel(XLABEL)
plt.ylabel(YLABEL)
plt.grid()
ax.yaxis.get_major_formatter().set_powerlimits((0, 1))
for i in range(DATASET_NUM):
    ys = yss[i]
    label = LABELS[i]
    color = COLORS[i]
    l,  = plt.plot(xs, ys, LINE_STYLE, markersize=1, linewidth=LINE_WIDTH, color="#fdae61", label=label)


plt.axhline(y=0.02, xmin=0, xmax=0.90, ls="--", color="r", linewidth=1)
plt.axhline(y=0.11, xmin=0.11, xmax=0.90, ls="--", color="r", linewidth=1)
plt.axhline(y=0.41, xmin=0.44, xmax=0.90, ls="--", color="r", linewidth=1)

plt.text(82, 0.02, r"$RTT_{NS-1}$", fontsize=12, color='r')
plt.text(82, 0.11, r"$RTT_{NS-2}$", fontsize=12, color='r')
plt.text(82, 0.41, r"$RTT_{NS-3}$", fontsize=12, color='r')
plt.savefig(OUT_FILE)
#plt.show()
