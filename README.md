About This Project
==================
This project aims to evaluate the NDNS, esp. how the multipath routing and adaptive forwarding
benefit the system:
- select the best name server according the realtime network traffic, related files:
  - results/aggregate-trace-<SUFFIX>.txt
  - graphs/request_delay_trace.awk
  - graphs/data/responses-from-ns-<SUFFIX>.txt
  - graphs/responses_from_ns.py
  - graphs/pdfs/responses-from-ns-<SUFFIX>.pdf
- fast retry after transmission failure to cover the time gap, related files:
  - results/request-delay-trace-<SUFFIX>.txt
  - graphs/request_delay_trace.awk
  - graphs/data/request-delay-<SUFFIX>.txt
  - graphs/delay_distribution.py
  - graphs/pdfs/delay-distribution-<SUFFIX>.{pdf, png}
- request distribution, related files:
  - graphs/data/request-distribution-com-all.txt
  - graphs/request_distribution.awk
  - (non-upload trace) results/time-name-type-sanitized.trace, but the distribution result is above

Note that the <SUFFIX> refers to a string which made up by parameters of the scenario.
For current, the <SUFFIX> is freq400-intv10-stg8, implying that the start request sending frequency is 400 per seconds (frequency=400),
and the frequency increases every 10 seconds (interval=10), until it increase for 8 times (stage=8).

Tools and Libraries
===================
- This project uses the ndnSIM scenario  template (git://github.com/cawka/ndnSIM-scenario-template.git) to seperate the scenarios from ndnSIM
- gawk: gawk is used to analyze the data of tracers of ndnSIM
- py-matplotlib: matplotlib is used to generate graphs

Notice
======
This project works with ndnSIM 1.0 and its corresponding ns-3, since some forwarding strategies are remove in ndnSIM2.
after ndnSIM and ns-3 are downloaded, checking out to the v1 is needed, with commands:
```shell
    git checkout origin/ndnSIM-v1 -b for-ndns
    git checkout origin/master-v1 -b for-ndns
```

Prerequisites
=============

Custom version of NS-3 and specified version of ndnSIM needs to be installed.

The code should also work with the latest version of ndnSIM, but it is not guaranteed.
```shell
    mkdir ns-dev
    cd ns-dev

    git clone git://github.com/cawka/ns-3-dev-ndnSIM.git ns-3
    git checkout origin/ndnSIM-v1 -b for-ndns
    git clone git://github.com/cawka/pybindgen.git pybindgen
    git clone git://github.com/NDN-Routing/ndnSIM.git ns-3/src/ndnSIM
    git checkout origin/master-v1 -b for-ndns
    git clone git://github.com/cawka/ndnSIM-scenario-template.git my-simulations

    cd ns-3
    ./waf configure -d optimized
    ./waf
    sudo ./waf install

    cd ../my-simulations
```
After which you can proceed to compile and run the code

For more information how to install NS-3 and ndnSIM, please refer to http://ndnsim.net website.

Compiling
=========

To configure in optimized mode without logging **(default)**:

    ./waf configure

To configure in optimized mode with scenario logging enabled (logging in NS-3 and ndnSIM modules will still be disabled,
but you can see output from NS_LOG* calls from your scenarios and extensions):

    ./waf configure --logging

To configure in debug mode with all logging enabled

    ./waf configure --debug

If you have installed NS-3 in a non-standard location, you may need to set up ``PKG_CONFIG_PATH`` variable.

Running
=======

Normally, you can run scenarios either directly

    ./build/<scenario_name>

or using waf

    ./waf --run <scenario_name>

If NS-3 is installed in a non-standard location, on some platforms (e.g., Linux) you need to specify ``LD_LIBRARY_PATH`` variable:

    LD_LIBRARY_PATH=/usr/local/lib ./build/<scenario_name>

or

    LD_LIBRARY_PATH=/usr/local/lib ./waf --run <scenario_name>

To run scenario using debugger, use the following command:

    gdb --args ./build/<scenario_name>


Running with visualizer
-----------------------

There are several tricks to run scenarios in visualizer.  Before you can do it, you need to set up environment variables for python to find visualizer module.  The easiest way to do it using the following commands:

    cd ns-dev/ns-3
    ./waf shell

After these command, you will have complete environment to run the vizualizer.

The following will run scenario with visualizer:

    ./waf --run <scenario_name> --vis

or

    PKG_LIBRARY_PATH=/usr/local/lib ./waf --run <scenario_name> --vis

If you want to request automatic node placement, set up additional environment variable:

    NS_VIS_ASSIGN=1 ./waf --run <scenario_name> --vis

or

    PKG_LIBRARY_PATH=/usr/local/lib NS_VIS_ASSIGN=1 ./waf --run <scenario_name> --vis

Available simulations
=====================

<Scenario Name>
---------------

For current, the only available simulation scenario is select-ns.cc, which adopts a very simple topology(4 nodes, 4 links),
to show how the adaptive forwarding choose the best name server (NS).
A tracer is install on the key router to trace how it forward/receive packets;
Another tracer is install on the consumer to trace the delay of sending requests
