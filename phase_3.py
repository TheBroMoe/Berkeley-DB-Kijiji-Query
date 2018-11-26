from bsddb3 import db
import re

# GRAMMAR CHECKS #

alphanumeric = "[0-9a-zA-Z._-]"
numeric = "[0-9]"
date = "(" + numeric * 4 + "/" + numeric * 2 + "/" + numeric * 2 + ")"
datePrefix = "(date)\s*(=|>|<|>=|<=)"
dateQuery = "(" + datePrefix + ")(\s*)(" + date + ")"
price = numeric + "+"
pricePrefix = 'price\s*(=|>|<|>=|<=)'
priceQuery = pricePrefix + "\s*" + "(" + price + ")"
location = alphanumeric + '+'
locationPrefix = 'location\s*='
locationQuery = "(" + locationPrefix + ')(\s*)(' + location + ")"
cat = alphanumeric + "+"
catPrefix = 'cat\s*='
catQuery = "(" + catPrefix + ")(\s*)(" + cat + ")"
term = alphanumeric + "+"
termSuffix = '%'
termQuery = "(" + term + termSuffix + "|" + term + ")"
output = "(output)(\s*)(=)(\s*)(" + alphanumeric + "+)"
expression = dateQuery + "|" + priceQuery + "|" + locationQuery + "|" + catQuery + "|" + output + "|" + termQuery


# MAIN #

def main():
    brief_output = False

    # create databases from idx files
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

    # create patterns for inputs
    date_pattern = re.compile(dateQuery)
    price_pattern = re.compile(priceQuery)
    location_pattern = re.compile(locationQuery)
    cat_pattern = re.compile(catQuery)
    term_pattern = re.compile(termQuery)
    output_pattern = re.compile(output)

    print("Hello :)")
    while True:
        print("===============================================================")
        user = input("Search (enter QUIT to exit): ")

        # end program
        if user == "QUIT":
            print("Goodbye :)")
            # close databases
            date_data.close()
            price_data.close()
            term_data.close()
            ad_data.close()
            return

        user = user.lower()
        result_set = set() # set of (result) ids

        # determine if program is looking at first user input expression
        first_exp = True

        # handle every expression
        for match in re.finditer(expression, user):
            match_expression = match.group(0)
            if output_pattern.match(match_expression):
                option = re.search(output, match_expression).group(5)
                if option == "full":
                    brief_output = False
                    continue
                elif option == "brief":
                    brief_output = True
                    continue

            elif date_pattern.match(match_expression):
                given_date = re.search(dateQuery, match_expression).group(5)
                operator = re.search(dateQuery, match_expression).group(3)
                new_set = set()
                equalset = set()
                if '<' in operator:
                    new_set = less_than_date(date_data, given_date)
                if '>' in operator:
                    new_set = greater_than_date(date_data, given_date)
                if '=' in operator:
                    equalset = search_date_term(date_data, given_date, 'exact')
                new_set = new_set.union(equalset)

            elif price_pattern.match(match_expression):
                given_price = int(re.search(priceQuery, match_expression).group(2))
                operator = (re.search(priceQuery, match_expression).group(1))
                new_set = set()
                equalset = set()
                if '<' in operator:
                    new_set = less_than_price(price_data, given_price)
                if '>' in operator:
                    new_set = greater_than_price(price_data, given_price)
                if '=' in operator:
                    equalset = search_equal_price(price_data, given_price)
                new_set = new_set.union(equalset)

            elif location_pattern.match(match_expression):
                given_loc = re.search(locationQuery, match_expression).group(3)
                new_set = search_loc_cat(ad_data, given_loc, 'location')

            elif cat_pattern.match(match_expression):
                given_cat = re.search(catQuery, match_expression).group(3)
                new_set = search_loc_cat(ad_data, given_cat, 'cat')

            elif term_pattern.match(match_expression):
                given_term = re.search(termQuery, match_expression).group(0)
                type = "part" if given_term[-1] == "%" else "exact"
                if given_term[-1] == "%":
                    given_term = given_term[:-1]
                new_set = search_date_term(term_data,given_term, type)

            else:
                print("Invalid input")

            # if it is the first expression, make it the result set
            if first_exp == True:
                result_set = new_set
                first_exp = False
            else:
                # intersect new_set of ids with result_set to get ads
                #   that adhere to all given expressions
                result_set = result_set.intersection(new_set)

            # if result_set is empty after second expression, there are no results
            if len(result_set) == 0:
                break

        print_out(ad_data, result_set, brief_output)



# FUNCTIONS #

def print_out(database, results, brief):
    # database is the database to look at (ad_data)
    # results is the set of ids for ads that match search
    # brief is True if the output is brief and False if output is full
    curs = database.cursor()

    # return if there are no results
    if len(results) == 0:
        print("\n-----------------")
        print("No results")
        print("-----------------")
        return

    # print the results in readable format
    for result in results:
        print("-----------------") # seperate results

        iter = database.get(result.encode("utf-8"))
        iteration = iter.decode("utf-8")

        print("ID: {}".format(result))

        if not brief:
            date = re.search("(<date>)(.*)(</date>)", iteration).group(2)
            print("Date: {}".format(date))

            location = re.search("(<loc>)(.*)(</loc>)", iteration).group(2)
            print("Location: {}".format(location))

            category = re.search("(<cat>)(.*)(</cat>)", iteration).group(2)
            print("Category: {}".format(category))

        term_ti = re.search("(<ti>)(.*)(</ti>)", iteration).group(2)
        term_ti = re.sub("&amp;", " ", term_ti)
        term_ti = re.sub("&.*?;", "", term_ti)
        term_ti = re.sub("[^0-9a-zA-Z-_]", " ", term_ti)
        print("Title: {}".format(term_ti))

        if not brief:
            term_desc = re.search("(<desc>)(.*)(</desc>)", iteration).group(2).lower()
            term_desc = re.sub("(&quot)|(&apos)|(&amp);", " ", term_desc)
            term_desc = re.sub("&.*?;", " ", term_desc)
            term_desc = re.sub("[^0-9a-zA-Z-_]", " ", term_desc)
            print("Description: {}".format(term_desc))

            price = re.search("(<price>)(.*)(</price>)", iteration).group(2)
            print("Price: {}".format(price))

    print("-----------------")
    print("\nTotal Results: " + str(len(results)))
#======================================================================================================#
def less_than_price(database, keyword):
    # database is the database to be looked at
    # keyword a string
    # returns set of ids of valid ads
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
def less_than_date(database, keyword):
    # database is the database to be looked at
    # keyword is a string
    # returns set of ids of valid ads
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
    # database is the database to be looked at
    # keyword is a string
    # returns set of ids of valid ads
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
def greater_than_price(database, keyword):
    # database is the database to be looked at
    # keyword is a string
    # returns set of ids of valid ads
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
#======================================================================================================#
def search_loc_cat(database, keyword, type):
    # database is the database to be looked at
    # keyword is a string
    # type is a string: 'location' to look for location and 'cat' to look for category
    # returns set of ids of valid ads
    res_set = set()
    cursor = database.cursor()
    k = cursor.first()

    while k:
        if type == 'location':
            location = re.search("(<loc>)(.*)(</loc>)", k[1].decode("utf-8")).group(2)
            if location.lower() == keyword:
                res_set.add(k[0].decode("utf-8"))

        elif type == 'cat':
            category = re.search("(<cat>)(.*)(</cat>)", k[1].decode("utf-8")).group(2)
            if category.lower() == keyword:
                res_set.add(k[0].decode("utf-8"))

        k = cursor.next()

    return res_set
#======================================================================================================#
def search_date_term(database, keyword, type):
    # database is the database to be looked at
    # keyword is a string
    # type is a string: 'exact' or 'part'
    # returns set of ids of valid ads
    res_set = set()
    cursor = database.cursor()
    k = cursor.first()

    while k:
        key = k[0].decode("utf-8")
        value = k[1].decode("utf-8")

        value = value.split(",")[0]
        if type == 'exact':
            if key == keyword:
                res_set.add(value)

        elif type == 'part':
            if key.startswith(keyword):
                res_set.add(value)

        k = cursor.next()

    return res_set
#======================================================================================================#
def search_equal_price(database, keyword):
    # database is the database to be looked at
    # keyword is the key to look for in database
    # returns set of ids of valid ads
    res_set = set()
    cursor = database.cursor()
    k = cursor.set(((12-len(str(keyword))) * ' ' + str(keyword)).encode("utf-8"))

    while k:
        key = k[0].decode("utf-8").strip()

        value = k[1].decode("utf-8")
        value = value.split(",")[0]
        if int(key) == keyword:
            res_set.add(value)

        k = cursor.next()

    return res_set


if __name__ == "__main__":
    main()
