BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "messages" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"regex_str"	TEXT NOT NULL,
	"resp"	TEXT NOT NULL,
	"is_on"	TEXT,
	"is_off"	TEXT,
	"set_on"	TEXT,
	"set_off"	TEXT,
	"next"	TEXT,
	"set_name"	TEXT NOT NULL
);
COMMIT;
