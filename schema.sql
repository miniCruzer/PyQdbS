drop table if exists quotes;

create table quotes (
	id integer primary key autoincrement,
	channel text,
	nickname text,
	quote text not null,
	timestamp timestamp default current_timestamp
);