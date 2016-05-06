Ernie Forzano
Herbert Gutierrez

CS327E: Supreme Nova


This file includes the create statements used to make your own tables to be compatible to our code

Notes
- In order to populate your database you must run lastfm_parse.py
- To run the UI select lastfm_user.py


Tables (3)


CREATE TABLE bandList
(bandID INT NOT NULL AUTO_INCREMENT,
bandName varchar(200),
genre varchar(200),
PRIMARY KEY (bandID));


CREATE TABLE similarBand
(bandID INT NOT NULL AUTO_INCREMENT,
bandName varchar(200),
genre varchar(200),
PRIMARY KEY (bandID),
similarBandID INT,
similarBandName varchar(200),
FOREIGN KEY (similarBandID) REFERENCES bandList(bandID));


CREATE TABLE event
(eventID INT NOT NULL AUTO_INCREMENT,
state varchar(20),
city varchar(200),
venue varchar(200),
date DATE,
time TIME,
PRIMARY KEY(eventID),
bandID INT,
bandName varchar(200),
FOREIGN KEY (bandID) REFERENCES bandList(bandID));
