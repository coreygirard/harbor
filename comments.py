
"""harbor: readme/how
The second is your source file, annotated with Harbor notation:

```
'''
{quickstart}[harborinit]
'''
```

"""


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

def collateDocs(markup):
    '''
    >>> raw = [['harbor: readme/example',
    ...         '',
    ...         '{TODO}[section]'],
    ...        ['harbor: readme/another',
    ...         'sample',
    ...         '',
    ...         'test']]
    >>> collateDocs(raw) == {'readme/example':
    ...                         ['',
    ...                           '{TODO}[section]'],
    ...                      'readme/another':
    ...                         ['sample',
    ...                           '',
    ...                           'test']}
    True
    '''

    d = {}
    for m in markup:
        assert(m[0].startswith('harbor: '))
        f,path = parsePath(m[0])
        if path not in d:
            d[path] = []

        for e in m[1:]:
            d[path].append(e)

    return d

def getComments(source):
    comments = [extractComments(f) for f in source]
    markup = []
    for f in comments:
        markup += extractMarkup(f)

    docs = collateDocs(markup)
    return docs
