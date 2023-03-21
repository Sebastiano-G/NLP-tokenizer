import re
import time

start = time.time()

class Tokenizer:
    def __init__(self, regex_rules, exception_lists, exception_regex):
        self.regex_rules = regex_rules
        self.exception_regex = exception_regex
        self.exception_lists = exception_lists
    
    def tokenize(self, text):
        if type(text) == type(""):
            text = [text]
        text = self._apply_exception_regex(text)
        text = self._apply_exception_lists(text)
        tokens = self._apply_regex_rules(text)
        return tokens
    
    def _apply_exception_regex(self, text):
        for subtext in text:
            for regex in self.exception_regex:
                a_list = re.findall(regex, subtext)
                self.exception_lists.update(set(a_list))
            
        return text
            
    def _apply_exception_lists(self, text):
        for exception in self.exception_lists:
            for n in range(len(text)):
                idx = n
                if exception in text[n] and text[n] != exception.strip():
                    sublist = text[n].split(exception)
                    for item in sublist:
                        if text[n].startswith(exception):
                            a_list = [exception]
                        else:
                            a_list = []
                        for el in sublist:
                            a_list.append(el)
                            if el != sublist[-1]:
                                a_list.append(exception)
                        if text[n].endswith(exception):
                            a_list.append(exception)                            
                    del text[idx]
                    for el in a_list:
                        text.insert(idx, el)
                        idx +=1
                elif exception in text[n] and text[n] == exception.strip():
                    idx += 1              
        return text

    
    def _apply_regex_rules(self, text):
        for regex_rule in self.regex_rules:
            second_text = text.copy()
            idx = 0
            for substring in second_text:
                new_subtext = ""
                new_subtext_list = []
                if self._check_exceptions(substring):
                    new_subtext = re.sub(regex_rule, r' \1 ', substring)
                    new_subtext_list = new_subtext.split()
                    text[idx:(idx+1)]= new_subtext_list
                    idx = idx + len(new_subtext_list)
                else:
                    idx +=1
                
                            
        return text
    
    def _check_exceptions(self, substring):
        if substring not in self.exception_lists:
            value = True
        elif substring in self.exception_lists:
            return False
        return value
    
    # Regular expression rules
regex_rules = [
    r"""([;!"?().,:])""", #   virg. r"""([‘'][.*?]['’])""",   (["'][^"']*["'])|
    r"([a-zA-Z]+[’\\']{1})",
    #r'([a-z][.][a-z][.])', ?
    r'([a-z][.][a-z][.])'   
]

# Exception lists
exception_lists = {'...', 'Ing.', 'Geom.', 'geom.', 'Avv.', 'prof.', 'dr.', 'dott.','racc.','P.S.','p.s.', 'p.es.','c.a.','S.r.l.','U.S.A.', 'U.E.', ':)', ':(', ';)', ':D', '<3',':P',':-)', ':,('}

# Regular expressions to identify exceptions
exception_regex = [
    r"([dD][a-z]+[’\\']{1}[A-Z]{1}[a-z]+)", #preposizioni articolate nei cognomi (es.: Dell'Anda)
    r'([\d]+[,\\.]+[\d\\.,]+[%]?)', #numeri decimali (. e ,) e percentuali
    r'([htps]+:\/[w.]?[-_.\w\/]+)', #url (anche con percorsi interni del tipo /.../.../....it)
    r"""([‘][^\n]*[’])""", # MWEs 
    r"""(['][^\n]*['])""",
    r"""(["][^\n]*["])""",
    r'([\w\d_\.-]+@{1}[\w_\.-]+\.{1}[a-z]+)' #email
]

# Create tokenizer object
tokenizer = Tokenizer(regex_rules, exception_lists, exception_regex)
