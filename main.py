import re
import time

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWinExtras import QWinTaskbarButton
from app_ui import Ui_GasStation
from reg_success_ui import Ui_RegSuccess
from msg_to_plan_ui import Ui_Dialog
from confirm_del_ui import Ui_ConfirmDel
import sys
from db import GasStationDB
import tools
from datetime import date
from werkzeug.security import generate_password_hash


class App(QtWidgets.QMainWindow, Ui_GasStation):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Gas station")
        self.label_143.setScaledContents(True)
        self.label_143.setPixmap(QtGui.QPixmap("image.webp"))
        self.currentUsername = None
        self.currentRole = None
        self.currentWindow = None
        self.lastWindow = None
        self.currentMonth = None

        self.db = GasStationDB()
        self.message = MessageBox()
        self.confirmDel = ConfirmDel()
        self.msgToPlan = MsgToPlan()

        self.oldUsername = None
        self.oldEmail = None
        self.oldPhone = None
        self.listType = None

        # Добавление масок и прочего для lineEdit`ов
        self.reg_Phone.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{11}")))
        self.reg_Phone.setInputMask("+0 (000) 000 00 00")
        self.reg_Pass_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_Pass2_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_Pass_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cp_OldPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cp_NewPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cp_NewPass2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ci_Phone.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{11}")))
        self.ci_Phone.setInputMask("+0 (000) 000 00 00")
        self.reg_BOD_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{8}")))
        self.reg_BOD_2.setInputMask("00/00/0000")
        self.ci_BOD.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{8}")))
        self.ci_BOD.setInputMask("00/00/0000")
        self.ca_Pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ca_Pass2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ca_Phone.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{11}")))
        self.ca_Phone.setInputMask("+0 (000) 000 00 00")
        self.ca_BOD.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{8}")))
        self.ca_BOD.setInputMask("00/00/0000")
        self.changePP_Price.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,}\.[0-9]{2}")))
        self.buyF_Price.setReadOnly(True)
        self.buyFB_Price.setReadOnly(True)
        self.buyP_Price.setReadOnly(True)
        self.buyPB_Price.setReadOnly(True)

        self.getPlan_Spent.setReadOnly(True)
        self.getPlan_Earn.setReadOnly(True)
        self.getPlan_Revenue.setReadOnly(True)
        self.getPlan_Status.setReadOnly(True)
        self.getPlan_Message.setReadOnly(True)
        self.getPlan_Orders.setReadOnly(True)
        self.getPlan_Purchases.setReadOnly(True)
        self.getPlan_Date.setReadOnly(True)
        self.getPlan_ExpectedRevenue.setReadOnly(True)
        self.getPlan_Date.setInputMask("00/00/0000")

        self.createPlan_Date.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{8}")))
        self.createPlan_Date.setInputMask("00/00/0000")
        self.createPlan_Revenue.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,}\.[0-9]{2}")))

        self.buyF_Balance.setReadOnly(True)
        self.buyFB_Balance.setReadOnly(True)
        self.buyP_Balance.setReadOnly(True)
        self.buyPB_Balance.setReadOnly(True)
        self.buyF_Cost.setReadOnly(True)
        self.buyFB_Cost.setReadOnly(True)
        self.buyP_Cost.setReadOnly(True)
        self.buyPB_Cost.setReadOnly(True)
        self.buyP_TotalCost.setReadOnly(True)
        self.buyPB_TotalCost.setReadOnly(True)
        self.buyFB_Quantity.setValidator(QtGui.QIntValidator(0, 1000))
        self.buyPB_Quantity.setValidator(QtGui.QIntValidator(0, 100))

        # Начальный экран
        self.login.clicked.connect(self.toLogin)
        self.sign_in.clicked.connect(self.toSignIn)

        # Окно входа
        self.login_Enter.clicked.connect(self.loginEnter)
        self.login_toReg_2.clicked.connect(self.loginReg)

        # Окно регистрации
        self.reg_Reg.clicked.connect(self.toReg)
        self.reg_Enter.clicked.connect(self.toLoginFromReg)

        # Окно управляющего
        self.man_ChangePass.clicked.connect(self.changePass)
        self.man_DelAcc.clicked.connect(self.manDelAcc)
        self.man_CreatePlan.clicked.connect(self.createPlan)
        self.man_GetPlan.clicked.connect(self.getPlan)
        self.man_FuelList.clicked.connect(lambda: self.manList(3))
        self.man_ChangePrice.clicked.connect(lambda: self.manChangeProductPrice(True))
        self.man_ChangeInfo.clicked.connect(self.changeInfo)
        self.man_ProductList.clicked.connect(lambda: self.manList(2))
        self.man_AutoProductList.clicked.connect(lambda: self.manList(1))
        self.man_Reg.clicked.connect(self.manReg)

        # Окно закупщика
        self.buyer_BuyFuel.clicked.connect(self.buyerBuyFuel)
        self.buyer_FuelList.clicked.connect(lambda: self.buyerList(3))
        self.buyer_BuyProduct.clicked.connect(self.buyerBuyProduct)
        self.buyer_ChangeInfo.clicked.connect(self.changeInfo)
        self.buyer_ShopHistory.clicked.connect(self.buyerShopHistory)
        self.buyer_ChangePass.clicked.connect(self.changePass)
        self.buyer_ProductList.clicked.connect(lambda: self.buyerList(2))
        self.buyer_AutoProductList.clicked.connect(lambda: self.buyerList(1))

        # Окно клиента
        self.client_DelAcc.clicked.connect(self.clientDelAcc)
        self.client_BuyFuel.clicked.connect(self.clientBuyFuel)
        self.client_ChangePass.clicked.connect(self.changePass)
        self.client_BuyProduct.clicked.connect(self.clientBuyProduct)
        self.client_ChangeInfo.clicked.connect(self.changeInfo)
        self.client_ShopHistory.clicked.connect(self.clientShopHistory)

        # Назад
        self.cp_Back.clicked.connect(self.goBack)
        self.ci_Back.clicked.connect(self.goBack)
        self.BL_Back.clicked.connect(self.goBack)
        self.ML_Back.clicked.connect(self.goBack)
        self.HB_Back.clicked.connect(self.goBack)
        self.HC_Back.clicked.connect(self.goBack)
        self.buyFB_Back.clicked.connect(self.goBack)
        self.buyF_Back.clicked.connect(self.goBack)
        self.buyPB_Back.clicked.connect(self.goBack)
        self.buyP_Back.clicked.connect(self.goBack)
        self.getPlan_Back.clicked.connect(self.goBack)
        self.createPlan_Back.clicked.connect(self.goBack)
        self.del_Back.clicked.connect(self.goBack)
        self.changePP_Back.clicked.connect(self.goBack)
        self.ca_Back.clicked.connect(self.goBack)

        # Выход из аккаунта
        self.man_Exit.clicked.connect(self.exit)
        self.client_Exit.clicked.connect(self.exit)
        self.buyer_Exit.clicked.connect(self.exit)

        # Другие кнопки
        self.cp_button.clicked.connect(self.changePassword)
        self.ci_Ok.clicked.connect(self.changeInformation)
        self.ci_NonOk.clicked.connect(self.returnInfo)
        self.ca_Reg.clicked.connect(self.createBuyerAcc)

        self.confirmDel.pushButton.clicked.connect(self.delAccClient)
        self.confirmDel.pushButton_2.clicked.connect(self.confirmDel.hide)
        self.message.pushButton.clicked.connect(self.message.hide)
        self.msgToPlan.pushButton.clicked.connect(self.writeMsgToPlan)

        self.ML_ChangePrice.clicked.connect(lambda: self.manChangeProductPrice(False))
        self.changePP_Change.clicked.connect(self.changeProductPrice)
        self.buyF_FuelList.currentTextChanged.connect(lambda: self.getPriceFromStock(1))
        self.buyP_ProductList.currentTextChanged.connect(lambda: self.getPriceFromStock(2))
        self.buyP_Type.currentTextChanged.connect(lambda: self.getFilter(True))
        self.buyPB_Type.currentTextChanged.connect(lambda: self.getFilter(False))
        self.buyP_Filter.currentTextChanged.connect(self.getProducts)
        self.buyPB_Filter.currentTextChanged.connect(self.getProductsFromSuppliers)
        self.buyFB_FuelList.currentTextChanged.connect(lambda: self.getSuppliers(True))
        self.buyPB_ProductList.currentTextChanged.connect(lambda: self.getSuppliers(False))
        self.changePP_Type.currentTextChanged.connect(self.changeType)
        self.changePP_ProductList.currentTextChanged.connect(lambda: self.getPriceFromStock(3))
        self.buyFB_SupplierList.currentTextChanged.connect(lambda: self.getPriceFromSuppliers(True))
        self.buyPB_SupplierList.currentTextChanged.connect(lambda: self.getPriceFromSuppliers(False))

        self.buyP_Quantity.textChanged.connect(lambda: self.getCost(False))
        self.buyF_Quantity.textChanged.connect(lambda: self.getCost(True))
        self.buyPB_Quantity.textChanged.connect(lambda: self.getCost(False))
        self.buyFB_Quantity.textChanged.connect(lambda: self.getCost(True))

        self.buyF_Buy.clicked.connect(self.buyFuelByClient)
        self.buyP_Buy.clicked.connect(self.buyProductByClient)
        self.buyP_Add.clicked.connect(lambda: self.addToOrder(True))
        self.buyPB_Add.clicked.connect(lambda: self.addToOrder(False))
        self.buyFB_Buy.clicked.connect(self.buyFuelByBuyer)
        self.buyPB_Buy.clicked.connect(self.buyProductByBuyer)
        self.buyP_DelLast.clicked.connect(lambda: self.deleteLastProduct(True))
        self.buyPB_DelLast.clicked.connect(lambda: self.deleteLastProduct(False))

        self.HC_NumberList.currentTextChanged.connect(lambda: self.changeOrderNumber(True))
        self.HB_NumberList.currentTextChanged.connect(lambda: self.changeOrderNumber(False))

        self.del_Delete.clicked.connect(self.delAccBuyer)

        self.createPlan_Create.clicked.connect(self.creationPlan)
        self.getPlan_NumberPlan.currentTextChanged.connect(self.getCurrentPlan)

        self.ML_Sort.currentTextChanged.connect(lambda: self.sortBy(True))
        self.BL_Sort.currentTextChanged.connect(lambda: self.sortBy(False))

    def toLogin(self):
        self.Main.hide()
        self.Login.show()

    def toSignIn(self):
        self.Main.hide()
        self.Sign_in.show()

    def loginEnter(self):
        match self.db.checkLogin(self.login_Username_2.text(), self.login_Pass_2.text()):
            case 1:
                self.currentUsername = self.login_Username_2.text()
                self.currentRole = 1
                self.login_Username_2.setText("")
                self.login_Pass_2.setText("")
                self.login_ErrMes.setText("")
                self.Login.hide()
                self.currentWindow = self.Manager
                self.Manager.show()
                if str(date.today().day) + str(date.today().month) + str(date.today().year) == tools.changeDateToOutput(
                        self.db.getLastPlanDate()) \
                        and self.db.getPlanByLastDate(self.db.getLastPlanDate())[6] == "Текущий":
                    plan = self.db.getPlanByLastDate(self.db.getLastPlanDate())
                    if float(plan[0]) > float(plan[1]) - float(plan[2]):
                        self.db.updatePlanStatus("Не выполнен", self.db.getLastPlanDate())
                        self.msgToPlan.show()
                    else:
                        self.db.updatePlanStatus("Выполнен", self.db.getLastPlanDate())
                    self.message.label.setText("Сегодня - дата окончания текущего плана.\n"
                                               "Необходимо создать новый план.")
                    self.message.show()
            case 2:
                self.currentUsername = self.login_Username_2.text()
                self.currentRole = 2
                self.login_Username_2.setText("")
                self.login_Pass_2.setText("")
                self.login_ErrMes.setText("")
                self.Login.hide()
                self.currentWindow = self.Buyer
                self.Buyer.show()
                self.buyFB_Balance.setText(str(self.db.getBalance(self.currentUsername, 2)))
                self.buyPB_Balance.setText(str(self.db.getBalance(self.currentUsername, 2)))
            case 3:
                self.currentUsername = self.login_Username_2.text()
                self.currentRole = 3
                self.login_Username_2.setText("")
                self.login_Pass_2.setText("")
                self.login_ErrMes.setText("")
                self.Login.hide()
                self.currentWindow = self.Client
                self.Client.show()
                self.buyF_Balance.setText(str(self.db.getBalance(self.currentUsername, 3)))
                self.buyP_Balance.setText(str(self.db.getBalance(self.currentUsername, 3)))
            case 0:
                self.login_ErrMes.setText("Неправильный логин или пароль")

    def loginReg(self):
        self.Login.hide()
        self.login_Username_2.setText("")
        self.login_Pass_2.setText("")
        self.login_ErrMes.setText("")
        self.Sign_in.show()

    def toReg(self):
        number = "".join(re.findall(r'\d+', self.reg_Phone.text()))
        errorsInfo = tools.checkInfo(self.reg_FN_2.text(), self.reg_SN_2.text(), self.reg_Username.text(),
                                     self.reg_BOD_2.text(), self.reg_Email.text(), number, "", "", "")
        errorsPass = tools.checkPassword(self.reg_Pass_2.text(), self.reg_Pass2_2.text())
        if len(errorsInfo) == 0 and len(errorsPass) == 0:
            self.db.registration(self.reg_FN_2.text(), self.reg_SN_2.text(), number,
                                 self.reg_Email.text(), self.reg_BOD_2.text(), self.reg_Username.text(),
                                 generate_password_hash(self.reg_Pass_2.text()), 3)
            self.Sign_in.hide()
            self.reg_FN_2.setText("")
            self.reg_SN_2.setText("")
            self.reg_Username.setText("")
            self.reg_BOD_2.setText("")
            self.reg_Email.setText("")
            self.reg_Phone.setText("")
            self.reg_Pass_2.setText("")
            self.reg_Pass2_2.setText("")
            self.Login.show()
            self.message.label.setText("Вы успешно зарегестрировались")
            self.message.show()
        else:
            if len(errorsInfo) != 0:
                toMsg = "Ошибка! Некорректный ввод данных: "
                for i in range(len(errorsInfo)):
                    toMsg += errorsInfo[i]
                    if i != len(errorsInfo) - 1:
                        toMsg += ", "
                if len(errorsPass) != 0:
                    toMsg += ".\n"
                    toMsg += "Ошибка! Некорректный ввод пароля: "
                    for i in range(len(errorsPass)):
                        toMsg += errorsPass[i]
                        if i != len(errorsPass) - 1:
                            toMsg += ", "
                    toMsg += "."
                else:
                    toMsg += "."
            else:
                toMsg = "Ошибка! Некорректный ввод пароля: "
                for i in range(len(errorsPass)):
                    toMsg += errorsPass[i]
                    if i != len(errorsPass) - 1:
                        toMsg += ", "
                toMsg += "."
            self.message.label.setText(toMsg)
            self.message.show()

    def toLoginFromReg(self):
        self.Sign_in.hide()
        self.reg_FN_2.setText("")
        self.reg_SN_2.setText("")
        self.reg_Username.setText("")
        self.reg_BOD_2.setText("")
        self.reg_Email.setText("")
        self.reg_Phone.setText("")
        self.reg_Pass_2.setText("")
        self.reg_Pass2_2.setText("")
        self.Login.show()

    def changePass(self):
        self.currentWindow.hide()
        self.lastWindow = self.ChangePassword
        self.lastWindow.show()

    def changeInfo(self):
        self.returnInfo()
        self.currentWindow.hide()
        self.lastWindow = self.ChangeInfo
        self.lastWindow.show()

    def manDelAcc(self):
        self.del_table.clear()
        labels = ["Имя", "Фамилия", "Email", "Username"]
        self.del_table.setColumnCount(len(labels))
        self.del_table.setHorizontalHeaderLabels(labels)
        buyers = self.db.getBuyers()
        for i in range(len(buyers)):
            self.del_table.setRowCount(i + 1)
            self.del_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(buyers[i][0])))
            self.del_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(buyers[i][1])))
            self.del_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(buyers[i][2])))
            self.del_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(buyers[i][3])))
            self.del_UsernameList.addItem(str(buyers[i][3]))
        self.currentWindow.hide()
        self.lastWindow = self.DelAccMan
        self.lastWindow.show()

    def createPlan(self):
        self.createPlan_Revenue.setText("")
        self.createPlan_Date.setText("")
        lastPlan = self.db.getPlanByLastDate(self.db.getLastPlanDate())
        if lastPlan[6] == "Текущий":
            if float(lastPlan[0]) > float(lastPlan[1]) - float(lastPlan[2]):
                self.db.updatePlanStatus("Не выполнен", self.db.getLastPlanDate())
                self.msgToPlan.show()
            else:
                self.db.updatePlanStatus("Не выполнен", self.db.getLastPlanDate())
            self.db.updatePlanLastDate(self.db.getLastPlanDate(), str(date.today().day) + "/"
                                       + str(date.today().month) + "/" + str(date.today().year))
        self.currentWindow.hide()
        self.lastWindow = self.CreatePlan
        self.lastWindow.show()

    def creationPlan(self):
        if tools.checkDate(self.createPlan_Date.text()):
            currentDate = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
            self.db.createPlan(self.db.getId(self.currentUsername, self.currentRole),
                               self.createPlan_Revenue.text(), currentDate, self.createPlan_Date.text())
            self.message.label.setText("План успешно создан")
            self.lastWindow.hide()
            self.currentWindow.show()
        else:
            self.message.label.setText("Ошибка! Некорректная дата")
        self.message.show()

    def getPlan(self):
        self.getPlan_Spent.setText("")
        self.getPlan_Earn.setText("")
        self.getPlan_Revenue.setText("")
        self.getPlan_Status.setText("")
        self.getPlan_Message.setText("")
        self.getPlan_Orders.setText("")
        self.getPlan_Purchases.setText("")
        self.getPlan_ExpectedRevenue.setText("")
        self.getPlan_Date.setText("")
        self.getPlan_NumberPlan.clear()
        plans = self.db.getPlans()
        for i in range(1, len(plans) + 1):
            self.getPlan_NumberPlan.addItem(plans[-i][0])
        self.currentWindow.hide()
        self.lastWindow = self.GetPlan
        self.lastWindow.show()

    def getCurrentPlan(self):
        if self.getPlan_NumberPlan.currentText() != "":
            creationDate = self.getPlan_NumberPlan.currentText()
            plan = self.db.getPlanByCreationDate(creationDate)
            self.getPlan_Spent.setText(str(plan[2]))
            self.getPlan_Earn.setText(str(plan[1]))
            self.getPlan_ExpectedRevenue.setText(str(plan[0]))
            self.getPlan_Status.setText(plan[6])
            self.getPlan_Message.setText(plan[7])
            self.getPlan_Orders.setText(str(plan[3]))
            self.getPlan_Purchases.setText(str(plan[4]))
            self.getPlan_Date.setText(tools.changeDateToOutput(str(plan[5])))
            self.getPlan_Revenue.setText(str(float(plan[1]) - float(plan[2])))

    def writeMsgToPlan(self):
        self.db.updatePlanMessage(self.msgToPlan.lineEdit.text(), self.db.getLastPlanDate())
        self.msgToPlan.hide()

    def manList(self, typeProduct):
        self.ML_Sort.setCurrentText("Алфавиту")
        self.listType = typeProduct
        labels = ["Название", "Количество", "Цена"]
        self.ML_Table.setColumnCount(len(labels))
        self.ML_Table.setHorizontalHeaderLabels(labels)
        products = self.db.getProducts(typeProduct)
        for i in range(self.db.getCountProducts(typeProduct)):
            self.ML_Table.setRowCount(i + 1)
            self.ML_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(products[i][0])))
            self.ML_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(products[i][1])))
            self.ML_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(products[i][2])))
        self.currentWindow.hide()
        self.lastWindow = self.ManagerList
        self.lastWindow.show()

    def sortBy(self, isManager):
        typeProduct = self.listType
        products = None
        if isManager:
            match self.ML_Sort.currentText():
                case "Алфавиту":
                    products = self.db.getProducts(typeProduct)
                case "Алфавиту в обратном порядке":
                    products = self.db.getProductsDesc(typeProduct)
                case "Количеству (по возрастанию)":
                    products = self.db.getProductsByQuantity(typeProduct)
                case "Количеству (по убыванию)":
                    products = self.db.getProductsByQuantityDesc(typeProduct)
            self.ML_Table.clear()
            labels = ["Название", "Количество", "Цена"]
            self.ML_Table.setColumnCount(len(labels))
            self.ML_Table.setHorizontalHeaderLabels(labels)
            for i in range(self.db.getCountProducts(typeProduct)):
                self.ML_Table.setRowCount(i + 1)
                self.ML_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(products[i][0])))
                self.ML_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(products[i][1])))
                self.ML_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(products[i][2])))
        else:
            match self.BL_Sort.currentText():
                case "Алфавиту":
                    products = self.db.getProducts(typeProduct)
                case "Алфавиту в обратном порядке":
                    products = self.db.getProductsDesc(typeProduct)
                case "Количеству (по возрастанию)":
                    products = self.db.getProductsByQuantity(typeProduct)
                case "Количеству (по убыванию)":
                    products = self.db.getProductsByQuantityDesc(typeProduct)
            self.BL_Table.clear()
            labels = ["Название", "Количество", "Цена"]
            self.BL_Table.setColumnCount(len(labels))
            self.BL_Table.setHorizontalHeaderLabels(labels)
            for i in range(self.db.getCountProducts(typeProduct)):
                self.BL_Table.setRowCount(i + 1)
                self.BL_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(products[i][0])))
                self.BL_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(products[i][1])))
                self.BL_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(products[i][2])))

    def manChangeProductPrice(self, isFromMain):
        if isFromMain:
            self.currentWindow.hide()
        else:
            self.lastWindow.hide()
        self.changePP_ProductList.clear()
        products = self.db.getProducts(1)
        for i in products:
            self.changePP_ProductList.addItem(i[0])
        self.changePP_Price.setText(str(self.db.getPrice(products[0][0])))
        self.lastWindow = self.ChangePriceProduct
        self.lastWindow.show()

    def manReg(self):
        self.currentWindow.hide()
        self.lastWindow = self.CreateAcc
        self.lastWindow.show()

    def buyerBuyFuel(self):
        self.buyFB_Cost.setText("0.0")
        self.buyFB_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
        self.buyFB_FuelList.clear()
        products = self.db.getProductNames(3)
        for i in products:
            self.buyFB_FuelList.addItem(i[0])
        suppliers = self.db.getSuppliers(products[0][0])
        self.buyFB_SupplierList.clear()
        for i in suppliers:
            self.buyFB_SupplierList.addItem(i[0])
        self.buyFB_Price.setText(str(self.db.getPriceFromSuppliers(products[0][0], suppliers[0][0])))
        self.currentWindow.hide()
        self.lastWindow = self.BuyFuelBuyer
        self.lastWindow.show()

    def buyerList(self, typeProduct):
        self.listType = typeProduct
        self.BL_Sort.setCurrentText("Алфавиту")
        labels = ["Название", "Количество", "Цена"]
        self.BL_Table.setColumnCount(len(labels))
        self.BL_Table.setHorizontalHeaderLabels(labels)
        products = self.db.getProducts(typeProduct)
        for i in range(self.db.getCountProducts(typeProduct)):
            self.BL_Table.setRowCount(i + 1)
            self.BL_Table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(products[i][0])))
            self.BL_Table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(products[i][1])))
            self.BL_Table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(products[i][2])))
        self.currentWindow.hide()
        self.lastWindow = self.BuyerList
        self.lastWindow.show()

    def buyerBuyProduct(self):
        self.buyPB_Cost.setText("0.0")
        self.buyPB_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
        self.buyPB_TotalCost.setText("0.0")
        self.buyPB_ProductList.clear()
        self.buyPB_Filter.clear()
        self.buyPB_Filter.addItem("Все товары")
        self.buyPB_Filter.addItem("Продукты")
        self.buyPB_Filter.addItem("Напитки")
        products = self.db.getProductNames(2)
        self.buyPB_Price.setText(str(self.db.getPrice(products[0][0])))
        self.currentWindow.hide()
        self.lastWindow = self.BuyProductBuyer
        self.lastWindow.show()

    def buyerShopHistory(self):
        orders = self.db.getPurchases(self.db.getId(self.currentUsername, self.currentRole))
        if len(orders) != 0:
            labels = ["Номер заказа", "Стоимость", "Дата"]
            self.HB_AllOrders.setColumnCount(len(labels))
            self.HB_AllOrders.setHorizontalHeaderLabels(labels)
            for i in range(len(orders)):
                self.HB_AllOrders.setRowCount(i + 1)
                self.HB_AllOrders.setItem(i, 0, QtWidgets.QTableWidgetItem(str(orders[i][0])))
                self.HB_AllOrders.setItem(i, 1, QtWidgets.QTableWidgetItem(str(orders[i][1])))
                self.HB_AllOrders.setItem(i, 2, QtWidgets.QTableWidgetItem(str(orders[i][2])))
                self.HB_NumberList.addItem(str(orders[i][0]))
            labels2 = ["Товар", "Производитель", "Количество", "Стоимость"]
            orderDetails = self.db.getPurchaseDetails(str(orders[0][0]))
            self.HB_OrderDetails.setColumnCount(len(labels2))
            self.HB_OrderDetails.setHorizontalHeaderLabels(labels2)
            for i in range(len(orderDetails)):
                self.HB_OrderDetails.setRowCount(i + 1)
                self.HB_OrderDetails.setItem(i, 0, QtWidgets.QTableWidgetItem(str(orderDetails[i][0])))
                self.HB_OrderDetails.setItem(i, 1, QtWidgets.QTableWidgetItem(str(orderDetails[i][1])))
                self.HB_OrderDetails.setItem(i, 2, QtWidgets.QTableWidgetItem(str(orderDetails[i][2])))
                self.HB_OrderDetails.setItem(i, 3, QtWidgets.QTableWidgetItem(str(orderDetails[i][3])))
            self.currentWindow.hide()
            self.lastWindow = self.HistoryBuyer
            self.lastWindow.show()
        else:
            self.message.label.setText("Вы еще не совершили ни один заказ")
            self.message.show()

    def clientBuyFuel(self):
        self.buyF_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
        self.buyF_FuelList.clear()
        products = self.db.getProductNames(3)
        for i in products:
            self.buyF_FuelList.addItem(i[0])
        self.buyF_Price.setText(str(self.db.getPrice(products[0][0])))
        self.currentWindow.hide()
        self.lastWindow = self.BuyFuelClient
        self.lastWindow.show()

    def clientBuyProduct(self):
        self.buyP_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
        self.buyP_TotalCost.setText("0.0")
        self.buyP_ProductList.clear()
        self.buyP_Filter.clear()
        self.buyP_Filter.addItem("Все товары")
        self.buyP_Filter.addItem("Продукты")
        self.buyP_Filter.addItem("Напитки")
        products = self.db.getProductNames(2)
        self.buyP_Price.setText(str(self.db.getPrice(products[0][0])))
        self.currentWindow.hide()
        self.lastWindow = self.BuyProductClient
        self.lastWindow.show()

    def deleteLastProduct(self, isClient):
        if isClient:
            if self.buyP_TotalCost != "0.0":
                self.buyP_TotalCost.setText(str(float(self.buyP_TotalCost.text()) -
                                                float(self.buyP_Order.item(self.buyP_Order.rowCount() - 1, 3).text())))
                self.buyP_Order.removeRow(self.buyP_Order.rowCount())
                self.buyP_Order.setRowCount(self.buyP_Order.rowCount() - 1)
        else:
            if self.buyPB_TotalCost != "0.0":
                self.buyPB_TotalCost.setText(str(float(self.buyPB_TotalCost.text()) -
                                                 float(
                                                     self.buyPB_Order.item(self.buyPB_Order.rowCount() - 1, 4).text())))
                self.buyPB_Order.removeRow(self.buyPB_Order.rowCount())
                self.buyPB_Order.setRowCount(self.buyPB_Order.rowCount() - 1)

    def clientShopHistory(self):
        orders = self.db.getOrders(self.db.getId(self.currentUsername, self.currentRole))
        if len(orders) != 0:
            labels = ["Номер заказа", "Стоимость", "Дата"]
            self.HC_AllOrders.setColumnCount(len(labels))
            self.HC_AllOrders.setHorizontalHeaderLabels(labels)
            for i in range(len(orders)):
                self.HC_AllOrders.setRowCount(i + 1)
                self.HC_AllOrders.setItem(i, 0, QtWidgets.QTableWidgetItem(str(orders[i][0])))
                self.HC_AllOrders.setItem(i, 1, QtWidgets.QTableWidgetItem(str(orders[i][1])))
                self.HC_AllOrders.setItem(i, 2, QtWidgets.QTableWidgetItem(str(orders[i][2])))
                self.HC_NumberList.addItem(str(orders[i][0]))
            labels2 = ["Товар", "Количество", "Стоимость"]
            orderDetails = self.db.getOrderDetails(str(orders[0][0]))
            self.HC_OrderDetails.setColumnCount(len(labels2))
            self.HC_OrderDetails.setHorizontalHeaderLabels(labels2)
            for i in range(len(orderDetails)):
                self.HC_OrderDetails.setRowCount(i + 1)
                self.HC_OrderDetails.setItem(i, 0, QtWidgets.QTableWidgetItem(str(orderDetails[i][0])))
                self.HC_OrderDetails.setItem(i, 1, QtWidgets.QTableWidgetItem(str(orderDetails[i][1])))
                self.HC_OrderDetails.setItem(i, 2, QtWidgets.QTableWidgetItem(str(orderDetails[i][2])))
            self.currentWindow.hide()
            self.lastWindow = self.HistoryClient
            self.lastWindow.show()
        else:
            self.message.label.setText("Вы еще не совершили ни один заказ")
            self.message.show()

    def clientDelAcc(self):
        self.confirmDel.show()

    def changePassword(self):
        if self.db.checkPassword(self.cp_OldPass.text(), self.currentUsername, self.currentRole):
            errors = tools.checkPassword(self.cp_NewPass.text(), self.cp_NewPass2.text())
            if len(errors) == 0:
                self.db.updatePassword(generate_password_hash(self.cp_NewPass.text()), self.currentUsername,
                                       self.currentRole)
                self.cp_NewPass.setText("")
                self.cp_NewPass2.setText("")
                self.cp_OldPass.setText("")
                self.currentWindow.show()
                self.lastWindow.hide()
                self.message.label.setText("Пароль успешно изменен")
                self.message.show()
                self.label_27.setText("")
            else:
                self.cp_NewPass.setText("")
                self.cp_NewPass2.setText("")
                self.cp_OldPass.setText("")
                toMsg = "Ошибка! Некорректный ввод нового пароля:\n"
                for i in range(len(errors)):
                    toMsg += errors[i]
                    if i != len(errors) - 1:
                        toMsg += ";\n"
                toMsg += "."
                self.message.label.setText(toMsg)
                self.message.show()
        else:
            self.cp_NewPass.setText("")
            self.cp_NewPass2.setText("")
            self.cp_OldPass.setText("")
            self.label_27.setText("Ошибка! Неправильный старый пароль")

    def changeInformation(self):
        number = "".join(re.findall(r'\d+', self.ci_Phone.text()))
        errors = tools.checkInfo(self.ci_FN.text(), self.ci_LN.text(), self.ci_Username.text(), self.ci_BOD.text(),
                                 self.ci_Email.text(), number, self.oldUsername, self.oldEmail, self.oldPhone)
        if len(errors) == 0:
            self.db.updateInfo(self.currentUsername, self.currentRole, self.ci_FN.text(), self.ci_LN.text(),
                               self.ci_Username.text(), self.ci_BOD.text(), self.ci_Email.text(), number)
            self.currentUsername = self.ci_Username.text()
            self.message.label.setText("Информация успешно обновлена")
            self.message.show()
        else:
            toMsg = "Ошибка! Некорректный ввод:\n"
            for i in range(len(errors)):
                toMsg += errors[i]
                if i != len(errors) - 1:
                    toMsg += ";\n"
            toMsg += "."
            self.message.label.setText(toMsg)
            self.message.show()

    def returnInfo(self):
        info = self.db.getInfo(self.currentUsername, self.currentRole)
        self.ci_FN.setText(info[0])
        self.ci_LN.setText(info[1])
        self.ci_Username.setText(self.currentUsername)
        self.ci_BOD.setText(tools.changeDateToOutput(info[4]))
        self.ci_Email.setText(info[3])
        self.ci_Phone.setText(info[2])
        self.oldUsername = self.currentUsername
        self.oldEmail = info[3]
        self.oldPhone = info[2]

    def delAccClient(self):
        self.db.delClient(self.currentUsername)
        self.message.label.setText("Аккаунт успешно удален")
        self.message.show()
        self.confirmDel.hide()
        self.currentWindow.hide()
        self.Main.show()

    def delAccBuyer(self):
        self.db.delBuyer(self.del_UsernameList.currentText())
        self.del_table.clear()
        self.del_UsernameList.clear()
        labels = ["Имя", "Фамилия", "Email", "Username"]
        self.del_table.setColumnCount(len(labels))
        self.del_table.setHorizontalHeaderLabels(labels)
        buyers = self.db.getBuyers()
        for i in range(len(buyers)):
            self.del_table.setRowCount(i + 1)
            self.del_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(buyers[i][0])))
            self.del_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(buyers[i][1])))
            self.del_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(buyers[i][2])))
            self.del_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(buyers[i][3])))
            self.del_UsernameList.addItem(str(buyers[i][3]))
        self.message.label.setText("Аккаунт успешно удален")
        self.message.show()

    def changeProductPrice(self):
        self.db.updatePrice(self.changePP_ProductList.currentText(), self.changePP_Price.text())
        self.message.label.setText("Цена успешно обновлена")
        self.message.show()

    def getFilter(self, isClient):
        if isClient:
            self.buyP_Filter.clear()
            filters = ["Все товары"]
            match self.buyP_Type.currentText():
                case 'Продукты питания':
                    filters.append("Напитки")
                    filters.append("Продукты")
                case 'Автотовары':
                    filters.append("Для легковых автомобилей")
                    filters.append("Для грузовых автомобилей")
            for i in filters:
                self.buyP_Filter.addItem(i)
        else:
            self.buyPB_Filter.clear()
            filters = ["Все товары"]
            match self.buyPB_Type.currentText():
                case 'Продукты питания':
                    filters.append("Напитки")
                    filters.append("Продукты")
                case 'Автотовары':
                    filters.append("Для легковых автомобилей")
                    filters.append("Для грузовых автомобилей")
            for i in filters:
                self.buyPB_Filter.addItem(i)

    def getProducts(self):
        self.buyP_ProductList.clear()
        products = None
        match self.buyP_Type.currentText():
            case 'Продукты питания':
                if self.buyP_Filter.currentText() == 'Все товары':
                    products = self.db.getProductNames(2)
                else:
                    products = self.db.getProductNamesWithFilter(2, self.buyP_Filter.currentText())
            case 'Автотовары':
                if self.buyP_Filter.currentText() == 'Все товары':
                    products = self.db.getProductNames(1)
                else:
                    products = self.db.getProductNamesWithFilter(1, self.buyP_Filter.currentText())
        for i in products:
            self.buyP_ProductList.addItem(i[0])

    def getPriceFromStock(self, tempWindow):
        match tempWindow:
            case 1:
                if self.buyF_FuelList.currentText() != "":
                    self.buyF_Quantity.setText("")
                    quantity = self.db.getQuantity(self.buyF_FuelList.currentText())
                    self.buyF_Quantity.setPlaceholderText("Максимум: " + str(quantity))
                    self.buyF_Quantity.setValidator(QtGui.QIntValidator(0, quantity))
                    self.buyF_Price.setText(str(self.db.getPrice(self.buyF_FuelList.currentText())))
            case 2:
                if self.buyP_ProductList.currentText() != "":
                    self.buyP_Quantity.setText("")
                    quantity = self.db.getQuantity(self.buyP_ProductList.currentText())
                    row = self.buyP_Order.rowCount()
                    for i in range(row):
                        if self.buyP_Order.item(i, 0).text() == self.buyP_ProductList.currentText():
                            quantity -= int(self.buyP_Order.item(i, 2).text())
                            break
                    self.buyP_Quantity.setPlaceholderText("Максимум: " + str(quantity))
                    self.buyP_Quantity.setValidator(QtGui.QIntValidator(0, quantity))
                    self.buyP_Price.setText(str(self.db.getPrice(self.buyP_ProductList.currentText())))
            case 3:
                if self.changePP_ProductList.currentText() != "":
                    self.changePP_Price.setText(str(self.db.getPrice(self.changePP_ProductList.currentText())))

    def getSuppliers(self, isFuelWindow):
        if isFuelWindow:
            self.buyFB_SupplierList.clear()
            suppliers = self.db.getSuppliers(self.buyFB_FuelList.currentText())
            for i in suppliers:
                self.buyFB_SupplierList.addItem(i[0])
        else:
            self.buyPB_SupplierList.clear()
            suppliers = self.db.getSuppliers(self.buyPB_ProductList.currentText())
            for i in suppliers:
                self.buyPB_SupplierList.addItem(i[0])

    def getPriceFromSuppliers(self, isFuelWindow):
        if isFuelWindow:
            if self.buyFB_FuelList.currentText() != "" and self.buyFB_SupplierList.currentText() != "":
                self.buyFB_Quantity.setText("")
                self.buyFB_Quantity.setPlaceholderText("Максимум: 1000")
                self.buyFB_Price.setText(str(self.db.getPriceFromSuppliers(self.buyFB_FuelList.currentText(),
                                                                           self.buyFB_SupplierList.currentText())))
        else:
            if self.buyPB_ProductList.currentText() != "" and self.buyPB_SupplierList.currentText() != "":
                self.buyPB_Quantity.setText("")
                quantity = 100
                row = self.buyPB_Order.rowCount()
                for i in range(row):
                    if self.buyPB_Order.item(i, 0).text() == self.buyPB_ProductList.currentText():
                        quantity = quantity - int(self.buyPB_Order.item(i, 3).text())
                        break
                self.buyPB_Quantity.setPlaceholderText("Максимум: " + str(quantity))
                self.buyPB_Price.setText(str(self.db.getPriceFromSuppliers(self.buyPB_ProductList.currentText(),
                                                                           self.buyPB_SupplierList.currentText())))

    def addToOrder(self, isClient):
        if isClient:
            if self.buyP_Quantity.text() != "" and int(self.buyP_Quantity.text()) != 0 \
                    and int(self.buyP_Quantity.text()) < self.db.getQuantity(self.buyP_ProductList.currentText()):
                labels = ["Товар", "Цена", "Количество", "Итог"]
                self.buyP_Order.setColumnCount(len(labels))
                self.buyP_Order.setHorizontalHeaderLabels(labels)
                row = self.buyP_Order.rowCount()
                self.buyP_Order.setRowCount(row + 1)
                self.buyP_Order.setItem(row, 0, QtWidgets.QTableWidgetItem(self.buyP_ProductList.currentText()))
                self.buyP_Order.setItem(row, 1, QtWidgets.QTableWidgetItem(self.buyP_Price.text()))
                self.buyP_Order.setItem(row, 2, QtWidgets.QTableWidgetItem(self.buyP_Quantity.text()))
                self.buyP_Order.setItem(row, 3, QtWidgets.QTableWidgetItem(self.buyP_Cost.text()))
                self.buyP_TotalCost.setText(str(float(self.buyP_TotalCost.text()) + float(self.buyP_Cost.text())))
                self.updateProductList(False, 3)
            else:
                self.message.label.setText("Ошибка! Некорректное количество")
                self.message.show()
        else:
            if self.buyPB_Quantity.text() != "" and int(self.buyPB_Quantity.text()) != 0:
                labels = ["Товар", "Производитель", "Цена", "Количество", "Итог"]
                self.buyPB_Order.setColumnCount(len(labels))
                self.buyPB_Order.setHorizontalHeaderLabels(labels)
                row = self.buyPB_Order.rowCount()
                self.buyPB_Order.setRowCount(row + 1)
                self.buyPB_Order.setItem(row, 0, QtWidgets.QTableWidgetItem(self.buyPB_ProductList.currentText()))
                self.buyPB_Order.setItem(row, 1, QtWidgets.QTableWidgetItem(self.buyPB_SupplierList.currentText()))
                self.buyPB_Order.setItem(row, 2, QtWidgets.QTableWidgetItem(self.buyPB_Price.text()))
                self.buyPB_Order.setItem(row, 3, QtWidgets.QTableWidgetItem(self.buyPB_Quantity.text()))
                self.buyPB_Order.setItem(row, 4, QtWidgets.QTableWidgetItem(self.buyPB_Cost.text()))
                self.buyPB_TotalCost.setText(str(float(self.buyPB_TotalCost.text()) + float(self.buyPB_Cost.text())))
                self.updateProductList(False, 2)
            else:
                self.message.label.setText("Ошибка! Некорректное количество")
                self.message.show()

    def getCost(self, isFuel):
        if self.currentRole == 2:
            if isFuel:
                if self.buyFB_Quantity.text() != "":
                    if int(self.buyFB_Quantity.text()) > 1000:
                        self.buyFB_Quantity.setText(str(1000))
                    self.buyFB_Cost.setText(str(float(self.buyFB_Price.text()) * int(self.buyFB_Quantity.text())))
                else:
                    self.buyFB_Cost.setText("0.0")
            else:
                if self.buyPB_Quantity.text() != "":
                    quantity = 100
                    row = self.buyPB_Order.rowCount()
                    for i in range(0, row):
                        if self.buyPB_Order.item(i, 0).text() == self.buyPB_ProductList.currentText():
                            quantity = quantity - (int(self.buyPB_Order.item(i, 3).text()))
                    if int(self.buyPB_Quantity.text()) > quantity:
                        self.buyPB_Quantity.setText(str(quantity))
                    self.buyPB_Cost.setText(str(float(self.buyPB_Price.text()) * int(self.buyPB_Quantity.text())))
                else:
                    self.buyPB_Cost.setText("0.0")
        else:
            if isFuel:
                if self.buyF_Quantity.text() != "":
                    quantity = self.db.getQuantity(self.buyF_FuelList.currentText())
                    if int(self.buyF_Quantity.text()) > quantity:
                        self.buyF_Quantity.setText(str(quantity))
                    self.buyF_Cost.setText(str(float(self.buyF_Price.text()) * int(self.buyF_Quantity.text())))
                else:
                    self.buyF_Cost.setText("0.0")
            else:
                if self.buyP_Quantity.text() != "":
                    quantity = self.db.getQuantity(self.buyP_ProductList.currentText())
                    row = self.buyP_Order.rowCount()
                    for i in range(0, row):
                        if self.buyP_Order.item(i, 0).text() == self.buyP_ProductList.currentText():
                            quantity = self.db.getQuantity(self.buyP_ProductList.currentText()) - \
                                       (int(self.buyP_Order.item(i, 2).text()))
                    if int(self.buyP_Quantity.text()) > quantity:
                        self.buyP_Quantity.setText(str(quantity))
                    self.buyP_Cost.setText(str(float(self.buyP_Price.text()) * int(self.buyP_Quantity.text())))
                else:
                    self.buyP_Cost.setText("0.0")

    def buyFuelByClient(self):
        if float(self.buyF_Balance.text()) > float(self.buyF_Cost.text()):
            toDate = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
            orderId = self.db.insertOrderByUsername(self.currentUsername, self.buyF_Cost.text(), toDate)
            self.db.insertOrderDetailandChangeQuantity(orderId, self.buyF_FuelList.currentText(),
                                                       self.buyF_Quantity.text(), self.buyF_Cost.text())
            newBalance = self.db.getBalance(self.currentUsername, self.currentRole) - float(self.buyF_Cost.text())
            self.db.updateBalance(self.currentUsername, self.currentRole, str(newBalance))
            self.message.label.setText("Заказ оплачен")
            self.buyF_Quantity.setText("")
            self.updateProductList(True, 3)
            self.buyF_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
            self.buyF_Cost.setText("0.0")
        else:
            self.message.label.setText("Ошибка! Недостаточно средств на балансе")
        self.message.show()

    def buyProductByClient(self):
        if self.buyP_TotalCost.text() == "0.0":
            self.message.label.setText("Ошибка! Вы не добавили в заказ ни одного товара")
        elif float(self.buyP_Balance.text()) > float(self.buyP_TotalCost.text()):
            toDate = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
            orderId = self.db.insertOrderByUsername(self.currentUsername, self.buyP_TotalCost.text(), toDate)
            for i in range(self.buyP_Order.rowCount()):
                self.db.insertOrderDetailandChangeQuantity(orderId, self.buyP_Order.item(i, 0).text(),
                                                           self.buyP_Order.item(i, 2).text(),
                                                           self.buyP_Order.item(i, 3).text())
            newBalance = self.db.getBalance(self.currentUsername, self.currentRole) - float(self.buyP_TotalCost.text())
            self.db.updateBalance(self.currentUsername, self.currentRole, str(newBalance))
            self.message.label.setText("Заказ оплачен")
            self.buyP_Quantity.setText("")
            self.buyP_Order.clear()
            self.buyP_Order.setRowCount(0)
            self.updateProductList(False, 3)
            self.buyP_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
            self.buyP_TotalCost.setText("0.0")
        else:
            self.message.label.setText("Ошибка! Недостаточно средств на балансе")
        self.message.show()

    def changeOrderNumber(self, isClient):
        if isClient:
            self.HC_OrderDetails.clear()
            labels = ["Товар", "Количество", "Стоимость"]
            orderDetails = self.db.getOrderDetails(self.HC_NumberList.currentText())
            self.HC_OrderDetails.setColumnCount(len(labels))
            self.HC_OrderDetails.setHorizontalHeaderLabels(labels)
            for i in range(len(orderDetails)):
                self.HC_OrderDetails.setRowCount(i + 1)
                self.HC_OrderDetails.setItem(i, 0, QtWidgets.QTableWidgetItem(str(orderDetails[i][0])))
                self.HC_OrderDetails.setItem(i, 1, QtWidgets.QTableWidgetItem(str(orderDetails[i][1])))
                self.HC_OrderDetails.setItem(i, 2, QtWidgets.QTableWidgetItem(str(orderDetails[i][2])))
        else:
            self.HB_OrderDetails.clear()
            labels = ["Товар", "Производитель", "Количество", "Стоимость"]
            orderDetails = self.db.getPurchaseDetails(self.HB_NumberList.currentText())
            self.HB_OrderDetails.setColumnCount(len(labels))
            self.HB_OrderDetails.setHorizontalHeaderLabels(labels)
            for i in range(len(orderDetails)):
                self.HB_OrderDetails.setRowCount(i + 1)
                self.HB_OrderDetails.setItem(i, 0, QtWidgets.QTableWidgetItem(str(orderDetails[i][0])))
                self.HB_OrderDetails.setItem(i, 1, QtWidgets.QTableWidgetItem(str(orderDetails[i][1])))
                self.HB_OrderDetails.setItem(i, 2, QtWidgets.QTableWidgetItem(str(orderDetails[i][2])))
                self.HB_OrderDetails.setItem(i, 3, QtWidgets.QTableWidgetItem(str(orderDetails[i][3])))

    def updateProductList(self, isFuel, role):
        if isFuel:
            if role == 2:
                self.buyFB_Quantity.setPlaceholderText("Максимум: 1000")
                self.buyFB_Price.setText(str(self.db.getPrice(self.buyFB_FuelList.currentText())))
            else:
                self.buyF_Quantity.setPlaceholderText(
                    "Максимум: " + str(self.db.getQuantity(self.buyF_FuelList.currentText())))
                self.buyF_Price.setText(str(self.db.getPrice(self.buyF_FuelList.currentText())))
        else:
            if role == 2:
                self.buyPB_Quantity.setPlaceholderText("Максимум: 100")
                row = self.buyPB_Order.rowCount()
                for i in range(0, row):
                    if self.buyPB_Order.item(i, 0).text() == self.buyPB_Order.item(row - 1, 0).text():
                        if i != row - 1 and row != 1:
                            self.buyPB_Order.item(i, 3).setText(str(int(self.buyPB_Order.item(i, 3).text()) +
                                                                    int(self.buyPB_Order.item(row - 1, 3).text())))
                            self.buyPB_Order.item(i, 4).setText(str(float(self.buyPB_Order.item(i, 4).text()) +
                                                                    float(self.buyPB_Order.item(row - 1, 4).text())))
                            self.buyPB_TotalCost.setText(str(float(self.buyPB_TotalCost.text()) +
                                                             float(self.buyPB_Order.item(row - 1, 4).text())))
                            self.deleteLastProduct(False)
                        self.buyPB_Quantity.setPlaceholderText(
                            "Максимум: " + str(100 - int(self.buyPB_Order.item(i, 3).text())))
                        break
                self.buyPB_Price.setText(str(self.db.getPrice(self.buyPB_ProductList.currentText())))
            else:
                self.buyP_Quantity.setPlaceholderText(
                    "Максимум: " + str(self.db.getQuantity(self.buyP_ProductList.currentText())))
                row = self.buyP_Order.rowCount()
                for i in range(0, row):
                    if self.buyP_Order.item(i, 0).text() == self.buyP_Order.item(row - 1, 0).text():
                        if i != row - 1 and row != 1:
                            self.buyP_Order.item(i, 2).setText(str(int(self.buyP_Order.item(i, 2).text()) +
                                                                   int(self.buyP_Order.item(row - 1, 2).text())))
                            self.buyP_Order.item(i, 3).setText(str(float(self.buyP_Order.item(i, 3).text()) +
                                                                   float(self.buyP_Order.item(row - 1, 3).text())))
                            self.buyP_TotalCost.setText(str(float(self.buyP_TotalCost.text()) +
                                                            float(self.buyP_Order.item(row - 1, 3).text())))
                            self.deleteLastProduct(True)
                        self.buyP_Quantity.setPlaceholderText(
                            "Максимум: " + str(int(self.db.getQuantity(str(self.buyP_ProductList.currentText())) -
                                                   int(self.buyP_Order.item(i, 2).text()))))
                        break
                self.buyP_Price.setText(str(self.db.getPrice(self.buyP_ProductList.currentText())))

    def buyFuelByBuyer(self):
        if float(self.buyFB_Balance.text()) > float(self.buyFB_Cost.text()):
            toDate = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
            orderId = self.db.insertPurchaseByUsername(self.currentUsername, self.buyFB_Cost.text(), toDate)
            self.db.insertPurchaseDetailandChangeQuantity(orderId, self.buyFB_FuelList.currentText(),
                                                          self.buyFB_SupplierList.currentText(),
                                                          self.buyFB_Quantity.text(), self.buyFB_Cost.text())
            newBalance = self.db.getBalance(self.currentUsername, self.currentRole) - float(self.buyFB_Cost.text())
            self.db.updateBalance(self.currentUsername, self.currentRole, str(newBalance))
            self.message.label.setText("Заказ оплачен")
            self.buyFB_Quantity.setText("")
            self.updateProductList(True, 2)
            self.buyFB_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
            self.buyFB_Cost.setText("0.0")
        else:
            self.message.label.setText("Ошибка! Недостаточно средств на балансе")
        self.message.show()

    def buyProductByBuyer(self):
        if self.buyPB_TotalCost.text() == "0.0":
            self.message.label.setText("Ошибка! Вы не добавили в заказ ни одного товара")
        elif float(self.buyPB_Balance.text()) > float(self.buyPB_TotalCost.text()):
            toDate = str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year)
            orderId = self.db.insertPurchaseByUsername(self.currentUsername, self.buyPB_TotalCost.text(), toDate)
            for i in range(self.buyPB_Order.rowCount()):
                self.db.insertPurchaseDetailandChangeQuantity(orderId, self.buyPB_Order.item(i, 0).text(),
                                                              self.buyPB_Order.item(i, 1).text(),
                                                              self.buyPB_Order.item(i, 3).text(),
                                                              self.buyPB_Order.item(i, 4).text())
            newBalance = self.db.getBalance(self.currentUsername, self.currentRole) - float(self.buyPB_TotalCost.text())
            self.db.updateBalance(self.currentUsername, self.currentRole, str(newBalance))
            self.message.label.setText("Заказ оплачен")
            self.buyPB_Quantity.setText("")
            self.buyPB_Order.clear()
            self.buyPB_Order.setRowCount(0)
            self.updateProductList(False, 2)
            self.buyPB_Balance.setText(str(self.db.getBalance(self.currentUsername, self.currentRole)))
            self.buyPB_TotalCost.setText("0.0")
        else:
            self.message.label.setText("Ошибка! Недостаточно средств на балансе")
        self.message.show()

    def getProductsFromSuppliers(self):
        self.buyPB_ProductList.clear()
        products = None
        match self.buyPB_Type.currentText():
            case 'Продукты питания':
                if self.buyPB_Filter.currentText() == 'Все товары':
                    products = self.db.getProductNames(2)
                else:
                    products = self.db.getProductNamesWithFilter(2, self.buyPB_Filter.currentText())
            case 'Автотовары':
                if self.buyPB_Filter.currentText() == 'Все товары':
                    products = self.db.getProductNames(1)
                else:
                    products = self.db.getProductNamesWithFilter(1, self.buyPB_Filter.currentText())
        for i in products:
            self.buyPB_ProductList.addItem(i[0])

    def changeType(self):
        self.changePP_ProductList.clear()
        products = None
        match self.changePP_Type.currentText():
            case 'Продукты':
                products = self.db.getProducts(2)
            case 'Автотовары':
                products = self.db.getProducts(1)
            case 'Топливо':
                products = self.db.getProducts(3)
        for i in products:
            self.changePP_ProductList.addItem(i[0])

    def createBuyerAcc(self):
        number = "".join(re.findall(r'\d+', self.ca_Phone.text()))
        errorsInfo = tools.checkInfo(self.ca_FN.text(), self.ca_LN.text(), self.ca_Username.text(),
                                     self.ca_BOD.text(), self.ca_Email.text(), number, "", "", "")
        errorsPass = tools.checkPassword(self.ca_Pass.text(), self.ca_Pass2.text())
        if len(errorsInfo) == 0 and len(errorsPass) == 0:
            self.db.registration(self.ca_FN.text(), self.ca_LN.text(), number,
                                 self.ca_Email.text(), self.ca_BOD.text(), self.ca_Username.text(),
                                 generate_password_hash(self.ca_Pass.text()), 2)
            self.message.label.setText("Вы успешно зарегестрировали аккаунт")
            self.Sign_in.hide()
            self.ca_FN.setText("")
            self.ca_LN.setText("")
            self.ca_Username.setText("")
            self.ca_BOD.setText("")
            self.ca_Email.setText("")
            self.ca_Phone.setText("")
            self.ca_Pass.setText("")
            self.ca_Pass2.setText("")
        else:
            if len(errorsInfo) != 0:
                toMsg = "Ошибка! Некорректный ввод данных: "
                for i in range(len(errorsInfo)):
                    toMsg += errorsInfo[i]
                    if i != len(errorsInfo) - 1:
                        toMsg += ", "
                if len(errorsPass) != 0:
                    toMsg += ".\n"
                    toMsg += "Ошибка! Некорректный ввод пароля: "
                    for i in range(len(errorsPass)):
                        toMsg += errorsPass[i]
                        if i != len(errorsPass) - 1:
                            toMsg += ", "
                    toMsg += "."
                else:
                    toMsg += "."
            else:
                toMsg = "Ошибка! Некорректный ввод пароля: "
                for i in range(len(errorsPass)):
                    toMsg += errorsPass[i]
                    if i != len(errorsPass) - 1:
                        toMsg += ", "
                toMsg += "."
            self.message.label.setText(toMsg)
        self.message.show()

    def exit(self):
        self.currentWindow.hide()
        self.Main.show()

    def goBack(self):
        self.lastWindow.hide()
        self.ci_FN.setText("")
        self.ci_LN.setText("")
        self.ci_Username.setText("")
        self.ci_BOD.setText("")
        self.ci_Email.setText("")
        self.ci_Phone.setText("")
        self.cp_NewPass.setText("")
        self.cp_NewPass2.setText("")
        self.cp_OldPass.setText("")
        self.buyF_Price.setText("")
        self.buyF_Quantity.setText("")
        self.buyFB_Price.setText("")
        self.buyFB_Quantity.setText("")
        self.buyP_Price.setText("")
        self.buyP_Quantity.setText("")
        self.buyPB_Price.setText("")
        self.buyPB_Quantity.setText("")
        self.ca_FN.setText("")
        self.ca_LN.setText("")
        self.ca_Username.setText("")
        self.ca_Email.setText("")
        self.ca_BOD.setText("")
        self.ca_Phone.setText("")
        self.ca_Pass.setText("")
        self.ca_Pass2.setText("")
        self.changePP_Price.setText("")
        self.buyP_Order.clear()
        self.buyP_Order.setRowCount(0)
        self.buyP_Quantity.setText("")
        self.buyPB_Order.clear()
        self.buyPB_Order.setRowCount(0)
        self.buyPB_Quantity.setText("")
        self.buyFB_Quantity.setText("")
        self.buyF_Quantity.setText("")
        self.del_UsernameList.clear()
        self.currentWindow.show()


class MessageBox(QtWidgets.QDialog, Ui_RegSuccess):
    def __init__(self):
        super(MessageBox, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("")
        self.pushButton.clicked.connect(self.close)


class MsgToPlan(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(MsgToPlan, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("")
        self.pushButton.clicked.connect(self.close)


class ConfirmDel(QtWidgets.QDialog, Ui_ConfirmDel):
    def __init__(self):
        super(ConfirmDel, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("")
        self.pushButton.clicked.connect(self.close)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    window = App()
    window.setWindowIcon(QtGui.QIcon('icon.png'))
    window.show()
    window.taskbar_button = QWinTaskbarButton()
    window.taskbar_button.setWindow(window.windowHandle())
    window.taskbar_button.setOverlayIcon(QtGui.QIcon('icon.png'))
    sys.exit(app.exec())
