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
priceQuery = pricePrefix + "\s*" + "(" + price + ")"
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

    result_set = set()

    for match in re.finditer(expression, user):
        match_expression = match.group(0)
        if date_pattern.match(match_expression):
            given_date = re.search(dateQuery, match_expression).group(5)
            operator = re.search(dateQuery, match_expression).group(3)
            #given_date = operator + given_date
        elif price_pattern.match(match_expression):
            given_price = int(re.search(priceQuery, match_expression).group(2))
            print("price match: " + str(given_price))
        elif location_pattern.match(match_expression):
            print("location match: " + match_expression)
        elif cat_pattern.match(match_expression):
            print("category match: " + match_expression)
        elif term_pattern.match(match_expression):
            print("term match: " + match_expression)
        else:
            print("Invalid input")

        result_set.intersection(new_set)

    new_set = search_equal(term_data, user, 'part')


    # result = date_data.get(user.encode("utf-8"))
    # result = str(result)
    # print(result)
    # print(given_date)
    #result = result[2:-1]
    #result = result.split(",")
    # greater_than_equal(date_data, given_date, None)
    #print("id: " + result[0] + " title: " + result[1])

    greater_than(date_data, given_date, None)
    #search_equal(term_data, user)

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
def greater_than(database, keyword, output_type):
    curs = database.cursor()
    iter = curs.set_range(keyword.encode("utf-8"))
    while iter:
        if iter[0].decode("utf-8") != keyword:
            print(iter[0].decode("utf-8"))
        iter = curs.next()

    return None;
def greater_than_price(database, keyword, output_type):
    curs = database.cursor()
    keyword += 1
    iter = curs.set_range(((12-len(str(keyword))) * ' ' + str(keyword)).encode("utf-8"))

    while iter:
        print(iter[0].strip())
        iter = curs.next()

def search_equal(database, keyword, type):
>>>>>>> 56f1eadae811f2d9eb5cee5caa6840f2024e9b98
    # database is the database to iterate over
    # keyword is the key to look for in database
    # type is a string: 'exact' or 'part'
    searched = set()
    print("***************************************")

    print(keyword)
    keyword = keyword.lower()
    cursor = database.cursor()
    k = cursor.first()

    if type == 'exact':
        while k:
            # print(k) #test
            key = str(k[0])
            key = key[2:-1]
            value = str(k[1])
            value = value.split(",")[0][2:-1]
            if key == keyword.lower():
                searched.add(value)
            k = cursor.next()

    elif type == 'part':
        while k:
            # print(k) #test
            key = str(k[0])
            key = key[2:-1]
            # print(key)
            value = str(k[1])
            value = value.split(",")[0][2:-1]
            # print(keyword)
            if key.startswith(keyword):
                searched.add(value)
            k = cursor.next()

    if len(searched) == 0:
        print("No elements in searched set")
    else:
        print(searched)

    return searched


if __name__ == "__main__":
    main()
