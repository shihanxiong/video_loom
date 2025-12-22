#!/bin/bash

# Video Loom Installation Script
# This script installs all dependencies for both v1 (Python/Tkinter) and v2 (Wails/Go)

# Don't exit on error for optional installations
set +e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_section() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Read Python version from .tool-versions
get_python_version_from_tool_versions() {
    if [ -f ".tool-versions" ]; then
        PYTHON_VERSION_LINE=$(grep "^python " .tool-versions | head -n1)
        if [ -n "$PYTHON_VERSION_LINE" ]; then
            echo "$PYTHON_VERSION_LINE" | awk '{print $2}'
        else
            echo ""
        fi
    else
        echo ""
    fi
}

# Read Node.js version from .tool-versions
get_nodejs_version_from_tool_versions() {
    if [ -f ".tool-versions" ]; then
        NODEJS_VERSION_LINE=$(grep "^nodejs " .tool-versions | head -n1)
        if [ -n "$NODEJS_VERSION_LINE" ]; then
            echo "$NODEJS_VERSION_LINE" | awk '{print $2}'
        else
            echo ""
        fi
    else
        echo ""
    fi
}

# Get the script directory (repo root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_section "Video Loom Installation Script"
print_info "This script will install dependencies for:"
print_info "  - Video Loom v1 (Python/Tkinter)"
print_info "  - Video Loom v2 (Wails/Go)"
echo ""

# Ask which version to install
print_info "Which version(s) would you like to install?"
echo "  1) Video Loom v1 (Python/Tkinter) only"
echo "  2) Video Loom v2 (Wails/Go) only"
echo "  3) Both versions"
echo ""
read -p "Enter choice (1/2/3) [default: 3]: " -r
INSTALL_CHOICE="${REPLY:-3}"

INSTALL_V1=false
INSTALL_V2=false

case $INSTALL_CHOICE in
    1)
        INSTALL_V1=true
        ;;
    2)
        INSTALL_V2=true
        ;;
    3)
        INSTALL_V1=true
        INSTALL_V2=true
        ;;
    *)
        print_error "Invalid choice. Installing both versions."
        INSTALL_V1=true
        INSTALL_V2=true
        ;;
esac

echo ""

# ============================================================================
# COMMON DEPENDENCIES
# ============================================================================

print_section "Checking Common Dependencies"

# Check for FFmpeg (required for both versions)
FFMPEG_INSTALLED=false
if command_exists ffmpeg; then
    FFMPEG_VERSION=$(ffmpeg -version 2>/dev/null | head -n1 | awk '{print $3}' || echo "unknown")
    print_success "FFmpeg is installed: $FFMPEG_VERSION"
    FFMPEG_INSTALLED=true
else
    print_warning "FFmpeg is not installed. This is required for video processing."
    print_info "You can install it now or later. The application will not work without it."
    echo ""
    read -p "Do you want to install FFmpeg now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command_exists brew; then
                print_info "Installing FFmpeg using Homebrew..."
                if brew install ffmpeg; then
                    print_success "FFmpeg installed via Homebrew"
                    FFMPEG_INSTALLED=true
                else
                    print_error "Failed to install FFmpeg. Please install manually:"
                    print_info "  brew install ffmpeg"
                fi
            else
                print_error "Homebrew is not installed. Please install FFmpeg manually:"
                print_info "  brew install ffmpeg"
                print_info "Or visit: https://ffmpeg.org/download.html"
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command_exists apt-get; then
                print_info "Installing FFmpeg using apt-get (requires sudo)..."
                if sudo apt-get update && sudo apt-get install -y ffmpeg; then
                    print_success "FFmpeg installed via apt-get"
                    FFMPEG_INSTALLED=true
                else
                    print_error "Failed to install FFmpeg. Please install manually."
                fi
            elif command_exists yum; then
                print_info "Installing FFmpeg using yum (requires sudo)..."
                if sudo yum install -y ffmpeg; then
                    print_success "FFmpeg installed via yum"
                    FFMPEG_INSTALLED=true
                else
                    print_error "Failed to install FFmpeg. Please install manually."
                fi
            else
                print_error "Please install FFmpeg manually for your Linux distribution"
                print_info "Visit: https://ffmpeg.org/download.html"
            fi
        elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            # Windows (Git Bash or similar)
            print_error "Please install FFmpeg manually on Windows:"
            print_info "  choco install ffmpeg-full"
            print_info "Or visit: https://ffmpeg.org/download.html"
        else
            print_error "Unknown OS type. Please install FFmpeg manually."
            print_info "Visit: https://ffmpeg.org/download.html"
        fi
    else
        print_warning "Skipping FFmpeg installation. Please install it manually before using the application."
    fi
fi

# ============================================================================
# VIDEO LOOM V1 (Python/Tkinter)
# ============================================================================

if [ "$INSTALL_V1" = true ]; then
    print_section "Installing Video Loom v1 Dependencies"

    # Check for asdf and .tool-versions
    REQUIRED_PYTHON_VERSION=$(get_python_version_from_tool_versions)
    USE_ASDF=false
    
    if [ -n "$REQUIRED_PYTHON_VERSION" ]; then
        print_info "Found .tool-versions with Python version: $REQUIRED_PYTHON_VERSION"
        
        if command_exists asdf; then
            print_success "asdf is installed"
            
            # Check if Python plugin is installed
            if asdf plugin list 2>/dev/null | grep -q "^python$"; then
                print_success "asdf Python plugin is installed"
                USE_ASDF=true
                
                # Check for Tcl/Tk (required for Tkinter support)
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    if ! command_exists brew; then
                        print_warning "Homebrew is not installed. Tkinter support may not be available."
                    else
                        # Check if tcl-tk@8 is installed (compatible with Python 3.12+)
                        if ! brew list tcl-tk@8 >/dev/null 2>&1; then
                            print_info "Installing tcl-tk@8 for Tkinter support..."
                            if brew install tcl-tk@8 >/dev/null 2>&1; then
                                print_success "tcl-tk@8 installed for Tkinter support"
                            else
                                print_warning "Failed to install tcl-tk@8. Tkinter may not work."
                            fi
                        else
                            print_success "tcl-tk@8 is installed (Tkinter support available)"
                        fi
                    fi
                fi
                
                # Check if the required Python version is installed via asdf
                if asdf list python 2>/dev/null | grep -q "^  $REQUIRED_PYTHON_VERSION"; then
                    # Check if Tkinter is available
                    if python3 -c "import tkinter" 2>/dev/null; then
                        print_success "Python $REQUIRED_PYTHON_VERSION is installed via asdf with Tkinter support"
                    else
                        print_warning "Python $REQUIRED_PYTHON_VERSION is installed but Tkinter is not available"
                        if [[ "$OSTYPE" == "darwin"* ]] && command_exists brew && brew list tcl-tk@8 >/dev/null 2>&1; then
                            print_info "Reinstalling Python $REQUIRED_PYTHON_VERSION with Tkinter support..."
                            export PATH="$(brew --prefix tcl-tk@8)/bin:$PATH"
                            export LDFLAGS="-L$(brew --prefix tcl-tk@8)/lib"
                            export CPPFLAGS="-I$(brew --prefix tcl-tk@8)/include"
                            asdf uninstall python "$REQUIRED_PYTHON_VERSION" 2>/dev/null || true
                            if asdf install python "$REQUIRED_PYTHON_VERSION" 2>/dev/null; then
                                print_success "Python $REQUIRED_PYTHON_VERSION reinstalled with Tkinter support"
                            else
                                print_error "Failed to reinstall Python with Tkinter support"
                            fi
                        fi
                    fi
                    # Activate the version for current directory
                    asdf local python "$REQUIRED_PYTHON_VERSION" 2>/dev/null || true
                    asdf reshim python 2>/dev/null || true
                else
                    print_info "Installing Python $REQUIRED_PYTHON_VERSION via asdf..."
                    # Set up Tcl/Tk environment for macOS
                    if [[ "$OSTYPE" == "darwin"* ]] && command_exists brew && brew list tcl-tk@8 >/dev/null 2>&1; then
                        export PATH="$(brew --prefix tcl-tk@8)/bin:$PATH"
                        export LDFLAGS="-L$(brew --prefix tcl-tk@8)/lib"
                        export CPPFLAGS="-I$(brew --prefix tcl-tk@8)/include"
                        print_info "Using tcl-tk@8 for Tkinter support"
                    fi
                    if asdf install python "$REQUIRED_PYTHON_VERSION" 2>/dev/null; then
                        print_success "Python $REQUIRED_PYTHON_VERSION installed via asdf"
                        asdf local python "$REQUIRED_PYTHON_VERSION" 2>/dev/null || true
                        asdf reshim python 2>/dev/null || true
                    else
                        print_error "Failed to install Python $REQUIRED_PYTHON_VERSION via asdf"
                        print_warning "Falling back to system Python..."
                        USE_ASDF=false
                    fi
                fi
            else
                print_warning "asdf Python plugin is not installed"
                print_info "Install it with: asdf plugin add python"
                print_info "Then run: asdf install python $REQUIRED_PYTHON_VERSION"
                print_warning "Falling back to system Python..."
            fi
        else
            print_warning "asdf is not installed, but .tool-versions specifies Python $REQUIRED_PYTHON_VERSION"
            print_info "Consider installing asdf: https://asdf-vm.com/guide/getting-started.html"
            print_info "Or ensure Python $REQUIRED_PYTHON_VERSION is installed system-wide"
        fi
    else
        print_info "No .tool-versions found or no Python version specified"
        print_info "Will use system Python if available"
    fi

    # Determine which Python command to use
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    
    if [ "$USE_ASDF" = true ] && [ -n "$REQUIRED_PYTHON_VERSION" ]; then
        # Try to use asdf's Python (asdf should be in PATH and activated)
        # First try 'python' (asdf should make this available)
        if command_exists python; then
            PYTHON_VERSION_CHECK=$(python --version 2>&1 | awk '{print $2}')
            if [ "$PYTHON_VERSION_CHECK" = "$REQUIRED_PYTHON_VERSION" ]; then
                PYTHON_CMD="python"
                PIP_CMD="pip"
                print_info "Using Python from asdf: $PYTHON_CMD ($REQUIRED_PYTHON_VERSION)"
            fi
        fi
        
        # Fallback: try to get the path directly
        if [ "$PYTHON_CMD" = "python3" ]; then
            ASDF_PYTHON_PATH=$(asdf which python 2>/dev/null || echo "")
            if [ -n "$ASDF_PYTHON_PATH" ] && [ -f "$ASDF_PYTHON_PATH" ]; then
                PYTHON_CMD="$ASDF_PYTHON_PATH"
                # Try to find pip in the same directory or use python -m pip
                ASDF_PIP_PATH="${ASDF_PYTHON_PATH%python}pip"
                if [ -f "$ASDF_PIP_PATH" ]; then
                    PIP_CMD="$ASDF_PIP_PATH"
                else
                    PIP_CMD="$PYTHON_CMD -m pip"
                fi
                print_info "Using Python from asdf: $PYTHON_CMD"
            fi
        fi
    fi

    # Check for Python
    if ! command_exists "$PYTHON_CMD"; then
        if [ "$USE_ASDF" = true ]; then
            print_error "Python $REQUIRED_PYTHON_VERSION is not available via asdf."
            print_info "Trying to install it: asdf install python $REQUIRED_PYTHON_VERSION"
        else
            print_error "Python 3 is not installed. Please install Python 3.9 or later."
            if [ -n "$REQUIRED_PYTHON_VERSION" ]; then
                print_info "Required version: $REQUIRED_PYTHON_VERSION (from .tool-versions)"
            fi
            print_info "Visit: https://www.python.org/downloads/"
        fi
        print_warning "Skipping v1 installation."
        INSTALL_V1=false
    else
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
        print_success "Python is installed: $PYTHON_VERSION"
        
        if [ -n "$REQUIRED_PYTHON_VERSION" ]; then
            INSTALLED_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
            if [ "$INSTALLED_VERSION" != "$REQUIRED_PYTHON_VERSION" ]; then
                print_warning "Python version mismatch:"
                print_warning "  Required: $REQUIRED_PYTHON_VERSION (from .tool-versions)"
                print_warning "  Installed: $INSTALLED_VERSION"
                if [ "$USE_ASDF" = false ]; then
                    print_info "Consider installing asdf to manage Python versions"
                fi
            else
                print_success "Python version matches .tool-versions: $REQUIRED_PYTHON_VERSION"
            fi
        fi

        # Check for pip
        if ! command_exists "$PIP_CMD"; then
            # Try to use python -m pip as fallback
            if $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
                PIP_CMD="$PYTHON_CMD -m pip"
                print_info "Using pip via Python module: $PIP_CMD"
            else
                print_error "pip is not installed. Please install pip."
                print_warning "Skipping v1 installation."
                INSTALL_V1=false
            fi
        else
            PIP_VERSION=$($PIP_CMD --version 2>&1 | awk '{print $2}' | head -n1)
            print_success "pip is installed: $PIP_VERSION"
        fi

        if [ "$INSTALL_V1" = true ]; then
            # Check for pkg-config (required for av/PyAV)
            if ! command_exists pkg-config; then
                print_warning "pkg-config is not installed. It's required for building PyAV (av package)."
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    print_info "Install it with: brew install pkg-config"
                elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                    print_info "Install it with: sudo apt-get install pkg-config"
                fi
                print_warning "Some Python packages may fail to install without pkg-config."
            else
                print_success "pkg-config is installed"
            fi
            
            # Install Python dependencies
            if [ -f "video_loom_v1/requirements.txt" ]; then
                print_info "Installing Python dependencies from requirements.txt..."
                set +e  # Don't exit on error - we'll check the result
                
                # Upgrade pip first
                $PIP_CMD install --upgrade pip >/dev/null 2>&1
                
                # Install newer av version first (compatible with Python 3.12+)
                # tkvideoplayer requires av==9.2.0 which doesn't build on Python 3.12
                # We'll install a newer av version and then tkvideoplayer without strict dependency
                print_info "Installing av package (newer version for Python 3.12 compatibility)..."
                $PIP_CMD install 'av>=12.0.0' >/dev/null 2>&1
                
                # Install dependencies except tkvideoplayer (which has strict av==9.2.0 requirement)
                print_info "Installing other Python dependencies..."
                grep -v "^tkvideoplayer" video_loom_v1/requirements.txt > /tmp/requirements_v1.txt
                $PIP_CMD install -r /tmp/requirements_v1.txt
                PIP_EXIT_CODE=$?
                
                # Try to install tkvideoplayer without strict dependency checking
                if [ $PIP_EXIT_CODE -eq 0 ]; then
                    print_info "Installing tkvideoplayer (may show version warning, but should work)..."
                    $PIP_CMD install --no-deps tkvideoplayer >/dev/null 2>&1
                    # Install Pillow if not already installed (required by tkvideoplayer)
                    $PIP_CMD install Pillow >/dev/null 2>&1
                fi
                
                set -e  # Re-enable exit on error
                
                if [ $PIP_EXIT_CODE -eq 0 ]; then
                    print_success "Python dependencies installed"
                    print_info "Note: Using av>=12.0.0 instead of av==9.2.0 for Python 3.12 compatibility"
                else
                    print_error "Failed to install some Python dependencies"
                    print_warning "This may be due to missing system dependencies (e.g., pkg-config for PyAV)"
                    print_info "You may need to install system dependencies and try again"
                    print_warning "Continuing with installation, but v1 may not work correctly"
                fi
            else
                print_warning "video_loom_v1/requirements.txt not found, skipping Python dependencies"
            fi

            # Windows-specific: Check for Chocolatey (for FFmpeg installation)
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
                if ! command_exists choco; then
                    print_warning "Chocolatey is not installed. It's recommended for Windows."
                    print_info "Install from: https://chocolatey.org/install"
                else
                    print_success "Chocolatey is installed"
                fi
            fi
        fi
    fi
fi

# ============================================================================
# VIDEO LOOM V2 (Wails/Go)
# ============================================================================

if [ "$INSTALL_V2" = true ]; then
    print_section "Installing Video Loom v2 Dependencies"

    # Check for Go
    if ! command_exists go; then
        print_error "Go is not installed. Please install Go 1.18 or later."
        print_info "Visit: https://go.dev/dl/"
        print_warning "Skipping v2 installation."
        INSTALL_V2=false
    else
        GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
        print_success "Go is installed: $GO_VERSION"

        # Check for Node.js and npm
        REQUIRED_NODEJS_VERSION=$(get_nodejs_version_from_tool_versions)
        USE_ASDF_NODEJS=false
        
        if [ -n "$REQUIRED_NODEJS_VERSION" ]; then
            print_info "Found .tool-versions with Node.js version: $REQUIRED_NODEJS_VERSION"
            
            if command_exists asdf; then
                print_success "asdf is installed"
                
                # Check if Node.js plugin is installed
                if asdf plugin list 2>/dev/null | grep -q "^nodejs$"; then
                    print_success "asdf Node.js plugin is installed"
                    USE_ASDF_NODEJS=true
                    
                    # Check if the required Node.js version is installed via asdf
                    if asdf list nodejs 2>/dev/null | grep -q "^  $REQUIRED_NODEJS_VERSION"; then
                        print_success "Node.js $REQUIRED_NODEJS_VERSION is installed via asdf"
                        # Activate the version for current directory
                        asdf local nodejs "$REQUIRED_NODEJS_VERSION" 2>/dev/null || true
                        asdf reshim nodejs 2>/dev/null || true
                    else
                        print_info "Installing Node.js $REQUIRED_NODEJS_VERSION via asdf..."
                        if asdf install nodejs "$REQUIRED_NODEJS_VERSION" 2>/dev/null; then
                            print_success "Node.js $REQUIRED_NODEJS_VERSION installed via asdf"
                            asdf local nodejs "$REQUIRED_NODEJS_VERSION" 2>/dev/null || true
                            asdf reshim nodejs 2>/dev/null || true
                        else
                            print_error "Failed to install Node.js $REQUIRED_NODEJS_VERSION via asdf"
                            print_warning "Falling back to system Node.js..."
                            USE_ASDF_NODEJS=false
                        fi
                    fi
                else
                    print_warning "asdf Node.js plugin is not installed"
                    print_info "Install it with: asdf plugin add nodejs"
                    print_info "Then run: asdf install nodejs $REQUIRED_NODEJS_VERSION"
                    print_warning "Falling back to system Node.js..."
                fi
            else
                print_warning "asdf is not installed, but .tool-versions specifies Node.js $REQUIRED_NODEJS_VERSION"
                print_info "Consider installing asdf: https://asdf-vm.com/guide/getting-started.html"
                print_info "Or ensure Node.js $REQUIRED_NODEJS_VERSION is installed system-wide"
            fi
        else
            print_info "No .tool-versions found or no Node.js version specified"
            print_info "Will use system Node.js if available"
        fi
        
        # Determine which Node.js command to use
        NODE_CMD="node"
        NPM_CMD="npm"
        
        if [ "$USE_ASDF_NODEJS" = true ] && [ -n "$REQUIRED_NODEJS_VERSION" ]; then
            # Try to use asdf's Node.js (asdf should be in PATH and activated)
            if command_exists node; then
                NODE_VERSION_CHECK=$(node --version 2>&1 | sed 's/v//')
                if [ "$NODE_VERSION_CHECK" = "$REQUIRED_NODEJS_VERSION" ]; then
                    NODE_CMD="node"
                    NPM_CMD="npm"
                    print_info "Using Node.js from asdf: $NODE_CMD ($REQUIRED_NODEJS_VERSION)"
                fi
            fi
            
            # Fallback: try to get the path directly
            if [ "$NODE_CMD" = "node" ]; then
                ASDF_NODE_PATH=$(asdf which node 2>/dev/null || echo "")
                if [ -n "$ASDF_NODE_PATH" ] && [ -f "$ASDF_NODE_PATH" ]; then
                    NODE_CMD="$ASDF_NODE_PATH"
                    # npm should be in the same directory or available via PATH
                    ASDF_NPM_PATH="${ASDF_NODE_PATH%node}npm"
                    if [ -f "$ASDF_NPM_PATH" ]; then
                        NPM_CMD="$ASDF_NPM_PATH"
                    fi
                    print_info "Using Node.js from asdf: $NODE_CMD"
                fi
            fi
        fi
        
        if ! command_exists "$NODE_CMD"; then
            if [ "$USE_ASDF_NODEJS" = true ]; then
                print_error "Node.js $REQUIRED_NODEJS_VERSION is not available via asdf."
                print_info "Trying to install it: asdf install nodejs $REQUIRED_NODEJS_VERSION"
            else
                print_error "Node.js is not installed. Please install Node.js 16 or later."
                if [ -n "$REQUIRED_NODEJS_VERSION" ]; then
                    print_info "Required version: $REQUIRED_NODEJS_VERSION (from .tool-versions)"
                fi
                print_info "Visit: https://nodejs.org/"
            fi
            print_warning "Skipping v2 installation."
            INSTALL_V2=false
        else
            NODE_VERSION=$($NODE_CMD --version 2>&1)
            print_success "Node.js is installed: $NODE_VERSION"
            
            if [ -n "$REQUIRED_NODEJS_VERSION" ]; then
                INSTALLED_VERSION=$($NODE_CMD --version 2>&1 | sed 's/v//')
                if [ "$INSTALLED_VERSION" != "$REQUIRED_NODEJS_VERSION" ]; then
                    print_warning "Node.js version mismatch:"
                    print_warning "  Required: $REQUIRED_NODEJS_VERSION (from .tool-versions)"
                    print_warning "  Installed: $INSTALLED_VERSION"
                    if [ "$USE_ASDF_NODEJS" = false ]; then
                        print_info "Consider installing asdf to manage Node.js versions"
                    fi
                else
                    print_success "Node.js version matches .tool-versions: $REQUIRED_NODEJS_VERSION"
                fi
            fi

            if ! command_exists "$NPM_CMD"; then
                print_error "npm is not installed. Please install npm."
                print_warning "Skipping v2 installation."
                INSTALL_V2=false
            else
                NPM_VERSION=$($NPM_CMD --version 2>&1)
                print_success "npm is installed: $NPM_VERSION"

                # Check for Wails CLI
                if ! command_exists wails; then
                    print_warning "Wails CLI is not installed. Installing..."
                    go install github.com/wailsapp/wails/v2/cmd/wails@latest
                    if command_exists wails; then
                        print_success "Wails CLI installed successfully"
                    else
                        print_error "Failed to install Wails CLI. Please install manually:"
                        print_info "  go install github.com/wailsapp/wails/v2/cmd/wails@latest"
                        print_info "  Make sure \$GOPATH/bin or \$HOME/go/bin is in your PATH"
                        print_warning "Continuing without Wails CLI..."
                    fi
                else
                    WAILS_VERSION=$(wails version 2>/dev/null | head -n1 || echo "unknown")
                    print_success "Wails CLI is installed: $WAILS_VERSION"
                fi

                # Install Go dependencies for v2
                if [ -d "video_loom_v2" ] && [ -f "video_loom_v2/go.mod" ]; then
                    print_info "Installing Go dependencies for v2..."
                    cd video_loom_v2
                    set -e  # Exit on error for critical steps
                    go mod download
                    go mod tidy
                    set +e  # Don't exit on error for remaining steps
                    print_success "Go dependencies installed"
                    cd ..
                else
                    print_warning "video_loom_v2 directory or go.mod not found, skipping Go dependencies"
                fi

                # Install frontend dependencies for v2
                if [ -d "video_loom_v2/frontend" ] && [ -f "video_loom_v2/frontend/package.json" ]; then
                    print_info "Installing frontend dependencies for v2..."
                    cd video_loom_v2/frontend
                    set +e  # Don't exit on error - we'll check the result
                    $NPM_CMD install
                    NPM_INSTALL_EXIT_CODE=$?
                    set -e  # Re-enable exit on error
                    
                    if [ $NPM_INSTALL_EXIT_CODE -eq 0 ]; then
                        print_success "Frontend dependencies installed"
                    else
                        print_error "Failed to install frontend dependencies"
                        print_warning "Continuing with installation, but v2 may not work correctly"
                    fi
                    cd ../..
                else
                    print_warning "video_loom_v2/frontend directory or package.json not found, skipping frontend dependencies"
                fi

                # Generate Wails bindings
                if command_exists wails && [ -d "video_loom_v2" ]; then
                    print_info "Generating Wails bindings..."
                    cd video_loom_v2
                    wails generate module
                    print_success "Wails bindings generated"
                    cd ..
                fi
            fi
        fi
    fi
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo ""
print_section "Installation Summary"

SUCCESS=true

if [ "$INSTALL_V1" = true ]; then
    if [ -f "video_loom_v1/requirements.txt" ] && command_exists python3 && command_exists pip3; then
        print_success "Video Loom v1: Ready"
    else
        print_warning "Video Loom v1: Incomplete (missing dependencies)"
        SUCCESS=false
    fi
fi

if [ "$INSTALL_V2" = true ]; then
    if [ -d "video_loom_v2" ] && command_exists go && command_exists node && command_exists npm; then
        print_success "Video Loom v2: Ready"
    else
        print_warning "Video Loom v2: Incomplete (missing dependencies)"
        SUCCESS=false
    fi
fi

if [ "$FFMPEG_INSTALLED" = false ]; then
    print_warning "FFmpeg: Not installed (required for both versions)"
    SUCCESS=false
else
    print_success "FFmpeg: Installed"
fi

echo ""
if [ "$SUCCESS" = true ] && [ "$FFMPEG_INSTALLED" = true ]; then
    print_success "=================================="
    print_success "Installation completed successfully!"
    print_success "=================================="
else
    print_warning "=================================="
    print_warning "Installation completed with warnings"
    print_warning "=================================="
fi

echo ""
print_info "Next steps:"

if [ "$FFMPEG_INSTALLED" = false ]; then
    print_info "  - Install FFmpeg:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "    brew install ffmpeg"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "    sudo apt-get install ffmpeg  # or yum install ffmpeg"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        print_info "    choco install ffmpeg-full"
    fi
    echo ""
fi

if [ "$INSTALL_V1" = true ]; then
    print_info "  Video Loom v1:"
    print_info "    - Run: cd video_loom_v1/src && python3 app.py"
    print_info "    - Build: cd video_loom_v1/src && ./bundle.sh app.win32.spec v1.x.x"
    print_info "    - Test: cd video_loom_v1/src && python3 -m pytest test_*.py -vvs"
    echo ""
fi

if [ "$INSTALL_V2" = true ]; then
    print_info "  Video Loom v2:"
    print_info "    - Run: cd video_loom_v2 && wails dev"
    print_info "    - Build: cd video_loom_v2 && wails build"
    echo ""
fi

echo ""

