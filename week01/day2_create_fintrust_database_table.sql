-- Create and select the FinTrust database
CREATE DATABASE IF NOT EXISTS fintrust;
USE fintrust;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
  customer_id  INT           PRIMARY KEY AUTO_INCREMENT,
  first_name   VARCHAR(100) NOT NULL,
  last_name    VARCHAR(100) NOT NULL,
  id_number    VARCHAR(13)  UNIQUE,
  email        VARCHAR(200) UNIQUE NOT NULL,
  phone        VARCHAR(20),
  province     VARCHAR(50),
  created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
  account_id     INT             PRIMARY KEY AUTO_INCREMENT,
  customer_id    INT             NOT NULL,
  account_type   ENUM('CHEQUE','SAVINGS','CREDIT','BUSINESS') NOT NULL,
  account_number VARCHAR(20)    UNIQUE NOT NULL,
  balance        DECIMAL(15,2) DEFAULT 0.00,
  status         ENUM('ACTIVE','SUSPENDED','CLOSED') DEFAULT 'ACTIVE',
  opened_date    DATE            NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
  transaction_id   INT             PRIMARY KEY AUTO_INCREMENT,
  account_id       INT             NOT NULL,
  transaction_type ENUM('DEBIT','CREDIT','TRANSFER','PAYMENT') NOT NULL,
  amount           DECIMAL(15,2) NOT NULL,
  description      VARCHAR(500),
  merchant_category VARCHAR(100),
  transaction_date DATETIME        DEFAULT CURRENT_TIMESTAMP,
  reference_no     VARCHAR(50),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);