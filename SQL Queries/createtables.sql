CREATE TABLE business (
business_id char(22) PRIMARY KEY,
name varchar(60) NOT NULL,
address varchar(75),
city varchar(30) NOT NULL,
postal_code varchar(7),
stars DECIMAL(2,1) CHECK (stars >= 1 AND stars <= 5),
review_count INT DEFAULT 0 CHECK (review_count >= 0)
);
CREATE TABLE user_yelp (
user_id char(22) PRIMARY KEY,
name varchar(35) NOT NULL,
review_count INT DEFAULT 0 CHECK (review_count >= 0),
yelping_since DATETIME NOT NULL DEFAULT GETDATE(),
useful INT NOT NULL DEFAULT 0 CHECK (useful >= 0),
funny INT NOT NULL DEFAULT 0 CHECK (funny >= 0),
cool INT NOT NULL DEFAULT 0 CHECK (cool >= 0),
fans INT NOT NULL DEFAULT 0 CHECK (fans >= 0),
average_stars DECIMAL(3,2) CHECK (average_stars >= 1 AND average_stars <= 5)
);
CREATE TABLE checkin (
checkin_id INT PRIMARY KEY,
business_id char(22) NOT NULL,
date DATETIME NOT NULL DEFAULT GETDATE(),
CONSTRAINT fk_business_id_check FOREIGN KEY (business_id) REFERENCES
business (business_id)
);
CREATE TABLE tip (
tip_id INT PRIMARY KEY,
user_id char(22) NOT NULL,
business_id char(22) NOT NULL,
date DATETIME NOT NULL DEFAULT GETDATE(),
compliment_count INT DEFAULT 0 CHECK (compliment_count >= 0),
CONSTRAINT fk_business_id_tip FOREIGN KEY (business_id) REFERENCES
business (business_id),
CONSTRAINT fk_user_id_tip FOREIGN KEY (user_id) REFERENCES user_yelp
(user_id)
);
CREATE TABLE friendship (
user_id char(22),
friend char(22),
PRIMARY KEY (user_id, friend),
CONSTRAINT fk_user_id_fri FOREIGN KEY (user_id) REFERENCES user_yelp
(user_id),
CONSTRAINT fk_friend FOREIGN KEY (friend) REFERENCES user_yelp (user_id)
);
CREATE TABLE review (
review_id char(22) PRIMARY KEY,
user_id char(22) NOT NULL,
business_id char(22) NOT NULL,
stars INT NOT NULL CHECK (stars >= 1 AND stars <= 5),
useful INT NOT NULL DEFAULT 0 CHECK (useful >= 0),
funny INT NOT NULL DEFAULT 0 CHECK (funny >= 0),
cool INT NOT NULL DEFAULT 0 CHECK (cool >= 0),
date DATETIME NOT NULL DEFAULT GETDATE(),
CONSTRAINT fk_business_id_rev FOREIGN KEY (business_id) REFERENCES
business (business_id),
CONSTRAINT fk_user_id_rev FOREIGN KEY (user_id) REFERENCES user_yelp
(user_id)
);