import re
'''
This file includes terms extracted from ad titles and descriptions; for our purpose, suppose a term is a consecutive sequence of alphanumeric,
underscore '_' and dashed '-' characters, i.e [0-9a-zA-Z_-]. The format of the file is as follows: for every termT in the title or the 
description of an ad with id a, there is a row in this file of the form t:a where t is the lowercase form of T. Ignore all special characters 
coded as &#number; such as &#29987; which represents 産 as well as &apos;, &quot; and &amp; which respectively represent ', " and &. Also ignore terms 
of length 2 or less. Convert the terms to all lowercase before writing them out.
'''
def write_terms(path):
    # Read file
    with open(path + '-terms.txt', 'w') as fout:
        with open(path + '.txt', 'r') as fin:
            for line in fin:
                if re.match("<ad>.*</ad>", line):
                    a = re.search("(<aid>)(.*)(</aid>)", line).group(2)

                    term_ti = re.search("(<ti>)(.*)(</ti>)", line).group(2).lower()
                    term_ti = re.sub("&amp;", " ", term_ti)
                    term_ti = re.sub("&.*?;", "", term_ti)
                    term_ti = re.sub("[^0-9a-zA-Z-_]", " ", term_ti)
                    ti_terms = term_ti.split()
                    for term in ti_terms:
                        result = re.search("([0-9a-zA-Z-_]+)", term).group(1)
                        if result is not None and len(result) > 2:
                            fout.write("{}:{}\n".format(result,a))

                    term_desc = re.search("(<desc>)(.*)(</desc>)", line).group(2).lower()
                    term_desc = re.sub("(&quot)|(&apos)|(&amp);", " ", term_desc)
                    term_desc = re.sub("&.*?;", "", term_desc)
                    term_desc = re.sub("[^0-9a-zA-Z-_]", " ", term_desc)
                    desc_terms = term_desc.split()
                    
                    for term in desc_terms:
                        result = re.search("([0-9a-zA-Z-_]+)", term).group(1)
                        if result is not None and len(result) > 2:
                            fout.write("{}:{}\n".format(result,a))

    print("written to " + path + '-terms.txt')

'''
This file includes one line for each ad that has a non-empty price field in the form of p:a,c,l
 where p is a number indicating the price and a, c, and l are respectively the ad id, category and location of the ad.
'''
def write_prices(path):
    # Read file
    with open(path + '-prices.txt', 'w') as fout:
        with open(path + '.txt', 'r') as fin:
            for line in fin:
                if re.match("<ad>.*</ad>", line):
                    p = re.search("(<price>)(.*)(</price>)", line).group(2)
                    p = ' ' * (12 - len(p)) + p
                    print(p)
                    a = re.search("(<aid>)(.*)(</aid>)", line).group(2)
                    c = re.search("(<cat>)(.*)(</cat>)", line).group(2)
                    l = re.search("(<loc>)(.*)(</loc>)", line).group(2)

                    fout.write("{}:{},{},{}\n".format(p,a,c,l))                    
    print("written to " + path + '-prices.txt')

'''
d:a,c,l where d is a non-empty date at which the ad is posted and a, c, and l are respectively the ad id, category and location of the ad.
'''
def write_pdates(path):
    # Read file
    with open(path + '-pdates.txt', 'w') as fout:
        with open(path + '.txt', 'r') as fin:
            for line in fin:
                if re.match("<ad>.*</ad>", line):
                    d = re.search("(<date>)(.*)(</date>)", line).group(2)
                    a = re.search("(<aid>)(.*)(</aid>)", line).group(2)
                    c = re.search("(<cat>)(.*)(</cat>)", line).group(2)
                    l = re.search("(<loc>)(.*)(</loc>)", line).group(2)

                    fout.write("{}:{},{},{}\n".format(d,a,c,l))                    
    print("written to " + path + '-pdates.txt')

'''
This file includes one line for each ad in the form of a:rec where a is the ad id and rec is the full ad record in xml. 
'''
def write_ads(path):
    # Read file
    with open(path + '-ads.txt', 'w') as fout:
        with open(path + '.txt', 'r') as fin:
            for line in fin:
                if re.match("<ad>.*</ad>", line):
                    a = re.search("(<aid>)(.*)(</aid>)", line).group(2)                    
                    fout.write("{}:{}".format(a,line))                    
    print("written to " + path + '-pdates.txt')


def main():
    print("================")
    path = input("enter xml file: ")

    write_terms(path)
    write_pdates(path)
    write_prices(path)
    write_ads(path)
    print("================")


    

if __name__ =='__main__':
    main()