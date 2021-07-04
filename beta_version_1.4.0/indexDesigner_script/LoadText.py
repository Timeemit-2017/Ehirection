import sys
import os

def deleteBlank(thisdata):
    if type(thisdata) is not str:
        raise TypeError
    return thisdata.lstrip().rstrip().replace("\u200b", "").replace("\t", "")


def deleteUselessData(thisdata):
    if deleteBlank(thisdata[-1]) == "}":
        thisdata.pop(-1)
    else:
        raise FileExistsError
    if deleteBlank(thisdata[0]) == "{":
        thisdata.pop(0)
    else:
        raise FileExistsError
    return thisdata


def TidyData(thisdata):
    afterData = []
    for line in thisdata:
        afterData.append(eval(deleteBlank(line)))
    return afterData


class TOT:  # TranslationOfText:
    def __init__(self):
        self.data = {}
        self.dataNum = []

    def init(self, type_in_need):
        direPath = "./indexDesigner_data"
        files = os.listdir(direPath)
        for paths in files:
            with open(direPath + "/" + paths, "r", encoding="UTF-8") as file:
                head = file.readline().split("(")[1].split(")")[0]
                if head == type_in_need:
                    data = file.readlines()
                    data = deleteUselessData(data)
                    data = TidyData(data)
                    print(data)
        for line in data:
            self.data[line[1]] = line[2]
            self.dataNum.insert(line[0], line[2])

    def get(self, orgin, number=None):
        if number is not None and 0 <= number < len(self.dataNum):
            return self.dataNum[number]
        if orgin in self.data:
            return self.data[orgin]
        else:
            return orgin
