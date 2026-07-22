CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL
);

CREATE TABLE houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    house_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    rent_amount FLOAT NOT NULL,
    house_type VARCHAR(50) NOT NULL,
    availability_status VARCHAR(30) NOT NULL
);

CREATE TABLE tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    aadhaar_number VARCHAR(20) UNIQUE NOT NULL,
    house_id INTEGER UNIQUE NOT NULL,
    move_in_date DATE NOT NULL,
    agreement_end_date DATE NOT NULL,
    FOREIGN KEY (house_id) REFERENCES houses(id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL,
    payment_month VARCHAR(20) NOT NULL,
    amount FLOAT NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    UNIQUE (tenant_id, payment_month),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);
