"""
复杂版，且暂不能使用（因为self.his_oppsite里没有“互为相反的操作”的数据）
基本思路：储存操作，撤销时执行相反的操作
bug：无法还原原数据顺序 如：原来[1, 2]，删除“2”[1]，撤销删除[2, 1]
但是我突然想到了一个更简单但是占用更多内存的方法，于是就不修辣哈哈我是傻
"""


class History:
    def __init__(self):
        self.history = []
        self.index = -1
        self.his_oppsite = {}

    def append(self, item):
        if not self.index == len(self.history) - 1:
            self.update()
        if len(item) == 1:
            item = (item[0], [], {})
        elif len(item) == 2:
            if type(item[1]) == list:
                item = (item[0], item[1], {})
            elif type(item[1]) == dict:
                item = (item[0], [], item[1])
        elif len(item) == 3:
            pass
        else:
            raise ValueError
        self.history.append(item)
        self.index += 1

    def load(self):
        return self.history[self.index]

    def pop(self):
        old = self.index
        self.index -= 1
        if self.index < -1:
            self.index = -1
        print(self.index, old)
        return self.his_oppsite[self.history[old][0]], self.history[old][1], self.history[old][2]

    def update(self):
        print(self.history)
        print(self.index)
        if self.index == len(self.history) - 1:
            return
        for i in range(self.index + 1, len(self.history)):
            self.history.pop(self.index + 1)

    def empty(self):
        self.history.clear()

    def undo(self):
        if self.index == -1:
            return
        result = self.pop()
        func_name = result[0].__name__
        args = ""
        for a in result[1]:
            if type(a) == str:
                a = "'" + a + "'"
            args += str(a) + ","
        for k, v in result[2]:
            if type(v) == str:
                v = "'" + v + "'"
            args += k + "=" + str(v) + ","
        print(func_name + "(" + args + ")")
        eval(func_name + "(" + args + ")")



