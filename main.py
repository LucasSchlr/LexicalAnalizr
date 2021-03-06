# eduardo arndt e lucas schuler

import re
import sys
import os
from keywords import keywords
from datetime import datetime

blank_char ="[ \n]+" #"[\\(\\):, ]+"

if os.path.exists("result.txt"):
  os.remove("result.txt")

result_file = open("result.txt", "a")

tokens = {
    "keywords":keywords,
    "string":"^\".*\"",
    "numerico":"[0-9]+",
    "operadores":"[+*\\-/]",
    "separadores":"[;\\{\\}.]",
    "identificador":"[a-zA-Z0-9_]+",
    "atribuicao":"=",
    "teste":"==",
    "ignorados":"[(),\\[\\]:]+"
}

def remove_ignored_chars(input):
    match = re.findall(blank_char, input)

    if (len(match) > 0) and (input[0:len(match[0])] == match[0]):
        return len(match[0])
    return 0

def match_tokens(input):
    i = 0    
    for key, value in tokens.items():
        if (key == "keywords"):
            for keyword in keywords:
                match = re.findall(keyword, input)
                if (len(match) > 0) and (input[0:len(match[0])] == match[0]):
                    return len(match[0]), key
        else:
            match = re.findall(value, input)
            if (len(match) > 0) and (input[0:len(match[0])] == match[0]):
                return len(match[0]), key
    
    return 0, ''

def extract_tokens_from_line(line, linePos):
    text = line

    while (len(text) > 0):
        text_len = len(text)
        text = text[remove_ignored_chars(text): text_len  ]

        if (len(text) > 0):
            posSubstr, tokenClass = match_tokens(text)
            if tokenClass:
                lexema = text[0:posSubstr]
                if tokenClass != "ignore":
                    content = "Linha : {} classe: {} lexema: {} \n".format(linePos, tokenClass, lexema )
                    result_file.write(content)
                    print(content) 
                
                text_len = len(text)
                text = text[posSubstr: text_len]

if len(sys.argv) > 1:
    print("reading file... {}".format(str(sys.argv[1])))
    file = str(sys.argv[1])
else:
    print("defaulting to file name Source.java")
    file = "Source.java"

file1 = open(file, 'r')
lines = file1.readlines()

count = 0
for line in lines:
     count += 1
     extract_tokens_from_line(line, count)

result_file.close()
