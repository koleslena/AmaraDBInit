import json

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from psycopg2.extras import Json

INS_SUB = """
            INSERT INTO subanta (name, description) 
            VALUES (%s, %s) 
            ON CONFLICT (name) DO NOTHING;
            """
INS_ZAB = """
            INSERT INTO zabda (word, stem, subs)
            VALUES (%s, %s, %s);
            """

FILE_ZABDA = "shabda.txt"


linga_map = {
        'P': {'ru': 'мужской род', 'en': 'masculine'},
        'S': {'ru': 'женский род', 'en': 'feminine'},
        'N': {'ru': 'средний род', 'en': 'neuter'},
        'A': {'ru': '', 'en': ''}
    }

def parse_subanta(conn):
    cur = None
    try:
        with open(FILE_ZABDA, 'r', encoding='utf-8') as f:
            data_file = json.load(f)

        cur = conn.cursor()
        
        if 'data' not in data_file:
            return
        
        for item in data_file['data']:
            if "word" in item:
                word = transliterate(item['word'], sanscript.DEVANAGARI, sanscript.SLP1)
            
                end = word[-1]
                if word[-1] not in ['a', 'A', 'i', 'I', 'u', 'U', 'e', 'E', 'o', 'O', 't', 'f', 'd', 'T'] and len(word) > 1:
                    end = word[-2:]

                if "prakriya_options" in item and item["prakriya_options"].get("सर्वादीनि_सर्वनामानि", False):
                    end = word
                
                linga = item['linga']

                if 'forms' in item:
                    forms_no_splited = [transliterate(form, sanscript.DEVANAGARI, sanscript.SLP1) for form in item['forms'].split(';')]
                    forms = [",".join([f for f in form.split('-') if len(f) > 0]) for form in forms_no_splited]
                    for i in range(1, 9):
                        subs = forms[(i - 1) * 3: i* 3]
                        if len([s for s in subs if len(s) > 0]) > 0:
                            sub = f'{i}_{end}_{linga}'
                            description_dict = {'en': f'-{end} stem {linga_map[linga]['en']}', 'ru': f'основа на -{end} {linga_map[linga]['ru']}'}
                            cur.execute(INS_SUB, (sub, Json(description_dict)))
                            print(f" [SUBANTA] Обработана форма: {sub}")
                            cur.execute(INS_ZAB, (word, sub, Json(subs)))
                            print(f" [ZABDA] Привязано слово: {word} -> к форме: {sub}")

        conn.commit()
        print(f" [ZABDA] commit")
    except Exception as e:
        print(f"❌ Ошибка при импорте: {e.with_traceback()}")
        if conn: conn.rollback()
    finally:
        if conn:
            if cur:
                cur.close()
            conn.close()

