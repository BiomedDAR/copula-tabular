import importlib.util
from bdarpack.CleanData import CleanData

# EXECUTE THE SELECTED CLEANING OPERATIONS IN SEQUENTIAL ORDER
#  -- definitions_path = Local filepath to definitions.py
# Initialize a CleanData instance
# Iterate through EXECUTE_STEPS variable found in definitions.py, and call the corresponding CleanData function for each operation, then print the final report
# e.g. EXECUTE_STEPS = {1: {"op":"DD"},2:{"op":"ST"},3:{"op":"ASCII"},4:{"op":"SD"},5:{"op":"CON"}}
def exec_cleanData(definitions_path):
  spec = importlib.util.spec_from_file_location("definitions", definitions_path)

  if spec and spec.loader:
    definitions = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(definitions)
    cd = CleanData(definitions)

    if hasattr(definitions, "EXECUTE_STEPS"):
      exec_steps = definitions.EXECUTE_STEPS
      for step_num in exec_steps:
          step = exec_steps[step_num]
          op = step["op"]
          
          try:
            if op == "DD":
              cd.drop_duplicate_rows()
            elif op == "ST":
              cd.standardise_text()
            elif op == "DATE":
              cd.standardise_date()
            elif op == "ASCII":
              cd.converting_ascii()
            else:
              print(f"Unknown operation: {op}")
              continue
          except Exception as e:
            print(f"Error during [Step {step_num}] {op}: {e}")
            raise
      cd.gen_data_report(cd.clean_df, dict=cd.clean_dict_df,report_filename="final_report_sample.xlsx")
      print(cd.report_df)
    else:
        print("definitions.py does not contain EXECUTE_STEPS")
  else:
      print("Failed to load definitions.py")