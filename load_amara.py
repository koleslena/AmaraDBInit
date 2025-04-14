import csv
from InitDB import initialize_database, insert_rows, get_list
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

SHLOKAS_TABLE = "shlokas"
INSERT_SH = f"INSERT INTO {SHLOKAS_TABLE} (sh_text_line1, sh_text_line2, sh_number) " + """VALUES ("{}", "{}", "{}");"""
INSERT_W = """INSERT INTO words (w_word, w_artha, w_linga, w_synonyms, w_shloka_id) VALUES ("{}", "{}", "{}", "{}", {});"""


def load_amara():
    initialize_database("InitDB.sql")
    load_shlokas()
    load_words()

def load_shlokas():
    with open("shlokas.csv", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        rows = list(reader)
        shlokas = []
        for row in rows:
            sh_lines = row[0].split("।")
            new_sh_1 = transliterate(sh_lines[0].lstrip(), sanscript.DEVANAGARI, sanscript.SLP1)
            new_sh_2 = transliterate(sh_lines[1].replace('"', "").lstrip(), sanscript.DEVANAGARI, sanscript.SLP1).replace("..", "")
            sh = INSERT_SH.format(new_sh_1, new_sh_2, row[1].lstrip().rstrip())
            shlokas.append(sh)

        insert_rows(shlokas)
        
def load_words():

    shlokas_lst = get_list(SHLOKAS_TABLE)
    shlokas = dict([(sh[3], sh[0]) for sh in shlokas_lst])

    syns = []
    with open("synonyms.csv", newline="") as csv_syn_file:
        reader = csv.reader(csv_syn_file, delimiter=",")
        syns = list(reader)

    with open("words.csv", newline="") as csv_words_file:
        reader = csv.reader(csv_words_file, delimiter=",")
        words = list(reader)
        rows = []
        for i in range(len(words)):
            word = transliterate(words[i][0], sanscript.DEVANAGARI, sanscript.SLP1)
            artha = transliterate(syns[i][1], sanscript.DEVANAGARI, sanscript.SLP1)
            syn = transliterate(syns[i][2], sanscript.DEVANAGARI, sanscript.SLP1)
            row = INSERT_W.format(word, artha, words[i][1], syn, shlokas[words[i][2]])
            rows.append(row)

        insert_rows(rows)

        