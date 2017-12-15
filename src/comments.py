from collections import namedtuple

Markup = namedtuple('Markup','dest contents')


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
    >>> parsePath('abc/def/ghi')
    ('abc', 'abc/def/ghi')
    '''
    line = line.strip()
    line = line.split('/')
    return line[0],'/'.join(line)



def extractMarkup(text):
    """
    >>> source = ["",
    ...           "'''harbor: readme",
    ...           "aaa",
    ...           "'''",
    ...           "bbb",
    ...           "'''",
    ...           "ccc",
    ...           "'''",
    ...           "ddd",
    ...           "'''harbor: readme",
    ...           "eee",
    ...           "fff",
    ...           "'''"]
    >>> extractMarkup(source) == [Markup('readme',
    ...                                  ['aaa']),
    ...                           Markup('readme',
    ...                                  ['eee', 'fff'])]
    True
    """

    groups = []
    indent = None
    buff = []
    comment = None
    for line in text:
        i = len("'''harbor: ")
        if (line.lstrip())[:i] in ["'''harbor: ",'"""harbor: '] and indent == None:
            indent = len(line) - len(line.lstrip())
            comment = (line.lstrip())[:3]
            buff = Markup(line[indent+i:],[])
        elif line.strip() == comment and indent != None:
            indent = None
            groups.append(buff)
            buff = []
        elif indent != None:
            buff = Markup(buff.dest,buff.contents + [line[indent:]])
    return groups



def collateDocs(markup):
    r'''
    >>> raw = [Markup('readme/example',
    ...               ['',
    ...                '{TODO}[section]']),
    ...        Markup('readme/another',
    ...               ['sample',
    ...                '',
    ...                'test'])]
    >>> collateDocs(raw) == {'readme/example': '\n'
    ...                                        '{TODO}[section]\n',
    ...                      'readme/another': 'sample\n'
    ...                                        '\n'
    ...                                        'test\n'}
    True
    '''

    d = {}
    for m in markup:
        f,path = parsePath(m.dest)
        if path not in d:
            d[path] = ''

        for e in m.contents:
            d[path] += e+'\n'

    return d

def getComments(source):
    r"""
    >>> source = [["",
    ...            "'''harbor: readme",
    ...            "aaa",
    ...            "'''",
    ...            "bbb",
    ...            "'''",
    ...            "ccc",
    ...            "'''",
    ...            "ddd",
    ...            "'''harbor: readme",
    ...            "eee",
    ...            "fff",
    ...            "'''"]]
    >>> getComments(source) == {'readme': 'aaa\n'
    ...                                   'eee\n'
    ...                                   'fff\n'}
    True
    """

    markup = []
    for f in source:
        markup += extractMarkup(f)

    docs = collateDocs(markup)
    return docs





