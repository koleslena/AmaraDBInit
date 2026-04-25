import json
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

FILE_ZABDA = "shabda.txt"


def main():
    try:
        with open(FILE_ZABDA, 'r', encoding='utf-8') as f:
            data_file = json.load(f)

        if 'data' not in data_file:
            return
        
        ends = {}
        for item in data_file['data']:
            if "word" in item:
                word = transliterate(item['word'], sanscript.DEVANAGARI, sanscript.SLP1)
            
                end = word[-1]
                if word[-1] not in ['a', 'A', 'i', 'I', 'u', 'U', 'e', 'E', 'o', 'O', 't', 'f', 'd', 'T'] and len(word) > 1:
                    end = word[-2:]

                if "prakriya_options" in item and item["prakriya_options"].get("सर्वादीनि_सर्वनामानि", False):
                    end = word

                if end in ends.keys():
                    ends[end].append(word)
                else:
                    ends[end] = [word]
                    
        print([elem for elem in ends.items() if elem[0] not in ['a', 'A', 'i', 'I', 'u', 'U', 'an', 'in', 'f', 't', 'as']])
    except Exception as e:
        print(f"❌ Ошибка при импорте: {e}")



if __name__ == '__main__':
    main()


    

