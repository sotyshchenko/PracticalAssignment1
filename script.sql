use practice;


DROP TABLE if exists accounts;


CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    balance DECIMAL(10, 2)
);


INSERT INTO accounts (name, balance) 
VALUES 
('Alice', 1000.00), 
('Bob', 1500.00);


select * from accounts a 