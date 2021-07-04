from script.Setting import SettingVar
default = SettingVar.keys_default
print(default)
with open("data/settings.txt", "r", encoding="UTF-8") as file:
    description = file.read().split("\n")[1]
with open("data/settings.txt", "w", encoding="UTF-8") as file:
    file.write(str(default) + "\n" + description)
