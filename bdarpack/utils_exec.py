
# EXECUTE THE SELECTED CLEANING OPERATIONS IN SEQUENTIAL ORDER
#  -- cd = CleanData instance
#  -- exec_steps = Selected Cleaning Operations e.g. {1: {"op":"DD"},2:{"op":"ST"}}
# Iterate through exec_steps, and call the corresponding CleanData function for each operation.
def exec_cleanData(cd, exec_steps = {}):
  for step_num in exec_steps:
      step = exec_steps[step_num]
      op = step["op"]
      
      if op == "DD":
          cd.drop_duplicate_rows()
      elif op == "ST":
          cd.standardise_text()
      elif op == "SD":
          cd.standardise_date()
      elif op == "ASCII":
          cd.converting_ascii()