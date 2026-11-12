@echo off
setlocal

if "%1"=="" goto help
if "%1"=="data" goto data
if "%1"=="train" goto train
if "%1"=="eval" goto eval
if "%1"=="test" goto test
if "%1"=="app" goto app
if "%1"=="web" goto web
if "%1"=="all" goto all

:help
echo Usage: make [data ^| train ^| eval ^| test ^| app ^| web ^| all]
exit /b 1

:data
echo [MAKE] Running data pipeline...
python -m src.data.pipeline
exit /b %ERRORLEVEL%

:train
echo [MAKE] Training price forecaster models...
python -m src.models.forecast
exit /b %ERRORLEVEL%

:eval
echo [MAKE] Running historical backtest evaluation...
python -m src.evaluation.evaluate
exit /b %ERRORLEVEL%

:test
echo [MAKE] Running pytest test suite...
pytest -v
exit /b %ERRORLEVEL%

:app
echo [MAKE] Launching Streamlit application...
streamlit run app.py
exit /b %ERRORLEVEL%

:web
echo [MAKE] Launching Full-Stack Web Application (FastAPI + Next.js)...
python run.py web
exit /b %ERRORLEVEL%

:all
call :data
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
call :train
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
call :eval
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
exit /b 0

