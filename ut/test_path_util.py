from unittest import TestCase
from path_util import decode_path, encode_path, simplify_path


class TestPathUtil(TestCase):
    def test_simplify_path(self):
        self.assertEqual('/', simplify_path('/'))
        self.assertEqual('/', simplify_path('///'))
        self.assertEqual('/', simplify_path(' / '))
        self.assertEqual('/', simplify_path(' / / '))
        self.assertEqual('/', simplify_path(' // '))
        self.assertEqual('/foo/bar', simplify_path('/foo/bar'))
        self.assertEqual('/foo/bar', simplify_path(' // / / foo  / / bar / '))
        self.assertEqual('/foo bar/bas', simplify_path('/foo bar/bas'))

    def test_encode_path(self):
        self.assertEqual('+', encode_path('/'))
        self.assertEqual('+', encode_path('//'))
        self.assertEqual('+foo+bar', encode_path('/foo/bar'))
        self.assertEqual('+foo+bar', encode_path('/foo/bar/'))
        self.assertEqual('+good food+good people',
                         encode_path(' /good food/good people '))

    def test_decode_path(self):
        self.assertEqual('/', decode_path('+'))
        self.assertEqual('/foo/bar', decode_path('+foo+bar'))
        self.assertEqual('/foo/bar', decode_path('+foo+bar+'))
        self.assertEqual('/good food/good people',
                         decode_path(' +good food+good people '))
