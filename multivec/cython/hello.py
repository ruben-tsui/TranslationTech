#!/usr/bin/python3

from flask import Flask, request

from multivec import BilingualModel, MonolingualModel
model = BilingualModel(b'/mnt/c/NLP/collo/un4m.lemma.bin')
en_model = MonolingualModel(b'/mnt/c/NLP/collo/un4m.lemma.en.bin')
zh_model = MonolingualModel(b'/mnt/c/NLP/collo/un4m.lemma.zhs.bin')

from opencc import OpenCC
ocs2t = OpenCC('s2t')
oct2s = OpenCC('t2s')

def en2zht(txt, n=5):
    retval = []
    for (x,s) in model.trg_closest(txt.encode('utf8'), n):
        retval.append(ocs2t.convert(x.decode('utf8')))
    return retval

def zht2en(txt, n=5):
    retval = []
    for (x,s) in model.src_closest(oct2s.convert(txt).encode('utf8'), n):
        retval.append(x.decode('utf8'))
    return retval

def enSynonyms(txt, n=5):
    retval = []
    for (x,s) in en_model.closest(txt.encode('utf8'), n):
        retval.append(x.decode('utf8'))
    return retval

def zhtSynonyms(txt, n=5):
    retval = []
    for (x,s) in zh_model.closest(oct2s.convert(txt).encode('utf8'), n):
        retval.append(ocs2t.convert(x.decode('utf8')))
    return retval

app = Flask(__name__)

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    word = request.args['word']
    lang = request.args['lang']
    if lang == 'zh':
        return str(zhtSynonyms(word, 15)) + '\n<br/>\n' + str(zht2en(word, 15))
    elif lang == 'en':
        return str(enSynonyms(word, 15)) + '\n<br/>\n' + str(en2zht(word, 15))
   
if __name__ == '__main__':
    app.run(debug=True)
    #print(enSynonyms('independent'))
