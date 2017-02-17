list_0 = [1, 2, 1, 1, 2, 3, 4]
dic = {}
dic_list = []
t = 0


for a,b in zip(list_0, list_0[1:]):
    if a == b:
        dic_list.append(a)

print(dic_list)
