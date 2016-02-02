#!/usr/bin/env make
all: acm-singlehop acm-twohop acm-twopath acm-twolink
debug: acm-twopath

loss=0
load=50
group=20

simple-script=scripts/simple.py
twopath-script=scripts/twopath.py

acm-singlehop: 
	${eval id=0}
	${eval inf=results/l3rate-trace-loss${loss}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-id${id}.pdf}
	python ${simple-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --id ${id}
	open ${outf}

acm-twohop:
	${eval id=1}
	${eval inf=results/l3rate-trace-loss${loss}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-id${id}.pdf}
	python ${simple-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --id ${id}
	open ${outf}

acm-twopath:
	${eval id=2}
	${eval inf=results/l3rate-trace-loss${loss}-load${load}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	python ${twopath-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --load ${load} --id ${id}
	open ${outf}

acm-twolink:
	${eval id=3}
	${eval inf=results/l3rate-trace-loss${loss}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-id${id}.pdf}
	python ${simple-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --id ${id}
	open ${outf}

acm-burst:
	${eval id=4}
	${eval inf=results/l3rate-trace-loss${loss}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-id${id}.pdf}
	python ${simple-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --id ${id}
	open ${outf}


test-${loss}:
	${eval id=2}
	${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	echo ${outf}