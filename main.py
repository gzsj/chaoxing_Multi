from widgets.test_u01 import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui
from PyQt5.Qt import QThread
import sys
import basic.login as login
import basic.do_work as dowork
import os
import json

i = 2


def check_path(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.LOGIN_BUTTON.clicked.connect(self.check)
        self.refresh.clicked.connect(self.refresh_act)
        self.phones = {}
        self.users = {}
        self.courses = {}
        self.currents = {}
        self.totals, self.starts, self.deletes = {}, {}, {}

    def init_from_file(self):
        global i
        users = os.listdir('saves')
        for user in users:
            courses = os.listdir(os.path.join('saves', user))
            for course in courses:
                path = os.path.join('saves', user, course)
                with open(os.path.join(path, 'user.json'), 'r') as f:
                    content = json.loads(f.read())
                    phone = content['usernm']
                    name = content['name']
                with open(os.path.join(path, 'course.json'), 'r') as f:
                    content = json.loads(f.read())
                    coursenm = content['coursenm']

                self.add_init(phone, name, coursenm, i)
                i += 1

    def add_init(self, phone, name, course, i):
        i = str(i)
        super(MainWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate

        self.phones[i] = QtWidgets.QLabel(self.gridLayoutWidget)
        self.phones[i].setObjectName(phone)
        self.gridLayout_2.addWidget(self.phones[i], int(i), 0, 1, 1)
        self.phones[i].setText(_translate("MainWindow", phone))

        self.users[i] = QtWidgets.QLabel(self.gridLayoutWidget)
        self.users[i].setObjectName(phone)
        self.gridLayout_2.addWidget(self.users[i], int(i), 2, 1, 1)
        self.users[i].setText(_translate("MainWindow", name))

        self.courses[i] = QtWidgets.QLabel(self.gridLayoutWidget)
        self.courses[i].setObjectName(phone)
        self.gridLayout_2.addWidget(self.courses[i], int(i), 4, 1, 1)
        self.courses[i].setText(_translate("MainWindow", course))

        # self.currents[i] = QtWidgets.QLabel(self.gridLayoutWidget)
        # self.currents[i].setObjectName(phone)
        # self.gridLayout_2.addWidget(self.currents[i], int(i), 6, 1, 1)
        # self.currents[i].setText(_translate("MainWindow", "点击按钮初始化"))
        #
        # self.totals[i] = QtWidgets.QLabel(self.gridLayoutWidget)
        # self.totals[i].setObjectName(phone)
        # self.gridLayout_2.addWidget(self.totals[i], int(i), 8, 1, 1)
        # self.totals[i].setText(_translate("MainWindow", "点击按钮初始化"))

        self.starts[i] = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.starts[i].setObjectName(phone)
        self.gridLayout_2.addWidget(self.starts[i], int(i), 6, 1, 1)
        self.starts[i].setText(_translate("MainWindow", "开始"))
        self.starts[i].clicked.connect(lambda: self.do_work(self.phones[i].text(), self.courses[i].text()))

        # self.deletes[i] = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.deletes[i].setObjectName(phone)
        # self.gridLayout_2.addWidget(self.deletes[i], int(i), 12, 1, 1)
        # self.deletes[i].setText(_translate("MainWindow", "删除"))

    def check(self):
        usernm = self.PHONE_INPUT.text()
        passwd = self.PASSWD_INPUT.text()
        self.getinfo = Add_new_user(usernm, passwd)
        self.getinfo.start()

    def refresh_act(self):
        global i
        d = []
        for item in self.phones:
            a = self.phones[item].text()
            b = self.courses[item].text()
            c = '{};{}'.format(a, b)
            d.append(c)
        users = os.listdir('saves')
        for user in users:
            courses = os.listdir(os.path.join('saves', user))
            for course in courses:
                path = os.path.join('saves', user, course)
                with open(os.path.join(path, 'user.json'), 'r') as f:
                    content = json.loads(f.read())
                    phone = content['usernm']
                    name = content['name']
                with open(os.path.join(path, 'course.json'), 'r') as f:
                    coursenm = json.loads(f.read())['coursenm']
                c = '{};{}'.format(phone, coursenm)
                if c in d:
                    pass
                else:
                    self.add_init(phone, name, coursenm, i)
                    i += 1

    def do_work(self, usernm, coursenm):
        path = os.path.join('saves', usernm)
        folders = os.listdir(path)
        for folder in folders:
            with open(os.path.join(path, folder, 'course.json'), 'r') as f:
                content = json.loads(f.read())
            with open(os.path.join(path, folder, 'user.json'), 'r') as f:
                content2 = json.loads(f.read())
                if content['coursenm'] == coursenm:
                    courseid = content['courseid']
                    passwd = content2['passwd']
                    break
        self.do_staff = Do_Work(usernm, passwd, courseid)
        self.do_staff.start()


class Add_new_user(QThread):  # 线程1
    def __init__(self, usernm, passwd):
        super().__init__()
        self.usernm = usernm
        self.passwd = passwd

    def run(self):
        super().__init__()
        getinfo = login.GetAllInfo(self.usernm, self.passwd)
        phone, name, course = getinfo.login()
        data = '添加完成{};{};{},请点击刷新按钮'.format(phone, name, course)
        print(data)


class Do_Work(QThread):
    def __init__(self, usernm, passwd, courseid):
        super().__init__()
        self.usernm = usernm
        self.passwd = passwd
        self.courseid = courseid

    def run(self):
        super().__init__()
        dowork.Learn_XueXiTong(self.usernm, self.passwd, self.courseid)


check_path('saves')
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
w.init_from_file()
sys.exit(app.exec_())
