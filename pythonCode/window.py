# 命令窗口

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from pythonCode import collect
from pythonCode import tools
from pythonCode import analyse
import threading

class Window(QWidget):
    def __init__(self,screenWidth,screenHeight):
        super().__init__()
        # 窗口初始化
        self.setWindowTitle(collect.configBase["APP_TITLE"])
        self.setWindowIcon(QtGui.QIcon(collect.configBase["APP_ICON"]))
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.resize(self.screenWidth,self.screenHeight)
        self.panel = QVBoxLayout()
        self.panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.panel)
        # 标志
        appLogo = QLabel()
        logoImage = QtGui.QPixmap(collect.configBase["APP_LOGO"])
        logoImage = logoImage.scaled(
            int(logoImage.width()/2),
            int(logoImage.height()/2),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
        )
        appLogo.setPixmap(logoImage)
        logoPanel = QHBoxLayout()
        tools.addPanelToParent(logoPanel,self.panel)
        logoPanel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logoPanel.addWidget(appLogo)
        # 输入框
        self.inputPanel = QHBoxLayout()
        tools.addPanelToParent(self.inputPanel,self.panel)
        self.inputLine = QLineEdit()
        self.runButton = QPushButton(collect.configBase["APP_runButton"])
        self.runButton.clicked.connect(self.btnDown)
        self.inputPanel.addWidget(self.inputLine)
        self.inputPanel.addWidget(self.runButton)
        # 输出框
        self.outputPanel = QVBoxLayout()
        tools.addPanelToParent(self.outputPanel,self.panel)
        self.outputPanel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.outputInfo = QLabel(collect.configBase["TIP_default"])
        self.outputPanel.addWidget(self.outputInfo)
        # 字体设置
        font = QtGui.QFont()
        font.setPointSize(collect.configBase["APP_fontSize"])
        font.setFamily(collect.configBase["APP_fontFamily"])
        self.setFont(font)
        # 状态管理
        self.running = False
        self.runCountNum = 0
        self.outDict = {}
        self.filename = ""
    # 重置状态
    def resetState(self):
        self.running = False
        self.runCountNum = 0
        self.outDict = {}
        self.filename = ""
        self.outputInfo.setText(collect.configBase["TIP_default"])
        self.runButton.setDisabled(False)
    # 开始运行
    def btnDown(self):
        if self.running==False: self.running=True
        else: return
        success = True
        try:
            inputStr = self.inputLine.text()
            self.outputInfo.setText(collect.configBase["TIP_running"])
            self.runButton.setDisabled(True)
            self.runningToGetData(inputStr)
        except:
            self.running = False
            success = False
            self.resetState()
        finally:
            if success==True: self.inputLine.clear()
            else: QMessageBox.warning(self,collect.configBase["TIP_failed"],collect.configBase["TIP_failed_text"])
    # 爬取数据
    def runningToGetData(self,inputStr:str):
        try:
            inputStrList = inputStr.split(" ")
            commend = inputStrList[0]
            biliID1 = inputStrList[1]
            biliID2 = inputStrList[2]
            # bilibili userID1 userID2
            # 爬取两个B站用户信息然后计算双向共同好友
            if commend==collect.configBase["RUN_bili"]:
                self.filename = f"{commend}-{biliID1}-{biliID2}.txt"
                # 如果收集过则跳过爬取
                pathname = tools.findFile(collect.configBase["APP_SAVE"],self.filename)
                if pathname!=None:
                    self.outDict = tools.jsonDecode(tools.getFromFile(pathname))
                    self.run_bili_collectOK()
                    return
                self.outDict = {
                    "user1":{},
                    "user1Fans":[],
                    "user1Follows":[],
                    "user2":{},
                    "user2Fans":[],
                    "user2Follows":[],
                    "commonFans":[],
                    "commonFollows":[],
                    "greatFriends":[],
                }
                userDict1 = collect.getBiliUserInfo(biliID1)["data"]["card"]
                userDict2 = collect.getBiliUserInfo(biliID2)["data"]["card"]
                self.outDict["user1"]["mid"] = userDict1["mid"]
                self.outDict["user1"]["name"] = userDict1["name"]
                self.outDict["user1"]["face"] = userDict1["face"]
                self.outDict["user1"]["sign"] = userDict1["sign"]
                self.outDict["user2"]["mid"] = userDict2["mid"]
                self.outDict["user2"]["name"] = userDict2["name"]
                self.outDict["user2"]["face"] = userDict2["face"]
                self.outDict["user2"]["sign"] = userDict2["sign"]
                self.run_bili_getFansAndFollows(biliID1,biliID2)
        except RuntimeError as e:
            print("runningToGetData error:",e)
            self.resetState()
            return
    # 两个B站用户分别获取一页的粉丝和关注
    def run_bili_getFansAndFollows(self,biliID1,biliID2):
        print("run_bili_getFansAndFollows")
        self.runCountNum += 1
        try:
            # 完成收集
            if self.runCountNum>collect.configVars["bilibili"]["pn"]:
                self.run_bili_collectOK()
                return
            theTimer = threading.Timer(collect.configBase["APP_runTimer"],self.run_bili_getFansAndFollows,args=(biliID1,biliID2,))
            theTimer.start()
            self.outDict["user1Fans"] = analyse.bili_addUserList(
                collect.getBiliUserFans(biliID1,self.runCountNum)["data"]["list"],
                self.outDict["user1Fans"]
            )
            self.outDict["user1Follows"] = analyse.bili_addUserList(
                collect.getBiliUserFollows(biliID1,self.runCountNum)["data"]["list"],
                self.outDict["user1Follows"]
            )
            self.outDict["user2Fans"] = analyse.bili_addUserList(
                collect.getBiliUserFans(biliID2,self.runCountNum)["data"]["list"],
                self.outDict["user2Fans"]
            )
            self.outDict["user2Follows"] = analyse.bili_addUserList(
                collect.getBiliUserFollows(biliID2,self.runCountNum)["data"]["list"],
                self.outDict["user2Follows"]
            )
        except (RuntimeError,KeyError) as e:
            print("run_bili_getFansAndFollows error:",e)
            theTimer.cancel()
            self.resetState()
            return
    # B站用户数据采集完成
    def run_bili_collectOK(self):
        tmpDict = analyse.bili_analyseRelationDict(self.outDict)
        self.outDict["commonFans"] = tmpDict["commonFans"]
        self.outDict["commonFollows"] = tmpDict["commonFollows"]
        self.outDict["greatFriends"] = tmpDict["greatFriends"]
        tools.saveToFile(collect.configBase["APP_SAVE"]+str(self.filename),tools.jsonEncode(self.outDict))
        tools.renderAndSaveDocs(
            collect.configBase["APP_htmlTemplate"]+collect.configOut["filenames"]["template_biliFriends"],
            collect.configOut["url"]["bili_htmlOut"]+self.filename+".html",
            self.outDict
        )
        self.resetState()
        self.outputInfo.setText(collect.configBase["TIP_success_text"])