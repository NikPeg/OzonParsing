links_file = open("kazan_links", "r")
categories_file = open("kazan_categories", "a")
for link in links_file:
    categories_file.write(link.split("/")[-1].split("?")[0] + "\n")
links_file.close()
categories_file.close()
