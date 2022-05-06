import os
from os import listdir


for file_path in listdir("ozon"):
    if os.stat("ozon/" + file_path).st_size == 0:
        os.remove("ozon/" + file_path)
