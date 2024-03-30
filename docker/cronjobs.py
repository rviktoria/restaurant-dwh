import os
import subprocess


# Function to execute Python scripts
def execute_python_scripts(script_name):
    script_path = os.path.join('/app/py_scripts', script_name)
    print(f"Executing Python script: {script_path}")
    try:
        subprocess.run(["/usr/local/bin/python", script_path])
        print(f"Python script '{script_name}' executed successfully.")
    except Exception as e:
        print(f"Error executing Python script {script_name}: {e}")


if __name__ == "__main__":
    
    # Execute scripts
    
    # Load stagins
    execute_python_scripts('load_stagings.py') #Step 1
    execute_python_scripts('load_dimensions.py') #Step 2
    execute_python_scripts('load_facts.py') #Step 3

    
