class o():
    def __init__(self, index):
        self.index = index
        self.target = 0
    def i(self):
        print(self.index)
    def set(self, t):
        self.target = t

o0 = o(0)
o1 = o(1)
o2 = o(2)
o3 = o(3)
d = {"0": o0, "1": o1, "2": o2, "3": o3}
d["0"].set(3)
print(o0.target)
