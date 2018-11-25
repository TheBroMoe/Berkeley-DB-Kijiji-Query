#!/bin/bash
<<<<<<< HEAD
sort -u 1k-ads.txt -o 1k-ads.txt |cat 1k-ads.txt | perl ./break.pl | db_load -T -t hash ad.idx
sort -u 1k-terms.txt -o 1k-terms.txt | cat 1k-terms.txt | perl ./break.pl | db_load -T -t btree te.idx
sort -u 1k-pdates.txt -o 1k-pdates.txt | cat 1k-pdates.txt | perl ./break.pl | db_load -T -t btree da.idx
sort -u 1k-prices.txt -o 1k-prices.txt | cat 1k-prices.txt | perl ./break.pl | db_load -T -t btree pr.idx
=======
sort -u 1k-ads.txt -o 1k-ads.txt |cat 10-ads.txt | perl ./break.pl | db_load -T -t hash ad.idx
sort -u 1k-terms.txt -o 1k-terms.txt | cat 10-terms.txt | perl ./break.pl | db_load -T -t btree te.idx
sort -u 10-pdates.txt -o 10-pdates.txt | cat 10-pdates.txt | perl ./break.pl | db_load -T -t btree da.idx
sort -u 1k-prices.txt -o 1k-prices.txt | cat 10-prices.txt | perl ./break.pl | db_load -T -t btree pr.idx
>>>>>>> 23ff5f0390ba53800cc2c28c8eb5ca3bfc8f5710
