#! /usr/bin/env gawk -f

BEGIN {
  avg = 0
  sqr = 0
  cnt = 0
  values = []
}
{
  print $2
  cnt += 1
  avg += $2
  sqr += $2 * $2

}
END {
  print cnt
  expectation = avg/cnt
  error = 
  variance = sqr/cnt - expectation * expectation

  print expectation, variance
}
