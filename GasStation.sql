use GasStation
go

create table Roles(
	RoleId int identity primary key,
	Name varchar(30) not null
);
go

create table Clients(
	ClientId int identity(1,1) primary key,
	FirstName varchar(30) not null,
	LastName varchar(30) not null,
	Phone varchar(11) not null,
	Email varchar(50) not null,
	DOB date not null,
	Balance real null,
	Username varchar(30) not null,
	Password varchar(128) not null,
	RoleId int not null foreign key references Roles
);
go

create table Managers(
	ManagerId int identity(1,1) primary key,
	FirstName varchar(30) not null,
	LastName varchar(30) not null,
	Phone varchar(11) not null,
	Email varchar(50) not null,
	DOB date not null,
	Balance real null,
	Username varchar(30) not null,
	Password varchar(128) not null,
	RoleId int not null foreign key references Roles
);
go

create table Buyers(
	BuyerId int identity(1,1) primary key,
	FirstName varchar(30) not null,
	LastName varchar(30) not null,
	Phone varchar(11) not null,
	Email varchar(50) not null,
	DOB date not null,
	Balance real null,
	Username varchar(30) not null,
	Password varchar(128) not null,
	RoleId int not null foreign key references Roles
);
go

create table ProductTypes(
	TypeId int identity(1,1) primary key,
	Name varchar(30) not null
);
go

create table Assignments(
	AssignmentId int identity(1,1) primary key,
	Name varchar(30) not null
);
go


create table Products(
	ProductId int identity(1,1) primary key,
	Name varchar(50) not null,
	Quantity int null,
	Price real not null,
	TypeId int not null foreign key references ProductTypes
);
go

create table AssignmentsProducts(
	AssignmentId int not null foreign key references Assignments,
	ProductId int not null foreign key references Products
);
go

create table Suppliers(
	SupplierId int identity(1,1) primary key,
	Name varchar(30) not null,
);
go

create table SuppliersProducts(
	SuppliersProductsId int identity(1,1) primary key,
	ProductId int not null foreign key references Products,
	SupplierId int not null foreign key references Suppliers,
	Price real not null
);
go

create table Purchases(
	PurchaseId int identity(1,1) primary key,
	BuyerId int not null foreign key references Buyers,
	TotalCost real not null,
	PurchaseDate date not null,
	foreign key (BuyerId) references Buyers on delete cascade
);
go

create table PurchaseDetails(
	PurchaseDetailsId int identity(1,1) primary key,
	PurchaseId int not null foreign key references Purchases,
	SuppliersProducts int not null foreign key references SuppliersProducts,
	Quantity int null,
	Cost real not null,
	foreign key (PurchaseId) references Purchases on delete cascade
);
go

create table Orders(
	OrderId int identity(1,1) primary key,
	ClientId int not null foreign key references Clients,
	TotalCost real not null,
	PurchaseDate date not null,
	foreign key (ClientId) references Clients on delete cascade
);
go

create table OrderDetails(
	OrderDetailsId int identity(1,1) primary key,
	OrderId int not null foreign key references Orders,
	ProductId int not null foreign key references Products,
	Quantity int null,
	Cost real not null,
	foreign key (OrderId) references Orders on delete cascade
);
go

create table Plans(
	PlanId int identity(1,1) primary key,
	ManagerId int not null foreign key references Managers,
	Revenue real not null,
	MoneyEarn real null,
	MoneySpent real null,
	OrderQuantity int null,
	PurchaseQuantity int null,
	CreationDate date not null,
	LastDate date not null,
	Status varchar(32) not null,
	Message varchar(256) null
);
go

create trigger updatePlanAfterOrder on Orders
for insert as
set nocount on
update Plans set OrderQuantity = OrderQuantity + 1 where PlanId=(select max(PlanId) from Plans)
update Plans set MoneyEarn = MoneyEarn + (select TotalCost from Orders where OrderId=(select max(OrderId) from Orders))
where PlanId=(select max(PlanId) from Plans)
go

create trigger updatePlanAfterPurchase on Purchases
for insert as
set nocount on
update Plans set PurchaseQuantity = PurchaseQuantity + 1 where PlanId=(select max(PlanId) from Plans)
update Plans set MoneySpent = MoneySpent + (select TotalCost from Purchases where PurchaseId=(select max(PurchaseId) from Purchases))
where PlanId=(select max(PlanId) from Plans) 
go
