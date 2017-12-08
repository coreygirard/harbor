 
# harbor 
 
[![Build Status](https://travis-ci.org/crgirard/harbor.svg?branch=master)](https://travis-ci.org/crgirard/harbor) 
[![Codecov](https://img.shields.io/codecov/c/github/crgirard/harbor.svg)](https://codecov.io/gh/crgirard/harbor/) 
 
### What 
**Harbor** aims to be a minimalist generator of fine Markdown documentation. 
There are plenty of powerful documentation generators out there, but I wanted 
something nice and simple for small projects, that reads straight from the source 
code, makes as few assumptions as possible, and outputs plain Markdown files. 
 
### Why 
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
 
### How 
Two files are required to generate documentation with **Harbor**. The first is 
a `.harbor` file, which specifies both the structure of the output files 
and any substitutions. For example: 
 
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
In the above, you can see two sections: `OUTLINE` and `PATTERNS`. They must be preceeded 
by those headers, in all-caps, and must be in that order. The `OUTLINE` section specifies 
the names of the files to be generated, and their internal structure. 
Each line in the `OUTLINE` section without indentation denotes a file. The form is `aaa: bbb`, 
where `aaa` is the nickname for the file, and `bbb` is the actual filename to use when saving 
the generated documentation. 
Basic outline indentation rules apply, with regard to how nesting works. The sections can have 
arbitrary names, excluding spaces. Best practice for multi-word sections is Lisp-style naming: 
`another-section` or `this-is-a-wordy-label`. 
 
### TODO 
[ ] Allow multiple inputs to text replacement macros 
[ ] Clean output to be even more human- readable/editable 
[ ] REFACTOR 
