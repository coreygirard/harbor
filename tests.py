import shutil, tempfile
from os import path
import unittest
import doctest

import harbor
from src import outline
from src import patterns
from src import comments
from src import parse
from src import output

from src.comments import Markup


# ------------------
# ---- COMMENTS ----
# ------------------

class TestParsePath(unittest.TestCase):
    def test_parse_path(self):
        cases = [['abc/def/ghi',('abc','abc/def/ghi')],
                 ['abc',('abc','abc')]]

        for case,expect in cases:
            result = comments.parsePath(case)
            self.assertEqual(result,expect)




class TestExtractMarkup(unittest.TestCase):
    def test_extract_markup(self):
        source = ["",
                  "'''harbor: readme",
                  "",
                  "{harbor}[title]",
                  "*docs made simple*",
                  "'''",
                  "",
                  "",
                  "def makePath(line):",
                  "    '''",
                  "    >>> makePath('harbor: abc/def/ghi')",
                  "    ['abc', 'def', 'ghi']",
                  "    '''",
                  "    assert(line.startswith('harbor: '))",
                  "    line = line[len('harbor: '):].strip()",
                  "    return line.split('/')",
                  "",
                  ""]

        expected = [Markup('readme',
                           [" ",
                            "{harbor}[title] ",
                            "*docs made simple* "])]

        result = comments.extractMarkup(source)
        self.assertEqual(expected,result)




class TestCollateDocs(unittest.TestCase):
    def test_collate_docs(self):
        raw = [Markup('readme',
                      [''])]

        result = comments.collateDocs(raw)
        expected = {'readme': '\n'}
        self.assertEqual(result,expected)

        raw = [Markup('readme',
                      ['aaa ',
                       'bbb ',
                       'ccc '])]

        result = comments.collateDocs(raw)
        expected = {'readme': 'aaa \nbbb \nccc \n'}
        self.assertEqual(result,expected)



class TestGetComments(unittest.TestCase):
    def test_get_comments(self):
        case = [["",
                 "'''harbor: readme",
                 "aaa",
                 "'''",
                 "bbb",
                 "'''",
                 "ccc",
                 "'''",
                 "ddd",
                 "'''harbor: readme",
                 "eee",
                 "fff",
                 "'''"]]

        result = comments.getComments(case)
        expected = {'readme': 'aaa \n'
                              'eee \n'
                              'fff \n'}
        self.assertEqual(result,expected)











# -----------------
# ---- OUTLINE ----
# -----------------

class TestExtractOutline(unittest.TestCase):
    def test_extract_outline(self):
        case = ['OUTLINE',
                'aaa',
                'bbb',
                'ccc',
                '',
                'PATTERNS',
                'ddd',
                'eee',
                'fff',
                '']

        result = outline.extractOutline(case)
        expected = ['aaa',
                    'bbb',
                    'ccc',
                    '']
        self.assertEqual(result,expected)


        case = ['PATTERNS',
                'aaa',
                'bbb',
                'ccc',
                '',
                'OUTLINE',
                'ddd',
                'eee',
                'fff',
                '']

        result = outline.extractOutline(case)
        expected = ['ddd',
                    'eee',
                    'fff',
                    '']
        self.assertEqual(result,expected)


        case = ['OUTLINE',
                'ddd',
                'eee',
                'fff',
                '']

        result = outline.extractOutline(case)
        expected = ['ddd',
                    'eee',
                    'fff',
                    '']
        self.assertEqual(result,expected)


        case = ['PATTERNS',
                'aaa',
                'bbb',
                'ccc',
                '']

        result = outline.extractOutline(case)
        expected = []
        self.assertEqual(result,expected)



class TestGetOutline(unittest.TestCase):
    def test_get_outline(self):
        case = [['OUTLINE',
                'readme: README.md',
                '  aaa',
                '  bbb',
                '    ccc',
                '  ddd',
                '    eee',
                '    fff'],
                ['OUTLINE',
                 'quickstart: quickstart.md',
                 '  step-1',
                 '  step-2',
                 '  step-3']]

        result = outline.getOutline(case)
        expected = {'README.md':['readme',
                                 'readme/aaa',
                                 'readme/bbb',
                                 'readme/bbb/ccc',
                                 'readme/ddd',
                                 'readme/ddd/eee',
                                 'readme/ddd/fff'],
                    'quickstart.md': ['quickstart',
                                      'quickstart/step-1',
                                      'quickstart/step-2',
                                      'quickstart/step-3']}

        self.assertEqual(result,expected)















# ----------------
# ---- OUTPUT ----
# ----------------

class TestToFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_to_files(self):
        case = {path.join(self.test_dir, 'test.md'): 'stuff\n'
                                                     'morestuff\n'
                                                     'hello\n'
                                                     ''}

        output.toFiles(case)

        with open(path.join(self.test_dir, 'test.md'),'r') as f:
            result = f.read()

        expected = '\n'.join(['stuff',
                              'morestuff',
                              'hello',
                              ''])

        self.assertEqual(result,expected)







# ---------------
# ---- PARSE ----
# ---------------


class TestP(unittest.TestCase):
    def test_p(self):
        case = ' '.join(['testing' for i in range(20)])

        result = parse.p(case)
        expected = ''.join(['testing testing testing testing testing ',
                            'testing testing testing testing testing\n',
                            'testing testing testing testing testing ',
                            'testing testing testing testing testing \n'])

        self.assertEqual(result,expected)

        case = ' '.join(['hello' for i in range(20)])

        result = parse.p(case)
        expected = ''.join(['hello hello hello hello hello hello hello ',
                            'hello hello hello hello hello hello\n',
                            'hello hello hello hello hello hello hello \n'])

        self.assertEqual(result,expected)


        case = ' '.join(['reallylongword']*3)

        result = parse.p(case,n=5)
        expected = ''.join(['reallylongword\n',
                            'reallylongword\n',
                            'reallylongword \n'])

        self.assertEqual(result,expected)


class TestParse(unittest.TestCase):
    def test_parse(self):
        case_line = 'hello'
        case_lookup = 'another'
        case_patterns = {'sample': '**{sample}**',
                         'another': '- *`{another}`*'}

        result = parse.parse(case_line,case_lookup,case_patterns)
        expected = '- *`hello`*'

        self.assertEqual(result,expected)




        case_line = 'hello world'
        case_lookup = 'p'
        case_patterns = {'sample': '**{sample}**',
                         'another': '- *`{another}`*'}

        result = parse.parse(case_line,case_lookup,case_patterns)
        expected = parse.p(case_line)

        self.assertEqual(result,expected)



class TestGetMacros(unittest.TestCase):
    def test_get_macros(self):
        case_text = '{abc}[another] {def}[sample]\n'
        case_valid = ['another', 'sample']

        result = parse.getMacros(case_text,case_valid)
        expected = ['',
                    ('abc', 'another'),
                    ' ',
                    ('def', 'sample'),
                    '\n']

        self.assertEqual(result,expected)




class TestApplyPatterns(unittest.TestCase):
    def test_apply_patterns(self):
        case_groups = {'aaa/bbb/ccc': '{abc}[another] {def}[sample]\n'
                                      '{ghi}[another] {jkl}[sample]\n',
                       'iii/jjj/kkk': '{mno}[another] {pqr}[sample]\n'
                                      '{stu}[another] {vwx}[sample]\n'}
        case_patterns = {'sample': '**{sample}**',
                         'another': '- *`{another}`*'}

        result = parse.applyPatterns(case_groups,case_patterns)
        expected = {'iii/jjj/kkk': '- *`mno`* **pqr**\n'
                                   '- *`stu`* **vwx**\n',
                    'aaa/bbb/ccc': '- *`abc`* **def**\n'
                                   '- *`ghi`* **jkl**\n'}

        self.assertEqual(result,expected)



class TestMakeAttrib(unittest.TestCase):
    def test_make_attrib(self):
        result = parse.makeAttrib()

        self.assertTrue('https://www.github.com/crgirard/harbor' in result)
        self.assertTrue('ocumentation generated by' in result)





class TestStructure(unittest.TestCase):
    def test_structure(self):
        case_comments = {'aaa/bbb': 'hello,',
                         'aaa/ccc': 'world!'}

        case_outline = {'readme.md':['aaa',
                                     'aaa/bbb',
                                     'aaa/ccc']}

        result = parse.structure(case_comments,case_outline)
        expected = {'readme.md': ['hello,', 'world!']}

        self.assertEqual(result,expected)



        case_comments = {'aaa/bbb': 'hello,',
                         'aaa/ccc': 'world!'}

        case_outline = {'readme.md':['aaa',
                                     'aaa/bbb',
                                     'aaa/ccc']}

        result = parse.structure(case_comments,case_outline,credit=True)
        expected = {'readme.md': ['hello,', 'world!']}

        self.assertEqual(list(result.keys())[0],'readme.md')
        v = result['readme.md']
        self.assertEqual(v[0],'hello,')
        self.assertEqual(v[1],'world!')
        self.assertEqual(v[2],parse.makeAttrib())


















# ------------------
# ---- PATTERNS ----
# ------------------

class TestExtractPatterns(unittest.TestCase):
    def test_extract_patterns(self):
        case = ['OUTLINE',
                'aaa',
                'bbb',
                'ccc',
                '',
                'PATTERNS',
                'ddd',
                'eee',
                'fff',
                '']

        result = patterns.extractPatterns(case)
        expected = ['ddd',
                    'eee',
                    'fff',
                    '']
        self.assertEqual(result,expected)


        case = ['PATTERNS',
                'aaa',
                'bbb',
                'ccc',
                '',
                'OUTLINE',
                'ddd',
                'eee',
                'fff',
                '']

        result = patterns.extractPatterns(case)
        expected = ['aaa',
                    'bbb',
                    'ccc',
                    '']
        self.assertEqual(result,expected)


        case = ['OUTLINE',
                'ddd',
                'eee',
                'fff',
                '']

        result = patterns.extractPatterns(case)
        expected = []
        self.assertEqual(result,expected)


        case = ['PATTERNS',
                'aaa',
                'bbb',
                'ccc',
                '']

        result = patterns.extractPatterns(case)
        expected = ['aaa',
                    'bbb',
                    'ccc',
                    '']
        self.assertEqual(result,expected)






class TestParsePatterns(unittest.TestCase):
    def test_parse_patterns(self):
        case = ['aaa:',
                '    **{aaa}**',
                '',
                'bbb:',
                '    ## {bbb}',
                '    *{bbb}*',
                '',
                'ccc:',
                '    ### {ccc}',
                '',
                '    **{ccc}**',
                '']

        result = patterns.parsePatterns(case)
        expected = {'aaa': '**{aaa}**\n',
                    'bbb': '## {bbb}\n*{bbb}*\n',
                    'ccc': '### {ccc}\n\n**{ccc}**\n'}

        self.assertEqual(result,expected)



        case = ['',
                '',
                '',
                'a:',
                '    **{a}**',
                '',
                'bbb:',
                '    ## {bbb}',
                '    *{bbb}*',
                '',
                'ccc:',
                '    ### {ccc}',
                '',
                '    **{ccc}**',
                '']

        result = patterns.parsePatterns(case)
        expected = {'a': '**{a}**\n',
                    'bbb': '## {bbb}\n*{bbb}*\n',
                    'ccc': '### {ccc}\n\n**{ccc}**\n'}

        self.assertEqual(result,expected)






























class TestFetchFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        with open(path.join(self.test_dir, 'test.py'), 'w') as f:
            f.write('\n'.join(['aaa',
                               '    bbb',
                               '    ccc']))

        with open(path.join(self.test_dir, 'test.harbor'), 'w') as f:
            f.write('\n'.join(['OUTLINE',
                               'readme: README.md',
                               '  aaa',
                               '    bbb',
                               '    ccc',
                               '',
                               '  ddd',
                               '    eee',
                               '',
                               '',
                               'PATTERNS',
                               '',
                               'sample:',
                               '    ' + '*{sample}*',
                               '',
                               'sample2:',
                               '    ' + '**{sample2}**',
                               '',
                               'sample3:',
                               '    ' + '`{sample3}`',
                               ]))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_source(self):
        results = harbor.loadFile(path.join(self.test_dir, 'test.py'))

        expected = ['aaa',
                    '    bbb',
                    '    ccc']

        self.assertEqual(results,expected)

    def test_load_pattern(self):
        results = harbor.loadFile(path.join(self.test_dir, 'test.harbor'))

        expected = ['OUTLINE',
                    'readme: README.md',
                    '  aaa',
                    '    bbb',
                    '    ccc',
                    '',
                    '  ddd',
                    '    eee',
                    '',
                    '',
                     'PATTERNS',
                    '',
                    'sample:',
                    '    *{sample}*',
                    '',
                    'sample2:',
                    '    **{sample2}**',
                    '',
                    'sample3:',
                    '    `{sample3}`']


        self.assertEqual(results,expected)











class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'test.py'), 'w') as f:
            f.write('\n'.join(['# some comments',
                               "'''harbor: test/aaa/bbb",
                               'stuff',
                               'morestuff',
                               "'''",
                               'a = 4',
                               'b = 2',
                               ' ',
                               "'''harbor: test/ddd",
                               'hello',
                               "'''",
                               'e = 5']))

        with open(path.join(self.test_dir, 'test.harbor'), 'w') as f:
            f.write('\n'.join(['OUTLINE',
                               'test: ' + path.join(self.test_dir,'test.md'),
                               '  aaa',
                               '    bbb',
                               '    ccc',
                               '  ddd',
                               '    eee',
                               'PATTERNS',
                               'sample:',
                               '    **{sample}**',
                               'another:',
                               '    - *`{another}`*']))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_integration(self):
        harbor.exe(path.join(self.test_dir, 'test.py'),
                   path.join(self.test_dir, 'test.harbor'),
                   debug=True)
        harbor.exe(path.join(self.test_dir, 'test.py'),
                   path.join(self.test_dir, 'test.harbor'),
                   debug=False)

        with open(path.join(self.test_dir, 'test.md'),'r') as f:
            data = f.read()

        expected = '\n'.join(['stuff ',
                              'morestuff ',
                              'hello ',
                              ''])

        self.assertEqual(data,expected)


def load_tests(loader, tests, ignore):
    for f in [harbor, outline, patterns, comments, parse, output]:
        try:
            tests.addTests(doctest.DocTestSuite(f))
        except:
            pass
    return tests


if __name__ == '__main__':
    unittest.main()
