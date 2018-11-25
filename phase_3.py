'''
alphanumeric    ::= [0-9a-zA-Z_-]
numeric		    ::= [0-9]
date            ::= numeric numeric numeric numeric '/' numeric numeric '/' numeric numeric
datePrefix      ::= 'date' whitespace* ('=' | '>' | '<' | '>=' | '<=')
dateQuery       ::= datePrefix whitespace* date
price	      	::= numeric+
pricePrefix     ::= 'price' whitespace* ('=' | '>' | '<' | '>=' | '<=')
priceQuery  	::= pricePrefix whitespace* price
location	    ::= alphanumeric+
locationPrefix  ::= 'location' whitespace* '='
locationQuery	::= locationPrefix whitespace* location
cat	        	::= alphanumeric+
catPrefix   	::= 'cat' whitespace* '='
catQuery	    ::= catPrefix whitespace* cat
term            ::= alphanumeric+
termSuffix      ::= '%'
termQuery       ::= term | term termSuffix
expression      ::= dateQuery | priceQuery | locationQuery | catQuery | termQuery
query           ::= expression (whitespace expression)*

'''
from bsddb3 import db

import re
from bsddb3 import db
briefOutput = True


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
# query = "(?:(" + expression + ")\s?)+"


def main():

    testString = input()
    database = db.DB()
    dbfile = "da.idx"
    database.open(dbfile, None, db.DB_UNKNOWN, db.DB_RDONLY)
    cur = database.cursor()
    user = input("Enter stuff: ")
    result = database.get(b+user)
    print(result)

<<<<<<< HEAD
    # if testString == 'output=full':
    #     briefOutput = False
    #
    # exp = []  # all inputs by the user
=======
    # iter = cur.next()
    # while iter:
    #     print(iter)
    #     iter = cur.next()
>>>>>>> 23ff5f0390ba53800cc2c28c8eb5ca3bfc8f5710
    # for match in re.finditer(expression, testString):
    #     # print(match.group(0))
    #     exp.append(match.group(0))
    #
    # iter = cur.first()
    # while iter:
    #     print(iter)
    #     iter = cur.next()




if __name__ == "__main__":
    main()
