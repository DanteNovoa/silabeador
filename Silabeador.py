import pylabeador
import unidecode
import re
import pandas as pd

class Silabeador:

    def __init__(self, archivo):
        self.nospaces: list = []
        self.filename: str = ""
        self.lineas: list = []
        self.cleannedList: list = []
        self.listPalabras: dict = {}
        self.ordered: dict = {}
        self.lowerCase: list = []
        self.noaccent: list = []
        self.syllable_count: list = []
        self.g_words: list = []
        self.w_words: list = []
        self.syll_ite: list = []
        self.syll_sum: int = 0

        with open(archivo, encoding='utf-8') as f:
            self.filename = f.name.replace(".txt", "")
            rl = f.readlines()
            for l in rl:
                self.lineas.append(l.split(" "))
            for n in self.lineas:
                for x in n:
                    if len(x) > 1:
                        self.nospaces.append(x.replace("\n", ""))
            self.lowerCase = [l.lower() for l in self.nospaces]
            self.noaccent = [unidecode.unidecode(w) for w in self.lowerCase]
            for palabra in self.noaccent:
                cleanned_line = re.sub('[^A-Za-z0-9 ]+', '', palabra)
                self.cleannedList.append(cleanned_line)
            for w in self.cleannedList:
                self.listPalabras[w] = self.cleannedList.count(w)
            self.ordered = {k: v for k, v in sorted(self.listPalabras.items(), key=lambda item: item[1], reverse=True)}
            for word in self.ordered:
                try:
                    splitword = pylabeador.syllabify(word)
                    self.goodwords.append(word)
                    self.syllable_count.append(splitword)
                except:
                    self.w_words.append(word)
                    pass
                print(self.w_words, "palabras mal")
            for i in self.syllable_count:
                self.syll_ite.append(len(i))
            self.syll_sum = sum(self.syll_ite)
            dframe = pd.DataFrame(list(self.ordered.items()))
            dframe.to_csv(f'{self.filename}-wordcount.csv', encoding="utf-8")
            extra_lines = 'Estas lineas son extra y necesitan ser checadas manualmente: '
            with open(f'{self.filename.replace("letrasfold/", "")}extras.txt', 'w') as file:
                file.write(f'Cantidad de palabras: {len(self.listPalabras)}')
                file.write(f'Cantidad de silabas: {self.syll_sum}')
                file.write('\n')
                file.write(extra_lines)
                for w in self.w_words:
                    file.write(w)
                    file.write('\n')

