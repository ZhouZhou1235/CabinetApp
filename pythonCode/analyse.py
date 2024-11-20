# 数据分析

# B站 原始粉丝或关注列表装入
def bili_addUserList(rawList:list,theList:list):
    for item in rawList:
        theList.append({
            "mid":item["mid"],
            "uname":item["uname"],
            "face":item["face"],
            "sign":item["sign"],
        })
    return theList

# B站 根据号码表添加用户
def bili_addToListByID(IDList:list,theList:list):
    outList = []
    for theID in IDList:
        for item in theList:
            if theID==item["mid"]:
                outList.append(item)
                break
    return outList


# B站 分析两用户数据得到共同好友
def bili_analyseRelationDict(theDict:dict):
    user1fans :list = theDict["user1Fans"]
    user2fans :list = theDict["user2Fans"]
    user1fansIDList = []
    user2fansIDList = []
    for item in user1fans: user1fansIDList.append(item["mid"])
    for item in user2fans: user2fansIDList.append(item["mid"])
    commonFansIDList = list(set(user1fansIDList).intersection(set(user2fansIDList)))
    user1follows :list = theDict["user1Follows"]
    user2follows :list = theDict["user2Follows"]
    user1followsIDList = []
    user2followsIDList = []
    for item in user1follows: user1followsIDList.append(item["mid"])
    for item in user2follows: user2followsIDList.append(item["mid"])
    commonFollowsIDList = list(set(user1followsIDList).intersection(set(user2followsIDList)))
    greatFriendsIDList = list(set(commonFansIDList).intersection(set(commonFollowsIDList)))
    return {
        "commonFans":bili_addToListByID(commonFansIDList,user1fans),
        "commonFollows":bili_addToListByID(commonFollowsIDList,user1follows),
        "greatFriends":bili_addToListByID(greatFriendsIDList,user1fans),
    }