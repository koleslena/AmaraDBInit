-- Создаем таблицу для типов основ имен (Subanta-prātipadika)
CREATE TABLE IF NOT EXISTS subanta (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description JSONB NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS subanta_name_unique ON subanta (name);

-- Таблица для глагольных типов окончаний (Tinanta-dhātu)
CREATE TABLE IF NOT EXISTS tinanta (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description JSONB NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS tinanta_name_unique ON tinanta (name);

-- Таблица для слов (Shabda/Zabda) — конкретные лексемы
-- stem ссылается на name в таблице subanta или tinanta
CREATE TABLE IF NOT EXISTS zabda (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255) NOT NULL,
    subs JSONB NOT NULL,        -- готовые парадигмы (3 формы для 3 лиц) для разных падежей 
    stem VARCHAR(255) NOT NULL
);

-- Таблица корней (Dhatu)
CREATE TABLE IF NOT EXISTS dhatu (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255) NOT NULL, -- сам корень (например, 'bhū', 'gam')
    tin VARCHAR(255) NOT NULL,
    tins JSONB NOT NULL,        -- готовые парадигмы (сетки 3x3) для разных лакаров
    gana INTEGER CHECK (gana >= 1 AND gana <= 10), -- класс глагола
    pada CHAR(1) CHECK (pada IN ('P', 'A', 'U'))  -- Parasmaipada, Atmanepada, Ubhayapada 
);

-- Таблица пользователей (tg_users)
-- Мы не используем SERIAL для id, так как будем вставлять user_id из Telegram API
CREATE TABLE IF NOT EXISTS tg_users (
    user_id BIGINT PRIMARY KEY, -- Telegram ID может быть очень большим
    passed JSONB DEFAULT '[]'::jsonb, -- список ID пройденных заданий или корней
    current_score JSONB DEFAULT '{}'::jsonb -- прогресс (например, {"noun": 10, "verb": 5})
);

-- Индексы для производительности
CREATE INDEX IF NOT EXISTS idx_subanta_name ON subanta (name);
CREATE INDEX IF NOT EXISTS idx_tinanta_name ON tinanta (name);
CREATE INDEX IF NOT EXISTS idx_zabda_stem ON zabda (stem);
CREATE INDEX IF NOT EXISTS idx_dhatu_gana ON dhatu (gana);

INSERT INTO tinanta (name, description) VALUES 
-- PARASMAIPADA (P-)
('plat', '{"en": "Present Tense (laṭ-lakāra-parasmaipada / लट्लकार-परस्मैपद)", "ru": "Настоящее время (laṭ-lakāra-parasmaipada / लट्लकार-परस्मैपद)"}'),
('plit', '{"en": "Perfect Tense (liṭ-lakāra-parasmaipada / लिट्लकार-परस्मैपद)", "ru": "Прошедшее совершенное время (liṭ-lakāra-parasmaipada / लिट्लकार-परस्मैपद)"}'),
('plut', '{"en": "First Future Tense (luṭ-lakāra-parasmaipada / लुट्लकार-परस्मैपद)", "ru": "Будущее первое время (luṭ-lakāra-parasmaipada / लुट्लकार-परस्मैपद)"}'),
('plrut', '{"en": "Second Future Tense (lṛt-lakāra-parasmaipada / लृट्लकार-परस्मैपद)", "ru": "Будущее второе время (lṛt-lakāra-parasmaipada / लृट्लकार-परस्मैपद)"}'),
('plot', '{"en": "Imperative Mood (loṭ-lakāra-parasmaipada / लोट्लकार-परस्मैपद)", "ru": "Повелительное наклонение (loṭ-lakāra-parasmaipada / लोट्लकार-परस्मैपद)"}'),
('plang', '{"en": "Imperfect Tense (laṅ-lakāra-parasmaipada / लङ्लकार-परस्मैपद)", "ru": "Прошедшее несовершенное время (laṅ-lakāra-parasmaipada / लङ्लकार-परस्मैपद)"}'),
('pvidhiling', '{"en": "Potential Mood (vidhiliṅ-parasmaipada / विधिलिङ्-परस्मैपद)", "ru": "Желательное наклонение (vidhiliṅ-parasmaipada / विधिलिङ्-परस्मैपद)"}'),
('pashirling', '{"en": "Benedictive Mood (āśīrliṅ-parasmaipada / आशीर्लिङ्-परस्मैपद)", "ru": "Благопожелание (āśīrliṅ-parasmaipada / आशीर्लिङ्-परस्मैपद)"}'),
('plung', '{"en": "Aorist Tense (luṅ-lakāra-parasmaipada / लुङ्लकार-परस्मैपद)", "ru": "Аорист (luṅ-lakāra-parasmaipada / लुङ्लकार-परस्मैपद)"}'),
('plrung', '{"en": "Conditional Mood (lṛṅ-lakāra-parasmaipada / लृङ्लकार-परस्मैपद)", "ru": "Условное наклонение (lṛṅ-lakāra-parasmaipada / लृङ्लकार-परस्मैपद)"}'),

-- ATMANEPADA (A-)
('alat', '{"en": "Present Tense (laṭ-lakāra-ātmanepada / लट्लकार-आत्मनेपद)", "ru": "Настоящее время (laṭ-lakāra-ātmanepada / लट्लकार-आत्मनेपद)"}'),
('alit', '{"en": "Perfect Tense (liṭ-lakāra-ātmanepada / लिट्लकार-आत्मनेपद)", "ru": "Прошедшее совершенное время (liṭ-lakāra-ātmanepada / लिट्लकार-आत्मनेपद)"}'),
('alut', '{"en": "First Future Tense (luṭ-lakāra-ātmanepada / लुट्लकार-आत्मнеपद)", "ru": "Будущее первое время (luṭ-lakāra-ātmanepada / लुट्लकार-आत्मनेपद)"}'),
('alrut', '{"en": "Second Future Tense (lṛt-lakāra-ātmanepada / लृट्लकार-आत्मनेपद)", "ru": "Будущее второе время (lṛt-lakāra-ātmanepada / लृट्लकार-आत्मनेपद)"}'),
('alot', '{"en": "Imperative Mood (loṭ-lakāra-ātmanepada / लोट्लकार-आत्मनेपद)", "ru": "Повелительное наклонение (loṭ-lakāra-ātmanepada / लोट्लकार-आत्मनेपद)"}'),
('alang', '{"en": "Imperfect Tense (laṅ-lakāra-ātmanepada / लङ्लकार-आत्मनेपद)", "ru": "Прошедшее несовершенное время (laṅ-lakāra-ātmanepada / लङ्लकार-आत्मनेपद)"}'),
('avidhiling', '{"en": "Potential Mood (vidhiliṅ-ātmanepada / विधिलिङ्-आत्मनेपद)", "ru": "Желательное наклонение (vidhiliṅ-ātmanepada / विधिलिङ्-आत्मनेपद)"}'),
('aashirling', '{"en": "Benedictive Mood (āśīrliṅ-ātmanepada / आशीर्लिङ्-आत्मनेपद)", "ru": "Благопожелание (āśīrliṅ-ātmanepada / आशीर्लिङ्-आत्मनेपद)"}'),
('alung', '{"en": "Aorist Tense (luṅ-lakāra-ātmanepada / लुङ्लकार-आत्मनेपद)", "ru": "Аорист (luṅ-lakāra-ātmanepada / लुङ्लकार-आत्मनेपद)"}'),
('alrung', '{"en": "Conditional Mood (lṛṅ-lakāra-ātmanepada / लृङ्लकार-आत्मनेपद)", "ru": "Условное наклонение (lṛṅ-lakāra-ātmanepada / लृङ्लकार-आत्मनेपद)"}') 
ON CONFLICT (name) DO NOTHING;


