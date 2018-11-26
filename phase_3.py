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

brief_output = True


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
output = "(output)(\s*)(=)(\s*)(" + alphanumeric + "+)"
expression = dateQuery + "|" + priceQuery + "|" + locationQuery + "|" + catQuery + "|" + output + "|" + termQuery


def main():

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
    user = input("Enter stuff: ").lower()

    date_pattern = re.compile(dateQuery)
    price_pattern = re.compile(priceQuery)
    location_pattern = re.compile(locationQuery)
    cat_pattern = re.compile(catQuery)
    term_pattern = re.compile(termQuery)
    output_pattern = re.compile(output)
    result_set = set()

    first_exp = True

    for match in re.finditer(expression, user):
        match_expression = match.group(0)
        if date_pattern.match(match_expression):
            given_date = re.search(dateQuery, match_expression).group(5)
            operator = re.search(dateQuery, match_expression).group(3)
            someset = set()
            equalset = set()
            if '<' in operator:
                someset = less_than_date(date_data, given_date)
            if '>' in operator:
                someset = greater_than_date(date_data, given_date)
            if '=' in operator:
                equalset = search_equal(date_data, given_date, 'exact')
            someset = someset.union(equalset)
            print(len(someset))

        elif price_pattern.match(match_expression):
            given_price = int(re.search(priceQuery, match_expression).group(2))
            operator = (re.search(priceQuery, match_expression).group(1))
            someset = set()
            equalset = set()
            if '<' in operator:
                someset = less_than_price(price_data, given_price)
            if '>' in operator:
                someset = greater_than_price(price_data, given_price)
            if '=' in operator:
                equalset = search_equal_price(price_data, given_price)
            someset = someset.union(equalset)
            print(len(someset))


        elif location_pattern.match(match_expression):
            print("location match: " + match_expression)
        elif cat_pattern.match(match_expression):
            print("category match: " + match_expression)
        elif output_pattern.match(match_expression):
            option = re.search(output, match_expression).group(5)
            if option == "full":
                brief_output = False
                print("brief_output is False")
            elif option == "brief":
                brief_output = True
                print("brief_output is True")
        elif term_pattern.match(match_expression):
            print("term match: " + match_expression)

        else:
            print("Invalid input")

def greater_than(database, keyword, output_type):

        if first_exp == True:
            result_set = new_set
            first_exp = False
        else:
            result_set.intersection(new_set)
            if len(result_set) == 0:
                print("No results")


        #result_set.intersection(new_set)



    # testset = greater_than_price(price_data, given_price, None)
    # # testset = less_than_price(price_data, given_price, None)
    # print(testset)

def print_out(database, results, option):
    pass

#======================================================================================================#
def less_than_price(database, keyword):
    curs = database.cursor()
    iter = curs.first()
    res_set = set()

    while iter:
        if int((iter[0].strip()).decode("utf-8")) != keyword:
            result = iter[1].decode("utf-8").split(',')
            result = result[0]
            res_set.add(result)
        else:
            break
        iter = curs.next()
    return res_set
#======================================================================================================

def less_than_date(database, keyword):
    curs = database.cursor()
    iter = curs.first()
    res_set = set()
    while iter:
        if iter[0].decode("utf-8") != keyword:
            result = iter[1].decode("utf-8").split(',')
            result = result[0]
            res_set.add(result)
        else:
            break
        iter = curs.next()
    return res_set
#======================================================================================================
def greater_than_date(database, keyword):

    curs = database.cursor()
    iter = curs.set_range(keyword.encode("utf-8"))
    res_set = set()
    while iter:
        if iter[0].decode("utf-8") != keyword:
            result = iter[1].decode("utf-8").split(',')
            result = result[0]
            res_set.add(result)
        iter = curs.next()

    return res_set
#======================================================================================================
def greater_than_price(database, keyword):
    curs = database.cursor()
    keyword += 1
    iter = curs.set_range(((12-len(str(keyword))) * ' ' + str(keyword)).encode("utf-8"))
    res_set = set()
    while iter:
        if int((iter[0].strip()).decode("utf-8")) != keyword:
            result = iter[1].decode("utf-8").split(',')
            result = result[0]
            res_set.add(result)
        else:
            break
        iter = curs.next()
    return res_set
#======================================================================================================
def search_loc_cat(database, keyword, type):
    res_set = set()
    cursor = database.cursor()
    k = cursor.first()
    while k:
        if type == 'location':
            location = re.search("(<loc>)(.*)(</loc>)", k[1].decode("utf-8")).group(2)
            print(location)
            if location.lower() == keyword:
                res_set.add(k[0].decode("utf-8"))

        elif type == 'cat':
            category = re.search("(<cat>)(.*)(</cat>)", k[1].decode("utf-8")).group(2)
            print(category)
            if category.lower() == keyword:
                res_set.add(k[0].decode("utf-8"))
        k = cursor.next()
        print()
    print(res_set)
    return res_set
#======================================================================================================#
def search_equal(database, keyword, type):
    # database is the database to iterate over
    # keyword is the key to look for in database
    # type is a string: 'exact' or 'part'
    searched = set()
    cursor = database.cursor()
    k = cursor.first()

    while k:
        key = k[0].decode("utf-8")
        print(key)
        value = k[1].decode("utf-8")

        value = value.split(",")[0]
        print(value)
        if type == 'exact':
            if key == keyword:
                searched.add(value)
        elif type == 'part':
            if key.startswith(keyword):
                searched.add(value)
        k = cursor.next()

    if len(searched) == 0:
        print("No elements in searched set")
    else:
        print(searched)

    return searched


#======================================================================================================#
def search_equal_price(database, keyword):
    # database is the database to iterate over
    # keyword is the key to look for in database
    searched = set()
    cursor = database.cursor()
    k = cursor.set(((12-len(str(keyword))) * ' ' + str(keyword)).encode("utf-8"))

    while k:
        key = k[0].decode("utf-8").strip()

        value = k[1].decode("utf-8")
        value = value.split(",")[0]
        if int(key) == keyword:
            searched.add(value)
        k = cursor.next()

    return searched

if __name__ == "__main__":
    main()
