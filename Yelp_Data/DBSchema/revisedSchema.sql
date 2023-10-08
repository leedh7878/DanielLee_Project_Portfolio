CREATE TABLE Users(
	user_id CHAR(22),
	avg_stars DECIMAL,
	cool INTEGER,
	funny INTEGER,
	useful INTEGER,
	yelping_since DATE,
	name VARCHAR,
	fans INTEGER,
	tipCount INTEGER DEFAULT 0,
	totalLikes INTEGER DEFAULT 0,
	user_latitude VARCHAR,
	user_longitude VARCHAR,
	PRIMARY KEY(user_id)
);

Create Table Business(
    business_id CHAR(22) PRIMARY KEY,
    name VARCHAR,
    address VARCHAR NOT NULL,
    state CHAR(2) NOT NULL,
    city VARCHAR NOT NULL,
    zipcode INTEGER,
    latitude DECIMAL,
    longitude DECIMAL,
    stars DECIMAL,
    is_open BOOLEAN NOT NULL,
		numCheckins INTEGER DEFAULT 0,
		numTips INTEGER DEFAULT 0
);

CREATE TABLE Tip(
  business_id CHAR(22),
	user_id CHAR(22),
	tipDate timestamp,
	likes INT NOT NULL,
	tipText VARCHAR,
	PRIMARY KEY (business_id, user_id, tipDate),
	FOREIGN KEY (business_id) REFERENCES Business(business_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


CREATE TABLE friend(
    friend_id CHAR(22),
    user_id CHAR(22),
    avg_stars DECIMAL,
    cool INTEGER,
    funny INTEGER,
    useful INTEGER,
    yelping_since DATE,
    name VARCHAR,
    fans INTEGER,
    tipCount INTEGER DEFAULT 0,
    totalLikes INTEGER DEFAULT 0,
    user_latitude VARCHAR,
    user_longitude VARCHAR,
    PRIMARY KEY(friend_id, user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (friend_id) REFERENCES Users(user_id)

);

Create Table Categories(
    business_id CHAR(22),
    category_name VARCHAR,
    PRIMARY KEY (business_id, category_name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

Create Table Attributes(
    attr_name VARCHAR,
    business_id CHAR(22),
		value VARCHAR,
    PRIMARY KEY (business_id, attr_name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)

);

Create Table Hours(
    dayofweek VARCHAR,
    open TIME,
		close TIME,
    business_id CHAR(22),
    PRIMARY KEY (business_id, dayofweek),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)

);

CREATE TABLE Checkins(
	business_id CHAR(22),
	cdate timestamp,
	PRIMARY KEY (business_id,  cdate),
	FOREIGN KEY (business_id) REFERENCES Business (business_id)
);
