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
    
    # Load fact tables
    execute_python_scripts('load_fact_orders.py')

