import tools

jsonStr = tools.getFromFile("data/bilibili-63629388-34849887.txt")
theDict = tools.jsonDecode(jsonStr)

list1 :list = theDict["user1Fans"]
list2 :list = theDict["user2Fans"]
list1IDs = []
list2IDs = []
for item in list1: list1IDs.append(item["mid"])
for item in list2: list2IDs.append(item["mid"])
commonFanIDs = list(set(list1IDs).intersection(set(list2IDs)))
list1 :list = theDict["user1Follows"]
list2 :list = theDict["user2Follows"]
list1IDs = []
list2IDs = []
for item in list1: list1IDs.append(item["mid"])
for item in list2: list2IDs.append(item["mid"])
commonFollowIDs = list(set(list1IDs).intersection(set(list2IDs)))
print(list(set(commonFanIDs).intersection(set(commonFollowIDs))))
