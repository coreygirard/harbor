from pprint import pprint
import re


def loadFile(filename):
    with open(filename,'r') as f:
        text = []
        for line in f:
            processed = line.strip('\n').strip()
            if processed != '':
                text.append(processed)
    return text

def getDocs(filename):
    text = loadFile(filename)

    groups = []
    flag = False
    buff = []
    for line in text:
        if line == "'''" and flag:
            flag = False
            groups.append(buff)
            buff = []
        elif line == "'''" and not flag:
            flag = True
        elif flag:
            buff += [line]

    temp = []
    for e in groups:
        if e[0].startswith('harbor: '):
            temp.append((e[0].strip('harbor: '),e[1:]))
    return temp

def getPattern(filename):
    text = loadFile(filename)
    d = {}

    while len(text) > 0:
        d[text[0].strip(':')] = text[1]
        del text[:2]

    return d

def parse(doc,pattern):
    for i in range(len(doc)):
        line = doc[i]
        s = re.split(r'(\{.*?\}\[.*?\])',line)

        for j in range(len(s)):
            w = s[j]
            match = re.fullmatch(r'\{(.*?)\}\[(.*?)\]',w)
            if match:
                fromStr,lookup = match.groups()
                if lookup in pattern:
                    toStr = re.sub('{'+lookup+'}',fromStr,pattern[lookup])
                    s[j] = toStr

        doc[i] = ''.join(s)

    return '\n'.join(doc)

def makeDocs(sourceFile,patternFile):
    groups = getDocs('example.py')
    docFile = {}
    for dest,group in groups:
        docFile[dest] = docFile.get(dest,[]) + [group]

    pattern = getPattern('example.harbor')

    for filename,notes in docFile.items():
        final = []
        for note in notes:
            final.append(parse(note,pattern))

        final = '\n'.join(final)

        with open(filename,'w') as f:
            f.write(final)


makeDocs('example.py', 'example.harbor')


