import importlib.util
import pandas as pd

from bdarpack.CleanData import CleanData

def exec_cleanData(cd, exec_steps: dict):
    """
    Execute a sequence of cleaning operations on the CleanData instance.

    Args:
        cd (CleanData): An initialized CleanData object.
        exec_steps (dict): Dictionary defining the cleaning steps, e.g.,
            {
                1: {"op": "DD"},
                2: {"op": "ST"},
                3: {"op": "ASCII"},
                4: {"op": "DATE"},
            }

    Raises:
        RuntimeError: If any operation fails or an unknown operation is encountered.
    """
    for step_num, step in exec_steps.items():
        op = step.get("op")

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
                raise ValueError(f"❌ Unknown operation '{op}' in step {step_num}")
        except Exception as e:
            raise RuntimeError(f"❌ Error during [Step {step_num}] {op}: {e}") from e


def run_clean_pipeline(definitions_path: str):
    """
    Load a definitions.py file and run the data cleaning pipeline.

    Workflow:
        1. Load definitions.py from the given path
        2. Extract EXECUTE_STEPS
        3. Initialize CleanData with definitions
        4. Execute all steps defined in EXECUTE_STEPS
        5. Generate report and return a summary

    Args:
        definitions_path (str): Absolute path to the definitions.py file

    Returns:
        dict: Summary containing:
            - success (bool): Whether the cleaning succeeded
            - message (str): User-friendly status message
            - output_dir (str): Output directory where results were written
            - report_preview (dict): Dict preview of the generated report

    Raises:
        RuntimeError: If any part of the pipeline fails
    """
    try:
        # Step 1: Dynamically import definitions.py
        spec = importlib.util.spec_from_file_location("definitions", definitions_path)
        if not spec or not spec.loader:
            raise RuntimeError("❌ Failed to load definitions.py — invalid spec or loader is None")

        definitions = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(definitions)

        # Step 2: Validate EXECUTE_STEPS presence
        if not hasattr(definitions, "EXECUTE_STEPS"):
            raise RuntimeError("❌ definitions.py does not contain EXECUTE_STEPS")

        # Step 3: Initialize CleanData and run cleaning steps
        cd = CleanData(definitions=definitions)
        exec_cleanData(cd, definitions.EXECUTE_STEPS)

        # Step 4: Generate report and preview
        cd.gen_data_report(cd.clean_df, dict=cd.clean_dict_df, report_filename="final_report_sample.xlsx")
        report_df_head = cd.report_df.head(5)
        report_preview = report_df_head.where(pd.notnull(report_df_head), None).to_dict()

        return {
            "success": True,
            "message": "✅ Cleaning completed",
            "output_dir": cd.train_data_path,
            "report_preview": report_preview,
        }
    
    except Exception as e:
        raise 