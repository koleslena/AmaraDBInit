-- Создание таблиц в SQLite

CREATE TABLE shlokas (
   sh_id INTEGER PRIMARY KEY AUTOINCREMENT,
   sh_text_line1 TEXT NOT NULL,
   sh_text_line2 TEXT NOT NULL,
   sh_number TEXT NOT NULL
);

CREATE TABLE words (
   w_id INTEGER PRIMARY KEY AUTOINCREMENT,
   w_word TEXT NOT NULL,
   w_artha TEXT NOT NULL,
   w_linga TEXT NOT NULL,
   w_synonyms TEXT NOT NULL,
   w_shloka_id INTEGER NOT NULL,
   FOREIGN KEY (w_shloka_id) REFERENCES shlokas(sh_id) ON DELETE CASCADE
);