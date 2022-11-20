use GasStation
go

insert Roles(Name) values ('Управляющий');
insert Roles(Name) values ('Закупщик');
insert Roles(Name) values ('Клиент');
go

insert Managers(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Илья', 'Князев', '79991234567', 
'myemail@gmail.com', cast('11-08-2002' as date), 10000000, 'Manager', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 1);
insert Buyers(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Иван', 'Иванов', '79991234987', 
'email2@gmail.com', cast('10-02-1999' as date), 100000, 'Buyer', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 2);
insert Buyers(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Савелий', 'Казаков', '79541234017', 
'email8@gmail.com', cast('11-03-1993' as date), 100000, 'Buyer2', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 2);
insert Clients(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Сергей', 'Сергеев', '79991239546', 
'email3@gmail.com', cast('11-11-2000' as date), 100000, 'Client1', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 3);
insert Clients(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Евгений', 'Смирнов', '79991207867', 
'email4@gmail.com', cast('18-12-1990' as date), 100000, 'Client2', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 3);
insert Clients(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Мария', 'Васильева', '79934534567', 
'email5@gmail.com', cast('25-08-1995' as date), 100000, 'Client3', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 3);
insert Clients(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Павел', 'Малышев', '79900234567', 
'email6@gmail.com', cast('31-12-1998' as date), 100000, 'Client4', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 3);
insert Clients(FirstName, LastName, Phone, Email, DOB, Balance, Username, Password, RoleId) values ('Владимир', 'Стахеев', '79991289567', 
'email7@gmail.com', cast('29-04-1989' as date), 100000, 'Client5', 'pbkdf2:sha256:260000$hgZa9hLpfudXdpLP$e12f4ed7e3bf50dc8f462bbbe0efea00badd8979200afca38bd655f730f254cf', 3);
go

insert ProductTypes(Name) values ('Автотовар');
insert ProductTypes(Name) values ('Продукт');
insert ProductTypes(Name) values ('Топливо');
go

insert Products(Name, Quantity, Price, TypeId) values('АИ-92', 300, 48.5, 3);
insert Products(Name, Quantity, Price, TypeId) values('АИ-95', 320, 52.0, 3);
insert Products(Name, Quantity, Price, TypeId) values('АИ-98', 350, 61.5, 3);
insert Products(Name, Quantity, Price, TypeId) values('Mars', 200, 30, 2);
insert Products(Name, Quantity, Price, TypeId) values('Twix', 100, 30, 2);
insert Products(Name, Quantity, Price, TypeId) values('Coca-Cola', 150, 50, 2);
insert Products(Name, Quantity, Price, TypeId) values('Orbit', 50, 25, 2);
insert Products(Name, Quantity, Price, TypeId) values('LiquiMoly Special Tec AA 5W-30', 100, 5500, 1);
insert Products(Name, Quantity, Price, TypeId) values('LiquiMoly ANTIFROST Scheiben-Frostschutz -5', 90, 400, 1);
insert Products(Name, Quantity, Price, TypeId) values('LiquiMoly ANTIFROST Scheiben-Frostschutz -20', 80, 600, 1);
insert Products(Name, Quantity, Price, TypeId) values('ZIC X7 LS 10W-30', 110, 2200, 1);
go


insert Suppliers(Name) values ('Лукойл');
insert Suppliers(Name) values ('Газпромнефть');
insert Suppliers(Name) values ('Роснефть');

insert Suppliers(Name) values ('Mars');
insert Suppliers(Name) values ('Coca-Cola');
insert Suppliers(Name) values ('Wrigley');

insert Suppliers(Name) values ('Liqui-Moly');
insert Suppliers(Name) values ('ZIC');
go

insert SuppliersProducts(ProductId, SupplierId, Price) values (1,1, 45);
insert SuppliersProducts(ProductId, SupplierId, Price) values (1,2, 46);
insert SuppliersProducts(ProductId, SupplierId, Price) values (1,3, 45.5);
insert SuppliersProducts(ProductId, SupplierId, Price) values (2,1, 51);
insert SuppliersProducts(ProductId, SupplierId, Price) values (2,2, 50);
insert SuppliersProducts(ProductId, SupplierId, Price) values (2,3, 50.5);
insert SuppliersProducts(ProductId, SupplierId, Price) values (3,1, 58);
insert SuppliersProducts(ProductId, SupplierId, Price) values (3,2, 59);
insert SuppliersProducts(ProductId, SupplierId, Price) values (3,3, 58.5);
insert SuppliersProducts(ProductId, SupplierId, Price) values (4,4, 20);
insert SuppliersProducts(ProductId, SupplierId, Price) values (5,4, 20);
insert SuppliersProducts(ProductId, SupplierId, Price) values (6,5, 35);
insert SuppliersProducts(ProductId, SupplierId, Price) values (7,6, 15);
insert SuppliersProducts(ProductId, SupplierId, Price) values (8,7, 5000);
insert SuppliersProducts(ProductId, SupplierId, Price) values (9,7, 300);
insert SuppliersProducts(ProductId, SupplierId, Price) values (10,7, 500);
insert SuppliersProducts(ProductId, SupplierId, Price) values (11,8, 1800);
go

insert Assignments(Name) values ('Продукты');
insert Assignments(Name) values ('Для легковых автомобилей');
insert Assignments(Name) values ('Для грузовых автомобилей');
insert Assignments(Name) values ('Напитки');
go

insert AssignmentsProducts(AssignmentId, ProductId) values (2,1);
insert AssignmentsProducts(AssignmentId, ProductId) values (3,1);
insert AssignmentsProducts(AssignmentId, ProductId) values (2,2);
insert AssignmentsProducts(AssignmentId, ProductId) values (3,2);
insert AssignmentsProducts(AssignmentId, ProductId) values (2,3);
insert AssignmentsProducts(AssignmentId, ProductId) values (3,3);
insert AssignmentsProducts(AssignmentId, ProductId) values (1,4);
insert AssignmentsProducts(AssignmentId, ProductId) values (1,5);
insert AssignmentsProducts(AssignmentId, ProductId) values (4,6);
insert AssignmentsProducts(AssignmentId, ProductId) values (1,7);
insert AssignmentsProducts(AssignmentId, ProductId) values (2,8);
insert AssignmentsProducts(AssignmentId, ProductId) values (3,8);
insert AssignmentsProducts(AssignmentId, ProductId) values (2,9);
insert AssignmentsProducts(AssignmentId, ProductId) values (3,9);
insert AssignmentsProducts(AssignmentId, ProductId) values (2,10);
insert AssignmentsProducts(AssignmentId, ProductId) values (3,10);
insert AssignmentsProducts(AssignmentId, ProductId) values (2,11);
go


insert Plans(ManagerId, Revenue, MoneyEarn, MoneySpent, OrderQuantity, PurchaseQuantity, 
CreationDate, LastDate, Status, Message) values(1, 150000, 250000.0, 60000.0, 987, 34, cast('06/11/2022' as date), 
cast('13/11/2022' as date), 'Выполнен', '');
insert Plans(ManagerId, Revenue, MoneyEarn, MoneySpent, OrderQuantity, PurchaseQuantity, 
CreationDate, LastDate, Status, Message) values(1, 200000, 260000.0, 90000.0, 930, 59, cast('13/11/2022' as date), 
cast('20/11/2022' as date), 'Текущий', '');
go