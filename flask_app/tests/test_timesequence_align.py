# -*- coding: utf-8 -*-

__author__ = 'jiaying.lu'

from unittest import TestCase
import numpy as np

from flask_app.timesequence_align import _get_sequence_length, _get_sequence_time_length, _get_time_distribution_params, _get_time_distribution
from flask_app.timesequence_align import generate_sequences_measures, choose_primary_key


class TestInnerMethod(TestCase):

    def test_get_sequence_length(self):
        # case 1
        tmp_list = range(10)
        self.assertEqual(10, _get_sequence_length(tmp_list))

        # case 2
        tmp_list = np.arange(10)
        self.assertEqual(10, _get_sequence_length(tmp_list))

    def test_get_sequence_time_length(self):
        # case 1
        tmp_list = [3, 11, 19, 21]
        self.assertEqual(18, _get_sequence_time_length(tmp_list))

        # case 2
        tmp_list = np.array([3, 11, 19, 21])
        self.assertEqual(18, _get_sequence_time_length(tmp_list))

    def test_get_time_distribution_params(self):
        # case 1
        sequence_list = np.array([[1, 3, 6],
                                  [3, 4, 7, 9],
                                  [2, 4, 6, 9]])
        self.assertEqual((2, 2), _get_time_distribution_params(sequence_list))

        # case 2
        sequence_list = np.array([[1],
                                  [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23],
                                  [2, 4, 6, 9]])
        self.assertEqual((3, 7), _get_time_distribution_params(sequence_list))

    def test_get_time_distribution(self):
        # case 1
        sequence = np.array([1, 2])
        self.assertEqual(0, _get_time_distribution(sequence, 1, 2))
        # case 2
        sequence = np.array([1, 2, 3, 4])
        self.assertEqual(0, _get_time_distribution(sequence, 1, 2))

        # case 3
        sequence = np.array([1, 3, 5])
        self.assertEqual(1, _get_time_distribution(sequence, 1, 2))

        # case 4
        sequence = np.array([1, 2, 3, 4, 5, 6])
        self.assertEqual(8, _get_time_distribution(sequence, 1, 2))
        # case 5
        sequence = np.array([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(8, _get_time_distribution(sequence, 1, 2))


class TestInterfaceMethod(TestCase):

    def test_generate_sequences_measures(self):
        # case 1
        sequence_list = np.array([[1],
                                  [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]])
        measures = np.array([[1, 0, 0],
                             [11, 20, 48]])
        np.testing.assert_array_equal(measures, generate_sequences_measures(sequence_list))

        # case 2
        # TODO: 这其实是一个 badcase，算第三行的 time_dis measure 不是从1开始算，而是从3开始算 [3,10),[10,17),[17,24)
        sequence_list = np.array([[1],
                                  [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23],
                                  [1, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]])
        measures = np.array([[1, 0, 0],
                             [11, 20, 48],
                             [13, 18, 42]])
        np.testing.assert_array_equal(measures, generate_sequences_measures(sequence_list))

    def test_choose_primary_key(self):
        # TODO: add more cases
        data = {
            "filter": 100,
            "key0": [{'timestamp': 2}, {'timestamp': 4}, {'timestamp': 6}, {'timestamp': 9}],
            "key1": [{'timestamp': 3}, {'timestamp': 4}, {'timestamp': 7}, {'timestamp': 9}],
            "key2": [],
            "primaryKey": "key2"
        }
        self.assertEqual('key0', choose_primary_key(data))