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

briefOutput = True


alphanumeric = "[0-9a-zA-Z_-]"
numeric = "[0-9]"
date = "(" + numeric * 4 + "/" + numeric * 2 + "/" + numeric * 2 + ")"
datePrefix = "(date)\s*(=|>|<|>=|<=)"
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

    # testString = input()
    date_data = db.DB()
    price_data = db.DB()
    term_data = db.DB()
    ad_data = db.DB()
    dbfile = "da.idx"
    date_data.open(dbfile, None, db.DB_BTREE, db.DB_RDONLY)
    dbfile = "pr.idx"
    price_data.open(dbfile, None, db.DB_BTREE, db.DB_RDONLY)
    dbfile = "te.idx"
    term_data.open(dbfile, None, db.DB_BTREE, db.DB_RDONLY)
    dbfile = "ad.idx"
    ad_data.open(dbfile, None, db.DB_HASH, db.DB_RDONLY)
    cur = date_data.cursor()
    user = input("Enter stuff: ")

    date_pattern = re.compile(dateQuery)
    price_pattern = re.compile(priceQuery)
    location_pattern = re.compile(locationQuery)
    cat_pattern = re.compile(catQuery)
    term_pattern = re.compile(termQuery)

    for match in re.finditer(expression, user):
        match_expression = match.group(0)
        if date_pattern.match(match_expression):
            print("Date match: " + match_expression)
        elif price_pattern.match(match_expression):
            print("price match: " + match_expression)
        elif location_pattern.match(match_expression):
            print("location match: " + match_expression)
        elif cat_pattern.match(match_expression):
            print("category match: " + match_expression)
        elif term_pattern.match(match_expression):
            print("term match: " + match_expression)
        print("=======")

    result = date_data.get(user.encode("utf-8"))
    result = str(result)
    print(result)

    #result = result[2:-1]
    #result = result.split(",")

    #print("id: " + result[0] + " title: " + result[1])

    search_equal(date_data, user, None)
    # print(result[0:])

    # print(str(result[0].decode("utf-8")), result[1], result[2])

    # if testString == 'output=full':
    #     briefOutput = False
    #
    # exp = []  # all inputs by the user

    # iter = cur.next()
    # while iter:
    #     print(iter)
    #     iter = cur.next()
    # for match in re.finditer(expression, user):
    #     print(match.group(0))
    #     exp.append(match.group(0))
    #
    # iter = cur.first()
    # while iter:
    #     print(iter)
    #     iter = cur.next()

def search_equal(database, keyword, output_type):
    # searched = set()
    print("***************************************")

    cursor = database.cursor()
    key = cursor.first()
    while key:
        # key = str(key)[2:-1]
        print(key.key())
        key = cursor.next()


    # for n in database.keys():
    #     n = str(n)
    #     n = n[2:-1]
    #     print(n)

    # return searced


if __name__ == "__main__":
    main()
