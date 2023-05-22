# LOAD DEPENDENCIES
import pprint, sys, os
import numpy as np
import pandas as pd

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)
head, sep, tail = dir_path.partition('copula-tabular')
sys.path.insert(0, head+sep) # adding par_dir to system path

from mz.Constraints import Constraints

con = Constraints(debug=True)

# FIX Race3 variable (categorical)
def con_Race3(df, con=con):

    # Convert categorical blanks to UNK
    vArray = ['Race1', 'Race3']
    df = con.convertBlankstoValue(df, var_array=vArray, value='UNK')

    # If SurveyYr=='2009_10', Race3 = '(blanks)'
    surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: surveyYr_2009_10},
            'value': 'N.A.'
        }
    }
    df = con.multiparent_conditions(df, ['Race3'], dict_conditions_values)

    return df, con

def con_GenderEducationMaritalStatus(df, con=con):

    # Convert categorical blanks to UNK
    vArray = ['Gender','Education','MaritalStatus']
    df = con.convertBlankstoValue(df, var_array=vArray, value='UNK')

    # If Age < 20, Education, MaritalStatus = 'N.A.'
    age_lessthan20 = {'parent': 'Age', 'condition': '<20'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan20},
            'value': 'N.A.'
        }
    }
    df = con.multiparent_conditions(df, ['Education','MaritalStatus'], dict_conditions_values)

    return df, con

def con_HHIncome(df, con=con):

    # Convert categorical blanks to UNK
    df = con.convertBlankstoValue(df, var_array=['HHIncome'], value='UNK')
    
    # Derive secondary variable HHIncomeMid from HHIncome
    def fn_1(x):
        if "-" in str(x):
            v = x.split("-")
            return ( int(v[1]) + 1 + int(v[0]) )/ 2
        elif "UNK" in str(x):
            return np.nan
        elif "more" in str(x):
            return 100000
        else:
            return np.nan
    con.evaluate_df_column(df, 'HHIncome', func=fn_1, output_column_name='HHIncomeMid')

    # If HHIncome="UNK", convert "Poverty" to np.nan
    hhincomeIsUNK = {'parent': 'HHIncome', 'condition': '=="UNK"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: hhincomeIsUNK},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['Poverty'], dict_conditions_values)
    df = con.convertBlankstoValue(df, var_array=['Poverty'], value=np.nan)

    return df, con

# FIX AgeDecade variable (age 80 is not coded as 70+)
def con_ageDecade(df, con=con):

    # Creating AgeDecade as a secondary variable
    dict_conditions_values = {}
    for i in range(1,11):
        if (i-1)*10 >= 70:
            value = ' 70+'
        else:
            value = f" {(i-1)*10}-{i*10-1}"  #' 0-9'
        dict_conditions_values.update({str(i): {
            'condition': f"{(i-1)*10} <= x and x < {i*10}", #"0 < x and x < 10",
            'value': f"'{value}'"
        }})
    df = con.evaluate_df_column(df, 'Age', dict_conditions_values, output_column_name="AgeDecade")

    # Convert categorical blanks to UNK
    df = con.convertBlankstoValue(df, var_array=['AgeDecade'], value='UNK')

    return df, con

# Fix AgeMonths variable
def con_ageMonths(df, con=con):

    # If SurveyYr=='2009_10' and Age>=80, AgeMonths = ''
    # If SurveyYr=='2009_10' and AgeMonths>=948, AgeMonths = ''
    # If SurveyYr=='2011_12' and Age>=3, AgeMonths = ''
    # If SurveyYr=='2011_12' and AgeMonths>=24, AgeMonths = ''

    surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
    surveyYr_2011_12 = {'parent': 'SurveyYr', 'condition': '=="2011_12"'}
    age_morethan80 = {'parent': 'Age', 'condition': '>=80'}
    age_morethan3 = {'parent': 'Age', 'condition': '>=3'}
    ageMonths_morethan948 = {'parent': 'AgeMonths', 'condition': '>=948'}
    ageMonths_morethan24 = {'parent': 'AgeMonths', 'condition': '>=24'}
    dict_conditions_values = {
        1: {
            'conditions': {1: surveyYr_2009_10, 2: age_morethan80},
            'value': np.nan
        },
        2: {
            'conditions': {1: surveyYr_2009_10, 2: ageMonths_morethan948},
            'value': np.nan
        },
        3: {
            'conditions': {1: surveyYr_2011_12, 2: age_morethan3},
            'value': np.nan
        },
        4: {
            'conditions': {1: surveyYr_2011_12, 2: ageMonths_morethan24},
            'value': np.nan
        }
    }

    var_array = ['AgeMonths']
    df = con.multiparent_conditions(df, var_array, dict_conditions_values)



    return df, con

# Fix HomeRooms, HomeOwn, Work variable
def con_HomeWork(df, con=con):

    # Convert categorical blanks to UNK
    vArray = ['HomeOwn', 'Work']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")

    return df, con

# FIX Weight, Length, HeadCirc, Height variable (numerical)
def con_WeightHeight(df, con=con):

    # If Age > 3, Length is (blanks)
    # If AgeMonths > 6, HeadCirc is (blanks)
    # If Age < 2, Height is (blanks)

    age_morethan3 = {'parent': 'Age', 'condition': '>3'}
    ageMonths_morethan6 = {'parent': 'AgeMonths', 'condition': '>6'}
    age_lessthan2 = {'parent': 'Age', 'condition': '<2'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_morethan3},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['Length'], dict_conditions_values)

    dict_conditions_values = {
        1: {
            'conditions': {1: ageMonths_morethan6},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['HeadCirc'], dict_conditions_values)

    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan2},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['Height'], dict_conditions_values)


    return df, con

# FIX BMI (numerical), BMICatUnder20yrs, BMI_WHO variables
def con_BMI(df, con=con, bmiChartPerc_filename=None):

    # Generate BMI Result
    # Body mass index (weight/height2 in kg/m2). Reported for participants aged 2 years or older.
    # Generate BMI result
    def compute_bmi(df_row):
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


# FIX Testosterone variable (numeric)
def con_Testosterone(df, con=con):

    # Testosterone total (ng/dL). Reported for participants aged 6 years or older. Not available for 2009 - 2010.
    surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
    surveyYr_2011_12 = {'parent': 'SurveyYr', 'condition': '=="2011_12"'}
    age_lessthan6 = {'parent': 'Age', 'condition': '<6'}
    dict_conditions_values = {
        1: {
            'conditions': {1: surveyYr_2009_10},
            'value': np.nan
        },
        2: {
            'conditions': {1: surveyYr_2011_12, 2: age_lessthan6},
            'value': np.nan
        }
    }
    var_array = ['Testosterone']
    df = con.multiparent_conditions(df, var_array, dict_conditions_values)

    return df, con

# FIX DirectChol, TotChol, UrineVol1, UrineFlow1, UrineVol2, UrineFlow2 variable (numeric)
def con_cholUrine(df, con=con):

    # Direct HDL cholesterol in mmol/L. Reported for participants aged 6 years or older.
    # Total HDL cholesterol in mmol/L. Reported for participants aged 6 years or older.
    # Urine volume in mL – first test. Reported for participants aged 6 years or older
    # Urine flow rate (urine volume/time since last urination) in mL/min – first test. Reported for participants aged 6 years or older
    # Urine volume in mL – second test. Reported for participants aged 6 years or older.
    # Urine flow rate (urine volume/time since last urination) in mL/min – second test. Reported for participants aged 6 years or older.
    age_lessthan6 = {'parent': 'Age', 'condition': '<6'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan6},
            'value': np.nan
        }
    }
    var_array = ['DirectChol', 'TotChol', 'UrineVol1', 'UrineFlow1', 'UrineVol2', 'UrineFlow2']
    df = con.multiparent_conditions(df, var_array, dict_conditions_values)

    # df = con.ifPpvvalthenC(df, pv='AgeDecade', val=np.nan, vchildList=['DirectChol', 'TotChol', 'UrineVol1', 'UrineFlow1', 'UrineVol2', 'UrineFlow2'], pvVal=['(blanks)'], cond_neg=(df['Age'] < 6))

    return df, con


# FIX Diabetes (categorical)
def con_diabetes(df, con=con):

    # Study participant told by a doctor or health professional that they have diabetes. Reported for participants aged 1 year or older as Yes or No
    df = con.convertBlankstoValue(df, var_array=['Diabetes'], value="UNK")
    age_lessthan1 = {'parent': 'Age', 'condition': '<1'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan1},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, ['Diabetes'], dict_conditions_values)

    # FIX DiabetesAge (numerical)
    # Age of study participant when first told they had diabetes. Reported for participants aged 1 year or older
    diabetes_notYes = {'parent': 'Diabetes', 'condition': '!="Yes"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan1},
            'value': np.nan
        },
        2: {
            'conditions': {1: diabetes_notYes},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['DiabetesAge'], dict_conditions_values)

    # FIX cases where DiabetesAge>Age. If DiabetesAge>Age, set to Age
    df = con.compare_columns_A_B(df, A='DiabetesAge', B='Age')


    # df = con.ifPnotpvvalthenC(df, pv='Diabetes', val=np.nan, vchildList=['DiabetesAge'], pvVal=['Yes'])
    # df = con.ifPpvvalthenC(df, pv='AgeDecade', val=np.nan, vchildList=['DiabetesAge'], pvVal=['(blanks)'], cond_neg=(df['Age'] < 1))
    # df = con.ifAversusB(df, 'Age', 'DiabetesAge')

    return df, con


# FIX HealthGen (categorical)
def con_HealthGen(df, con=con):

    # Self-reported rating of participant’s health in general Reported for participants aged 12 years or older. One of Excellent, Vgood, Good, Fair, or Poor.
    df = con.convertBlankstoValue(df, var_array=['HealthGen'], value="UNK")
    age_lessthan12 = {'parent': 'Age', 'condition': '<12'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan12},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, ['HealthGen'], dict_conditions_values)

    # FIX DaysPhysHlthBad, DaysMentHlthBad (numerical)
    # Self-reported number of days participant's physical/mental health was not good out of the past 30 days. Reported for participants aged 12 years or older.
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan12},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['DaysPhysHlthBad', 'DaysMentHlthBad'], dict_conditions_values)

    return df, con


# FIX LittleInterest, Depressed (categorical)
def con_Depression(df, con=con):

    # Self-reported number of days where participant had little interest in doing things. Reported for participants aged 18 years or older. One of None, Several, Most (more than half the days), or AlmostAll.
    # Self-reported number of days where participant felt down, depressed, or hopeless. Reported for participants aged 18 years or older. One of None, Several, Most (more than half the days), or AlmostAll.
    vArray = ['LittleInterest', 'Depressed']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan18 = {'parent': 'Age', 'condition': '<18'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)
    # df = con.convertBlanksToA(df, vArray=vArray, A="UNK")
    # df = con.ifPpvvalthenC(df, pv='AgeDecade', val='N.A.', vchildList=vArray, pvVal=['(blanks)'], cond_neg=(df['Age'] < 18))

    return df, con


# FIX nPregnancies, nBabies, Age1stBaby (numerical)
def con_Pregnancies(df, con=con):

    # How many times participant has been pregnant. Reported for female participants aged 20 years or older
    # How many of participants deliveries resulted in live births. Reported for female participants aged 20 years or older.
    # Age of participant at time of first live birth. 14 years or under = 14, 45 years or older = 45. Reported for female participants aged 20 years or older.
    # nBabies <= nPregnancies, else nBabies=nPregnancies
    # Age1stBaby <= Age, else Age1stBaby=Age
    vArray = ['nPregnancies', 'nBabies', 'Age1stBaby']
    age_lessthan20 = {'parent': 'Age', 'condition': '<20'}
    genderisMale = {'parent': 'Gender', 'condition': '=="male"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan20},
            'value': np.nan
        },
        2: {
            'conditions': {1: genderisMale},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    df = con.compare_columns_A_B(df, 'nBabies', 'nPregnancies')
    df = con.compare_columns_A_B(df, 'Age1stBaby', 'Age')

    age1stBaby_lessthan14 = {'parent': 'Age1stBaby', 'condition': '<14'}
    age1stBaby_morethan45 = {'parent': 'Age1stBaby', 'condition': '>45'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age1stBaby_lessthan14},
            'value': 14
        },
        2: {
            'conditions': {1: age1stBaby_morethan45},
            'value': 45
        }
    }

    return df, con


def con_Activeness(df, con=con):
    # FIX SleepHrsNight (numerical)
    # Self-reported number of hours study participant usually gets at night on weekdays or workdays. Reported for participants aged 16 years and older.
    age_lessthan16 = {'parent': 'Age', 'condition': '<16'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan16},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['SleepHrsNight'], dict_conditions_values)

    # FIX SleepTrouble (categorical)
    # Participant has told a doctor or other health professional that they had trouble sleeping. Reported for participants aged 16 years and older. Coded as Yes or No.
    vArray = ['SleepTrouble']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan16},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)
    
    # FIX PhysActive (categorical)
    # Participant does moderate or vigorous-intensity sports, fitness or recreational activities (Yes or No). Reported for participants 12 years or older.
    vArray = ['PhysActive']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan12 = {'parent': 'Age', 'condition': '<12'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan12},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    # FIX PhysActiveDays (numerical)
    # Number of days in a typical week that participant does moderate or vigorous-intensity activity. Reported for participants 12 years or older.
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan12},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['PhysActiveDays'], dict_conditions_values)

    return df, con

def con_Activity(df, con=con):

    # FIX TVHrsDay, CompHrsDay (categorical)
    # Number of hours per day on average participant watched TV over the past 30 days. Reported for participants 2 years or older. One of 0_to_1hr, 1_hr, 2_hr, 3_hr, 4_hr, More_4_hr. Not available 2009-2010.
    vArray = ['TVHrsDay', 'CompHrsDay']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan2 = {'parent': 'Age', 'condition': '<2'}
    surveyYr_2009_10 = {'parent': 'SurveyYr', 'condition': '=="2009_10"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan2},
            'value': "N.A."
        },
        2: {
            'conditions': {1: surveyYr_2009_10},
            'value': "N.A."
        },
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)
    
    # FIX TVHrsDayChild, CompHrsDayChild (numerical)
    # Number of hours per day on average participant watched TV over the past 30 days. Reported for participants 2 to 11 years.  Not available 2011-2012.
    # Number of hours per day on average participant used a computer or gaming device over the past 30 days. Reported for participants 2 to 11 years.  Not available 2011-2012.
    vArray = ['TVHrsDayChild', 'CompHrsDayChild']
    age_morethan11 = {'parent': 'Age', 'condition': '>11'}
    surveyYr_2011_12 = {'parent': 'SurveyYr', 'condition': '=="2011_12"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan2},
            'value': np.nan
        },
        2: {
            'conditions': {1: age_morethan11},
            'value': np.nan
        },
        3: {
            'conditions': {1: surveyYr_2011_12},
            'value': np.nan
        },
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    return df, con


def con_Alcohol(df, con=con):

    # FIX Alcohol12PlusYr (categorical)
    # Participant has consumed at least 12 drinks of any type of alcoholic beverage in any one year. Reported for participants 18 years or older as Yes or No.
    vArray = ['Alcohol12PlusYr']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan18 = {'parent': 'Age', 'condition': '<18'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    # FIX AlcoholDay, AlcoholYear (numerical)
    # Average number of drinks consumed on days that participant drank alcoholic beverages. Reported for participants aged 18 years or older.
    # Estimated number of days over the past year that participant drank alcoholic beverages. Reported for participants aged 18 years or older.
    vArray = ['AlcoholDay', 'AlcoholYear']
    age_lessthan18 = {'parent': 'Age', 'condition': '<18'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    return df, con


def con_Smoking(df, con=con):

    # FIX Smoke100 (categorical)
    # Study participant has smoked at least 100 cigarettes in their entire life. Reported for participants aged 20 years or older as Yes or No.
    vArray = ['Smoke100']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan20 = {'parent': 'Age', 'condition': '<20'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan20},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    # FIX SmokeNow (categorical)
    # Study participant currently smokes cigarettes regularly. Reported for participants aged  20 years or older as Yes or No, provided they answered Yes to having smoked 100 or more cigarettes in their lifetime. All subjects who have not smoked 100 or more cigarettes are listed as NA here.
    vArray = ['SmokeNow']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    smoke100NotYes = {'parent': 'Smoke100', 'condition': '!="Yes"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan20},
            'value': "N.A."
        },
        2: {
            'conditions': {1: smoke100NotYes},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)
    
    # Smoke100n	
    # Generate Smoke100n variable
    # Convert 'Yes' to 'Smoker', 'No' to 'Non-Smoker'
    def compute_smoke100n(df_row):
        w = df_row['Smoke100']
        smoke100n = "N.A."
        if (w=='Yes'):
            smoke100n = 'Smoker'
        elif (w=='No'):
            smoke100n = 'Non-Smoker'
        else:
            smoke100n = w

        return smoke100n
    df = con.evaluate_df_column(df, ['Smoke100'], func=compute_smoke100n, output_column_name='Smoke100n')

    # FIX SmokeAge (numerical)
    # Age study participant first started to smoke cigarettes fairly regularly. Reported for participants aged 20 years or older.
    vArray = ['SmokeAge']
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan20},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)
    df = con.compare_columns_A_B(df, 'SmokeAge', 'Age')

    return df, con

def con_Drugs(df, con=con):

    # FIX Marijuana, RegularMarij (categorical)
    # Marijuana	Participant has tried marijuana. Reported for participants aged 18 to 59 years as Yes or No.
    # RegularMarij	Participant has been/is a regular marijuana user (used at least once a month for a year). Reported for participants aged 18 to 59 years as Yes or No.
    vArray = ['Marijuana', 'RegularMarij']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan18 = {'parent': 'Age', 'condition': '<18'}
    age_morethan59 = {'parent': 'Age', 'condition': '>59'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': "N.A."
        },
        2: {
            'conditions': {1: age_morethan59},
            'value': "N.A."
        },
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    # FIX AgeFirstMarij (numerical)
    # AgeFirstMarij	Age participant first tried marijuana. Reported for participants aged 18 to 59 years.
    # AgeRegMarij Age of participant when first started regularly using marijuana. Reported for participants aged 18 to 59 years.
    vArray = ['AgeFirstMarij', 'AgeRegMarij']
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': np.nan
        },
        2: {
            'conditions': {1: age_morethan59},
            'value': np.nan
        },
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    marijuanaNotYes = {'parent': 'Marijuana', 'condition': '!="Yes"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: marijuanaNotYes},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['AgeFirstMarij'], dict_conditions_values)

    RegMarijuanaNotYes = {'parent': 'RegularMarij', 'condition': '!="Yes"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: RegMarijuanaNotYes},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['AgeRegMarij'], dict_conditions_values)

    df = con.compare_columns_A_B(df, 'AgeFirstMarij', 'Age')
    df = con.compare_columns_A_B(df, 'AgeRegMarij', 'Age')


    # FIX HardDrugs, SexEver, SameSex (categorical)
    # Participant has tried cocaine, crack cocaine, heroin or methamphetamine. Reported for participants aged 18 to 69 years as Yes or No.
    # Participant has had any kind of sex with a same sex partner. Reported for participants aged 18 to 69 years ad Yes or No.
    vArray = ['HardDrugs', 'SexEver', 'SameSex']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")

    age_morethan69 = {'parent': 'Age', 'condition': '>69'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': "N.A."
        },
        2: {
            'conditions': {1: age_morethan69},
            'value': "N.A."
        },
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    SexEverNotYes = {'parent': 'SexEver', 'condition': '!="Yes"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: SexEverNotYes},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, ['SameSex'], dict_conditions_values)

    return df, con


def con_Sex(df, con=con):

    # FIX SexAge, SexNumPartnLife (numerical)
    # Age of participant when had sex for the first time. Reported for participants aged 18 to 69 years.
    # Number of opposite sex partners participant has had any kind of sex with over their lifetime. Reported for participants aged 18 to 69 years.
    vArray = ['SexAge', 'SexNumPartnLife']
    age_lessthan18 = {'parent': 'Age', 'condition': '<18'}
    age_morethan59 = {'parent': 'Age', 'condition': '>59'}
    age_morethan69 = {'parent': 'Age', 'condition': '>69'}
    SexEverNotYes = {'parent': 'SexEver', 'condition': '!="Yes"'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': np.nan
        },
        2: {
            'conditions': {1: age_morethan69},
            'value': np.nan
        },
        3: {
            'conditions': {1: SexEverNotYes},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)
    df = con.compare_columns_A_B(df, 'SexAge', 'Age')

    # FIX SexNumPartYear (numerical)
    # Number of opposite sex partners participant has had any kind of sex with over the past 12 months. Reported for participants aged 18 to 59 years.
    vArray = ['SexNumPartYear']
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': np.nan
        },
        2: {
            'conditions': {1: age_morethan59},
            'value': np.nan
        },
        3: {
            'conditions': {1: SexEverNotYes},
            'value': np.nan
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    # FIX SexOrientation (categorical)
    # Participant’s sexual orientation (self-described). Reported for participants aged 18 to 59 years. One of Heterosexual, Homosexual, Bisexual.
    vArray = ['SexOrientation']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan18},
            'value': "N.A."
        },
        2: {
            'conditions': {1: age_morethan59},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    return df, con



def con_Pregnancies_2(df, con=con):

    # FIX PregnantNow (categorical)
    # Pregnancy status at the time of the health examination was ascertained for females 8-59 years of age. Due to disclosure risks, pregnancy status was only released for women 20-44 years of age. Information used includes urine pregnancy test results and self-reported pregnancy status. Urine pregnancy tests were performed prior to the dual energy x-ray absorptiometry (DXA) exam. Persons who reported they were pregnant at the time of exam were assumed to be pregnant. As a result, if the urine test was negative, but the subject reported they were pregnant, the status was coded as "Yes". If the urine pregnancy results were negative and the respondent stated that they were not pregnant, the respondent was coded as "No". If the urine pregnancy results were negative and the respondent did not know her pregnancy status, the respondent was coded "Unknown". Persons who were interviewed, but not examined also have a value of "Unknown". In addition, there are missing values.

    vArray = ['PregnantNow']
    df = con.convertBlankstoValue(df, var_array=vArray, value="UNK")
    age_lessthan20 = {'parent': 'Age', 'condition': '<20'}
    age_morethan44 = {'parent': 'Age', 'condition': '>44'}
    dict_conditions_values = {
        1: {
            'conditions': {1: age_lessthan20},
            'value': "N.A."
        },
        2: {
            'conditions': {1: age_morethan44},
            'value': "N.A."
        }
    }
    df = con.multiparent_conditions(df, vArray, dict_conditions_values)

    return df, con