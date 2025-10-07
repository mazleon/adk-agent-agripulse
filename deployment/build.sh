#!/bin/bash
# ============================================================================
# AgriPulse AI - Docker Build Script
# ============================================================================
# Builds optimized Docker image with proper tagging and caching
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
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default values
IMAGE_NAME="agripulse-ai"
IMAGE_TAG="latest"
BUILD_ARGS=""
NO_CACHE=""

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
Usage: $0 [OPTIONS]

Build AgriPulse AI Docker image

OPTIONS:
    -t, --tag TAG           Image tag (default: latest)
    -n, --no-cache          Build without using cache
    -p, --platform PLATFORM Build for specific platform (e.g., linux/amd64)
    -h, --help              Show this help message

EXAMPLES:
    $0                          # Build with default settings
    $0 -t v1.0.0                # Build with specific tag
    $0 -t v1.0.0 --no-cache     # Build without cache
    $0 -p linux/amd64           # Build for specific platform

EOF
}

# ============================================================================
# Parse Arguments
# ============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        -n|--no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        -p|--platform)
            BUILD_ARGS="$BUILD_ARGS --platform $2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# ============================================================================
# Pre-build Checks
# ============================================================================

print_header "Pre-build Checks"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi
print_success "Docker is installed"

# Check if Dockerfile exists
if [ ! -f "$SCRIPT_DIR/Dockerfile" ]; then
    print_error "Dockerfile not found at $SCRIPT_DIR/Dockerfile"
    exit 1
fi
print_success "Dockerfile found"

# Check if pyproject.toml exists
if [ ! -f "$PROJECT_ROOT/pyproject.toml" ]; then
    print_error "pyproject.toml not found at $PROJECT_ROOT/pyproject.toml"
    exit 1
fi
print_success "pyproject.toml found"

# ============================================================================
# Build Docker Image
# ============================================================================

print_header "Building Docker Image"

print_info "Image name: $IMAGE_NAME:$IMAGE_TAG"
print_info "Build context: $PROJECT_ROOT"
print_info "Dockerfile: $SCRIPT_DIR/Dockerfile"

if [ -n "$NO_CACHE" ]; then
    print_warning "Building without cache"
fi

# Build command
BUILD_CMD="docker build \
    -f $SCRIPT_DIR/Dockerfile \
    -t $IMAGE_NAME:$IMAGE_TAG \
    $BUILD_ARGS \
    $NO_CACHE \
    $PROJECT_ROOT"

print_info "Executing: $BUILD_CMD"
echo ""

# Execute build
if eval $BUILD_CMD; then
    print_success "Docker image built successfully!"
else
    print_error "Docker build failed!"
    exit 1
fi

# ============================================================================
# Post-build Information
# ============================================================================

print_header "Build Summary"

# Get image size
IMAGE_SIZE=$(docker images $IMAGE_NAME:$IMAGE_TAG --format "{{.Size}}")
print_info "Image: $IMAGE_NAME:$IMAGE_TAG"
print_info "Size: $IMAGE_SIZE"

# Show image layers (optional)
print_info "Image layers:"
docker history $IMAGE_NAME:$IMAGE_TAG --human=true --format "table {{.CreatedBy}}\t{{.Size}}" | head -10

echo ""
print_header "Next Steps"
echo ""
echo "1. Test the image:"
echo "   docker run --rm -p 8501:8501 --env-file deployment/.env $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "2. Run with docker-compose:"
echo "   cd deployment && docker-compose up -d"
echo ""
echo "3. Tag for registry:"
echo "   docker tag $IMAGE_NAME:$IMAGE_TAG your-registry/$IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "4. Push to registry:"
echo "   docker push your-registry/$IMAGE_NAME:$IMAGE_TAG"
echo ""

print_success "Build completed successfully!"
