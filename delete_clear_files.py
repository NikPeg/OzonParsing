import os
from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir("ozon") if isfile(join("ozon", f))]
for file_path in listdir("ozon"):
    if os.stat("ozon/" + file_path).st_size == 0:
        os.remove("ozon/" + file_path)
