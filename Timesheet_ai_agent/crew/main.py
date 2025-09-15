# crew/main.py

from tasks.tasks_sheet import define_tasks

def run_timesheet_pipeline():
    """
    Runs the Timesheet AI Agent pipeline sequentially using defined tasks.
    Returns:
        dict: Outputs from each task.
    """

    # Initialize inputs (replace this with dynamic user input in production)
    inputs = {
        "file_path": "/path/to/timesheet.csv"  # 🔧 Replace with user input or upload in your Streamlit app
    }
    outputs = {}

    try:
        tasks = define_tasks()

        for task in tasks:
            agent = task["agent"]
            input_data = inputs.get(task["input_key"]) or outputs.get(task["input_key"])

            # Ensure input data is available before running agent
            if input_data is None:
                raise ValueError(f"Missing input for task: {task['name']}")

            result = agent.run(input_data)
            outputs[task["output_key"]] = result

        return outputs

    except Exception as e:
        # Return error details for Streamlit display
        return {"error": str(e)}



#-----------------------------------------------------------------------------

# crew/main.py

# from tasks.tasks_sheet import define_tasks

# def run_timesheet_pipeline(file_path):
#     """
#     Runs the Timesheet AI Agent pipeline sequentially using defined tasks.

#     Args:
#         file_path (str): Path to the input timesheet CSV file.

#     Returns:
#         dict: Outputs from each task.
#     """
#     inputs = {
#         "file_path": file_path
#     }
#     outputs = {}

#     try:
#         tasks = define_tasks()

#         for task in tasks:
#             agent = task["agent"]
#             input_data = inputs.get(task["input_key"]) or outputs.get(task["input_key"])

#             if input_data is None:
#                 raise ValueError(f"Missing input for task: {task['name']}")

#             result = agent.run(input_data)
#             outputs[task["output_key"]] = result

#         return outputs

#     except Exception as e:
#         # Return error details for Streamlit display
#         return {"error": str(e)}
