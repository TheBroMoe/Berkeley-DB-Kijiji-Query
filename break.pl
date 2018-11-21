#!/usr/bin/perl

while (<STDIN>) {
  chomp;
  if (/^(.*?):(.*?)$/) {
    $key=$1; $rec=$2;
    # BDB treats backslash as a special character, and we would get rid of it!
    $rec =~ s/\\/&92;/g;
    print $key, "\n", $rec, "\n";
  }
}
