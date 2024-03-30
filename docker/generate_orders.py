import os
import subprocess


# Function to execute Python scripts
def execute_python_scripts(script_name):
    script_path = os.path.join('./py_scripts', script_name)
    print(f"Executing Python script: {script_path}")
    try:
        subprocess.run(["python", script_path])
        print(f"Python script '{script_name}' executed successfully.")
    except Exception as e:
        print(f"Error executing Python script {script_name}: {e}")


if __name__ == "__main__":
    
    # Execute scripts
    
    # Generate new orders
    execute_python_scripts('generate_new_order_into_restaurant_db.py')

