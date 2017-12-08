import unittest
import doctest
import harbor


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




def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(harbor))
    return tests


if __name__ == '__main__':
    unittest.main()
