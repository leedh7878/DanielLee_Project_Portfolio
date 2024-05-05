Create Table Brands(
    brand_id INTEGER PRIMARY KEY,
    brand_name VARCHAR NOT NULL
);

Create Table Categories(
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR NOT NULL
);

Create Table Stores(
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR NOT NULL,
    phone CHAR(14),
    email VARCHAR,
    street VARCHAR,
    city VARCHAR,
    state CHAR(2),
    zip_code CHAR(5)
);

Create Table Customers(
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR,
    phone CHAR(14),
    email VARCHAR NOT NULL,
    street VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    state CHAR(2),
    zip_code CHAR(5)
);

Create Table Staffs(
    staff_id INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone CHAR(14),
    active INTEGER DEFAULT 1,
    store_id INTEGER,
    manager_id INTEGER,
    FOREIGN KEY(store_id) REFERENCES Stores(store_id),
    FOREIGN KEY(manager_id) REFERENCES Staffs(staff_id)
);

Create Table Orders(
    order_id INTEGER PRIMARY KEY, 
    customer_id INTEGER NOT NULL,
    order_status INTEGER NOT NULL,
    order_date DATE,
    required_date DATE,
    shipped_date DATE,
    store_id INTEGER,
    staff_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (store_id) REFERENCES Stores(store_id),
    FOREIGN KEY (staff_id) REFERENCES Staffs(staff_id)
);

Create Table Products(
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR NOT NULL,
    brand_id INTEGER,
    category_id INTEGER,
    model_year INTEGER,
    list_price DECIMAL(8,2),
    FOREIGN KEY(brand_id) REFERENCES Brands(brand_id),
    FOREIGN KEY(category_id) REFERENCES Categories(category_id)
);


Create Table Order_Items(
    order_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    product_id INTEGER,
    list_price DECIMAL(8,2),
    discount DECIMAL(3,2),
    PRIMARY KEY(order_id, item_id),
    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);



Create Table Stocks(
    store_id INTEGER,
    product_id INTEGER,
    quantity INTEGER DEFAULT 0,
    FOREIGN KEY(store_id) REFERENCES Stores(store_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
);
