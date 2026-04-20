
-- Создание таблиц в SQLite

CREATE TABLE shabda (
   sha_id INTEGER PRIMARY KEY AUTOINCREMENT,
   sha_urlid TEXT NOT NULL,
   sha_word TEXT NOT NULL,
   sha_artha TEXT,
   sha_artha_eng TEXT,
   sha_artha_hind TEXT,
   sha_linga TEXT,
   sha_sk TEXT,
   sha_lsk TEXT,
   sha_shabda_notes TEXT,
   sha_forms TEXT,
   sha_zbaseindex TEXT,
   sha_vyutpatti TEXT,
   sha_info TEXT,
   sha_prakriya_options TEXT
);