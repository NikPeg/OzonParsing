links_file = open("links", "r")
categories_file = open("categories", "a")
for link in links_file:
    categories_file.write(link.split('/')[-2] + "\n")
links_file.close()
categories_file.close()
