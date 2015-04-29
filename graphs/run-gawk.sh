suffix="-freq400-intv10-stg8"
gawk -v suffix="${suffix}" -f aggregate_trace.awk ../results/aggregate-trace${suffix}.txt
gawk -v suffix="${suffix}" -f delay_trace.awk ../results/delay-trace${suffix}.txt
#gawk -v suffix=-com-all -f request_distribution.awk ../results/time-name-type-sanitized.trace
