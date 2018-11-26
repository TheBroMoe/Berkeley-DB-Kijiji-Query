#!/bin/bash
sort -d -u 1k-ads.txt -o 1k-ads.txt |cat 1k-ads.txt | ./break.pl | db_load -T -t hash ad.idx
sort -d -u 1k-terms.txt -o 1k-terms.txt | cat 1k-terms.txt | ./break.pl | db_load -c duplicates=1 -T -t btree te.idx
sort -d -u 1k-pdates.txt -o 1k-pdates.txt | cat 1k-pdates.txt | ./break.pl | db_load -c duplicates=1 -T -t btree da.idx
sort -d -u 1k-prices.txt -o 1k-prices.txt | cat 1k-prices.txt | ./break.pl | db_load -c duplicates=1 -T -t btree pr.idx
