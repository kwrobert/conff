import os
from unittest import TestCase

import yaml
from cryptography.fernet import Fernet

import conff


class ConffTestCase(TestCase):
    def setUp(self):
        super(ConffTestCase, self).setUp()
        # set path
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data_path = os.path.join(current_path, 'data')

    def get_test_data_path(self, fs_path: str):
        return os.path.join(self.test_data_path, fs_path)

    def test_simple_load_yaml(self):
        fs_path = self.get_test_data_path('test_config_01.yml')
        data = conff.load(fs_path=fs_path)
        data = data if data else {}
        self.assertDictEqual(data, {'test_1': 'test_1', 'test_2': ''})

    def test_complex_load_yml(self):
        fs_path = self.get_test_data_path('test_config_02.yml')
        key = Fernet.generate_key()
        errs = []
        data = conff.load(fs_path=fs_path, params={'ekey': key}, errors=errs)
        data = data if data else {}
        if errs:
            print("Error list: ", errs)
        # test simple types
        self.assertEqual(data.get('test_1'), 'test_1')
        self.assertEqual(data.get('test_2'), 2)
        self.assertListEqual(data.get('test_3'), ['test_3', 3])
        self.assertDictEqual(data.get('test_4'), {'test_4_1': 'test_4_1'})
        self.assertDictEqual(data.get('test_5'), {'test_5_1': 'test_5_1', 'test_5_2': {'test_5_2_1': 'test_5_2_1'}})
        # test expression
        self.assertEqual(data.get('test_6'), 'test_6')
        # test extends
        self.assertListEqual(data.get('test_7', {}).get('test_7_1'), [1, 2])
        self.assertListEqual(data.get('test_7', {}).get('test_7_2'), [1, 2])
        self.assertDictEqual(data.get('test_7', {}).get('test_7_3'), {'data2_1': 1, 'data2_2': 2, 'data2_3': 3})
        # test complex extends
        self.assertDictEqual(data.get('test_8'), {'data2_1': 1, 'data2_2': '2a', 'data2_3': 3, 'data2_4': 4})
        # test complex expressions
        self.assertListEqual(data.get('test_9', {}).get('test_9_1'), [True, False, True, False])
        self.assertListEqual(data.get('test_9', {}).get('test_9_2'), [1, 'RO'])
        self.assertEqual(data.get('test_9', {}).get('test_9_3'), '1 2 3')
        self.assertEqual(data.get('test_9', {}).get('test_9_4'), 'ro/ro')
        # test error expressions
        self.assertEqual(data.get('test_10'), 'F.no_exist()')
        # test encryption
        self.assertEqual(data.get('test_11'), 'test_11')
        # test importing
        self.assertDictEqual(data.get('test_12'), {'test_1': 'test_1', 'test_2': ''})
        # test update
        data_test_13 = {'test_13_1': 1, 'test_13_2': 2, 'test_13_3': 3, 'test_13_5': {'test_13_5_1': 1},
                        'test_13_6': {'test_13_6_1': 1}}
        self.assertDictEqual(data.get('test_13'), data_test_13)
        # test extend + update
        data_test_14 = {'test_13_1': 11, 'test_13_2': 2, 'test_13_3': 3, 'test_13_5': 5,
                        'test_13_6': {'test_13_6_1': 1, 'test_13_6_2': {'test_13_6_2_1': 1, 'test_13_6_2_2': 2}},
                        'test_13_4': 4}
        self.assertDictEqual(data.get('test_14'), data_test_14)
        # test foreach with linspace
        data_test_15 = {'test0': {'value': 0, 'length': 3},
                        'test1': {'value': 3, 'length': 3},
                        'test2': {'value': 6, 'length': 3}}
        self.assertDictEqual(data.get('test_15'), data_test_15)
        # test foreach with arange. Should get same result as above
        data_test_16 = data_test_15
        self.assertDictEqual(data.get('test_16'), data_test_16)
        # test foreach with arange. Testing behavior of arange
        data_test_17 = {'test0': {'value': 0, 'length': 2},
                        'test1': {'value': 4, 'length': 2}}
        self.assertDictEqual(data.get('test_17'), data_test_17)

    def test_error_load_yaml(self):
        fs_path = self.get_test_data_path('test_config_03.yml')
        data = conff.load(fs_path=fs_path)
        self.assertIsNone(data)

    def test_parse(self):
        data = conff.parse('{"a": "a", "b": "1/0"}', names={}, fns={})
        self.assertDictEqual(data, {'a': 'a', 'b': '1/0'})

    def test_encryption(self):
        # generate key, save it somewhere safe
        names = {'R': {'_': {'etype': 'fernet'}}}
        etype = conff.generate_key(names)()
        ekey = 'FOb7DBRftamqsyRFIaP01q57ZLZZV6MVB2xg1Cg_E7g='
        names = {'R': {'_': {'etype': 'fernet', 'ekey': ekey}}}
        original_value = 'ACCESSSECRETPLAIN1234'
        encrypted_value = conff.encrypt(names)(original_value)
        # decrypt data
        value = conff.decrypt(names)(encrypted_value)
        self.assertEqual(original_value, value, 'Value mismatch')

    def test_sample(self):
        # nose2 conff.test.ConffTestCase.test_sample
        fs_path = self.get_test_data_path('sample_config_01.yml')
        with open(fs_path) as stream:
            r1 = yaml.safe_load(stream)
        fs_path = self.get_test_data_path('sample_config_02.yml')
        ekey = 'FOb7DBRftamqsyRFIaP01q57ZLZZV6MVB2xg1Cg_E7g='
        errors = []
        r2 = conff.load(fs_path=fs_path, params={'ekey': ekey}, errors=errors)
        print(errors)
        fs_path = self.get_test_data_path('sample_config_03.yml')
        r3 = conff.load(fs_path=fs_path, params={'ekey': ekey})
        self.assertDictEqual(r1['job'], r2['job'], 'Mismatch value')
        self.assertDictEqual(r2['job'], r3['job'], 'Mismatch value')

    def test_object(self):
        # nose2 conff.test.ConffTestCase.test_object
        # TODO: add test when trying to combine config as object with conff
        # test update
        class Test(object):
            test = None

        data = Test()
        conff.update(data, {'test': 'test'})
        self.assertEqual('test', data.test, 'Value mismatch')
