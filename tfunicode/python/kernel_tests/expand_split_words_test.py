# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from builtins import chr
# from future.standard_library import install_aliases
#
# install_aliases()
from tfunicode.python.ops import expand_split_words
# from urllib.request import urlopen
import numpy as np
import tensorflow as tf
import re


class ExpandSplitWordsTest(tf.test.TestCase):
    def testWork(self):
        expected = tf.convert_to_tensor([u'\u0001', u'\u0061' ,u'\u003A'], dtype=tf.string)
        result = expand_split_words(u'\u0001\u0061\u003A')
        result = tf.sparse_tensor_to_dense(result, default_value='')

        with self.test_session():
            expected, result = expected.eval(), result.eval()
            # print(result)
            print([r.decode('utf-8') for r in result])
            self.assertAllEqual(expected, result)

    # def testInferenceShape(self):
    #     source = [
    #         ['1', '2', '3'],
    #         ['4', '5', '6'],
    #     ]
    #     result = expand_split_words(source)
    #
    #     self.assertEqual([None, 3], result.indices.shape.as_list())
    #     self.assertEqual([None], result.values.shape.as_list())
    #     self.assertEqual([3], result.dense_shape.shape.as_list())
    #
    # def testActualShape(self):
    #     source = [
    #         ['1', '2', '3'],
    #         ['4', '5', '6'],
    #     ]
    #     result = expand_split_words(source)
    #
    #     with self.test_session():
    #         result = result.eval()
    #         self.assertAllEqual([2, 3, 1], result.dense_shape)
    #
    # def testEmpty(self):
    #     expected = tf.convert_to_tensor([''], dtype=tf.string)
    #     result = expand_split_words('')
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def test0D(self):
    #     expected = tf.convert_to_tensor(['x', '!'], dtype=tf.string)
    #     result = expand_split_words('x!')
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def test1D(self):
    #     expected = tf.convert_to_tensor([['x', '!']], dtype=tf.string)
    #     result = expand_split_words(['x!'])
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def test2D(self):
    #     expected = tf.convert_to_tensor([[['x', '!']]], dtype=tf.string)
    #     result = expand_split_words([['x!']])
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def testSparse(self):
    #     source = tf.string_split(['ab|c d|e', 'f|'], delimiter='|')
    #     result = expand_split_words(source)
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #     expected = tf.convert_to_tensor([
    #         [
    #             ['ab', '', ''],
    #             ['c', ' ', 'd'],
    #             ['e', '', '']
    #         ],
    #         [
    #             ['f', '', ''],
    #             ['', '', ''],
    #             ['', '', ''],
    #         ]
    #     ], dtype=tf.string)
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected.tolist(), result.tolist())
    #
    # def testRestore(self):
    #     source = u'Hey\n\tthere\t«word», !!!'
    #     expected = tf.convert_to_tensor(source, dtype=tf.string)
    #     result = expand_split_words(source)
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #     result = tf.reduce_join(result)
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def testWrapped(self):
    #     expected = [
    #         [' ', '"', 'word', '"', ' '],
    #         [' ', u'«', 'word', u'»', ' '],
    #         [' ', u'„', 'word', u'“', ' '],
    #         [' ', '{', 'word', '}', ' '],
    #         [' ', '(', 'word', ')', ' '],
    #         [' ', '[', 'word', ']', ' '],
    #         [' ', '<', 'word', '>', ' '],
    #     ]
    #     expected = tf.convert_to_tensor(expected, dtype=tf.string)
    #     result = expand_split_words([
    #         ' "word" ',
    #         u' «word» ',
    #         u' „word“ ',
    #         ' {word} ',
    #         ' (word) ',
    #         ' [word] ',
    #         ' <word> ',
    #     ])
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def testWordPunkt(self):
    #     expected = [
    #         [' ', 'word', '.', ' ', '', ''],
    #         [' ', 'word', '.', '.', ' ', ''],
    #         [' ', 'word', '.', '.', '.', ' '],
    #         [' ', 'word', u'…', ' ', '', ''],
    #         [' ', 'word', ',', ' ', '', ''],
    #         [' ', 'word', '.', ',', ' ', ''],
    #         [' ', 'word', ':', ' ', '', ''],
    #         [' ', 'word', ';', ' ', '', ''],
    #         [' ', 'word', '!', ' ', '', ''],
    #         [' ', 'word', '?', ' ', '', ''],
    #         [' ', 'word', '%', ' ', '', ''],
    #         [' ', '$', 'word', ' ', '', ''],
    #     ]
    #     expected = tf.convert_to_tensor(expected, dtype=tf.string)
    #     result = expand_split_words([
    #         ' word. ',
    #         ' word.. ',
    #         ' word... ',
    #         u' word… ',
    #         ' word, ',
    #         ' word., ',
    #         ' word: ',
    #         ' word; ',
    #         ' word! ',
    #         ' word? ',
    #         ' word% ',
    #         ' $word ',
    #     ])
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)
    #
    # def testComplexWord(self):
    #     expected = [
    #         [' ', 'test', '@', 'test.com', ' ', '', '', '', ''],
    #         [' ', 'www.test.com', ' ', '', '', '', '', '', ''],
    #         [' ', 'word', '.', '.', 'word', ' ', '', '', ''],
    #         [' ', 'word', '+', 'word', '-', 'word', ' ', '', ''],
    #         [' ', 'word', '\\', 'word', '/', 'word', '#', 'word', ' '],
    #     ]
    #     expected = tf.convert_to_tensor(expected, dtype=tf.string)
    #     result = expand_split_words([
    #         ' test@test.com ',
    #         ' www.test.com ',
    #         ' word..word ',
    #         ' word+word-word ',
    #         ' word\\word/word#word ',
    #     ])
    #     result = tf.sparse_tensor_to_dense(result, default_value='')
    #
    #     with self.test_session():
    #         expected, result = expected.eval(), result.eval()
    #         self.assertAllEqual(expected, result)

    def testIcuWordBreak(self):

        ICU_TEST_URL = 'https://www.unicode.org/Public/UCD/latest/ucd/auxiliary/WordBreakTest.txt'

        with open('/Users/alex/HDD/Develop/semtech/tfunicode/WordBreakTest.txt', 'rb') as ft:
            test_data = ft.read().decode('utf-8').strip().split('\n')
        # for line in urlopen(ICU_TEST_URL).readlines():

        expected, source, description = [], [], []
        for row, line in enumerate(test_data):
            if line.startswith('#'):
                continue

            if ' 0308 ' in line:
                continue

            example, rule = line.split('#')

            example = example.strip().strip(u'÷').strip().replace(u'÷', '00F7').replace(u'×', '00D7').split(' ')
            example = [code.zfill(8) if len(code) > 4 else code.zfill(4) for code in example]
            example = [u'\\U{}'.format(code) if len(code) > 4 else u'\\u{}'.format(code) for code in example]
            example = [code.decode('unicode-escape') for code in example]
            example = u''.join(example).replace(u'×', '')

            expected.append(example.split(u'÷'))
            source.append(example.replace(u'÷', ''))

            rule = rule.strip().strip(u'÷').strip()
            description.append(u'Row #{}. {}'.format(row + 1, rule))

        max_len = len(sorted(expected, key=len, reverse=True)[0])
        expected = [e + ['']*(max_len - len(e)) for e in expected]

        expected_tensor = tf.convert_to_tensor(expected, dtype=tf.string)
        result_tensor = tf.sparse_tensor_to_dense(expand_split_words(source), default_value='')

        debug = []
        with self.test_session():
            expected_value, result_value = expected_tensor.eval(), result_tensor.eval()

            for exp, res, desc in zip(expected_value, result_value, description):
                exp = [_ for _ in exp if len(_)]
                res = [_ for _ in res if len(_)]
                if exp != res:
                    desc = desc.split('. ')[1].replace('[0.2]', '').replace('[0.3]', '')
                    desc = re.sub('[^\d\.\[\]]', '', desc)
                    debug.append(desc)
                    # print(expected_value, result_value)
                    # self.assertAllEqual(expected_value.tolist(), result_value.tolist(), desc)
        print('\n'.join(debug))
        # self.assertTrue(False)


if __name__ == "__main__":
    tf.test.main()
