 
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
- Have no opinions: *Don't enforce any particular style. Just allow the definition of 
arbitrary macros for text modification. This could conceivably generate HTML with the 
correct `.harbor` file.* 
 
### How 
Two files are required to generate documentation with **Harbor**. The first is 
a `.harbor` file, which specifies both the structure of the output files 
and any substitutions. For example: 
 
```
OUTLINE
spec: specifications.md
  first
    sec1
    sec2
  second
    sec1
    sec2
    sec3
quickstart: quickstart.md
  first
  second
  third
PATTERNS
title:
    # {title}
section:
    ### {section}
``` 
In the above, you can see two sections: `OUTLINE` and `PATTERNS`. They must be preceeded 
by those headers, in all-caps, and must be in that order. The `OUTLINE` section specifies 
the names of the files to be generated, and their internal structure. 
Each line in the `OUTLINE` section without indentation denotes a file. The part 
before the `:` is the nickname for the file, to be used elsewhere to refer to that file. 
The part after the `:` is the actual filename, to be used when saving the generated Markdown. 
All of the indented lines follow general grade-school outlining rules, in terms of how 
nesting works. The sections can have arbitrary names, excluding spaces. Best practice 
is Lisp-style naming for multi-word sections: `another-section` or `this-is-a-wordy-label`. 
 
[ ] Allow multiple inputs to text replacement macros 
[ ] Clean output to be even more human- readable/editable 
