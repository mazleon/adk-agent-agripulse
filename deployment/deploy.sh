#!/bin/bash
# ============================================================================
# AgriPulse AI - Docker Deployment Script
# ============================================================================
# Deploys application using docker-compose with proper validation
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"
ACTION="up"

# ============================================================================
# Functions
# ============================================================================

print_header() {
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] [ACTION]

Deploy AgriPulse AI using Docker Compose

ACTIONS:
    up          Start services (default)
    down        Stop and remove services
    restart     Restart services
    logs        Show service logs
    status      Show service status
    build       Build images before starting

OPTIONS:
    -f, --file FILE         Docker Compose file (default: docker-compose.yml)
    -e, --env FILE          Environment file (default: .env)
    -d, --dev               Use development configuration
    -h, --help              Show this help message

EXAMPLES:
    $0                      # Start services
    $0 down                 # Stop services
    $0 -d up                # Start in development mode
    $0 logs                 # Show logs
    $0 restart              # Restart services

EOF
}

check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check if compose file exists
    if [ ! -f "$SCRIPT_DIR/$COMPOSE_FILE" ]; then
        print_error "Compose file not found: $SCRIPT_DIR/$COMPOSE_FILE"
        exit 1
    fi
    print_success "Compose file found: $COMPOSE_FILE"
    
    # Check if env file exists
    if [ ! -f "$SCRIPT_DIR/$ENV_FILE" ]; then
        print_warning "Environment file not found: $SCRIPT_DIR/$ENV_FILE"
        print_info "Creating from template..."
        
        if [ -f "$SCRIPT_DIR/.env.docker" ]; then
            cp "$SCRIPT_DIR/.env.docker" "$SCRIPT_DIR/$ENV_FILE"
            print_warning "Please edit $SCRIPT_DIR/$ENV_FILE with your configuration"
            exit 1
        else
            print_error "Template file .env.docker not found"
            exit 1
        fi
    fi
    print_success "Environment file found: $ENV_FILE"
    
    # Check secrets directory
    if [ ! -d "$SCRIPT_DIR/secrets" ]; then
        print_warning "Secrets directory not found"
        mkdir -p "$SCRIPT_DIR/secrets"
        print_info "Created secrets directory at $SCRIPT_DIR/secrets"
        print_warning "Please place your Snowflake private key at: $SCRIPT_DIR/secrets/snowflake_key.pem"
    fi
    
    # Check if Snowflake key exists
    if [ ! -f "$SCRIPT_DIR/secrets/snowflake_key.pem" ]; then
        print_warning "Snowflake private key not found at $SCRIPT_DIR/secrets/snowflake_key.pem"
        print_info "Please copy your Snowflake private key to this location"
    else
        print_success "Snowflake private key found"
    fi
}

validate_env_file() {
    print_header "Validating Environment Configuration"
    
    # Check required variables
    local required_vars=(
        "GOOGLE_API_KEY"
        "SNOWFLAKE_USER"
        "SNOWFLAKE_ACCOUNT"
        "SNOWFLAKE_ROLE"
        "SNOWFLAKE_WAREHOUSE"
        "SNOWFLAKE_DATABASE"
        "SNOWFLAKE_SCHEMA"
    )
    
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" "$SCRIPT_DIR/$ENV_FILE" || grep -q "^${var}=your_" "$SCRIPT_DIR/$ENV_FILE"; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        print_error "Missing or incomplete configuration for:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        print_info "Please update $SCRIPT_DIR/$ENV_FILE"
        exit 1
    fi
    
    print_success "Environment configuration is valid"
}

# ============================================================================
# Parse Arguments
# ============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            COMPOSE_FILE="$2"
            shift 2
            ;;
        -e|--env)
            ENV_FILE="$2"
            shift 2
            ;;
        -d|--dev)
            COMPOSE_FILE="docker-compose.dev.yml"
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        up|down|restart|logs|status|build)
            ACTION="$1"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# ============================================================================
# Main Execution
# ============================================================================

cd "$SCRIPT_DIR"

# Run checks
check_prerequisites
validate_env_file

# Execute action
print_header "Executing: $ACTION"

case $ACTION in
    up)
        print_info "Starting services..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
        print_success "Services started successfully!"
        echo ""
        print_info "Application is running at: http://localhost:${APP_PORT:-8501}"
        echo ""
        print_info "View logs with: $0 logs"
        ;;
    
    down)
        print_info "Stopping services..."
        docker-compose -f "$COMPOSE_FILE" down
        print_success "Services stopped successfully!"
        ;;
    
    restart)
        print_info "Restarting services..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" restart
        print_success "Services restarted successfully!"
        ;;
    
    logs)
        print_info "Showing logs (Ctrl+C to exit)..."
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    
    status)
        print_info "Service status:"
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
    
    build)
        print_info "Building and starting services..."
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d --build
        print_success "Services built and started successfully!"
        ;;
    
    *)
        print_error "Unknown action: $ACTION"
        show_usage
        exit 1
        ;;
esac

print_success "Deployment completed successfully!"
