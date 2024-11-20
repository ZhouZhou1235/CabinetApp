# 数据采集
# 伪装用户构造请求爬取服务器数据

from pythonCode import tools
import requests
import random
requests.packages.urllib3.disable_warnings()

# base 基本 api 爬取的接口 cookies 网站身份验证 imitate 伪装用户 vars 网站参数 out 结果输出
configBase = tools.jsonDecode(tools.getFromFile(tools.findFile("resource/","base.json")))
configApi = tools.jsonDecode(tools.getFromFile(tools.findFile("resource/","api.json")))
configCookies = tools.jsonDecode(tools.getFromFile(tools.findFile("resource/","cookies.json")))
configImitate = tools.jsonDecode(tools.getFromFile(tools.findFile("resource/","imitate.json")))
configVars = tools.jsonDecode(tools.getFromFile(tools.findFile("resource/","vars.json")))
configOut = tools.jsonDecode(tools.getFromFile(tools.findFile("resource/","out.json")))

# 获取B站用户基本信息
def getBiliUserInfo(biliID):
    url = configApi["bili_user"]+f"?mid={biliID}"
    agentList :list = configImitate["userAgents"]
    theAgent = agentList[random.randint(0,len(agentList)-1)]
    head = {"user-agent":theAgent}
    res = requests.get(url,headers=head,verify=False,)
    res.encoding = configBase["APP_ENCODING"]
    return tools.jsonDecode(res.text)

# 获取B站用户粉丝
def getBiliUserFans(biliID,pn=1):
    url = configApi["bili_fans"]+f"?vmid={biliID}&pn={pn}"
    agentList :list = configImitate["userAgents"]
    theAgent = agentList[random.randint(0,len(agentList)-1)]
    head = {"user-agent":theAgent,"Cookie":configCookies["bilibili"]}
    res = requests.get(url,headers=head,verify=False,)
    res.encoding = configBase["APP_ENCODING"]
    return tools.jsonDecode(res.text)

# 获取B站用户关注
def getBiliUserFollows(biliID,pn=1):
    url = configApi["bili_follows"]+f"?vmid={biliID}&pn={pn}"
    agentList :list = configImitate["userAgents"]
    theAgent = agentList[random.randint(0,len(agentList)-1)]
    head = {"user-agent":theAgent,"Cookie":configCookies["bilibili"]}
    res = requests.get(url,headers=head,verify=False,)
    res.encoding = configBase["APP_ENCODING"]
    return tools.jsonDecode(res.text)
