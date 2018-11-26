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
dateQuery = "(" + datePrefix + ")(\s*)(" + date + ")"
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
            given_date = re.search(dateQuery, match_expression).group(5)
            giv_date = re.search(dateQuery, match_expression).group(3)
            print(giv_date)
        elif price_pattern.match(match_expression):
            print("price match: " + match_expression)
        elif location_pattern.match(match_expression):
            print("location match: " + match_expression)
        elif cat_pattern.match(match_expression):
            print("category match: " + match_expression)
        elif term_pattern.match(match_expression):
            print("term match: " + match_expression)


    result = date_data.get(user.encode("utf-8"))
    result = str(result)
    print(result)

    #result = result[2:-1]
    #result = result.split(",")

    #print("id: " + result[0] + " title: " + result[1])

    search_equal(term_data, user, 'exact_term')

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

def search_equal(database, keyword, type):
    # database is the database to iterate over
    # keyword is the key to look for in database
    # type is a string: 'date', 'price', 'exact_term', 'part_term'
    searched = set()
    print("***************************************")

    print(keyword)
    cursor = database.cursor()
    k = cursor.first()

    if type == 'date':
        while k:
            print(k) #test
            key = str(k[0])
            key = key[2:-1]
            print(key) #test
            value = str(k[1])
            value = value.split(",")[0][2:]
            print(value) #test
            if key == keyword:
                searched.add(value)
            k = cursor.next()

    elif type == 'price':
        while k:
            print(k) #test

    elif type == 'exact_term':
        while k:
            # print(k) #test
            key = str(k[0])
            key = key[2:-1]
            # print(key) #test
            value = str(k[1])
            value = value.split(",")[0][2:]
            if key == keyword:
                searched.add(value)

            k = cursor.next()


    if len(searched) == 0:
        print("No elements in searched set")
    else:
        print(searched)
    # print(searched.key())


    # for n in database.keys():
    #     n = str(n)
    #     n = n[2:-1]
    #     print(n)

    # return searced


if __name__ == "__main__":
    main()
