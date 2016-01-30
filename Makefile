#!/usr/bin/env make
all: chunkloss

script=scripts/chunkloss.py
rawI=/Users/shock/workspaces/ndnSIM/ns-3/results/aggregate-trace-acm.txt
inf=results/aggregate-trace-acm.txt
outf=figures/chunkloss.pdf
chunkloss:${inf1}
	cp ${rawI} ${inf}
	python ${script} -i ${inf} -o ${outf}
