#!/usr/bin/env python
# coding: utf-8

import hanlp
import os.path
tokenizer = hanlp.load('CTB6_CONVSEG')
BATCH_SIZE = 200

def segment(fin, fon):
    '''
    Segment (tokenize) a Chinese text and save it 
    Input:
        input file (path + file), encoded in UTF-8
    Output:
        tokenized file (path + file), encoded in UTF-8
    '''
    if not os.path.isfile(fin):
        print(f"Sorry, file {fin} doesn't exist!")
        return None
    if os.path.isfile(fon):
        print(f"Sorry, file {fon} already exists!")
        return None

    delim = ' ' # delimiter between tokens
    tokenizer = hanlp.load('CTB6_CONVSEG')

    n = 0
    with open(fon, "w", encoding='UTF-8', newline="\n") as fo:
        with open(fin, "r", encoding='UTF-8') as fi:
            cnt = 0
            batch = ''
            for line in fi:
                cnt += 1
                batch += line
                n += 1
                if cnt % BATCH_SIZE == 0:
                    tokens = tokenizer(batch)
                    batch_out = delim.join(tokens).replace(f'{delim}\n{delim}', '\n')
                    fo.write(batch_out )
                    batch = ''
                if n % 1000 == 0:
                    fo.flush()
                    print(f"{n} lines processed...")
            tokens = tokenizer(batch)
            batch_out = delim.join(tokens).replace(f'{delim}\n{delim}', '\n')
            fo.write(batch_out )

segment('nyt002.zh', f'out{BATCH_SIZE}.txt')
