PRAGMA encoding = "UTF-8";
ATTACH DATABASE 'application.db' AS "dbname";
PRAGMA dbname.encoding;

CREATE TABLE "comments" (
	"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name" TEXT NOT NULL,
	"surname" TEXT NOT NULL,
	"patronymic" TEXT,
	"city_id" INTEGER,
	"region_id"	INTEGER,
	"email"	TEXT,
	"phone"	TEXT,
	"text" TEXT NOT NULL
);

CREATE TABLE "region" (
	"id" INTEGER NOT NULL PRIMARY KEY,
	"name" TEXT NOT NULL
);

CREATE TABLE "city" (
	"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"region_id" INTEGER NOT NULL,
	"name" TEXT NOT NULL
);

INSERT INTO city (region_id, name) VALUES
    (0, 'Город не указан'),
    (1, 'Ставрополь'),
    (1, 'Кисловодск'),
    (1, 'Пятигорск'),
    (2, 'Ростов'),
    (2, 'Шахты'),
    (2, 'Батайск'),
    (3, 'Краснодар'),
    (3, 'Крапоткин'),
    (3, 'Славянск');

INSERT INTO region (id, name) VALUES
    (0, 'Регион не указан'),
    (1, 'Ставропольский край'),
    (2, 'Ростовская область'),
    (3, 'Краснодарский край');

