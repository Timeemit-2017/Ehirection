
boxs = [[[0,0],[1,1],[2,1],[3,1],[3,1]],["2st"]]
class Box():
    def __init__(self,hero,canvas):
        self.hero = hero
        self.canvas = canvas
        self.qua_list = [0,1,2,3]
        self.qua_prob_list = []
    def box_init(self,num):
        self.this_box = boxs[num]
        #print(self.this_box)
        #self.this_box.pop(0)
        self.index_prob = random.randint(0,99)
        self.this_qua = self.qua_prob_list[self.index_prob]
        self.items = []
        for item in self.this_box:
            if item[0] == self.this_qua:
                self.items.append(item[1])
    def set_prob(self,gold,purple,blue,green):
        self.qua_prob_list = []
        if not gold + purple + blue + green == 100:
            return
        prob_list = [gold,purple,blue,green]
        for porb in prob_list:
            porb = porb * 10
        prob_i = 0
        for qua in self.qua_list:
            i = 0
            while i < prob_list[prob_i]:
                self.qua_prob_list.append(qua)
                i += 1
            prob_i += 1
    def summon(self):
        items = Items(self.hero,self.canvas)
        self.real_items = []
        for item_id in self.items:
            self.real_items.append(items.list[item_id][0])
        return self.real_items