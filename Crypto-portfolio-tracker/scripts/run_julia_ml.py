from pathlib import Path
import subprocess
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ML_DIR = PROJECT_ROOT / "ml"
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# (label, script_path, expected_output_csv)
JULIA_STAGES = [
    ("Preprocessing", ML_DIR / "preprocess.jl", DATA_DIR / "BTC_preprocessed.csv"),
    ("Forecast", ML_DIR / "forecast.jl", DATA_DIR / "forecast_output.csv"),
    ("Portfolio Forecast", SCRIPTS_DIR / "calculate_portfolio_forecast.py", DATA_DIR / "portfolio_forecast.csv"),
]

def run_script(script_path):
    """Run Julia or Python script based on file extension"""
    if script_path.suffix == '.jl':
        command = ['julia', str(script_path)]
    elif script_path.suffix == '.py':
        command = ['python', str(script_path)]
    else:
        raise ValueError(f"Unsupported script type: {script_path.suffix}")

    try:
        result = subprocess.run(
            command,
            capture_output=True, text=True, check=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed for {script_path}:")
        print(e.stdout)
        print(e.stderr)
        return False

def ensure_required_paths():
    for path in [PROJECT_ROOT, ML_DIR, DATA_DIR]:
        if not path.exists():
            raise FileNotFoundError(f"Required path is missing: {path}")

def run_stage(label, script_path, output_csv):
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    print(f"\n=== {label}: running {script_path.relative_to(PROJECT_ROOT)} ===")
    success = run_script(script_path)
    if not success:
        raise RuntimeError(f"{label} failed.")
    print(f"[OK] {label} finished. Reading {output_csv.name}...")

    if not output_csv.exists():
        raise FileNotFoundError(f"{label} completed but no CSV was created at {output_csv}")

    df = pd.read_csv(output_csv)
    row_count = len(df)
    print(f"- Loaded {row_count} rows from {output_csv.name}")
    preview_rows = min(5, row_count)
    if preview_rows:
        print(df.head(preview_rows).to_string(index=False))
    else:
        print("- CSV is empty; check upstream data.")

def explain_failure(error):
    print("\n[ERROR] ML pipeline failed.")
    print(f"Reason: {error}")
    missing_path = str(error)
    if ".jl" in missing_path or ".py" in missing_path:
        print("- Troubleshooting: confirm the script directory exists and the requested file is present.")
    elif ".csv" in missing_path:
        print("- Troubleshooting: the script may have crashed before writing its CSV. Re-run the script manually to inspect the error.")
    elif isinstance(error, RuntimeError):
        print("- Troubleshooting: inspect the stdout printed above for specific error messages. Ensure required interpreters (julia/python) are on PATH and all dependencies are installed.")
    else:
        print("- Troubleshooting: rerun after fixing the issue above or examine logs at data/*.csv for more context.")

def main():
    try:
        ensure_required_paths()
        for label, script_path, output_path in JULIA_STAGES:
            run_stage(label, script_path, output_path)
        print("\n[OK] ML pipeline completed successfully.")
    except Exception as exc:
        explain_failure(exc)
        raise SystemExit(1) from exc

if __name__ == "__main__":
    main()
