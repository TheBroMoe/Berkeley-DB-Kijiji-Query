#!/bin/bash
sort -u 1k-ads.txt -o 1k-ads.txt |cat 10-ads.txt | perl ./break.pl | db_load -T -t hash ad.idx
sort -u 1k-terms.txt -o 1k-terms.txt | cat 10-terms.txt | perl ./break.pl | db_load -T -t btree te.idx
sort -u 10-pdates.txt -o 10-pdates.txt | cat 10-pdates.txt | perl ./break.pl | db_load -T -t btree da.idx
sort -u 1k-prices.txt -o 1k-prices.txt | cat 10-prices.txt | perl ./break.pl | db_load -T -t btree pr.idx
