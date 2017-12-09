
# harbor

*docs made simple* 

[![Build Status](https://travis-ci.org/crgirard/harbor.svg?branch=master)](https://travis-ci.org/crgirard/harbor)

[![Codecov](https://img.shields.io/codecov/c/github/crgirard/harbor.svg)](https://codecov.io/gh/crgirard/harbor/)
 

**Harbor**
1. *(noun)* A place of shelter
2. *(noun)* An area for ships to dock
3. *(noun)* An elegant documentation generator

### What

**Harbor** aims to be a minimalist generator of fine Markdown documentation. 

### Why

There are plenty of powerful documentation generators out there, but I wanted
something nice and simple for small projects, that reads straight from the
source code, makes as few assumptions as possible, and outputs plain Markdown
files.

It's designed to be simple enough to be used manually to generate a doc skeleton
for manual tweaking, but also modular enough to be used in an automated build
pipeline.

### Philosophy
- **Have no opinions:** *Don't enforce any particular style. Just allow the
definition of arbitrary macros for text modification. With the correct `.harbor`
file, this could conceivably generate HTML.*
- **Favor flexibility over power:** *The small convenience gained by
auto-detecting which class or function definitions a given docs section is near
is far outweighed by the loss of potential layout options or non-standard
formatting choices*
- **Favor clarity over speed:** *The purpose here is mainly to provide ease of
use. Simple rules, easily remembered, beat clever tricks that squeeze a few
microseconds out of compile time. At least in this use case. Harbor is for when
you value your own time above computation time.* 
The second is your source file, annotated with Harbor notation:

```
'''
harbor: quickstart

'''
```
 

### How


Two files are required to generate documentation with **Harbor**. The first is a
`.harbor` file, which specifies both the structure of the output files and any
substitutions. For example: 

```
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

```


In the above, you can see two sections: `OUTLINE` and `PATTERNS`. They must be
preceeded by those headers, in all-caps, and must be in that order. The
`OUTLINE` section specifies the names of the files to be generated, and their
internal structure.

Each line in the `OUTLINE` section without indentation denotes a file. The form
is `aaa: bbb`, where `aaa` is the nickname for the file, and `bbb` is the actual
filename to use when saving the generated documentation.

Basic outline indentation rules apply, with regard to how nesting works. The
sections can have arbitrary names, excluding spaces. Best practice for
multi-word sections is Lisp-style naming: `another-section` or
`this-is-a-wordy-label`. 

### TODO


[ ] Allow multiple inputs to text replacement macros
[ ] Clean output to be even more human- readable/editable
[ ] Handle multi-line inputs to macros
[ ] REFACTOR
[ ] Experiment with supporting project languages other than Python 
