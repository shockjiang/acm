#!/usr/bin/env make
all: acm-singlehop acm-twohop acm-twopath acm-twolink
debug: acm-twopath

loss=5
load=30
group=20

simple-script=scripts/simple.py
twopath-script=scripts/twopath.py

all: acm-singlehop acm-twohop acm-twopath acm-twolink acm-burst

w-dist:
	${eval id=2}
	${eval loss=5}
	${eval load=30}
	${eval inf=results/l3rate-trace-loss${loss}-load${load}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	python ${twopath-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --load ${load} --id ${id}
	open ${outf}
	
	${eval load=80}
	${eval inf=results/l3rate-trace-loss${loss}-load${load}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	python ${twopath-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --load ${load} --id ${id}
	open ${outf}

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
	${eval load=50}
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

acm-twosouce:
	${eval id=5}
	${eval inf=results/l3rate-trace-loss${loss}-load${load}-id${id}.txt}
	${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	python ${twopath-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --load ${load} --id ${id}
	open ${outf}
	
	#${eval load=80}
	#${eval inf=results/l3rate-trace-loss${loss}-load${load}-id${id}.txt}
	#${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	#python ${twopath-script} -i ${inf} -o ${outf} -g ${group} -l ${loss} --load ${load} --id ${id}
	#open ${outf}


test:
	${eval id=2}
	${eval load=30}
	${eval outf=figures/chunklossrate-loss${loss}-load${load}-id${id}.pdf}
	echo ${outf}
