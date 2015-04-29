#! /usr/bin/env gawk -f

BEGIN {
  OutFile = "data/request-distribution" suffix ".txt"
  print "#request", "count" > OutFile
  #data[request] = count
}
{
  #1273795499.895	wustat.windows.com	A
  request = $2 "/" $3
  if (request in data) {
    data[request] += 1
  } else {
    data[request] = 1
  }

}
END {
  n = asort(data)
  hitUpper = 1 - n/FNR
  print "caching hit ratio upper bound: ", hitUpper
  print "#caching hit ratio upper bound:", hitUpper > OutFile
  for (i=n; i >=1; i--) {
    print i, data[i] > OutFile
  }

  print "Done. FNR: ", FNR
  print "InFile:", FILENAME
  print "OutFile:", OutFile
}
