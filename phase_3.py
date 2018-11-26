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
    user = input("Enter stuff: ")

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
            #given_date = operator + given_date
        elif price_pattern.match(match_expression):
            given_price = int(re.search(priceQuery, match_expression).group(2))

        elif location_pattern.match(match_expression):
            print("location match: " + match_expression)
        elif cat_pattern.match(match_expression):
            print("category match: " + match_expression)
        elif output_pattern.match(match_expression):
            option = re.search(output, match_expression).group(5)
            if option == "full":
                briefOutput = False
                print("briefOutput is False")
            elif option == "brief":
                briefOutput = True
                print("briefOutput is True")
        elif term_pattern.match(match_expression):
            print("term match: " + match_expression)

        else:
            print("Invalid input")


        # if first_exp == True:
        #     result_set = new_set
        #     first_exp = False
        # else:
        #     result_set.intersection(new_set)
        #     if len(result_set) == 0:
        #         print("No results")
        #         break;

        #result_set.intersection(new_set)


#    new_set = search_equal(term_data, user, 'part')

    # testset = greater_than_price(price_data, given_price, None)
    # # testset = less_than_price(price_data, given_price, None)
    # print(testset)


def less_than_price(database, keyword, output_type):
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
#======================================================================================================#
def less_than_date(database, keyword, output_type):
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
#======================================================================================================#
def greater_than_date(database, keyword, output_type):

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
#======================================================================================================#
def greater_than_price(database, keyword, output_type):
    curs = database.cursor()
    keyword += 1
    iter = curs.set_range(((12-len(str(keyword))) * ' ' + str(keyword)).encode("utf-8"))
    res_set = set()
    while iter:
        if int((iter[0].strip()).decode("utf-8")) != keyword:
            print(iter)
            result = iter[1].decode("utf-8").split(',')
            result = result[0]
            res_set.add(result)
        else:
            break
        iter = curs.next()
#======================================================================================================#
def search_loc_cat(database, keyword, type):
    res_set = set()
    keyword = keyword.lower()
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
    keyword = keyword.lower()
    cursor = database.cursor()
    k = cursor.first()

    while k:
        key = str(k[0])
        key = key[2:-1]
        value = str(k[1])
        value = value.split(",")[0][2:-1]
        if type == 'exact':
            if key == keyword.lower():
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


if __name__ == "__main__":
    main()
