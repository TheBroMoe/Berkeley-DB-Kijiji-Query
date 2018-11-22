#!/bin/bash

sort -u 1k-ads.txt -o 1k-ads.txt
sort -u 1k-terms.txt -o 1k-terms.txt
sort -u 1k-pdates.txt -o 1k-pdates.txt
sort -u 1k-prices.txt -o 1k-prices.txt

cat 1k-ads.txt | ./break.pl | db_load -T -t hash ad.idx
cat 1k-terms.txt | ./break.pl | db_load -T -t btree te.idx
cat 1k-pdates.txt | ./break.pl | db_load -T -t btree da.idx
cat 1k-prices.txt | ./break.pl | db_load -T -t btree pr.idx


