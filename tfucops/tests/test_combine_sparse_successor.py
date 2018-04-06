# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from .. import combine_sparse_successor


class CombineSparseScuccessorTest(tf.test.TestCase):
    def testInferenceShape(self):
        source = [
            'abcde fghi',
            'jkl mn',
            'o'
        ]

        parent = tf.string_split(source, delimiter=' ')
        child = tf.string_split(parent.values, delimiter='')
        result = combine_sparse_successor(
            parent.indices,
            parent.dense_shape,
            child.indices,
            child.values,
            child.dense_shape
        )

        self.assertEqual([None, 3], result.indices.shape.as_list())
        self.assertEqual([None], result.values.shape.as_list())
        self.assertEqual([3], result.dense_shape.shape.as_list())

    def testActualShape(self):
        source = [
            'abcde fghi',
            'jkl mn',
            'o'
        ]

        parent = tf.string_split(source, delimiter=' ')
        child = tf.string_split(parent.values, delimiter='')
        result = combine_sparse_successor(
            parent.indices,
            parent.dense_shape,
            child.indices,
            child.values,
            child.dense_shape
        )

        result_indices = tf.shape(result.indices)
        result_values = tf.shape(result.values)
        result_shape = tf.shape(result.dense_shape)

        with self.test_session():
            result_indices, result_values, result_shape = result_indices.eval(), result_values.eval(), result_shape.eval()
            print(result_indices)
            self.assertEqual([15, 3], result_indices.tolist())
            self.assertEqual([15], result_values.tolist())
            self.assertEqual([3], result_shape.tolist())

    def testEmptyParent(self):
        parent = tf.SparseTensor(
            indices=tf.constant([], shape=[0, 2], dtype=tf.int64),
            values=tf.constant([], dtype=tf.string),
            dense_shape=[1,0]
        )
        child = tf.string_split(parent.values, delimiter='')
        result = combine_sparse_successor(
            parent.indices,
            parent.dense_shape,
            child.indices,
            child.values,
            child.dense_shape
        )

        with self.test_session():
            print(parent.eval())
            print(child.eval())
            result = result.eval()
            self.assertEqual([], result.indices.tolist())
            self.assertEqual([], result.values.tolist())
            self.assertEqual([1, 0, 0], result.dense_shape.tolist())

    def test1DParent(self):
        parent = tf.SparseTensor(
            indices=[[0,0]],
            values=[b'0d'],
            dense_shape=[1,1]
        )
        child = tf.string_split(parent.values, delimiter='')
        result = combine_sparse_successor(
            parent.indices,
            parent.dense_shape,
            child.indices,
            child.values,
            child.dense_shape
        )

        with self.test_session():
            result = result.eval()
            self.assertEqual([[0,0,0], [0,0,1]], result.indices.tolist())
            self.assertEqual([b'0', b'd'], result.values.tolist())
            self.assertEqual([1, 1, 2], result.dense_shape.tolist())

    def testFullRows(self):
        source = [
            'abcde fghi',
            'jkl mn',
            'o'
        ]

        parent = tf.string_split(source, delimiter=' ')
        child = tf.string_split(parent.values, delimiter='')
        result = combine_sparse_successor(
            parent.indices,
            parent.dense_shape,
            child.indices,
            child.values,
            child.dense_shape
        )

        expected = tf.SparseTensor(
            indices=[
                [0, 0, 0],
                [0, 0, 1],
                [0, 0, 2],
                [0, 0, 3],
                [0, 0, 4],

                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 2],
                [0, 1, 3],

                [1, 0, 0],
                [1, 0, 1],
                [1, 0, 2],

                [1, 1, 0],
                [1, 1, 1],

                [2, 0, 0],
            ],
            values=[
                'a', 'b', 'c', 'd', 'e',
                'f', 'g', 'h', 'i',
                'j', 'k', 'l',
                'm', 'n',
                'o'
            ],
            dense_shape=[3, 2, 5]
        )

        with self.test_session():
            expected, result = expected.eval(), result.eval()
            self.assertEqual(expected.indices.tolist(), result.indices.tolist())
            self.assertEqual(expected.values.tolist(), result.values.tolist())
            self.assertEqual(expected.dense_shape.tolist(), result.dense_shape.tolist())

    def testEmptyRows(self):
        parent = tf.SparseTensor(
            indices=[
                [0, 0],
                [0, 1],
                # empty row
                [2, 0],
            ],
            values=[
                'abc', 'de',
                # empty row
                'g'
            ],
            dense_shape=[3, 2]
        )
        child = tf.string_split(parent.values, delimiter='')
        result = combine_sparse_successor(
            parent.indices,
            parent.dense_shape,
            child.indices,
            child.values,
            child.dense_shape
        )

        expected = tf.SparseTensor(
            indices=[
                [0, 0, 0],
                [0, 0, 1],
                [0, 0, 2],

                [0, 1, 0],
                [0, 1, 1],

                # empty row

                [2, 0, 0],
            ],
            values=[
                'a', 'b', 'c',
                'd', 'e',
                # empty row
                'g',
            ],
            dense_shape=[3, 2, 3]
        )

        with self.test_session():
            expected, result = expected.eval(), result.eval()
            self.assertEqual(expected.indices.tolist(), result.indices.tolist())
            self.assertEqual(expected.values.tolist(), result.values.tolist())
            self.assertEqual(expected.dense_shape.tolist(), result.dense_shape.tolist())
