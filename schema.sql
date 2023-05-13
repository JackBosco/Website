CREATE TABLE IP (
    IPv4Address VARCHAR(20) NOT NULL,
    PRIMARY KEY (IPv4Address),
    FOREIGN KEY (IPv4Address) REFERENCES Client(IPv4),
    FOREIGN KEY (IPv4Address) REFERENCES Request(IPv4)
);

CREATE TABLE Client(
    IPv4 VARCHAR(20) NOT NULL PRIMARY KEY,
    City VARCHAR(128) NOT NULL,
    State VARCHAR(32) NOT NULL,
    Country VARCHAR(32) NOT NULL,
    zip int NOT NULL,
    FOREIGN KEY (IPv4) REFERENCES IP(IPv4Address),
    FOREIGN KEY (IPv4) REFERENCES Services(IPv4)
);

CREATE TABLE Organization(
    OrgName VARCHAR(256) NOT NULL PRIMARY KEY,
    Ref VARCHAR(512),
    FOREIGN KEY (OrgName) REFERENCES Services(OrgName)
);

CREATE TABLE Services(
    OrgName varchar(256) NOT NULL,
    IPv4 varchar(20) NOT NULL,
    FOREIGN KEY (OrgName) REFERENCES Organization(OrgName),
    FOREIGN KEY (IPv4) REFERENCES Client(IPv4),
    PRIMARY KEY (OrgName, IPv4)
);

CREATE TABLE Request(
    IPv4 VARCHAR(20) NOT NULL,
    RenderPage VARCHAR(8),
    Method VARCHAR(7),
    TimeOfRequest DATETIME NOT NULL,
    FOREIGN KEY (IPv4) REFERENCES IP(IPv4Address),
    CONSTRAINT PK_Request PRIMARY KEY (IPv4, TimeOfRequest)
);