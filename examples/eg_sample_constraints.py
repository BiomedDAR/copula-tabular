# LOAD DEPENDENCIES
import pprint, sys, os
import numpy as np
import pandas as pd
from datetime import datetime

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)
head, sep, tail = dir_path.partition('copula-tabular')
sys.path.insert(0, head+sep) # adding par_dir to system path

from bdarpack.Constraints import Constraints

con = Constraints(debug=True)


# FIX Age (numerical)
def con_age(df, con=con):

  # Generate Age variable from Date of Birth variable
  # Subtract birth year from current year
  # Subtract 1 more year if the birthday has not occured in the current year          
  def compute_age(df_row):
    dob_str = df_row['Date of Birth']
    if (pd.isnull(dob_str)):
      age = np.nan
    else:
      dob = datetime.strptime(dob_str,"%a, %d %B %y")
      today = datetime.today()
      age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
      return age

  df = con.evaluate_df_column(df, ['Date of Birth'], func=compute_age, output_column_name="Age")

  return df, con

# FIX BMI (numerical), BMICatUnder20yrs, BMI_WHO variables
def con_BMI(df, con=con, bmiChartPerc_filename=None):

    # Generate BMI Result
    # Body mass index (weight/height2 in kg/m2). Reported for participants aged 2 years or older.
    # Generate BMI result
    def compute_bmi(df_row):
        # print(df_row)
        w = df_row['Weight']
        h = df_row['Height']
        if any(pd.isnull(value) for value in df_row):
            BMI = np.nan
        else:
            h2 = h / 100
            BMI = w / (h2 * h2)
            BMI = round(BMI, 2)

        return BMI
    df = con.evaluate_df_column(df, ['Height', 'Weight'], func=compute_bmi, output_column_name="BMI")

    # Generate BMICatUnder20yrs https://www.cdc.gov/growthcharts/percentile_data_files.htm
    # Body mass index category. Reported for participants aged 2 to 19 years. One of UnderWeight (BMI < 5th percentile) NormWeight (BMI 5th to < 85th percentile), OverWeight (BMI 85th to < 95th percentile), Obese (BMI >= 95th percentile).
    bmiChartPerc_df = pd.read_excel(bmiChartPerc_filename, sheet_name='bmiage')
    def compute_bmiCatUnder20yrs(df_row, bmiChartPerc_df=bmiChartPerc_df):
        g = df_row['Gender']
        a = df_row['AgeMonths']
        bmi = df_row['BMI']
        age = df_row['Age']

        sex = int(1 if g == "male" else 2)
        if pd.isnull(a):
            a = age * 12

        # CASE 1: exact match of Agemos (float) with AgeMonths
        extractedRow = bmiChartPerc_df.loc[(bmiChartPerc_df['Sex'] == sex) & (np.isclose(bmiChartPerc_df['Agemos'], a)) ]

        # CASE 2: two closest matches
        if extractedRow.empty:
            extractedGender = bmiChartPerc_df.loc[(bmiChartPerc_df['Sex'] == sex)]
            df_sort = extractedGender.iloc[(extractedGender['Agemos']-a).abs().argsort()[:2]]
            df_sort_index_list = df_sort.index.tolist()
            extractedRow = bmiChartPerc_df.iloc[df_sort_index_list]
        # Average
        extractedRow = extractedRow.mean(axis=0)

        if (a < 24 or a > 240.5):
            BMICatUnder20yrs = "N.A."
        else:
            if (pd.isnull(bmi)):
                BMICatUnder20yrs = "UNK"
            elif (bmi < extractedRow['P5']):
                BMICatUnder20yrs = "UnderWeight"
            elif (bmi < extractedRow['P85']):
                BMICatUnder20yrs = "NormWeight"
            elif (bmi < extractedRow['P95']):
                BMICatUnder20yrs = "OverWeight"
            else:
                BMICatUnder20yrs = "Obese"
        
        return BMICatUnder20yrs
    
    column_names = ['Gender', 'AgeMonths', 'BMI', 'Age']
    df = con.evaluate_df_column(df, column_names, func=compute_bmiCatUnder20yrs, output_column_name="BMICatUnder20yrs")

    # Generate BMI_WHO variable
    # Body mass index category. Reported for participants aged 2 years or older. One of 12.0_18.4, 18.5_24.9, 25.0_29.9, or 30.0_plus.
    def bmi_who(df_row):
        age = df_row['Age']
        bmi = df_row['BMI']
        if age < 2:
            BMI_WHO = "N.A."
        else:
            if (pd.isnull(bmi)):
                BMI_WHO = "UNK"
            else:
                if bmi <= 18.4:
                    BMI_WHO = "12.0_18.5"
                elif bmi <= 24.9:
                    BMI_WHO = "18.5_to_24.9"
                elif bmi <= 29.9:
                    BMI_WHO = "25.0_to_29.9"
                else:
                    BMI_WHO = "30.0_plus"
        
        return BMI_WHO
    df = con.evaluate_df_column(df, ['BMI', 'Age'], func=bmi_who, output_column_name="BMI_WHO")
    

    return df, con
