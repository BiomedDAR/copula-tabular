import unittest
import pickle
import sys, os

# run this in cmd: python -m mz.tests.test_transformer -v

if __name__ == '__main__':
    if __package__ is None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        par_dir = os.path.dirname(dir_path)
        sys.path.insert(0, par_dir)
        head, sep, tail = dir_path.partition('copula-tabular')
        sys.path.insert(0, head+sep) # adding par_dir to system path


from bdarpack.Transformer import Transformer
from bdarpack import utils_ as ut_

class TestTransformerMethods(unittest.TestCase):

    def setUp(self):

        # rawData generated using following specifications:
        # dtypes = ['bool', 'float', 'int', 'datetime', 'str', 'str', 'str', 'str']
        # nans = [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        # size = 12

        # rawData_df = ut_.gen_randomData(dtypes=dtypes, nans=nans, size=size)

        # filename = "C:/Users/tanmz/OneDrive - A STAR/DAR/synData/copula-tabular/mz/tests/rawData/transformer_testSet_1.pkl"
        # pk_filename = open(filename, "wb")
        # pickle.dump(rawData_df, pk_filename)
        # pk_filename.close()

        dir_path = os.path.dirname(os.path.realpath(__file__))

        testset_filename = dir_path+'/rawData/'+"transformer_testSet_1.pkl"
        with open(testset_filename, 'rb') as fl:
            self.rawData_1_df = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"transformer_gdtruth_1.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gd_truth_1 = pickle.load(fl)

    def test_transformer(self):

        metadata = {
            '2_float': {
                'null': '33'
            },
            '3_int': {
                'null': 'mean'
            },
            '4_datetime': {
                'null': 'mean',
                'datetime_format': f"%Y-%m-%d %H:%M:%S"
            },
            '5_str': {
                'transformer_type': 'Cat1'
            },
            '6_str': {
                'transformer_type': 'Cat1Fuzzy'
            },
            '7_str': {
                'transformer_type': 'One-Hot'
            },
            '8_str': {
                'transformer_type': 'LabelEncoding'
            }
        }

        transformer = Transformer(
            metaData=metadata,
            debug=False
        )
        numeric_df = transformer.transform(self.rawData_1_df)

        cols = list(self.gd_truth_1.columns)
        cols.remove('6_str.value') #fuzzy
        cols.remove('8_str.value') #random assignation of labels
        for col in cols:
            gdtruth_col = self.gd_truth_1[col]
            tr_col = numeric_df[col]
            if gdtruth_col.isnull().any():
                gdtruth_col_null_boolean = gdtruth_col.isnull()
                tr_col_null_boolean = tr_col.isnull()
                for index,value in gdtruth_col_null_boolean.items():
                    self.assertEqual(value, tr_col_null_boolean[index])

                gdtruth_nonull_col = gdtruth_col[~gdtruth_col_null_boolean]
                tr_nonull_col = tr_col[~tr_col_null_boolean]
                for index,value in gdtruth_nonull_col.items():
                    self.assertEqual(value, tr_nonull_col[index])

            else:
                for index, value in gdtruth_col.items():
                    self.assertEqual(value, tr_col[index])

        reversed_df = transformer.reverse(numeric_df)
        cols = list(self.rawData_1_df.columns)
        for col in cols:
            gdtruth_col = self.rawData_1_df[col]
            tr_col = reversed_df[col]
            if gdtruth_col.isnull().any():
                gdtruth_col_null_boolean = gdtruth_col.isnull()
                tr_col_null_boolean = tr_col.isnull()
                for index,value in gdtruth_col_null_boolean.items():
                    self.assertEqual(value, tr_col_null_boolean[index])

                gdtruth_nonull_col = gdtruth_col[~gdtruth_col_null_boolean]
                tr_nonull_col = tr_col[~tr_col_null_boolean]
                for index,value in gdtruth_nonull_col.items():
                    self.assertEqual(value, tr_nonull_col[index])

            else:
                for index, value in gdtruth_col.items():
                    self.assertEqual(value, tr_col[index])


if __name__ == '__main__':
    if __package__ is None:
        test = TestTransformerMethods()
        test.setUp()
        test.test_transformer()

        test.tearDown()
    else:
        unittest.main()