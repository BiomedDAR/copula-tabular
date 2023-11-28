# TEST CLEANDATA

# LOAD DEPENDENCIES
import pprint, sys, os

# Add path (if necessary)
dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.dirname(dir_path)
sys.path.insert(0, par_dir)
head, sep, tail = dir_path.partition('copula-tabular')
sys.path.insert(0, head+sep) # adding par_dir to system path

from bdarpack.CleanData import CleanData
from bdarpack.Constraints import Constraints
import definitions as defi
import script_nhanes_constraints as n_con

# Initialise the CleanData class with definitions
cd = CleanData(definitions=defi)

# Generate Report
# report = cd.gen_data_report(data=cd.raw_df, dict=cd.dict_df)

# Clean the data by dropping duplicate rows
cd.drop_duplicate_rows()

# Use Constraints
df = cd.clean_df
con = Constraints(debug=True)


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

pprint.pprint(con.log)

# Update the CleanData class with constrained data
cd.update_data(new_df = df, filename_suffix = cd.suffix_constraints)

# Clean the data by standardising all to uppercase/lowercase
cd.standardise_text()