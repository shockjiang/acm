#! /usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

XLABEL = "Timeline (by seconds) or Requests Sending Frequency"
YLABEL = "Load (percentage)"
OUT_FILE = 'pdfs/responses-from-ns.pdf'
TITLE = "Select the Best Name Server (NS)"
YLIMIT = (-1, 1)
LABELS = ["NS-1", "NS-2", "NS-3"]
COLORS = ["#2b83ba", "#abdda4", "#fdae61", "#d7191c", "#ffffbf"]

YLIMIT2 = (-1, -1)

DATASET_NUM = len(LABELS)

#for bar
BAR_WIDTH = 200
#BAR_GAP = 1000

#for line
LINE_STYLE = "o-"
LINE_WIDTH = 1

xs = []
ys1 = []
ys2 = []
ys3 = []
yss = [ys1, ys2, ys3]

DATA_FILE = "data/responses-from-ns.txt"
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
if YLIMIT[0] != -1:
    ax.set_ylim(ymin = YLIMIT[0])
if YLIMIT[1] != -1:
    ax.set_ylim(ymax = YLIMIT[1])

Total = 600.0

plt.title(TITLE)
plt.xlabel(XLABEL)
plt.ylabel(YLABEL)
plt.grid()
for i in range(DATASET_NUM):
    ys = yss[i]
    ys = [float(y)/Total for y in ys]
    label = LABELS[i]
    color = COLORS[i]
    l,  = plt.plot(xs, ys, LINE_STYLE, markersize=3, linewidth=LINE_WIDTH, color=color, label=label)
plt.legend(loc="center left")

ax.yaxis.get_major_formatter().set_powerlimits((0, 100))

el = mpatches.Ellipse((12, 570/Total), 7, 80/Total, alpha=0.2, color="y")
ax.add_artist(el)
el = mpatches.Ellipse((42, 320/Total), 7, 80/Total, alpha=0.2, color="y")
ax.add_artist(el)

ax.annotate("",
            xy=(17, 420/Total), xycoords='data',
            xytext=(15, 0.9), textcoords='data',
            arrowprops=dict(arrowstyle="<-",
                            connectionstyle="arc3"),
            )
ax.annotate("",
            xy=(35, 390/Total), xycoords='data',
            xytext=(40, 350/Total), textcoords='data',
            arrowprops=dict(arrowstyle="<-",
                            connectionstyle="arc3"),
            )
plt.text(17, 400/Total, "NDN Reacts to Load", fontsize=12, bbox=dict(facecolor='y', alpha=0.10))



el = mpatches.Ellipse((16, 55/Total), 7, 80/Total, alpha=0.2, color='r')
plt.gca().add_artist(el)
el = mpatches.Ellipse((44, 20/Total), 7, 80/Total, alpha=0.2, color='r')
ax.add_artist(el)
ax.annotate("",
            xy=(30, 90/Total), xycoords='data',
            xytext=(18, 0.10), textcoords='data',
            arrowprops=dict(arrowstyle="<-",
                            connectionstyle="arc3"),
            )
ax.annotate("",
            xy=(40, 90/Total), xycoords='data',
            xytext=(45, 0.1), textcoords='data',
            arrowprops=dict(arrowstyle="<-",
                            connectionstyle="arc3"),
            )
plt.text(25, 100/Total, "New NS is Selected", fontsize=12, bbox=dict(facecolor='r', alpha=0.10))


plt.savefig(OUT_FILE)
#plt.show()
