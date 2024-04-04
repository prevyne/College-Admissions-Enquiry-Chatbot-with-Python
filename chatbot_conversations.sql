PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE conversations (
        id INTEGER PRIMARY KEY,
        user_input TEXT,
        bot_response TEXT,
        timestamp TEXT,
        username TEXT
    );
INSERT INTO conversations VALUES(1,'Hello','Hi','2024-04-03 08:35:50','Okech');
INSERT INTO conversations VALUES(2,'Tell me about fee','FEE PAYMENT New Reporting students Fees should be made to any of the below fee collection bank accounts integrated with student finance ERP module; New & Reporting students to indicate reference number indicated on the top of your admission letter eg. Ref: XX/YYYY For more Fee detail visit <a target="_blank" href="https://kabarak.ac.ke/payment"> Kabarak fees and payment</a>','2024-04-03 08:36:16','Okech');
INSERT INTO conversations VALUES(3,'Thanks','I am glad I helped you','2024-04-03 08:36:26','Okech');
INSERT INTO conversations VALUES(4,'Admissions office contact info','contact info','2024-04-03 08:37:18','Okech');
INSERT INTO conversations VALUES(5,'Admissions office contact','You can contact admissions office at: 072923370 or admissions@kabarak.ac.ke','2024-04-03 08:37:31','Okech');
INSERT INTO conversations VALUES(6,'Thanks','I am glad I helped you','2024-04-03 08:37:50','Okech');
COMMIT;
