import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
             command.extend(args)

        result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        # result IS the CompletedProcess object. Access the attributes by result.etc
        output_string = []
        if result.returncode != 0:
             output_string.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
             output_string.append("No output produced")
        if result.stdout:
             output_string.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_string.append(f"STDERR: {result.stderr}")
        return "\n".join(output_string)
    
    except Exception as e:
		# runs ONLY if something inside the try block raised
	    return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="allows the LLM to run a python file, within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Allows the LLM to run a python file, within the working directory",
            ),
            "args": types.Schema(
                 type=types.Type.ARRAY,
                 description="Optional input for function",
                 items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)