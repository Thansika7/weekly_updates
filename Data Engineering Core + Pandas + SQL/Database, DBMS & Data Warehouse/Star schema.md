# Sales Data Warehouse – Star Schema (MySQL)

## Tables

### Fact Table
    -> Fact_sales

### Dimension Tables
    -> Customer_dt
    -> Product_dt
    -> Store_dt

### Database
    -> Database Name: sales

        USE sales;
        SELECT DATABASE();

### Dimention Tables

#### 1. Customer Table: 

        CREATE TABLE Customer_dt(
        Customer_ID INT PRIMARY KEY,
        Customer_Name VARCHAR(100),
        Age INT,
        Mobile_No INT,
        City VARCHAR(50)
        );

#### 2. Product Table: 

        CREATE TABLE Product_dt(
        Product_ID INT PRIMARY KEY,
        Product_Name VARCHAR(100),
        Catogory VARCHAR(100),
        Price DECIMAL(10,2)
        );

#### 3. Store Table: 

        CREATE TABLE Store_dt(
        Store_ID INT PRIMARY KEY,
        Store_Name VARCHAR(20),
        Branch VARCHAR(30)
        );


### Fact Table

        CREATE TABLE Fact_sales(
        Sales_ID INT PRIMARY KEY AUTO_INCREMENT,
        Customer_ID INT,
        Product_ID INT,
        Store_ID INT,
        Quantity INT,
        Total_amount DECIMAL(10,2),

        FOREIGN KEY (Customer_ID) REFERENCES Customer_dt(Customer_ID),
        FOREIGN KEY (Product_ID) REFERENCES Product_dt(Product_ID),
        FOREIGN KEY (Store_ID) REFERENCES Store_dt(Store_ID)
        );


## Sample Data Insertion

### Dimention tables

#### 1. Customer
        INSERT INTO Customer_dt VALUES (1,'Thansika', 20, 6789054321, 'Coimbatore');
        INSERT INTO Customer_dt VALUES (2, 'Fathima', 21, 9087654321, 'Coonoor');
        INSERT INTO Customer_dt VALUES(3, 'Tara', 20, 8907654321, 'Coimbatore');
        INSERT INTO Customer_dt VALUES(3, 'Thanisha', 21, 2345167890, 'Ooty');

#### 2. Product
        INSERT INTO Product_dt VALUES (01, 'Laptop', 'Electronics', 70000);
        INSERT INTO Product_dt VALUES (02, 'Airpots', 'Gadgets', 1500);
        INSERT INTO Product_dt VALUES (03, 'CPU', 'Electronics', 60000);
        INSERT INTO Product_dt VALUES (04, 'Smart Watch', 'Gadgets', 12000);

### 3. Store
        
        INSERT INTO Store_dt VALUES (001, 'Vasanth&Co', 'Crosscut');
        INSERT INTO Store_dt VALUES (002, 'Sathya', 'Vadavalli');

### Fact table

        INSERT INTO Fact_sales (Customer_ID,Product_ID,Store_ID, Quantity,Total_amount) VALUES (1, 01, 001, 2, 140000);
        INSERT INTO Fact_sales (Customer_ID,Product_ID,Store_ID, Quantity,Total_amount) VALUES (2, 02, 002, 1, 1500);


## Execution
        SELECT * FROM Fact_sales;
        SELECT * FROM Store_dt;
        SELECT * FROM Customer_dt;
        SELECT * FROM Product_dt;