"""Cross-platform workflow runner for Farmer Sell Advisor."""

import sys
import subprocess


def run_step(cmd, desc):
    print(f"\n==========================================")
    print(f"RUNNING: {desc}")
    print(f"COMMAND: {cmd}")
    print(f"==========================================")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"\n[ERROR] Command failed with exit code {res.returncode}")
        sys.exit(res.returncode)
    print(f"[SUCCESS] {desc} completed successfully.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [data | train | eval | test | app | web | all]")
        sys.exit(1)

    target = sys.argv[1].lower()

    if target == "data":
        run_step("python -m src.data.pipeline", "Data Pipeline Processing")
    elif target == "train":
        run_step("python -m src.models.forecast", "Model Training & Forecaster Validation")
    elif target == "eval":
        run_step("python -m src.evaluation.evaluate", "Advisor Historical Backtest Evaluation")
    elif target == "test":
        run_step("pytest -v", "Unit and Integration Tests")
    elif target == "app":
        run_step("streamlit run app.py", "Streamlit Demo App")
    elif target == "web":
        print("\n==========================================")
        print("LAUNCHING: Production Web Application")
        print("Backend:  http://localhost:8000 (FastAPI Docs: /docs)")
        print("Frontend: http://localhost:3000 (Next.js)")
        print("==========================================")
        import os
        backend_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])
        frontend_proc = subprocess.Popen(["npm", "run", "dev"], cwd=os.path.join(os.getcwd(), "frontend"), shell=True)
        try:
            backend_proc.wait()
            frontend_proc.wait()
        except KeyboardInterrupt:
            print("\nShutting down web services...")
            backend_proc.terminate()
            frontend_proc.terminate()
    elif target == "all":
        run_step("python -m src.data.pipeline", "Data Pipeline Processing")
        run_step("python -m src.models.forecast", "Model Training & Forecaster Validation")
        run_step("python -m src.evaluation.evaluate", "Advisor Historical Backtest Evaluation")
        run_step("pytest -v", "Unit and Integration Tests")
    else:
        print(f"Unknown target: {target}")
        print("Available targets: data, train, eval, test, app, all")
        sys.exit(1)


if __name__ == "__main__":
    main()

