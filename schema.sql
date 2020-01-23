CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  acctype TEXT NOT NULL,
  password TEXT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);


CREATE TABLE stocks (

  id Integer Primary key autoincrement,
  ticker text not null,
  company text not null,
  industry text not null,
  sector text 
  

);

CREATE TABLE stockselect (
  stock_id integer,
  user_id Integer,
  primary key(stock_id,user_id),
  foreign key (user_id) references user (id)
  on delete  cascade on update no action ,
  foreign key (stock_id) references stocks (id)
  on delete  cascade on update no action 
);