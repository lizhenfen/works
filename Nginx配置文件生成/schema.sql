create table proxy_info (
  `id` int PRIMARY KEY auto_increment,
  `ip` VARCHAR(64) not NULL ,
  `backstage` VARCHAR(2048)
);



create table proxy_info (
  `ip` VARCHAR(64) PRIMARY KEY,
  `backstage` VARCHAR(2048)
);