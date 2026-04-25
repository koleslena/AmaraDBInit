import json

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from psycopg2.extras import Json


FILE_TINS = "dhatuforms_kartari.txt"

FILE_DHATU = "data.txt"

INS_DHATU = """
            INSERT INTO dhatu (word, tin, tins, gana, pada)
            VALUES (%s, %s, %s, %s, %s);
            """

def parse_tinanta(conn):
    cur = None
    try:
        with open(FILE_DHATU, 'r', encoding='utf-8') as f:
            data_file = json.load(f)

        with open(FILE_TINS, 'r', encoding='utf-8') as f:
            tins_file = json.load(f)

        cur = conn.cursor()
        
        if 'data' not in data_file:
            return
        
        for item in data_file['data']:
            if "dhatu" in item:
                baseindex = item['baseindex']
                gana = item['gana']
                pada = item['pada']
                word = transliterate(item['dhatu'], sanscript.DEVANAGARI, sanscript.SLP1)

                if baseindex in tins_file:
                    forms = tins_file[baseindex]
                    for elem in forms.items():
                        tin = elem[0]
                        tins = [transliterate(it, sanscript.DEVANAGARI, sanscript.SLP1) for it in elem[1].split(';')]

                        cur.execute(INS_DHATU, (word, tin, Json(tins), gana, pada))
                        print(f" [DHATU] Добавлено слово: {word} -> для формы: {tin}")

        conn.commit()
        print(f" [DHATU] commit")
    except Exception as e:
        print(f"❌ Ошибка при импорте: {e.with_traceback()}")
        if conn: conn.rollback()
    finally:
        if conn:
            if cur:
                cur.close()
            conn.close()

