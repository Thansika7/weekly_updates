use laptop;

select database();

show tables;

ALTER TABLE laptop_data
RENAME COLUMN Company TO company,
RENAME COLUMN TypeName TO type_name,
RENAME COLUMN Inches TO screen_size,
RENAME COLUMN ScreenResolution TO screen_resolution,
RENAME COLUMN CpuType TO cpu,
RENAME COLUMN Ram TO ram,
RENAME COLUMN TotalMemory TO memory,
RENAME COLUMN Gpu TO gpu,
RENAME COLUMN OpSys TO operating_system,
RENAME COLUMN Price TO price;

ALTER TABLE laptop_data RENAME COLUMN S_No TO s_no;

SELECT * FROM laptop_data LIMIT 10;

ALTER TABLE laptop_data MODIFY ram INT;

SELECT ram FROM laptop_data LIMIT 10;

UPDATE laptop_data
SET ram = REPLACE(ram, 'GB', '');

ALTER TABLE laptop_data
MODIFY ram INT;

ALTER TABLE laptop_data ADD cpu_speed DECIMAL(4,2);

UPDATE laptop_data
SET cpu_speed = CAST(REPLACE(SUBSTRING_INDEX(Cpu,' ',-1),'GHz','') AS DECIMAL(4,2));

ALTER TABLE laptop_data MODIFY price DECIMAL (10,2);

SELECT COUNT(*) FROM laptop_data;

SELECT MIN(s_no), MAX(s_no) FROM laptop_data;

SELECT (MAX(s_no) - MIN(s_no) + 1) AS expected_rows,
COUNT(*) AS actual_rows
FROM laptop_data;

DELETE FROM laptop_data WHERE s_no IS NULL;

SELECT (MAX(s_no) - MIN(s_no) + 1) AS expected_rows,
COUNT(*) AS actual_rows
FROM laptop_data;

SELECT * 
FROM laptop_data
WHERE s_no IS NULL;

SELECT s_no, COUNT(*) 
FROM laptop_data
GROUP BY s_no HAVING COUNT(*) > 1;

ALTER TABLE laptop_data
MODIFY s_no INT NOT NULL;

ALTER TABLE laptop_data ADD PRIMARY KEY(s_no);

SELECT COUNT(*) AS total_rows 
FROM laptop_data;

SELECT 
SUM(Company IS NULL OR Company = '') AS missing_company,
SUM(Ram IS NULL) AS missing_ram,
SUM(Price IS NULL) AS missing_price
FROM laptop_data;

SELECT COUNT(*) 
FROM laptop_data
WHERE Ram <= 0;

SELECT * FROM laptop_data LIMIT 10;

UPDATE laptop_data
SET Cpu = REPLACE(Cpu, SUBSTRING_INDEX(Cpu, ' ', -1), '');

SELECT * FROM laptop_data LIMIT 10;

DELETE FROM laptop_data
WHERE s_no IS NULL 
   OR s_no = '' 
   OR s_no = 0;
   
SELECT COUNT(*) FROM laptop_data;

SELECT * FROM laptop_data LIMIT 10;