#!-*-coding:utf-8 -*-]


def store_links(searchword, res):
    print("Storing...")
    with open("%s.txt" % searchword, "w") as txt:
        for item in res:
            txt.write(item['title']+"\n")
            txt.write(item['link']+"\n")
    print("Storage success!")

