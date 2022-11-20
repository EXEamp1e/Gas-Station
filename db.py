import pyodbc
from werkzeug.security import check_password_hash


class GasStationDB:
    def __init__(self):
        self.connection = pyodbc.connect("Driver={SQL SERVER}; Server=HOME-PC;Database=GasStation; "
                                         "Trusted_Connection=yes;")
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    # Процедуры
    def insertOrderByUsername(self, username, cost, date):
        with self.connection:
            return self.cursor.execute("declare @id int;"
                                       "exec insertOrderByUsername  ?, ?, ?, @orderId = @id output;"
                                       "select @id", (username, cost, date,)).fetchone()[0]

    def insertPurchaseByUsername(self, username, cost, date):
        with self.connection:
            return self.cursor.execute("declare @id int;"
                                       "exec insertPurchaseByUsername  ?, ?, ?, @purchaseId = @id output;"
                                       "select @id", (username, cost, date,)).fetchone()[0]

    def getProductNamesWithFilter(self, productType, filter):
        with self.connection:
            return self.cursor.execute(
                "exec getProductsWithFilter ?, ?", (productType, filter,)).fetchall()

    def insertOrderDetailandChangeQuantity(self, orderId, productName, quantity, cost):
        with self.connection:
            self.cursor.execute("exec insertOrderDetailandChangeQuantity ?, ?, ?, ?",
                                (orderId, productName, quantity, cost,))

    def insertPurchaseDetailandChangeQuantity(self, orderId, productName, supplierName, quantity, cost):
        with self.connection:
            self.cursor.execute("exec insertPurchaseDetailandChangeQuantity ?, ?, ?, ?, ?",
                                (orderId, productName, supplierName, quantity, cost,))

    # Запросы
    def getId(self, username, role):
        with self.connection:
            match role:
                case 1:
                    return self.cursor.execute(
                        "select ManagerId from Managers where Username = ?", (username,)).fetchone()[0]
                case 2:
                    return self.cursor.execute(
                        "select BuyerId from Buyers where Username = ?", (username,)).fetchone()[0]
                case 3:
                    return self.cursor.execute(
                        "select ClientId from Clients where Username = ?", (username,)).fetchone()[0]

    def getBuyers(self):
        with self.connection:
            return self.cursor.execute("select FirstName, LastName, Email, Username from Buyers").fetchall()

    def delBuyer(self, username):
        with self.connection:
            self.cursor.execute("delete from Buyers where Username = ?", (username,))

    def delClient(self, username):
        with self.connection:
            self.cursor.execute("delete from Clients where Username = ?", (username,))

    def checkLogin(self, username, password):
        with self.connection:
            result = self.cursor.execute("select * from Managers where Username = ?", (username,)).fetchone()
            if result is None:
                result = self.cursor.execute("select * from Buyers where Username = ?", (username,)).fetchone()
                if result is None:
                    result = self.cursor.execute("select * from Clients where Username = ?", (username,)).fetchone()
                    if result is None:
                        return 0
                    else:
                        if check_password_hash(self.cursor.execute("select Password from Clients where Username = ?",
                                                                   (username,)).fetchone()[0], password):
                            return 3
                        else:
                            return 0
                else:
                    if check_password_hash(self.cursor.execute("select Password from Buyers where Username = ?",
                                                               (username,)).fetchone()[0], password):
                        return 2
                    else:
                        return 0
            else:
                if check_password_hash(self.cursor.execute("select Password from Managers where Username = ?",
                                                           (username,)).fetchone()[0], password):
                    return 1
                else:
                    return 0

    def registration(self, firstName, lastName, phone, email, date, username, password, role):
        with self.connection:
            match role:
                case 2:
                    self.cursor.execute("insert into Buyers(FirstName, LastName, Phone, Email, DOB, Balance, Username, "
                                        "Password, RoleId) values(?, ?, ?, ?, cast(? as date), 0, ?, ?, ?)",
                                        (firstName, lastName, phone, email, date, username, password, role,))
                case 3:
                    self.cursor.execute("insert into Clients(FirstName, LastName, Phone, Email, DOB, Balance, Username,"
                                        "Password, RoleId) values(?, ?, ?, ?, cast(? as date), 0, ?, ?, ?)",
                                        (firstName, lastName, phone, email, date, username, password, role,))

    def checkPassword(self, password, username, role):
        with self.connection:
            match role:
                case 1:
                    return check_password_hash(self.cursor.execute("select Password from Managers where Username = ?",
                                                                   (username,)).fetchone()[0], password)
                case 2:
                    return check_password_hash(self.cursor.execute("select Password from Buyers where Username = ?",
                                                                   (username,)).fetchone()[0], password)
                case 3:
                    return check_password_hash(self.cursor.execute("select Password from Clients where Username = ?",
                                                                   (username,)).fetchone()[0], password)

    def updatePassword(self, password, username, role):
        with self.connection:
            match role:
                case 1:
                    self.cursor.execute("update Managers set Password = ?  where Username = ?", (password, username,))
                case 2:
                    self.cursor.execute("update Buyers set Password = ?  where Username = ?", (password, username,))
                case 3:
                    self.cursor.execute("update Clients set Password = ?  where Username = ?", (password, username,))

    def updateInfo(self, currentUsername, role, firstName, lastName, username, date, email, phone):
        with self.connection:
            match role:
                case 1:
                    self.cursor.execute("update Managers set FirstName = ?, LastName = ?, Phone = ?, Email = ?,"
                                        " DOB = ?, Username = ?  where Username = ?",
                                        (firstName, lastName, phone, email, date, username, currentUsername,))
                case 2:
                    self.cursor.execute("update Buyers set FirstName = ?, LastName = ?, Phone = ?, Email = ?,"
                                        " DOB = ?, Username = ? where Username = ?",
                                        (firstName, lastName, phone, email, date, username, currentUsername,))
                case 3:
                    self.cursor.execute("update Clients set FirstName = ?, LastName = ?, Phone = ?, Email = ?,"
                                        " DOB = ?, Username = ? where Username = ?",
                                        (firstName, lastName, phone, email, date, username, currentUsername,))

    def checkUsername(self, username):
        with self.connection:
            result = self.cursor.execute("select * from Managers where Username = ?", (username,)).fetchone()
            if result is None:
                result = self.cursor.execute("select * from Buyers where Username = ?", (username,)).fetchone()
                if result is None:
                    result = self.cursor.execute("select * from Clients where Username = ?", (username,)).fetchone()
                    if result is None:
                        return True
            return False

    def checkEmail(self, email):
        with self.connection:
            result = self.cursor.execute("select * from Managers where Email = ?", (email,)).fetchone()
            if result is None:
                result = self.cursor.execute("select * from Buyers where Email = ?", (email,)).fetchone()
                if result is None:
                    result = self.cursor.execute("select * from Clients where Email = ?", (email,)).fetchone()
                    if result is None:
                        return True
            return False

    def checkPhone(self, phone):
        with self.connection:
            result = self.cursor.execute("select * from Managers where Phone = ?", (phone,)).fetchone()
            if result is None:
                result = self.cursor.execute("select * from Buyers where Phone = ?", (phone,)).fetchone()
                if result is None:
                    result = self.cursor.execute("select * from Clients where Phone = ?", (phone,)).fetchone()
                    if result is None:
                        return True
            return False

    def getInfo(self, username, role):
        with self.connection:
            match role:
                case 1:
                    return self.cursor.execute(
                        "select FirstName, LastName, Phone, Email, DOB from Managers where Username = ?",
                        (username,)).fetchone()
                case 2:
                    return self.cursor.execute(
                        "select FirstName, LastName, Phone, Email, DOB from Buyers where Username = ?",
                        (username,)).fetchone()
                case 3:
                    return self.cursor.execute(
                        "select FirstName, LastName, Phone, Email, DOB from Clients where Username = ?",
                        (username,)).fetchone()

    def getProductNames(self, productType):
        with self.connection:
            return self.cursor.execute(
                "select Name from Products where TypeId = ?", (productType,)).fetchall()

    def getProducts(self, productType):
        with self.connection:
            return self.cursor.execute(
                "select Name, Quantity, Price from Products where TypeId = ? order by Name", (productType,)).fetchall()

    def getProductsDesc(self, productType):
        with self.connection:
            return self.cursor.execute(
                "select Name, Quantity, Price from Products where TypeId = ? order by Name desc",
                (productType,)).fetchall()

    def getProductsByQuantityDesc(self, productType):
        with self.connection:
            return self.cursor.execute(
                "select Name, Quantity, Price from Products where TypeId = ? order by Quantity desc",
                (productType,)).fetchall()

    def getProductsByQuantity(self, productType):
        with self.connection:
            return self.cursor.execute(
                "select Name, Quantity, Price from Products where TypeId = ? order by Quantity",
                (productType,)).fetchall()

    def getProductsWithFilter(self, productType, filter):
        with self.connection:
            return self.cursor.execute(
                "select P.Name, Quantity, Price from Products P "
                "join AssignmentsProducts AP on AP.ProductId = P.ProductId "
                "join Assignments A on A.AssignmentId = AP.AssignmentId "
                "where TypeId = ? and A.Name = ?", (productType, filter,)).fetchall()

    def getCountProducts(self, productType):
        with self.connection:
            return self.cursor.execute(
                "select count(*) from Products where TypeId = ?", (productType,)).fetchone()[0]

    def updatePrice(self, name, price):
        with self.connection:
            self.cursor.execute("update Products set Price = ? where Name = ?", (price, name,))

    def getQuantity(self, product):
        with self.connection:
            return self.cursor.execute("select Quantity from Products where Name = ?", (product,)).fetchone()[0]

    def getPrice(self, product):
        with self.connection:
            return self.cursor.execute("select Price from Products where Name = ?", (product,)).fetchone()[0]

    def getSuppliers(self, product):
        with self.connection:
            return self.cursor.execute("select S.Name from Suppliers S "
                                       "join SuppliersProducts SP on S.SupplierId = SP.SupplierId "
                                       "join Products P on P.ProductId = SP.ProductId "
                                       "where P.Name = ?", (product,)).fetchall()

    def getPriceFromSuppliers(self, product, supplier):
        with self.connection:
            return self.cursor.execute("select SP.Price from SuppliersProducts SP "
                                       "join Suppliers S on S.SupplierId = SP.SupplierId "
                                       "join Products P on P.ProductId = SP.ProductId "
                                       "where P.Name = ? and S.Name = ?", (product, supplier,)).fetchone()[0]

    def getBalance(self, username, role):
        with self.connection:
            match role:
                case 1:
                    return self.cursor.execute(
                        "select Balance from Managers where Username = ?", (username,)).fetchone()[0]
                case 2:
                    return self.cursor.execute(
                        "select Balance from Buyers where Username = ?", (username,)).fetchone()[0]
                case 3:
                    return self.cursor.execute(
                        "select Balance from Clients where Username = ?", (username,)).fetchone()[0]

    def insertOrder(self, clientId, cost, toDate):
        with self.connection:
            self.cursor.execute(
                "insert into Orders(ClientId, TotalCost, PurchaseDate) values(?, ?, cast(? as date))",
                (clientId, cost, toDate,))
            return self.cursor.execute("select OrderId from Orders where OrderId=(select max(OrderId) from Orders)"
                                       ).fetchone()[0]

    def getOrders(self, clientId):
        with self.connection:
            return self.cursor.execute("select OrderId, TotalCost, PurchaseDate from Orders where ClientId = ?",
                                       (clientId,)).fetchall()

    def insertOrderDetails(self, orderId, productId, quantity, cost):
        with self.connection:
            self.cursor.execute(
                "insert into OrderDetails(OrderId, ProductId, Quantity, Cost) values(?, ?, ?, ?)",
                (orderId, productId, quantity, cost,))

    def getOrderDetails(self, orderId):
        with self.connection:
            return self.cursor.execute("select P.Name, OD.Quantity, Cost from OrderDetails OD "
                                       "join Products P on OD.ProductId = P.ProductId "
                                       "where OrderId = ?",
                                       (orderId,)).fetchall()

    def getProductId(self, name):
        with self.connection:
            return self.cursor.execute("select ProductId from Products where Name = ?",
                                       (name,)).fetchone()[0]

    def updateBalance(self, username, role, balance):
        with self.connection:
            match role:
                case 1:
                    self.cursor.execute("update Managers set Balance = ? where Username = ?", (balance, username,))
                case 2:
                    self.cursor.execute("update Buyers set Balance = ? where Username = ?", (balance, username,))
                case 3:
                    self.cursor.execute("update Clients set Balance = ? where Username = ?", (balance, username,))

    def updateProductQuantity(self, quantity, name):
        with self.connection:
            self.cursor.execute("update Products set Quantity = ? where Name = ?", (quantity, name,))

    def insertPurchase(self, buyerId, cost, toDate):
        with self.connection:
            self.cursor.execute(
                "insert into Purchases(BuyerId, TotalCost, PurchaseDate) values(?, ?, cast(? as date))",
                (buyerId, cost, toDate,))
            return self.cursor.execute("select PurchaseId from Purchases where PurchaseId="
                                       "(select max(PurchaseId) from Purchases)"
                                       ).fetchone()[0]

    def getPurchases(self, buyerId):
        with self.connection:
            return self.cursor.execute("select PurchaseId, TotalCost, PurchaseDate from Purchases where BuyerId = ?",
                                       (buyerId,)).fetchall()

    def insertPurchaseDetails(self, purchaseId, suppliersProducts, quantity, cost):
        with self.connection:
            self.cursor.execute(
                "insert into PurchaseDetails(PurchaseId, SuppliersProducts, Quantity, Cost) values(?, ?, ?, ?)",
                (purchaseId, suppliersProducts, quantity, cost,))

    def getPurchaseDetails(self, purchaseId):
        with self.connection:
            return self.cursor.execute("select P.Name, S.Name, PD.Quantity, PD.Cost from PurchaseDetails PD "
                                       "join SuppliersProducts SP on PD.SuppliersProducts = SP.SuppliersProductsId "
                                       "join Suppliers S on S.SupplierId = SP.SupplierId "
                                       "join Products P on P.ProductId = SP.ProductId "
                                       "where PurchaseId = ?",
                                       (purchaseId,)).fetchall()

    def getSuppliersProducts(self, productId, supplierId):
        with self.connection:
            return self.cursor.execute("select SP.SuppliersProductsId from SuppliersProducts SP "
                                       "join Suppliers S on S.SupplierId = SP.SupplierId "
                                       "join Products P on P.ProductId = SP.ProductId "
                                       "where P.ProductId = ? and S.SupplierId = ?",
                                       (productId, supplierId,)).fetchone()[0]

    def getSupplierId(self, name):
        with self.connection:
            return self.cursor.execute("select SupplierId from Suppliers where Name = ?", (name,)).fetchone()[0]

    def createPlan(self, managerId, revenue, creationDate, lastDate):
        with self.connection:
            self.cursor.execute(
                "insert into Plans(ManagerId, Revenue, MoneyEarn, MoneySpent, OrderQuantity, PurchaseQuantity, "
                "CreationDate, LastDate, Status, Message) values(?, ?, 0.0, 0.0, 0, 0, cast(? as date), "
                "cast(? as date), 'Текущий', '')", (managerId, revenue, creationDate, lastDate,))

    def getPlans(self):
        with self.connection:
            return self.cursor.execute("select CreationDate from Plans").fetchall()

    def getPlanByCreationDate(self, creationDate):
        with self.connection:
            return self.cursor.execute("select Revenue, MoneyEarn, MoneySpent, OrderQuantity, PurchaseQuantity, "
                                       "LastDate, Status, Message from Plans where CreationDate = ?",
                                       (creationDate,)).fetchone()

    def getPlanByLastDate(self, lastDate):
        with self.connection:
            return self.cursor.execute("select Revenue, MoneyEarn, MoneySpent, OrderQuantity, PurchaseQuantity, "
                                       "LastDate, Status, Message from Plans where LastDate = cast(? as date)",
                                       (lastDate,)).fetchone()

    def getLastPlanDate(self):
        with self.connection:
            return self.cursor.execute("select LastDate from Plans where PlanId=(select max(PlanId) from Plans)"
                                       ).fetchone()[0]

    def updatePlanStatus(self, status, lastDate):
        with self.connection:
            self.cursor.execute("update Plans set Status = ? where LastDate = cast(? as date)", (status, lastDate))

    def updatePlanLastDate(self, oldDate, newDate):
        with self.connection:
            self.cursor.execute("update Plans set LastDate = ? where LastDate = cast(? as date)", (newDate, oldDate))

    def updatePlanMessage(self, message, lastDate):
        with self.connection:
            self.cursor.execute("update Plans set Message = ? where LastDate = cast(? as date)", (message, lastDate))

    def updatePlanSpent(self, spent, lastDate):
        with self.connection:
            self.cursor.execute("update Plans set MoneySpent = ? where LastDate = cast(? as date)", (spent, lastDate))

    def updatePlanEarn(self, earn, lastDate):
        with self.connection:
            self.cursor.execute("update Plans set MoneyEarn = ? where LastDate = cast(? as date)", (earn, lastDate))

    def getPlanSpent(self, lastDate):
        with self.connection:
            return self.cursor.execute("select MoneySpent from Plans where LastDate = cast(? as date)", (lastDate,)
                                       ).fetchone()[0]

    def getPlanEarn(self, lastDate):
        with self.connection:
            return self.cursor.execute("select MoneyEarn from Plans where LastDate = cast(? as date)", (lastDate,)
                                       ).fetchone()[0]

    def updatePlanOrders(self, orders, lastDate):
        with self.connection:
            self.cursor.execute("update Plans set OrderQuantity = ? where LastDate = cast(? as date)",
                                (orders, lastDate))

    def updatePlanPurchases(self, purchases, lastDate):
        with self.connection:
            self.cursor.execute("update Plans set PurchaseQuantity = ? where LastDate = cast(? as date)",
                                (purchases, lastDate))

    def getPlanOrders(self, lastDate):
        with self.connection:
            return self.cursor.execute("select OrderQuantity from Plans where LastDate = cast(? as date)",
                                       (lastDate,)).fetchone()[0]

    def getPlanPurchases(self, lastDate):
        with self.connection:
            return self.cursor.execute("select PurchaseQuantity from Plans where LastDate = cast(? as date)",
                                       (lastDate,)).fetchone()[0]
