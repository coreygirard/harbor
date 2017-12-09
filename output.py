



def toScreen(docs):
    '''
    >>> d = {'readme.md':['hello,',
    ...                   'world!']}

    >>> toScreen(d)
    -----------------
        readme.md
    -----------------
    <BLANKLINE>
    <BLANKLINE>
    hello,
    world!
    '''

    for filename,lines in docs.items():
        print('-'*(len(filename)+8))
        print(' '*4 + filename)
        print('-'*(len(filename)+8) + '\n\n')
        for i in lines:
            print(i)

def toFiles(docs):
    for filename,lines in docs.items():
        with open(filename,'w') as f:
            for i in lines:
                f.write(i)
