class Account():
    def __init__(self, fileRoad="data/player.txt"):
        self.fileRoad = fileRoad
        self.get_c = 0
        self.coin = 0
        self.name = "None"
        self.items = []
        self.if_login = False
    def init(self, gameVar):
        gameVar.coin = self.coin
    def login(self, name):
        self.load()
        self.if_login = True
    def register(self,name):
        with open(self.fileRoad, "w", encoding="UTF-8") as file:
            data = {"name": name, "coin": 0}
            file.write(data)
    def load(self, name):
        datas = []
        with open(self.fileRoad, encoding="UTF-8") as file:
            data = file.read()
            data = eval(data)

        self.name = data["name"]
        self.coin = data["coin"]
    def save(self):
        self.coin = GameVar.coin
        with open(self.fileRoad, "w", encoding="UTF-8") as file:
            data = {"name":self.name, "coin":self.coin}
            file.write(data)
        i = 0
        with open("data/settings.txt", "r", encoding="UTF-8") as file:
            lines = file.readlines()
        with open("data/settings.txt", "w", encoding="UTF-8") as file:
            for line in lines:
                if i == 0:
                    line = str(SettingVar.keys) + "\n"
                    file.write(line)
                else:
                    file.write(line)
                i += 1

class Account_Item():
    def __init__(self, id, number):
        self.id = id
        self.number = number
    def get_item(self, idlist):
        return idlist[self.id][0]

def check_login(account):
    if account.login:
        return True
    else:
        account.login()
