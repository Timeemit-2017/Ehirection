listTemp = [0, 1, 2, 3, 4, 5]
temp = listTemp[0]
listTemp[0] = listTemp[-1]
listTemp.insert(1, temp)
listTemp.pop(-1)
print(listTemp)