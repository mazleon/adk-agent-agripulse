@echo off
REM ============================================================================
REM AgriPulse AI - Docker Deployment Script (Windows)
REM ============================================================================
REM Deploys application using docker-compose with proper validation
REM ============================================================================

setlocal enabledelayedexpansion

REM Default values
set COMPOSE_FILE=docker-compose.yml
set ENV_FILE=.env
set ACTION=up

REM Script directory
set SCRIPT_DIR=%~dp0

REM ============================================================================
REM Parse Arguments
REM ============================================================================

:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="-f" (
    set COMPOSE_FILE=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--file" (
    set COMPOSE_FILE=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="-e" (
    set ENV_FILE=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--env" (
    set ENV_FILE=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="-d" (
    set COMPOSE_FILE=docker-compose.dev.yml
    shift
    goto parse_args
)
if /i "%~1"=="--dev" (
    set COMPOSE_FILE=docker-compose.dev.yml
    shift
    goto parse_args
)
if /i "%~1"=="-h" goto show_usage
if /i "%~1"=="--help" goto show_usage
if /i "%~1"=="up" (
    set ACTION=up
    shift
    goto parse_args
)
if /i "%~1"=="down" (
    set ACTION=down
    shift
    goto parse_args
)
if /i "%~1"=="restart" (
    set ACTION=restart
    shift
    goto parse_args
)
if /i "%~1"=="logs" (
    set ACTION=logs
    shift
    goto parse_args
)
if /i "%~1"=="status" (
    set ACTION=status
    shift
    goto parse_args
)
if /i "%~1"=="build" (
    set ACTION=build
    shift
    goto parse_args
)
shift
goto parse_args

:end_parse

REM ============================================================================
REM Check Prerequisites
REM ============================================================================

echo ============================================================================
echo Checking Prerequisites
echo ============================================================================

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed
    exit /b 1
)
echo [OK] Docker is installed

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker Compose is not installed
        exit /b 1
    )
)
echo [OK] Docker Compose is installed

REM Check if compose file exists
if not exist "%SCRIPT_DIR%%COMPOSE_FILE%" (
    echo [ERROR] Compose file not found: %SCRIPT_DIR%%COMPOSE_FILE%
    exit /b 1
)
echo [OK] Compose file found: %COMPOSE_FILE%

REM Check if env file exists
if not exist "%SCRIPT_DIR%%ENV_FILE%" (
    echo [WARNING] Environment file not found: %SCRIPT_DIR%%ENV_FILE%
    
    if exist "%SCRIPT_DIR%.env.docker" (
        echo [INFO] Creating from template...
        copy "%SCRIPT_DIR%.env.docker" "%SCRIPT_DIR%%ENV_FILE%"
        echo [WARNING] Please edit %SCRIPT_DIR%%ENV_FILE% with your configuration
        exit /b 1
    ) else (
        echo [ERROR] Template file .env.docker not found
        exit /b 1
    )
)
echo [OK] Environment file found: %ENV_FILE%

REM Check secrets directory
if not exist "%SCRIPT_DIR%secrets" (
    echo [WARNING] Secrets directory not found
    mkdir "%SCRIPT_DIR%secrets"
    echo [INFO] Created secrets directory at %SCRIPT_DIR%secrets
    echo [WARNING] Please place your Snowflake private key at: %SCRIPT_DIR%secrets\snowflake_key.pem
)

REM Check if Snowflake key exists
if not exist "%SCRIPT_DIR%secrets\snowflake_key.pem" (
    echo [WARNING] Snowflake private key not found at %SCRIPT_DIR%secrets\snowflake_key.pem
    echo [INFO] Please copy your Snowflake private key to this location
) else (
    echo [OK] Snowflake private key found
)

REM ============================================================================
REM Execute Action
REM ============================================================================

cd /d "%SCRIPT_DIR%"

echo.
echo ============================================================================
echo Executing: %ACTION%
echo ============================================================================
echo.

if /i "%ACTION%"=="up" goto action_up
if /i "%ACTION%"=="down" goto action_down
if /i "%ACTION%"=="restart" goto action_restart
if /i "%ACTION%"=="logs" goto action_logs
if /i "%ACTION%"=="status" goto action_status
if /i "%ACTION%"=="build" goto action_build

echo [ERROR] Unknown action: %ACTION%
goto show_usage

:action_up
echo [INFO] Starting services...
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services
    exit /b 1
)
echo.
echo [SUCCESS] Services started successfully!
echo.
echo [INFO] Application is running at: http://localhost:8501
echo.
echo [INFO] View logs with: %~nx0 logs
goto end_action

:action_down
echo [INFO] Stopping services...
docker-compose -f "%COMPOSE_FILE%" down
if errorlevel 1 (
    echo [ERROR] Failed to stop services
    exit /b 1
)
echo [SUCCESS] Services stopped successfully!
goto end_action

:action_restart
echo [INFO] Restarting services...
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" restart
if errorlevel 1 (
    echo [ERROR] Failed to restart services
    exit /b 1
)
echo [SUCCESS] Services restarted successfully!
goto end_action

:action_logs
echo [INFO] Showing logs (Ctrl+C to exit)...
docker-compose -f "%COMPOSE_FILE%" logs -f
goto end_action

:action_status
echo [INFO] Service status:
docker-compose -f "%COMPOSE_FILE%" ps
goto end_action

:action_build
echo [INFO] Building and starting services...
docker-compose -f "%COMPOSE_FILE%" --env-file "%ENV_FILE%" up -d --build
if errorlevel 1 (
    echo [ERROR] Failed to build and start services
    exit /b 1
)
echo [SUCCESS] Services built and started successfully!
goto end_action

:end_action
echo.
echo [SUCCESS] Deployment completed successfully!
goto :eof

REM ============================================================================
REM Show Usage
REM ============================================================================

:show_usage
echo Usage: %~nx0 [OPTIONS] [ACTION]
echo.
echo Deploy AgriPulse AI using Docker Compose
echo.
echo ACTIONS:
echo     up          Start services (default)
echo     down        Stop and remove services
echo     restart     Restart services
echo     logs        Show service logs
echo     status      Show service status
echo     build       Build images before starting
echo.
echo OPTIONS:
echo     -f, --file FILE         Docker Compose file (default: docker-compose.yml)
echo     -e, --env FILE          Environment file (default: .env)
echo     -d, --dev               Use development configuration
echo     -h, --help              Show this help message
echo.
echo EXAMPLES:
echo     %~nx0                      # Start services
echo     %~nx0 down                 # Stop services
echo     %~nx0 -d up                # Start in development mode
echo     %~nx0 logs                 # Show logs
echo     %~nx0 restart              # Restart services
echo.
exit /b 0
