CREATE TABLE Employees (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Department NVARCHAR(50),
    Salary FLOAT,
    PhoneNumber NVARCHAR(20),
    IsActive BIT DEFAULT 1
);
