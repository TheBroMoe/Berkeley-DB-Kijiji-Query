'''
alphanumeric    ::= [0-9a-zA-Z_-]
numeric		::= [0-9]
date            ::= numeric numeric numeric numeric '/' numeric numeric '/' numeric numeric
datePrefix      ::= 'date' whitespace* ('=' | '>' | '<' | '>=' | '<=')
dateQuery       ::= datePrefix whitespace* date
price		::= numeric+
pricePrefix     ::= 'price' whitespace* ('=' | '>' | '<' | '>=' | '<=')
priceQuery	::= pricePrefix whitespace* price
location	::= alphanumeric+
locationPrefix  ::= 'location' whitespace* '='
locationQuery	::= locationPrefix whitespace* location
cat		::= alphanumeric+
catPrefix  	::= 'cat' whitespace* '='
catQuery	::= catPrefix whitespace* cat
term            ::= alphanumeric+
termSuffix      ::= '%' 
termQuery       ::= term | term termSuffix
expression      ::= dateQuery | priceQuery | locationQuery | catQuery | termQuery 
query           ::= expression (whitespace expression)*

'''

import re

alphanumeric = "[0-9a-zA-Z_-]"
numeric = "[0-9]"
date = "(" + numeric * 4 + "/" + numeric * 2 + "/" + numeric * 2 + ")"
datePrefix = "date\s*(=|>|<|>=|<=)"
dateQuery = datePrefix + "\s*" + date
price = numeric + "+"
pricePrefix = 'price\s*(=|>|<|>=|<=)'
priceQuery = pricePrefix + "\s*" + price
location = alphanumeric + '+'
locationPrefix = 'location\s*='
locationQuery = locationPrefix + '\s*' + location
cat = alphanumeric + "+"
catPrefix = 'cat\s*='
catQuery = catPrefix + "\s*" + cat
term = alphanumeric + "+"
termSuffix = '%'
termQuery = "(" + term + termSuffix + "|" + term + ")"
expression = dateQuery + "|" + priceQuery + "|" + locationQuery + "|" + catQuery + "|" + termQuery
query = "(\s*" + expression + ")*"





def main():
    testString = input()
    print(re.search(query, testString))


if __name__ == "__main__":
    main()