BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "states" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"set_name"	TEXT NOT NULL UNIQUE,
	"default_state"	TEXT
);
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
INSERT INTO "states" VALUES (1,'intro','room1');
INSERT INTO "messages" VALUES (1,'.','You can''t seem to take your eyes off the ring. It''s so pretty.','ring',NULL,NULL,NULL,NULL,'intro');
INSERT INTO "messages" VALUES (2,'help','Try looking around.','room1',NULL,NULL,NULL,NULL,'intro');
INSERT INTO "messages" VALUES (3,'help','How did you get here without learning to look around?',NULL,'room1',NULL,NULL,NULL,'intro');
INSERT INTO "messages" VALUES (4,'look','You are in a dusty cave. There is a door to the north and a door to the west.','room1',NULL,NULL,NULL,NULL,'intro');
INSERT INTO "messages" VALUES (5,'north|up','You move north through the doorway. Things don''t smell so good.','room1',NULL,'room2','room1','look','intro');
INSERT INTO "messages" VALUES (6,'west|left','You go west, my friend.','room1',NULL,'room3','room1','look','intro');
INSERT INTO "messages" VALUES (7,'look','This room is filled with piles of trash. Amongst the trash is a lovely blue key.','room2','key','',NULL,NULL,'intro');
INSERT INTO "messages" VALUES (8,'look','This room is filled with piles of trash.','room2,key','','','','','intro');
INSERT INTO "messages" VALUES (9,'back|south|exit','You return the way you came. That was a gross place.','room2',NULL,'room1','room2','look','intro');
INSERT INTO "messages" VALUES (10,'key','You snatch up the blue key. It''s pretty!','room2','key','key',NULL,NULL,'intro');
INSERT INTO "messages" VALUES (11,'look','A small chest is sitting in the middle of this empty room. There is a lock on it. The only exit is the way you entered.','room3','chest_open','','','','intro');
INSERT INTO "messages" VALUES (12,'look','An open chest is sitting in the middle of this empty room. The door to the east returns the way you came.','room3,chest_open','','','','','intro');
INSERT INTO "messages" VALUES (13,'back|east|exit','You return the way you came. That room was creepy anyway.','room3',NULL,'room1','room3','look','intro');
INSERT INTO "messages" VALUES (14,'key|lock|chest','You try to open the chest, but it won''t budge. Perhaps if you had the key?','room3','key,chest_open',NULL,NULL,NULL,'intro');
INSERT INTO "messages" VALUES (15,'key|lock|chest','You open the chest to reveal a beautiful golden ring. Plucking it from the velvety interior, you slip in onto your finger. It feels cool and heavy, and you have the sense that this was a mistake.','room3,key','chest_open','ring,chest_open','',NULL,'intro');
COMMIT;
