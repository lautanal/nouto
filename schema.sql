CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    date DATE,
    week_nr INTEGER,
    day_nr INTEGER,
    work_day BOOLEAN
);
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    postcode TEXT,
    phone TEXT,
    email TEXT,
    instructions TEXT
);
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers,
    date_id INTEGER REFERENCES calendar,
    time_frame INTEGER,
    task_type INTEGER,
    description TEXT,
    time_required INTEGER,
    price INTEGER,
    discount INTEGER,
    deleted BOOLEAN
);
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES calendar,
    p1 INTEGER,
    p2 INTEGER,
    p3 INTEGER,
    p4 INTEGER
);
CREATE TABLE offtimes (
    id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES calendar,
    p1 INTEGER,
    p2 INTEGER,
    p3 INTEGER,
    p4 INTEGER
);


