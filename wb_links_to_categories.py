links_file = open("wb_links", "r")
categories_file = open("wb_categories", "a")
for link in links_file:
    categories_file.write(link.partition('catalog/')[-1] + "\n")
links_file.close()
categories_file.close()
