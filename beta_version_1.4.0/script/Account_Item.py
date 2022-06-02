
# 存储在存档中的物品类
class Account_Item():
    def __init__(self, id, number, ITEMS):
        self.id = id
        self.number = number
        self.item = ITEMS.get_item(self.id)
        self.img = self.item.img
        self.quality = self.item.quality
        self.type = self.item.type
        self.name = self.item.name

    # def update_old(self):
    #     if self.type == "material" or self.type == "effect_m" or self.type == "noneffect_m":
    #         if self.number <= 0:
    #             self.remove()
    #         elif self.number >= 99:
    #             self.number = 99
    #     else:
    #         self.number = 1

    def update(self, GameVar):
        if self.number <= 0:
            self.remove(GameVar)
        elif self.number >= 99:
            self.number = 99

    def remove(self, GameVar):
        GameVar.backpack.remove(self)