USE fintrust; 

-- Create branch tables
CREATE TABLE IF NOT EXISTS branches(
	branch_id INT PRIMARY KEY AUTO_INCREMENT,
    branch_name VARCHAR(150) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- add branch column to branch table
ALTER TABLE accounts
ADD COLUMN branch_id INT NULL,
ADD CONSTRAINT fk_accounts_branches
	FOREIGN KEY (branch_id)
    REFERENCES branches(branch_id);
    
-- branch samples
INSERT INTO branches
	(branch_name. province, city)
VALUES
	('Sandton City Branch', 'Gauteng', 'Johannesburg'),
    ('Cape Town CBD Branch', 'Western Cape', 'Cape Town'),
    ('Gateway Branch', 'KwaZulu-Natal', 'Durban');
    
-- Account Updates
UPDATE accounts
SET branch_id = 1
WHERE account_id = 1;

UPDATE accounts
SET branch_id = 2
WHERE accounts_id = 6;

-- Verify results
SELECT a.account_id, a.account_number, a.account_type, b.branch_name, b.city, b.province
FROM accounts a
LEFT JOIN branches b
	ON a.branch_id = b.branch_id;