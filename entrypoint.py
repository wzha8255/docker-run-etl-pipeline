import subprocess

def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    print("Starting ETL pipeline...")
    run_script("extract_yf.py")
    run_script("transform.py")
    run_script("load.py")
    print("ETL pipeline completed successfully!")