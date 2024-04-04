PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            );
INSERT INTO users VALUES(1,'admin','admin','admin@gmail.com',0);
INSERT INTO users VALUES(2,'Okech','Justcause2!','prevyneoketch6@gmail.com',0);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',2);
COMMIT;
