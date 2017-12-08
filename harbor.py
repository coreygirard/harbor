from pprint import pprint
import re

'''
harbor: readme/todo

{TODO}[section]

[ ] Allow multiple inputs to text replacement macros
[ ] Clean output to be even more human- readable/editable
[ ] REFACTOR
'''



'''
harbor: readme

{harbor}[title]
'''


'''
harbor: readme/badges

{harbor}[buildbadge]
{harbor}[codecovbadge]
'''

'''
harbor: readme/what

{What}[section]
**Harbor** aims to be a minimalist generator of fine Markdown documentation.
There are plenty of powerful documentation generators out there, but I wanted
something nice and simple for small projects, that reads straight from the source
code, makes as few assumptions as possible, and outputs plain Markdown files.
'''

'''
harbor: readme/why

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
- **Favor flexibility over power:** *Rather than features like auto-detecting which
class or function definitions a given section of docs is near, make the user type it
'''

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
    comment = None
    for line in text:
        if line.strip() in ["'''",'"""'] and indent == None:
            indent = len(line) - len(line.strip())
            comment = line.strip()
        elif line.strip() == comment and indent != None:
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

'''
harbor: readme/how/pattern
The `PATTERN` section specifies essentially macros to be executed on all generated documentation.
This will make more sense when we look at the next file.
'''

def extractPatternSection(text):
    assert('PATTERNS' in text)
    return text[text.index('PATTERNS')+1:]

'''
harbor: readme/how/pattern

'''

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


'''
harbor: readme/how/outline

{}[samplepattern]

In the above, you can see two sections: `OUTLINE` and `PATTERNS`. They must be preceeded
by those headers, in all-caps, and must be in that order. The `OUTLINE` section specifies
the names of the files to be generated, and their internal structure.
'''

def extractOutlineSection(text):
    assert('OUTLINE' in text)
    assert('PATTERNS' in text)
    return text[text.index('OUTLINE')+1:text.index('PATTERNS')]

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

def atomicSub(group,patterns):
    '''
    >>> group = ['{hello}[another] {world}[sample]',
    ...          '{abc}[another] {def}[sample]',
    ...          '{ghi}[another] {jkl}[sample]',
    ...          '{mno}[another] {pqr}[sample]']
    >>> patterns = {'sample': '**{sample}**',
    ...             'another': '- *`{another}`*'}
    >>> atomicSub(group,patterns) == ['- *`hello`* **world**',
    ...                               '- *`abc`* **def**',
    ...                               '- *`ghi`* **jkl**',
    ...                               '- *`mno`* **pqr**']
    True
    '''
    return [parse(g,patterns) for g in group]

def sub(groups,patterns):
    '''
    >>> groups = {'aaa': {'aaa/bbb/ccc': ['{abc}[another] {def}[sample]',
    ...                                   '{ghi}[another] {jkl}[sample]']},
    ...           'iii': {'iii/jjj/kkk': ['{mno}[another] {pqr}[sample]',
    ...                                   '{stu}[another] {vwx}[sample]']}}
    >>> patterns = {'sample': '**{sample}**',
    ...             'another': '- *`{another}`*'}
    >>> result = sub(groups,patterns)
    >>> list(result['aaa'].keys()) == ['aaa/bbb/ccc']
    True
    >>> list(result['iii'].keys()) == ['iii/jjj/kkk']
    True
    >>> type(result['aaa']['aaa/bbb/ccc']) == type('string')
    True
    '''

    for f in groups.keys():
        for path in groups[f].keys():
            groups[f][path] = atomicSub(groups[f][path],patterns)
            groups[f][path] = ' \n' + ' \n'.join(groups[f][path]) + ' \n'
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


def makeDocs(sourceFile,patternFile,debug=False,verbose=False):
    groups = getDocs(sourceFile)

    outline = getOutline(patternFile)
    patterns = getPatterns(patternFile)

    groups = sub(groups,patterns)

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
                    elif verbose:
                        print('\n\n\n --- NO TEXT ASSIGNED TO SECTION: {0} --- \n\n\n'.format(path))
        else:
            print(filepath+':')
            for path in docOutline:
                if path in docGroups:
                    print(path)
                    print(docGroups[path])
                    print(' ')
                elif verbose:
                    print('\n\n\n --- NO TEXT ASSIGNED TO SECTION: {0} --- \n\n\n'.format(path))
            print('-----------------------\n')




#makeDocs('harbor.py','harbor.harbor',debug=False,verbose=True)

