# from unittest import TestCase
import unittest
import pickle
import sys, os
import math

if __name__ == '__main__':
    if __package__ is None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        par_dir = os.path.dirname(dir_path)
        sys.path.insert(0, par_dir)
        head, sep, tail = dir_path.partition('copula-tabular')
        sys.path.insert(0, head+sep) # adding par_dir to system path

        from mz.CleanData import CleanData
        from mz.Constraints import Constraints
        import definitions as defi
        import definitions_date as defi_date
        import script_nhanes_constraints as n_con
    else: #run cmd python -m mz.tests.test_clean -v
        from mz.CleanData import CleanData
        from mz.Constraints import Constraints
        from mz.tests import definitions as defi
        from mz.tests import definitions_date as defi_date
        from mz.tests import script_nhanes_constraints as n_con

class TestCleanDataMethods(unittest.TestCase):

    def setUp(self):
        self.defi_date = defi_date
        self.defi = defi

        dir_path = os.path.dirname(os.path.realpath(__file__))

        # load definitions_settings ground truth for dates
        # self.cd_defi = CleanData(definitions=self.defi_date, debug=False)

        gd_filename = dir_path+'/rawData/'+"date_dataset_dict_definitions_gdtruth_dd.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gd_truth_defi_dd = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"date_dataset_dict_definitions_gdtruth_dd_con.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gd_truth_defi_dd_con = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"date_dataset_dict_definitions_gdtruth_dd_case.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gd_truth_defi_dd_case = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"date_dataset_dict_definitions_gdtruth_dates.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gdtruth_defi_dates = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"date_dataset_dict_definitions_gdtruth_ascii.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gdtruth_defi_ascii = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"date_dataset_dict_definitions_gdtruth_dates_ascii.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gdtruth_defi_dates_ascii = pickle.load(fl)

        gd_filename = dir_path+'/rawData/'+"date_dataset_manualSettings_gdtruth_dates.pkl"
        with open(gd_filename, 'rb') as fl:
            self.gdtruth_manual_dates = pickle.load(fl)

    # def tearDown(self):
    #     self.defi_date.dispose()

    def test_cleanData_dd_dict_definitions(self):
        cd = CleanData(
            definitions=self.defi,
            debug=False
        )

        # clean data by dropping duplicate rows
        cd.drop_duplicate_rows()

        cols = ['TESTID']
        for index, row in self.gd_truth_defi_dd.iterrows():
            for col in cols:
                self.assertEqual(cd.clean_df[col][index], row[col])

    def test_cleanData_con_dict_definitions(self):
        cd = CleanData(
            definitions=self.defi,
            debug=False
        )

        cd.drop_duplicate_rows()
        
        df = cd.clean_df
        con = Constraints(debug=False)
        df, con = n_con.con_ageDecade(df, con)
        df, con = n_con.con_ageMonths(df, con)
        df, con = n_con.con_Race3(df, con)
        df, con = n_con.con_GenderEducationMaritalStatus(df, con)
        df, con = n_con.con_HHIncome(df, con)
        df, con = n_con.con_HomeWork(df, con)
        df, con = n_con.con_WeightHeight(df, con)
        df, con = n_con.con_BMI(df, con, bmiChartPerc_filename=f"{cd.raw_data_path}bmiagerev.xls")
        df, con = n_con.con_Testosterone(df, con)
        df, con = n_con.con_cholUrine(df, con)
        df, con = n_con.con_diabetes(df, con)
        df, con = n_con.con_HealthGen(df, con)
        df, con = n_con.con_Depression(df, con)
        df, con = n_con.con_Pregnancies(df, con)
        df, con = n_con.con_Activeness(df, con)
        df, con = n_con.con_Activity(df, con)
        df, con = n_con.con_Alcohol(df, con)
        df, con = n_con.con_Smoking(df, con)
        df, con = n_con.con_Drugs(df, con)
        df, con = n_con.con_Sex(df, con)
        df, con = n_con.con_Pregnancies_2(df, con)

        # Update the CleanData class with constrained data
        cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)

        cols = list(self.gd_truth_defi_dd_con.columns)
        for col in cols:
            gdtruth_col = self.gd_truth_defi_dd_con[col]
            cd_col = cd.clean_df[col]
            if gdtruth_col.isnull().any():
                gdtruth_col_null_boolean = gdtruth_col.isnull()
                cd_col_null_boolean = cd_col.isnull()
                for index,value in gdtruth_col_null_boolean.items():
                    self.assertEqual(value, cd_col_null_boolean[index])

                gdtruth_nonull_col = gdtruth_col[~gdtruth_col_null_boolean]
                cd_nonull_col = cd_col[~cd_col_null_boolean]
                for index,value in gdtruth_nonull_col.items():
                    self.assertEqual(value, cd_nonull_col[index])
            else:
                for index, value in gdtruth_col.items():
                    self.assertEqual(value, cd_col[index])

    def test_cleanData_case_dict_definitions(self):
        cd = CleanData(
            definitions=self.defi,
            debug=False
        )

        # clean data by dropping duplicate rows
        cd.drop_duplicate_rows()
        # Clean the data by standardising all to uppercase/lowercase
        cd.standardise_text()

        cols = list(self.gd_truth_defi_dd_case.columns)
        for col in cols:
            gdtruth_col = self.gd_truth_defi_dd_case[col]
            cd_col = cd.clean_df[col]
            if gdtruth_col.isnull().any():
                gdtruth_col_null_boolean = gdtruth_col.isnull()
                cd_col_null_boolean = cd_col.isnull()
                for index,value in gdtruth_col_null_boolean.items():
                    self.assertEqual(value, cd_col_null_boolean[index])

                gdtruth_nonull_col = gdtruth_col[~gdtruth_col_null_boolean]
                cd_nonull_col = cd_col[~cd_col_null_boolean]
                for index,value in gdtruth_nonull_col.items():
                    self.assertEqual(value, cd_nonull_col[index])
            else:
                for index, value in gdtruth_col.items():
                    self.assertEqual(value, cd_col[index])

    def test_cleanData_date_dict_definitions(self):
        cd = CleanData( #initialise class
            definitions=self.defi_date,
            debug=False
        )
        cd.standardise_date() #run standardise_date using settings in definitions
        
        cols = list(self.gdtruth_defi_dates.columns)
        for index, row in self.gdtruth_defi_dates.iterrows():
            for col in cols:
                self.assertEqual(cd.clean_df[col][index], row[col])

    def test_cleanData_ascii_dict_definitions(self):
        cd = CleanData(
            definitions=self.defi_date,
            debug=False
        )
        cd.converting_ascii() #run ascii conversion using settings in definitions

        cols = list(self.gdtruth_defi_ascii.columns)
        for index, row in self.gdtruth_defi_ascii.iterrows():
            for col in cols:
                self.assertEqual(cd.clean_df[col][index], row[col])

    def test_cleanData_date_ascii_dict_definitions(self):
        cd = CleanData(
            definitions=self.defi_date,
            debug=False
        )
        cd.standardise_date()
        cd.converting_ascii()

        cols = list(self.gdtruth_defi_dates_ascii.columns)
        for index, row in self.gdtruth_defi_dates_ascii.iterrows():
            for col in cols:
                self.assertEqual(cd.clean_df[col][index], row[col])

    def test_cleanData_date_manualSettings(self):
        cd = CleanData(
            definitions=self.defi_date,
            debug=False
        )

        cd.standardise_date( #convert date formats to 'yyyy-mm-dd'
            def_date_format='yyyy-mm-dd'
        )

        cols = list(self.gdtruth_manual_dates.columns)
        for index, row in self.gdtruth_manual_dates.iterrows():
            for col in cols:
                self.assertEqual(cd.clean_df[col][index], row[col])

    

if __name__ == '__main__':
    if __package__ is None:
        test = TestCleanDataMethods()
        test.setUp()
        test.test_cleanData_dd_dict_definitions()
        test.test_cleanData_con_dict_definitions()
        test.test_cleanData_case_dict_definitions()
        test.test_cleanData_date_dict_definitions()
        test.test_cleanData_ascii_dict_definitions()
        test.test_cleanData_date_ascii_dict_definitions()
        test.test_cleanData_date_manualSettings()

        test.tearDown()
    else:
        unittest.main()