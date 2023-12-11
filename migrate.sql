Drop table if exists TradingData;
Drop table if exists FinancialData;
Drop table if exists IPO;
Drop table if exists Bankruptcy;
Drop table if exists Event;
Drop table if exists AnalystRating;
Drop table if exists Analyst;
Drop table if exists Firm;
Drop table if exists Comment;
Drop table if exists Stock;
Drop table if exists InternalUser;

-- Stock Table
CREATE TABLE Stock (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Symbol VARCHAR(5) NOT NULL
);

-- TradingData Table
CREATE TABLE TradingData (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    stockID INT,
    Date DATE,
    Volume FLOAT(16),
    Open FLOAT(16),
    High FLOAT(16),
    Low FLOAT(16),
    Close FLOAT(16),
    AdjustedClose FLOAT(16),

    FOREIGN KEY (stockID) REFERENCES Stock(ID)ON DELETE CASCADE ON UPDATE CASCADE
);

-- FinancialData Table
CREATE TABLE FinancialData (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    stockID INT,
    Year INT,
    Revenue FLOAT(16),
    RevenueGrowth FLOAT(16),
    CostofRevenue FLOAT(16),
    GrossProfit FLOAT(16),
    RDExpenses FLOAT(16),
    SGAExpenses FLOAT(16),
    OperatingExpenses FLOAT(16),
    OperatingIncome FLOAT(16),
    InterestExpense FLOAT(16),
    FOREIGN KEY (stockID) REFERENCES Stock(ID)ON DELETE CASCADE ON UPDATE CASCADE
);

-- Event Table
CREATE TABLE Event (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    stockID INT,
    Date DATE,
    Type ENUM('IPO', 'Bankruptcy'),
    FOREIGN KEY (stockID) REFERENCES Stock(ID)ON DELETE CASCADE ON UPDATE CASCADE
);

-- IPO Table
CREATE TABLE IPO (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    eventID INT,
    PricePerShare FLOAT(16),
    NumShares INT,
    FOREIGN KEY (eventID) REFERENCES Event(ID)ON DELETE CASCADE ON UPDATE CASCADE
);

-- Bankruptcy Table
CREATE TABLE Bankruptcy (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    eventID INT,
    FilingType ENUM('Chapter 11', 'Chapter 8'),
    FOREIGN KEY (eventID) REFERENCES Event(ID)ON DELETE CASCADE ON UPDATE CASCADE
);


-- User Table
CREATE TABLE InternalUser (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);


-- Firm Table
CREATE TABLE Firm (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
);

-- Analyst Table
CREATE TABLE Analyst (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    firmID INT,
    FOREIGN KEY (userID) REFERENCES InternalUser(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (firmID) REFERENCES Firm(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- AnalystRating Table
CREATE TABLE AnalystRating (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    stockID INT,
    analystID INT,
    Date DATE,
    Rating ENUM('Buy', 'Sell', 'Hold', 'Underperform', 'Outperform'),
    TargetPrice FLOAT(16),
    FOREIGN KEY (stockID) REFERENCES Stock(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (analystID) REFERENCES Analyst(ID) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Comment Table
CREATE TABLE Comment (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    stockID INT,
    Date DATE,
    FOREIGN KEY (userID) REFERENCES InternalUser(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (stockID) REFERENCES Stock(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

