from pprint import pprint
import re


def loadFile(filename):
    with open(filename,'r') as f:
        text = []
        for line in f:
            processed = line.strip('\n')
            if processed.strip() != '':
                text.append(processed)
    return text

def makePath(line):
    '''
    >>> makePath('harbor: abc/def/ghi')
    ['abc', 'def', 'ghi']
    '''
    assert(line.startswith('harbor: '))
    line = line[len('harbor: '):].strip()
    return line.split('/')

def extractBlockComments(text):
    groups = []
    indent = None
    buff = []
    for line in text:
        if line.strip() == "'''" and indent == None:
            indent = len(line) - len(line.strip())
        elif line.strip() == "'''" and indent != None:
            indent = None
            groups.append(buff)
            buff = []
        elif indent != None:
            buff += [line[indent:]]
    return groups

def getOnlyHarborMarkup(groups):
    text = []
    for g in groups:
        if g[0].startswith('harbor: '):
            text += g

    groups = []
    t = 0
    buff = []
    while len(text) > 0:
        t = 1
        while not (t >= len(text) or text[t].startswith('harbor: ')):
            t += 1

        groups.append(text[:t])
        del text[:t]

    return groups

def getDocs(filename):
    text = loadFile(filename)

    groups = extractBlockComments(text)
    groups = getOnlyHarborMarkup(groups)

    temp = {}
    for g in groups:
        path = makePath(g[0])
        filepath = path[0]
        if filepath not in temp:
            temp[filepath] = {}
        path = '/'.join(path)

        data = g[1:]
        temp[filepath][path] = temp[filepath].get(path,[])+data

    return temp

def extractPatternSection(text):
    assert('PATTERNS' in text)
    return text[text.index('PATTERNS')+1:]

def getPatterns(filename):
    text = loadFile(filename)
    text = extractPatternSection(text)

    d = []

    while len(text) > 0:
        if len(text[0]) < 4 or text[0][:4] != ' '*4:
            d.append([text[0].strip(':'),[]])
        else:
            d[-1][1].append(text[0][4:])
        del text[0]

    d = {e[0]:'\n'.join(e[1]) for e in d}

    return d

def extractOutlineSection(text):
    assert('OUTLINE' in text)
    assert('PATTERNS' in text)
    return text[text.index('OUTLINE')+1:text.index('PATTERNS')]

def getOutline(filename):
    text = loadFile(filename)
    text = extractOutlineSection(text)

    filenames = {}

    d = {}
    for line in text:
        if line.strip() != '':
            n,line = len(line)-len(line.strip()),line.strip()
            assert(n%2 == 0)

            if n == 0:
                slug,f = line.split(' ')
                slug = slug.strip(':')
                filenames[slug] = {'filename':f,
                                   'contents':[]}
                line = slug

            d[n] = line
            d = {k:v for k,v in d.items() if k <= n}
            path = '/'.join([d[k] for k in sorted(d.keys())])
            filenames[slug]['contents'] += [path]

    return filenames

def parse(line,pattern):
    s = re.split(r'(\{.*?\}\[.*?\])',line)

    temp = []
    for w in s:
        match = re.fullmatch(r'\{(.*?)\}\[(.*?)\]',w)
        if match:
            fromStr,lookup = match.groups()
            if lookup in pattern:
                toStr = re.sub('{'+lookup+'}',fromStr,pattern[lookup])
                temp.append(toStr)
            else:
                temp.append(w)
        else:
            temp.append(w)

    return ''.join(temp)

def atomicSub(group,patterns):
    return [parse(g,patterns) for g in group]

def sub(groups,patterns):
    for f in groups.keys():
        for path in groups[f].keys():
            groups[f][path] = atomicSub(groups[f][path],patterns)
            groups[f][path] = '\n'.join(groups[f][path])
    return groups

def makeDocs(sourceFile,patternFile,debug=False):
    groups = getDocs(sourceFile)

    outline = getOutline(patternFile)
    patterns = getPatterns(patternFile)

    groups = sub(groups,patterns)

    #pprint(groups)
    #pprint(outline)
    #pprint(patterns)

    assert(all([k in outline for k in groups.keys()]))

    for doc in outline.keys():
        filepath = outline[doc]['filename']

        docGroups = groups[doc]
        docOutline = outline[doc]['contents']

        if not debug:
            with open(filepath,'w') as f:
                for path in docOutline:
                    if path in docGroups:
                        f.write(docGroups[path])
        else:
            print(filepath+':')
            for path in docOutline:
                if path in docGroups:
                    print(path)
                    print(docGroups[path])
                    print(' ')
            print('-----------------------\n')




#makeDocs('examples/helloworld/helloworld.py', 'examples/helloworld/helloworld.harbor', debug=True)


