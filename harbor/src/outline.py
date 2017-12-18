
'''harbor: readme/how/outline

{
OUTLINE
readme: README.md
  badges
  what
  why
  how
    intro
    outline
    patterns

  todo

PATTERNS
title:
    # {title}
section:
    ### {section}
}[code]

{The outline section of the `.harbor` file must be preceded by `OUTLINE`.
This section specifies the names of the files to be generated, and their internal
structure}[p]

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
    assert(text.count('OUTLINE') <= 1)
    assert(text.count('PATTERNS') <= 1)

    if 'OUTLINE' in text:
        text = text[text.index('OUTLINE')+1:]
    if 'PATTERNS' in text:
        text = text[:text.index('PATTERNS')]
    return text

'''harbor: readme/how/outline

{Each line in the `OUTLINE` section without indentation denotes a file. The form is `aaa: bbb`,
where `aaa` is the nickname for the file, and `bbb` is the actual filename to use when saving
the generated documentation.}[p]

{Basic outline indentation rules apply, with regard to how nesting works. The sections can have
arbitrary names, excluding spaces. Best practice for multi-word sections is Lisp-style naming:
`another-section` or `this-is-a-wordy-label`.}[p]
'''

def getOutline(i):
    '''
    >>> raw = [['OUTLINE',
    ...         'readme: README.md',
    ...         '  aaa',
    ...         '  bbb',
    ...         '    ccc',
    ...         '  ddd',
    ...         '    eee',
    ...         '    fff'],
    ...        ['OUTLINE',
    ...         'quickstart: quickstart.md',
    ...         '  step-1',
    ...         '  step-2',
    ...         '  step-3']]

    >>> getOutline(raw) == {'README.md':['readme',
    ...                                  'readme/aaa',
    ...                                  'readme/bbb',
    ...                                  'readme/bbb/ccc',
    ...                                  'readme/ddd',
    ...                                  'readme/ddd/eee',
    ...                                  'readme/ddd/fff'],
    ...                     'quickstart.md': ['quickstart',
    ...                                       'quickstart/step-1',
    ...                                       'quickstart/step-2',
    ...                                       'quickstart/step-3']}
    True
    '''


    text = []
    for e in i:
        text += extractOutline(e)

    filenames = {}

    stack = {}
    for line in text:
        if line.strip() != '':
            n = len(line)-len(line.lstrip())
            line = line.strip()
            assert(n%2 == 0)

            if n == 0:
                line,f = line.split(' ')
                line = line.strip(':')
                filenames[f] = []

            stack[n] = line
            stack = {k:v for k,v in stack.items() if k <= n}

            path = '/'.join([stack[k] for k in sorted(stack.keys())])
            filenames[f] += [path]

    return filenames
