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

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_something(self):
        results = harbor.loadFile(path.join(self.test_dir, 'test.py'))

        expected = ['aaa',
                    '    bbb',
                    '    ccc']

        self.assertEqual(results,expected)


class TestGetOutline(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        with open(path.join(self.test_dir, 'test.harbor'), 'w') as f:
            f.write('\n'.join(['OUTLINE',
                               'quickstart: quickstart.md',
                               '  aaa',
                               '    bbb',
                               '    ccc',
                               '  ddd',
                               '    eee',
                               'PATTERNS',
                               'sample:',
                               '    **{sample}**']))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_getOutline(self):
        results = harbor.getOutline(path.join(self.test_dir, 'test.harbor'))

        expected = {'quickstart': {'contents': ['quickstart',
                                                'quickstart/aaa',
                                                'quickstart/aaa/bbb',
                                                'quickstart/aaa/ccc',
                                                'quickstart/ddd',
                                                'quickstart/ddd/eee'],
                                   'filename': 'quickstart.md'}}

        self.assertEqual(results,expected)

class TestGetPatterns(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'test.harbor'), 'w') as f:
            f.write('\n'.join(['OUTLINE',
                               'quickstart: quickstart.md',
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

    def test_getPatterns(self):
        results = harbor.getPatterns(path.join(self.test_dir, 'test.harbor'))

        expected = {'sample': '**{sample}**',
                    'another': '- *`{another}`*'}

        self.assertEqual(results,expected)


class TestGetDocs(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'test.py'), 'w') as f:
            f.write('\n'.join(['# some comments',
                               "'''",
                               'harbor: aaa/bbb/ccc',
                               'stuff',
                               'morestuff',
                               "'''",
                               'a = 4',
                               'b = 2',
                               ' ',
                               "'''",
                               'harbor: iii/jjj/kkk',
                               'hello',
                               "'''",
                               'e = 5']))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_docs(self):
        results = harbor.getDocs(path.join(self.test_dir, 'test.py'))

        expected = {'aaa': {'aaa/bbb/ccc': ['stuff',
                                            'morestuff']},
                    'iii': {'iii/jjj/kkk': ['hello']}}

        self.assertEqual(results,expected)


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
        harbor.makeDocs(path.join(self.test_dir, 'test.py'),
                        path.join(self.test_dir, 'test.harbor'),
                        debug=True)
        harbor.makeDocs(path.join(self.test_dir, 'test.py'),
                        path.join(self.test_dir, 'test.harbor'),
                        debug=False)

        with open(path.join(self.test_dir, 'test.md'),'r') as f:
            data = f.read()

        self.assertEqual(data,' \nstuff \nmorestuff \n \nhello \n')


class TestExtractBlockComments(unittest.TestCase):
    def test_extract_block_comments(self):
        test = """
        aaa
        '''
        bbb
        ccc
        '''
        ddd
        """.split('\n')

        results = harbor.extractBlockComments(test)
        self.assertEqual(results,[['bbb', 'ccc']])

class TestGetOnlyHarborMarkup(unittest.TestCase):
    def test_get_only_harbor_markup(self):
        test = """
        aaa
        '''
        harbor: abc/def/ghi
        bbb
        '''
        ccc
        """.split('\n')

        results = harbor.extractBlockComments(test)
        results = harbor.getOnlyHarborMarkup(results)
        self.assertEqual(results,[['harbor: abc/def/ghi', 'bbb']])

class TestExtractPatternSection(unittest.TestCase):
    def test_extract_pattern_section(self):
        test = '''
        OUTLINE
        aaa
        bbb

        PATTERNS
        ccc
        ddd
        '''

        test = [t.strip() for t in test.split('\n') if t.strip() != '']

        results = harbor.extractPatternSection(test)
        self.assertEqual(results,['ccc','ddd'])

class TestExtractOutlineSection(unittest.TestCase):
    def test_extract_outline_section(self):
        test = '''
        OUTLINE
        aaa
        bbb

        PATTERNS
        ccc
        ddd
        '''

        test = [t.strip() for t in test.split('\n') if t.strip() != '']

        results = harbor.extractOutlineSection(test)
        self.assertEqual(results,['aaa','bbb'])


class TestParse(unittest.TestCase):
    def test_parse(self):
        test = '{hello}[another] {world}[sample]'

        patterns = {'sample': '**{sample}**',
                    'another': '- *`{another}`*'}

        result = harbor.parse(test,patterns)
        expected = '- *`hello`* **world**'

        self.assertEqual(result,expected)


        test = '{hello}[another] {world}[sample2]'

        patterns = {'sample': '**{sample}**',
                    'another': '- *`{another}`*'}

        result = harbor.parse(test,patterns)
        expected = '- *`hello`* {world}[sample2]'

        self.assertEqual(result,expected)



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(harbor))
    return tests


if __name__ == '__main__':
    unittest.main()
