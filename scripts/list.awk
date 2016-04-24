#! /usr/bin/env gawk -f

BEGIN {
}
{
    if (false) {
      if ($2 == "Node0" && $3 == "256" && $4 == "netDeviceFace://" && $5 == "InInterests")
        print $6, $0
      if ($2 == "Node0" && $3 == "256" && $4 == "netDeviceFace://" && $5 == "OutData")
        print $6, $0
    }

    if (false) {
      if ($2 == "Node0" && $3 == "256" && $4 == "netDeviceFace://" && $5 == "OutInterests")
        print $0
      if ($2 == "Node0" && $3 == "256" && $4 == "netDeviceFace://" && $5 == "InData")
        print $0
    }

   if (1) {
      if ($2 == "Node2" && $3 == "256" && $4 == "netDeviceFace://" && $5 == "InInterests")
        print $0
      if ($2 == "Node2" && $3 == "257" && $4 == "netDeviceFace://" && $5 == "OutInterests")
        print $0
    }
}
END {
}
