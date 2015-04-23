#! /usr/bin/env gawk -f
#time(1) face0-InInterests face0-OutInterests face0-DropInterests face0-InNacks  face0-OutNacks face0-DropNacks face0-InData face0-OutData face0-DropData

BEGIN {
  #data(time,face, type)
  OutFile = "data/responses-from-ns.txt"
  MaxTime = 0
}
{
  faceId = $3
  if (faceId == "-1" || faceId == "FaceId" || faceId == "0")
    next

  time = $1
  dataType = $5
  value = $6
  data[time,faceId,dataType] = value
  if (time > MaxTime)
    MaxTime = time
}
END {
  print "#time", "Face1-InData", "Face2-InData", "Face3-InData" > OutFile
  for (i=1; i <= MaxTime; i++) {
    print i, data[i,1,"InData"], data[i,2,"InData"], data[i,3,"InData"] > OutFile
  }
  print "Done. FNR: ", FNR
  print "InFile:", FILENAME
  print "MaxTime:", MaxTime
  print "OutFile:", OutFile
}
