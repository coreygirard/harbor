from pprint import pprint
import re

'''
def p(text,n=80):
    text = re.sub(r'[ ]\n',r' ',text)
    text = re.sub(r'\n[ ]',r' ',text)
    text = re.sub(r'\n',r' ',text)

    temp = []

    while len(text) > 0:
        if len(text) <= n:
            temp.append(text)
            text = []
            break

        t = n
        while t > 0 and text[t] != ' ':
            t -= 1
        if t == 0:
            while t < len(text) and text[t] != ' ':
                t += 1

        temp.append(text[:t])
        text = text[t+1:]

    return '\n'.join(temp)


text = 'Harbor aims to be\na \nminimalist generator of fine Markdown documentation. There are plenty of powerful documentation generators out there, but I wanted something nice and simple for small projects, that reads straight from the source code, makes as few assumptions as possible, and outputs plain Markdown files.'

pprint(p(text,70))
'''



class Match(object):
    def __init__(self,*args):
        self.loc = {'{': args[0],
                    '}': args[1]-1,
                    '[': args[1],
                    ']': args[2]-1}

        self.string = args[3]

        for s in '{}[]':
            assert(self.string[self.loc[s]] == s)

    def getOutput(self):
        return (self.string[self.loc['{']+1:self.loc['}']],
                self.string[self.loc['[']+1:self.loc[']']])

    def __repr__(self):
        return 'Match{0}'.format(self.getOutput())

def getMacros(text,valid):
    temp = []

    patt = r'\}\[.+?\]'
    for m in re.finditer(patt,text):
        n = 1
        t = m.start()
        while n > 0 and t > 0:
            t -= 1
            if text[t] == '}':
                n += 1
            elif text[t] == '{':
                n -= 1

        a,b,c = [t,m.start()+1,m.end()]
        if text[b+1:c-1] in valid:
            temp.append(Match(a,b,c,text))

    out = [temp.pop(0)]
    for e in temp:
        if e.loc['{']-1 > out[-1].loc[']']+1:
            out.append(e)

    pprint(out)

    trailing = 0
    temp = []
    for e in out:
        temp.append(text[trailing:e.loc['{']])
        temp.append(e.getOutput())
        trailing = e.loc[']']
    temp.append(text[trailing:])

    return temp


text = ' aaa bbb {ccc ddd}[eee] {{fff}[ggg] hhh {iii jjj}[kkk]}[lll] {mmm} nnn'


pprint(getMacros(text,['eee','lll','ggg']))







