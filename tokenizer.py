import re

class Tokenizer:
    def __init__(self, regex_rules, exception_lists):
        self.regex_rules = regex_rules
        self.exception_lists = exception_lists
    
    def tokenize(self, text):
        if type(text) == type(""):
            text = [text]
        text = self._apply_exception_lists(text)
        tokens = self._apply_regex_rules(text)
        return tokens
    
    def _apply_exception_lists(self, text):
        for exception_list in self.exception_lists:
            for exception in exception_list:
                for n in range(len(text)):
                    idx = n
                    if exception in text[n] and text[n] != exception.strip():
                        sublist = text[n].split(exception)
                        if text[n].endswith(exception):
                            a_list = [sublist[0].strip(), exception.strip()]
                        elif text[n].startswith(exception):
                            a_list = [exception.strip(), sublist[1].strip()]
                        else:
                            a_list = [sublist[0].strip(), exception.strip(), sublist[1].strip()]
                        del text[idx]
                        for el in a_list:
                            text.insert(idx, el)
                            idx +=1
                            
        return text

    
    def _apply_regex_rules(self, text):
        for regex_rule in self.regex_rules:
            second_text = []
            for el in text:
                second_text.append(el)
            idx = 0
            for substring in second_text:
                new_subtext = ""
                new_subtext_list = []
                if self._check_exceptions(substring):
                    new_subtext = re.sub(regex_rule, r' \1 ', substring)
                    new_subtext_list = new_subtext.split()
                    del text[idx]
                    for el in new_subtext_list:
                        text.insert(idx, el)
                        idx +=1
                else:
                    idx +=1
                
                            
        return text
    
    def _check_exceptions(self, substring):
        for exception_list in self.exception_lists:
            for exception in exception_list:
                if exception not in substring:
                    value = True
                elif exception in substring:
                    return False
        return value

# Regular expression rules
regex_rules = [
   
    r"([.,;:!¡?()])", #lasciando il punto e la virgola qui, i decimali e le mail non vengono tokenizzati.

    r'([\d]+[,\\.]+[\d\\.,]+[%]?)', #numeri comprese le percentuali -> non matcha i decimali
    
    r"([a-zA-Z]+[’\\']{1})", #articoli/preposizioni articolate con apostrofo -> "Dell'Anda"viene separato
        
    r'(:[)(pP])', #emoticon (servono anche qui?)

    r'([a-z][.][a-z][.])', 
    
    r'([a-z]+[\\.][a-z@]+[\\.]+[a-z]+)',#email ->non matcha  #r'([0-9_a-zA-Z.]+[@]{1}[a-z]+[\\.]{1}[a-z]+)',   #r'(/^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/)'
    r'(/^http://www[a-z]+/)' #url  oppure /\b(https?):\/\/([a-z\.]+)(\/[^ $]*)*/  -> mo match
   
    
]

# Exception lists
exception_lists = [
    # Abbreviations
    ['Ing.', 'Geom.', 'geom.', 'Avv.', 'prof.', 'dr.', 'dott.','racc.'],
    # Acronyms
    ['U.S.A.', 'U.E.', 'S.r.l.','c.a.', 'P.S.'],
    # Emoticons and emojis
    [':)', ':(', ';)', ':D', '<3',':P',':-)']
]

# Create tokenizer object
tokenizer = Tokenizer(regex_rules, exception_lists)

# Tokenize text
text = """Questo è un test di tokenizzazione, e vediamo come va, perché ci serve 
caro dott. Dell'Anda. Io credevo che la batteria dell'automobile fosse 
ok; ma in realtà non lo è.
Le lascio il mio email f.tambu@unibo.it e la mia URL http://www.unibo.it 
così controlla.
Io sono l'Ing. Geom. geom. Avv. prof. dr. Pincopallo e andrò negli 
U.S.A. e vediamo se mi compri una S.r.l. e poi la mettiamo
alla c.a. di Luigi come p.es. la racc.

P.S.:
        Nuovo paragrafo EVVIVA! L’apprezzerò di più!
"Ma le quote come le gestisce?"
'Ma le quote 'come' le gestisce?'

dell'automobile
c'è c’è
e'
‘e’
citta' città’ citta’
l'Italia l’Italia
all'estero all’estero
l'hanno l’hanno
'città' aperta ‘città’ aperta
#Grisù presidente!
10.9 100,000,000
10,9 100.000.000
10.67% 10,67%
10,56,89 10.56.89
‘anch'io’ ‘anch’io’
mi stai proprio 'sui coglioni'!
mi “stai” proprio 'sui coglioni'
nato nel '73, bello!
l'84"""+"""% """+"""di noi
un 'bel'22%
un 'bell'uomo
E c'è pure gli emoticon!!! :P
:-) ;) Viva viva <3 il regimentoooo!
un 'bell’uomo
"""

tokens = tokenizer.tokenize(text)
print(tokens)