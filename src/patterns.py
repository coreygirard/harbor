
'''harbor: readme/how/pattern

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

    assert(text.count('OUTLINE') <= 1)
    assert(text.count('PATTERNS') <= 1)

    if 'PATTERNS' in text:
        text = text[text.index('PATTERNS')+1:]
    if 'OUTLINE' in text:
        text = text[:text.index('OUTLINE')]
    return text

'''harbor: readme/how/pattern

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

def getPatterns(text):
    r'''
    >>> text = [['OUTLINE',
    ...          'aaa',
    ...          'bbb',
    ...          'ccc',
    ...          '',
    ...          'PATTERNS',
    ...          'aaa:',
    ...          '    **{aaa}**',
    ...          '',
    ...          'bbb:',
    ...          '    ## {bbb}',
    ...          '    *{bbb}*',
    ...          '',
    ...          'ccc:',
    ...          '    ### {ccc}',
    ...          '',
    ...          '    **{ccc}**',
    ...          '']]
    >>> expected = {'aaa': '**{aaa}**\n',
    ...             'bbb': '## {bbb}\n*{bbb}*\n',
    ...             'ccc': '### {ccc}\n\n**{ccc}**\n'}
    >>> result = getPatterns(text)
    >>> result == expected
    True
    '''



    patterns = [extractPatterns(f) for f in text]
    p = {}
    for f in patterns:
        for k,v in parsePatterns(f).items():
            assert(k not in p.keys())
            p[k] = v

    return p
