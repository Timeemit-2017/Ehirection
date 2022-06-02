class History:
    def __init__(self):
        self.index = -1
        self.has_save = True
        self.history = []

    def append(self, item):
        """
        添加一个历史记录。

        :param item: 添加的数据。
        """
        self.has_save = False
        self.update()
        self.history.append(item)
        self.index += 1

    def update(self):
        """
        删除已经撤回的数据。
        """
        if self.index == len(self.history) - 1:
            return
        for i in range(self.index + 1, len(self.history)):
            self.history.pop(self.index + 1)

    def empty(self):
        """
        清空历史记录。
        """
        self.history.clear()
        self.index = -1

    def back(self):
        """
        回滚历史记录，但不删除。

        :return: 被撤回的数据。
        """
        old = self.index
        self.index -= 1
        if self.index <= -1:
            self.index = -1
            return
        return self.history[old]

    def forward(self):
        """
        将历史记录向前进一

        :return:前进后指向的数据
        """
        self.index += 1
        if self.index >= len(self.history):
            self.index = len(self.history) - 1
        if self.index == -1:
            return
        return self.load()

    def load(self):
        """
        :return: 当前指向的数据。
        """
        # print(self.history)
        return self.history[self.index]

    def undo(self):
        """
        撤销。

        :return: 撤销后的数据。
        """
        self.has_save = False
        if self.index <= -1:
            return "None"
        self.back()
        return self.load()

    def redo(self):
        self.has_save = False
        if len(self.history) != 0 and self.index != len(self.history) - 1:
            return self.forward()
        return "None"

    def checkIfHasUndo(self):
        return self.index != len(self.history) - 1