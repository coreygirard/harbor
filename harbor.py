from pprint import pprint
import re

from src import outline
from src import patterns
from src import comments
from src import parse
from src import output

'''harbor: readme/todo

{TODO}[section]

- [ ] Allow multiple inputs to text replacement macros
- [ ] Clean output to be even more human- readable/editable
- [ ] Handle multi-line inputs to macros
- [ ] REFACTOR
- [ ] Implement a 'trace' function to print an outline of the docs' origins (file name and line number)
- [ ] Experiment with supporting project languages other than Python
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
'''

'''harbor: readme/why

{Why}[section]
{There are plenty of powerful documentation generators out there, but I wanted
something nice and simple for small projects, that reads straight from the source
code, makes as few assumptions as possible, and outputs plain Markdown files.}[p]

{It's designed to be simple enough to be used manually to generate a doc skeleton
for manual tweaking, but also modular enough to be used in an automated build pipeline.}[p]

### Philosophy
{- **Have no opinions:** *Don't enforce any particular style. Just allow the definition of
arbitrary macros for text modification. With the correct `.harbor` file, this
could conceivably generate HTML.*}[p]
{- **Favor flexibility over power:** *The small convenience gained by auto-detecting
which class or function definitions a given docs section is near is far outweighed by the loss
of potential layout options or non-standard formatting choices*}[p]
{- **Favor clarity over speed:** *The purpose here is mainly to provide ease of use. Simple rules,
easily remembered, beat clever tricks that squeeze a few microseconds out of compile time. At least
in this use case. Harbor is for when you value your own time above computation time.*}[p]
'''

def loadFile(filename):
    with open(filename,'r') as f:
        return f.read().split('\n')


'''harbor: readme/how/intro

{How}[section]

{Only one file is required to generate documentation with **Harbor**. It is a
`.harbor` file, which specifies both the structure of the output files and any
substitutions. For example:
}[p]


{Two files are required to generate documentation with **Harbor**. The first is
a `.harbor` file, which specifies both the structure of the output files
and any substitutions. For example:}[p]
'''


def exe(sourceFile,harborFile,debug=False,verbose=False,credit=False):
    if type(sourceFile) == type('string'):
        source = [loadFile(sourceFile)]
    else:
        source = [loadFile(f) for f in sourceFile]

    if type(harborFile) == type('string'):
        harbor = [loadFile(harborFile)]
    else:
        harbor = [loadFile(f) for f in harborFile]

    docs = {'comments': comments.getComments(source),
            'outline':  outline.getOutline(harbor),
            'patterns': patterns.getPatterns(harbor)}

    docs['comments'] = parse.applyPatterns(docs['comments'],docs['patterns'])
    docs['final'] = parse.structure(docs['comments'],docs['outline'],verbose,credit)

    if not debug:
        output.toFiles(docs['final'])
    else:
        output.toScreen(docs['final'])

'''
exe(['harbor.py',
     'src/outline.py',
     'src/patterns.py',
     'src/comments.py',
     'src/parse.py',
     'src/output.py'],
    'harbor.harbor',
    verbose=True,
    debug=False,
    credit=True)
'''
