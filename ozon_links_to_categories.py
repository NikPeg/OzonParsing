links_file = open("ozon_links", "r")
categories_file = open("ozon_categories", "a")
for link in links_file:
    categories_file.write(link.split('/')[-2] + "\n")
links_file.close()
categories_file.close()
