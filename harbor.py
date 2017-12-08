from pprint import pprint
import re

'''harbor: readme/todo

{TODO}[section]

[ ] Allow multiple inputs to text replacement macros
[ ] Clean output to be even more human- readable/editable
[ ] Handle multi-line inputs to macros
[ ] REFACTOR
'''



'''harbor: readme

{harbor}[title]
*docs made simple*
'''


'''harbor: readme/badges

{harbor}[buildbadge]
{harbor}[codecovbadge]
'''

'''harbor: readme/what

**Harbor**
1. *(noun)* A place of shelter
2. *(noun)* An area for ships to dock
3. *(noun)* An elegant documentation generator

{What}[section]
**Harbor** aims to be a minimalist generator of fine Markdown documentation.
There are plenty of powerful documentation generators out there, but I wanted
something nice and simple for small projects, that reads straight from the source
code, makes as few assumptions as possible, and outputs plain Markdown files.
'''

'''harbor: readme/why

{Why}[section]
**Harbor** aims to be a minimalist generator of fine Markdown documentation.
There are plenty of powerful documentation generators out there, but I wanted
something nice and simple for small projects, that reads straight from the source
code, makes as few assumptions as possible, and outputs plain Markdown files.

It's designed to be simple enough to be used manually to generate a doc skeleton
for manual tweaking, but also modular enough to be used in an automated build pipeline.

### Philosophy
- **Have no opinions:** *Don't enforce any particular style. Just allow the definition of
arbitrary macros for text modification. With the correct `.harbor` file, this
could conceivably generate HTML.*
- **Favor flexibility over power:** *The small convenience gained by auto-detecting
which class or function definitions a given docs section is near is far outweighed by the loss
of potential layout options or non-standard formatting choices*
- **Favor clarity over speed:** *The purpose here is mainly to provide ease of use. Simple rules,
easily remembered, beat clever tricks that squeeze a few microseconds out of compile time. At least
in this use case. Harbor is for when you value your own time above computation time.*
'''

def loadFile(filename):
    with open(filename,'r') as f:
        return f.read().split('\n')

def parsePath(line):
    '''
    >>> parsePath('harbor: abc/def/ghi')
    ('abc', 'abc/def/ghi')
    '''
    assert(line.startswith('harbor: '))
    line = line[len('harbor: '):]
    line = line.strip()
    line = line.split('/')
    return line[0],'/'.join(line)

def extractComments(text):
    """
    >>> source = ["",
    ...           "'''harbor: readme",
    ...           "aaa",
    ...           "'''",
    ...           "bbb",
    ...           "'''",
    ...           "ccc",
    ...           "'''"]
    >>> extractComments(source)
    [['harbor: readme', 'aaa'], ['', 'ccc']]
    """
    groups = []
    indent = None
    buff = []
    comment = None
    for line in text:
        if (line.lstrip())[:3] in ["'''",'"""'] and indent == None:
            indent = len(line) - len(line.lstrip())
            comment = (line.lstrip())[:3]
            buff = [line[indent+3:]]
        elif line.strip() == comment and indent != None:
            indent = None
            groups.append(buff)
            buff = []
        elif indent != None:
            buff += [line[indent:]]
    return groups

def extractMarkup(groups):
    '''
    >>> groups = [['harbor: readme', 'aaa'], ['', 'bbb'], ['harbor: readme', 'ccc']]
    >>> extractMarkup(groups)
    [['harbor: readme', 'aaa'], ['harbor: readme', 'ccc']]
    '''

    text = []
    for g in groups:
        if g[0].startswith('harbor: '):
            text += [g]

    return text

def getDocs2(filename):
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

'''
harbor: readme/how/pattern
The `PATTERN` section specifies essentially macros to be executed on all generated documentation.
'''

def extractPatterns(text):
    '''
    >>> text = ['OUTLINE',
    ...         'aaa',
    ...         'bbb',
    ...         'ccc',
    ...         '',
    ...          'PATTERNS',
    ...         'ddd',
    ...         'eee',
    ...         'fff',
    ...         '']

    >>> extractPatterns(text)
    ['ddd', 'eee', 'fff', '']
    '''
    assert('PATTERNS' in text)
    text = text[text.index('PATTERNS')+1:]
    if 'OUTLINE' in text:
        text = text[:text.index('OUTLINE')]
    return text

'''
harbor: readme/how/pattern

Format is
'''

def parsePatterns(text):
    r'''
    >>> text = ['aaa:',
    ...         '    **{aaa}**',
    ...         '',
    ...         'bbb:',
    ...         '    ## {bbb}',
    ...         '    *{bbb}*',
    ...         '',
    ...         'ccc:',
    ...         '    ### {ccc}',
    ...         '',
    ...         '    **{ccc}**',
    ...         '']
    >>> expected = {'aaa': '**{aaa}**\n',
    ...             'bbb': '## {bbb}\n*{bbb}*\n',
    ...             'ccc': '### {ccc}\n\n**{ccc}**\n'}
    >>> result = parsePatterns(text)
    >>> result == expected
    True
    '''

    while text[0] == '':
        text.pop(0)

    d = []

    while len(text) > 0:
        head = text.pop(0)
        if head.strip() == '':
            divider = False
        elif len(head) < 4:
            divider = True
        elif head[:4] != ' '*4:
            divider = True
        else:
            divider = False

        if divider:
            d.append([head.strip(':'),[]])
        else:
            d[-1][1].append(head[4:])

    d = {e[0]:'\n'.join(e[1]) for e in d if e[0]}

    return d


'''
harbor: readme/how/outline

{}[samplepattern]

In the above, you can see two sections: `OUTLINE` and `PATTERNS`. They must be preceeded
by those headers, in all-caps, and must be in that order. The `OUTLINE` section specifies
the names of the files to be generated, and their internal structure.
'''

def extractOutline(text):
    '''
    >>> text = ['OUTLINE',
    ...         'aaa',
    ...         'bbb',
    ...         'ccc',
    ...         '',
    ...          'PATTERNS',
    ...         'ddd',
    ...         'eee',
    ...         'fff',
    ...         '']

    >>> extractOutline(text)
    ['aaa', 'bbb', 'ccc', '']
    '''
    assert('OUTLINE' in text)
    text = text[text.index('OUTLINE')+1:]
    if 'PATTERNS' in text:
        text = text[:text.index('PATTERNS')]
    return text

'''
harbor: readme/how/outline
Each line in the `OUTLINE` section without indentation denotes a file. The form is `aaa: bbb`,
where `aaa` is the nickname for the file, and `bbb` is the actual filename to use when saving
the generated documentation.

Basic outline indentation rules apply, with regard to how nesting works. The sections can have
arbitrary names, excluding spaces. Best practice for multi-word sections is Lisp-style naming:
`another-section` or `this-is-a-wordy-label`.
'''

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

def parse(line,patterns):
    '''
    >>> line = '{hello}[another] {world}[sample]'
    >>> patterns = {'sample': '**{sample}**',
    ...            'another': '- *`{another}`*'}
    >>> parse(line,patterns)
    '- *`hello`* **world**'
    '''

    s = re.split(r'(\{.*?\}\[.*?\])',line)

    temp = []
    for w in s:
        match = re.fullmatch(r'\{(.*?)\}\[(.*?)\]',w)
        if match:
            fromStr,lookup = match.groups()
            if lookup in patterns:
                toStr = re.sub('{'+lookup+'}',fromStr,patterns[lookup])
                temp.append(toStr)
            else:
                temp.append(w)
        else:
            temp.append(w)

    return ''.join(temp)


def applyMacros(groups,patterns):
    r'''
    >>> groups = {'aaa': {'aaa/bbb/ccc': [['{abc}[another] {def}[sample]'],
    ...                                   ['{ghi}[another] {jkl}[sample]']]},
    ...           'iii': {'iii/jjj/kkk': [['{mno}[another] {pqr}[sample]'],
    ...                                   ['{stu}[another] {vwx}[sample]']]}}

    >>> patterns = {'sample': '**{sample}**',
    ...             'another': '- *`{another}`*'}

    >>> expected = {'iii': {'iii/jjj/kkk': '- *`mno`* **pqr**\n'
    ...                                    '- *`stu`* **vwx**'},
    ...             'aaa': {'aaa/bbb/ccc': '- *`abc`* **def**\n'
    ...                                    '- *`ghi`* **jkl**'}}

    >>> applyMacros(groups,patterns) == expected
    True
    '''

    for f in groups.keys():
        for path in groups[f].keys():
            for i in range(len(groups[f][path])):
                temp = groups[f][path][i]

                temp = '\n'.join(temp)
                temp = parse(temp,patterns)

                groups[f][path][i] = temp
            groups[f][path] = '\n'.join(groups[f][path])
    return groups

'''
harbor: readme/how/intro
{How}[section]

Two files are required to generate documentation with **Harbor**. The first is
a `.harbor` file, which specifies both the structure of the output files
and any substitutions. For example:
'''



"""
The second is your source file, annotated with Harbor notation:

```
'''
{quickstart}[harborinit]
'''
```

"""

def makeAttrib():
    attrib = ''.join(['<br>\n<br>\n<br>\n<p align="center">\n',
                      '*This documentation generated by [{0}]({1} "{2}")*',
                      '\n</p>'])
    attrib = attrib.format('harbor',
                           'https://www.github.com/crgirard/harbor',
                           'harbor: docs made simple')
    return attrib

def collate():
    pass

def toScreen():
    print(filepath+':')
    for path in docOutline:
        if path in docGroups:
            print(path)
            print(docGroups[path])
            print(' ')
        elif verbose:
            print('\n\n\n --- NO TEXT ASSIGNED TO SECTION: {0} --- \n\n\n'.format(path))
    print('-----------------------\n')

    print(makeAttrib())

def toFiles():
    with open(filepath,'w') as f:
        for path in docOutline:
            if path in docGroups:
                f.write(docGroups[path])
            elif verbose:
                print('\n\n\n --- NO TEXT ASSIGNED TO SECTION: {0} --- \n\n\n'.format(path))
        if credit:
            f.write(makeAttrib())

def makeDocs(sourceFile,patternFile,debug=False,verbose=False,credit=False):
    groups = getDocs(sourceFile)

    outline = getOutline(patternFile)
    patterns = getPatterns(patternFile)

    groups = sub(groups,patterns)

    assert(all([k in outline for k in groups.keys()]))

    for doc in outline.keys():
        filepath = outline[doc]['filename']

        docGroups = groups[doc]
        docOutline = outline[doc]['contents']


from pprint import pprint


def collateDocs(markup):
    '''
    >>> raw = [['harbor: readme/example',
    ...         '',
    ...         '{TODO}[section]'],
    ...        ['harbor: readme/another',
    ...         'sample',
    ...         '',
    ...         'test']]
    >>> collateDocs(raw) == {'readme':
    ...                          {'readme/another':
    ...                              [['harbor: readme/another',
    ...                                'sample', '', 'test']],
    ...                           'readme/example':
    ...                              [['harbor: readme/example',
    ...                                '',
    ...                                '{TODO}[section]']]}}
    True
    '''

    d = {}
    for m in markup:
        assert(m[0].startswith('harbor: '))
        f,path = parsePath(m[0])
        if f not in d:
            d[f] = {}
        if path not in d[f]:
            d[f][path] = []

        d[f][path].append(m)

    return d

def getDocs(sourceFile):
    source = [loadFile(f) for f in sourceFile]
    comments = [extractComments(f) for f in source]
    markup = []
    for f in comments:
        markup += extractMarkup(f)

    docs = collateDocs(markup)
    return docs

def getPatterns(patternFile):
    source = [loadFile(f) for f in patternFile]
    patterns = [extractPatterns(f) for f in source]
    p = {}
    for f in patterns:
        for k,v in parsePatterns(f).items():
            assert(k not in p.keys())
            p[k] = v

    return p


def exe(sourceFile,patternFile,debug=False,verbose=False,credit=False):
    if type(sourceFile) == type('string'):
        sourceFile = [sourceFile]
    if type(patternFile) == type('string'):
        patternFile = [patternFile]

    docs =     getDocs(sourceFile)
    patterns = getPatterns(patternFile)

    docs = applyMacros(docs,patterns)





#exe('harbor.py','harbor.harbor')

#exe('harbor.py','harbor.harbor',debug=False,verbose=True,credit=True)

