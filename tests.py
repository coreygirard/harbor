import shutil, tempfile
from os import path
import unittest
import doctest
import harbor

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



class TestExtractComments(unittest.TestCase):
    def test_extract_comments(self):
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

        expected = [["harbor: readme",
                     "",
                     "{harbor}[title]",
                     "*docs made simple*"],
                    ["",
                     ">>> makePath('harbor: abc/def/ghi')",
                     "['abc', 'def', 'ghi']"]]

        result = harbor.extractComments(source)
        self.assertEqual(expected,result)


class TestExtractMarkup(unittest.TestCase):
    def test_extract_markup(self):
        source = [["harbor: readme",
                   "",
                   "{harbor}[title]",
                   "*docs made simple*"],
                  ["",
                   ">>> makePath('harbor: abc/def/ghi')",
                   "['abc', 'def', 'ghi']"],
                  ["harbor: readme",
                   "",
                   "{harbor}[title]",
                   "*docs made simple*"]]

        expected = [["harbor: readme",
                     "",
                     "{harbor}[title]",
                     "*docs made simple*"],
                    ["harbor: readme",
                     "",
                     "{harbor}[title]",
                     "*docs made simple*"]]

        result = harbor.extractMarkup(source)
        self.assertEqual(expected,result)



class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'test.py'), 'w') as f:
            f.write('\n'.join(['# some comments',
                               "'''",
                               'harbor: test/aaa/bbb',
                               'stuff',
                               'morestuff',
                               "'''",
                               'a = 4',
                               'b = 2',
                               ' ',
                               "'''",
                               'harbor: test/ddd',
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
        #harbor.exe(path.join(self.test_dir, 'test.py'),
        #           path.join(self.test_dir, 'test.harbor'),
        #           debug=False)

        #with open(path.join(self.test_dir, 'test.md'),'r') as f:
        #    data = f.read()

        #self.assertEqual(data,' \nstuff \nmorestuff \n \nhello \n')



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(harbor))
    return tests


if __name__ == '__main__':
    unittest.main()
