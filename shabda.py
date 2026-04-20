import json
from DB import DB
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

INSERT_SHA = """INSERT INTO shabda (sha_urlid, sha_word, sha_linga, sha_artha, sha_artha_hind, sha_artha_eng, sha_sk, sha_lsk, sha_vyutpatti, sha_shabda_notes, sha_info, sha_prakriya_options, sha_forms, sha_zbaseindex) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");"""
DB_NAME = "shabda.db"

def parse_shabda(db):
    with open("shabda.txt") as file_sha:
        sha_json = json.load(file_sha)
        sha_lst = sha_json['data']
        rows = []
        for shabda in sha_lst:
            word = transliterate(shabda['word'], sanscript.DEVANAGARI, sanscript.SLP1)
            artha = transliterate(shabda['artha'], sanscript.DEVANAGARI, sanscript.SLP1)
            forms = transliterate(shabda['forms'], sanscript.DEVANAGARI, sanscript.SLP1)
            vyutpatti = shabda['vyutpatti']
            if len(vyutpatti) > 0:
                vyutpatti = transliterate(vyutpatti, sanscript.DEVANAGARI, sanscript.SLP1).replace("\"", "'")
            shabda_notes = shabda['shabda_notes']
            if len(shabda_notes) > 0:
                shabda_notes = transliterate(shabda_notes, sanscript.DEVANAGARI, sanscript.SLP1).replace("\"", "'")
            info = shabda['info']
            if len(info) > 0:
                info = transliterate(info, sanscript.DEVANAGARI, sanscript.SLP1).replace("\"", "'")
            prakriya_options_lst = []
            for option, flag in shabda['prakriya_options'].items():
                if flag:
                    prakriya_options_lst.append(transliterate(option, sanscript.DEVANAGARI, sanscript.SLP1)) 
            prakriya_options = ";".join(prakriya_options_lst)
            row = INSERT_SHA.format(shabda['urlid'], word, shabda['linga'], artha, 
                                    shabda['artha_hin'], shabda['artha_eng'], shabda['sk'],
                                    shabda['lsk'], vyutpatti, shabda_notes, 
                                    info, prakriya_options, forms, shabda['zbaseindex'])
            rows.append(row)
        db.insert_rows(rows)

def load_shabda():
    db = DB(DB_NAME)
    db.initialize_database("shabdaInitDB.sql")
    parse_shabda(db)

def main():
    load_shabda()

if __name__ == '__main__':
    main()