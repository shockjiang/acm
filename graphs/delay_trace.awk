#! /usr/bin/env gawk -f

BEGIN {
  OutFile = "data/request-delay" suffix ".txt"
  print "#time", "FullDelay" > OutFile
}
{
  dataType = $5
  if (dataType != "FullDelay")
    next
  time = $1
  value = $6
  appId = $3
  SeqNo = $4
  print time, value > OutFile
}
END {
  print "Done. FNR: ", FNR
  print "InFile:", FILENAME
  print "OutFile:", OutFile
}
