use spiders;

drop table if exists node;

CREATE TABLE node (
    id INT NOT NULL AUTO_INCREMENT,
    parent_id INT NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    `code` VARCHAR(258) NOT NULL,
    `level` int not null,
    url VARCHAR(512) NULL,
    create_time TIMESTAMP DEFAULT now(),
    update_time TIMESTAMP null,
    primary key(id)
)  ENGINE=INNODB;