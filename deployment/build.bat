@echo off
REM ============================================================================
REM AgriPulse AI - Docker Build Script (Windows)
REM ============================================================================
REM Builds optimized Docker image with proper tagging and caching
REM ============================================================================

setlocal enabledelayedexpansion

REM Default values
set IMAGE_NAME=agripulse-ai
set IMAGE_TAG=latest
set BUILD_ARGS=
set NO_CACHE=

REM Script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM ============================================================================
REM Parse Arguments
REM ============================================================================

:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="-t" (
    set IMAGE_TAG=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--tag" (
    set IMAGE_TAG=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="-n" (
    set NO_CACHE=--no-cache
    shift
    goto parse_args
)
if /i "%~1"=="--no-cache" (
    set NO_CACHE=--no-cache
    shift
    goto parse_args
)
if /i "%~1"=="-h" goto show_usage
if /i "%~1"=="--help" goto show_usage
shift
goto parse_args

:end_parse

REM ============================================================================
REM Pre-build Checks
REM ============================================================================

echo ============================================================================
echo Pre-build Checks
echo ============================================================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)
echo [OK] Docker is installed

REM Check if Dockerfile exists
if not exist "%SCRIPT_DIR%Dockerfile" (
    echo [ERROR] Dockerfile not found at %SCRIPT_DIR%Dockerfile
    exit /b 1
)
echo [OK] Dockerfile found

REM Check if pyproject.toml exists
if not exist "%PROJECT_ROOT%pyproject.toml" (
    echo [ERROR] pyproject.toml not found at %PROJECT_ROOT%pyproject.toml
    exit /b 1
)
echo [OK] pyproject.toml found

REM ============================================================================
REM Build Docker Image
REM ============================================================================

echo.
echo ============================================================================
echo Building Docker Image
echo ============================================================================
echo Image name: %IMAGE_NAME%:%IMAGE_TAG%
echo Build context: %PROJECT_ROOT%
echo Dockerfile: %SCRIPT_DIR%Dockerfile
echo.

if not "%NO_CACHE%"=="" (
    echo [WARNING] Building without cache
)

REM Build command
docker build -f "%SCRIPT_DIR%Dockerfile" -t %IMAGE_NAME%:%IMAGE_TAG% %BUILD_ARGS% %NO_CACHE% "%PROJECT_ROOT%"

if errorlevel 1 (
    echo.
    echo [ERROR] Docker build failed!
    exit /b 1
)

echo.
echo [SUCCESS] Docker image built successfully!

REM ============================================================================
REM Post-build Information
REM ============================================================================

echo.
echo ============================================================================
echo Build Summary
echo ============================================================================

docker images %IMAGE_NAME%:%IMAGE_TAG%

echo.
echo ============================================================================
echo Next Steps
echo ============================================================================
echo.
echo 1. Test the image:
echo    docker run --rm -p 8501:8501 --env-file deployment\.env %IMAGE_NAME%:%IMAGE_TAG%
echo.
echo 2. Run with docker-compose:
echo    cd deployment ^&^& docker-compose up -d
echo.
echo 3. Tag for registry:
echo    docker tag %IMAGE_NAME%:%IMAGE_TAG% your-registry/%IMAGE_NAME%:%IMAGE_TAG%
echo.
echo 4. Push to registry:
echo    docker push your-registry/%IMAGE_NAME%:%IMAGE_TAG%
echo.

echo [SUCCESS] Build completed successfully!
goto :eof

REM ============================================================================
REM Show Usage
REM ============================================================================

:show_usage
echo Usage: %~nx0 [OPTIONS]
echo.
echo Build AgriPulse AI Docker image
echo.
echo OPTIONS:
echo     -t, --tag TAG           Image tag (default: latest)
echo     -n, --no-cache          Build without using cache
echo     -h, --help              Show this help message
echo.
echo EXAMPLES:
echo     %~nx0                          # Build with default settings
echo     %~nx0 -t v1.0.0                # Build with specific tag
echo     %~nx0 -t v1.0.0 --no-cache     # Build without cache
echo.
exit /b 0
