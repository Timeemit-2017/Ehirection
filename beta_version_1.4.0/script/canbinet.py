from script.basic import ActivityControlPixel


class CanbinetVar:
    scale = 8
    background_image_path = "images/canbinet/background.png"
    items = []


class Canbinet(ActivityControlPixel):
    def __init__(self, canvas, SIZE):
        ActivityControlPixel.__init__(canvas, SIZE, CanbinetVar.background_image_path, backType=True)

    def loadItems(self):
        with open("data/shop.txt") as file:
            data = file.readlines()
            for i in range(len(data)):
                thisLine = data[i].rstrip()
                if thisLine[0] == "+":  # 一个商品的开头标识
                    thisLine.pop(0)
                    split = thisLine.split(": ")
                    value = split[1]
                    thisItem = {split[0]: value}
                elif thisLine[0] == "-":  # 一个商品的结束标识
                    thisLine.pop(0)
                    split = thisLine.split(": ")
                    value = split[1]
                    thisItem[split[0]] = value
                    CanbinetVar.items.append(Commodity(thisItem["type"], thisItem["id"], thisItem["cost"]))
                else:
                    split = thisLine.split(": ")
                    value = split[1]
                    thisItem[split[0]] = value

    def drawItem(self):
        pass


class Commodity:
    def __init__(self, type, id, cost):
        self.type = type
        self.id = id
        self.cost = cost
