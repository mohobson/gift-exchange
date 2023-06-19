CREATE TABLE PARTICIPANT (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PARTICIPANT VARCHAR(80) NOT NULL,
    EMAIL VARCHAR(80) NOT NULL
);

CREATE TABLE COUPLE (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PARTNERONE VARCHAR(80) NOT NULL,
    PARTNERTWO VARCHAR(80) NOT NULL
);

CREATE TABLE ASSIGNMENT (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAMEONE VARCHAR(80) NOT NULL,
    NAMETWO VARCHAR(80) NOT NULL
);