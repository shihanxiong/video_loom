#!/bin/bash

# Build script for Video Loom v2
# Generates distributables for all operating systems

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Get version from changelog
get_version() {
    local version_line=$(grep -m 1 "^## v[0-9]" changelog.md | head -1)
    if [ -z "$version_line" ]; then
        # Fallback: try ### format
        version_line=$(grep -m 1 "^### v[0-9]" changelog.md | head -1)
    fi
    if [ -z "$version_line" ]; then
        echo "v2.0.0"  # Default version
        return
    fi
    # Extract version (e.g., "## v2.0.0" -> "v2.0.0")
    echo "$version_line" | sed -E 's/^##?[[:space:]]*(v[0-9]+\.[0-9]+\.[0-9]+).*/\1/'
}

VERSION=$(get_version)
VERSION_NUM=$(echo "$VERSION" | sed 's/\./_/g')  # v2.0.0 -> v2_0_0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Video Loom v2 Build Script${NC}"
echo -e "${BLUE}Version: ${VERSION}${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if wails is installed
if ! command -v wails &> /dev/null; then
    echo -e "${RED}Error: wails CLI not found. Please install Wails v2.${NC}"
    echo "Install: go install github.com/wailsapp/wails/v2/cmd/wails@latest"
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "video_loom_v2" ]; then
    echo -e "${RED}Error: video_loom_v2 directory not found.${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

cd video_loom_v2

# Create dist directory
DIST_DIR="../dist/video_loom_${VERSION_NUM}"
mkdir -p "$DIST_DIR"

echo -e "${GREEN}Building for all platforms...${NC}"
echo ""

# Detect current platform
CURRENT_OS=$(uname -s)
CURRENT_ARCH=$(uname -m)

# Function to create DMG installer
create_dmg() {
    local app_path="$1"
    local dmg_name="$2"
    local temp_dmg_dir=$(mktemp -d)
    local dmg_path="$DIST_DIR/${dmg_name}.dmg"
    
    echo "  Creating DMG installer..."
    
    # Copy app to temp directory and rename to "Video Loom.app"
    cp -r "$app_path" "$temp_dmg_dir/Video Loom.app"
    
    # Create Applications symlink
    ln -s /Applications "$temp_dmg_dir/Applications"
    
    # Create DMG
    hdiutil create -volname "Video Loom ${VERSION}" \
        -srcfolder "$temp_dmg_dir" \
        -ov -format UDZO \
        "$dmg_path" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "  ${GREEN}✓${NC} DMG created: $(basename "$dmg_path")"
        rm -rf "$temp_dmg_dir"
        return 0
    else
        echo -e "  ${YELLOW}⚠${NC} DMG creation failed"
        rm -rf "$temp_dmg_dir"
        return 1
    fi
}

# Build for macOS (darwin)
echo -e "${YELLOW}[1/3] Building for macOS...${NC}"
MACOS_APP_PATH=""
if [ "$CURRENT_OS" = "Darwin" ]; then
    # Build for current architecture
    if [ "$CURRENT_ARCH" = "arm64" ]; then
        echo "  Building for darwin/arm64..."
        wails build -platform darwin/arm64 -clean
        MACOS_APP_PATH="$DIST_DIR/macos_video_loom_${VERSION_NUM}_arm64.app"
        cp -r build/bin/video_loom_v2.app "$MACOS_APP_PATH"
        echo -e "  ${GREEN}✓${NC} macOS ARM64 build complete"
        
        # Create DMG installer
        create_dmg "$MACOS_APP_PATH" "macos_video_loom_${VERSION_NUM}_arm64_installer"
    elif [ "$CURRENT_ARCH" = "x86_64" ]; then
        echo "  Building for darwin/amd64..."
        wails build -platform darwin/amd64 -clean
        MACOS_APP_PATH="$DIST_DIR/macos_video_loom_${VERSION_NUM}_amd64.app"
        cp -r build/bin/video_loom_v2.app "$MACOS_APP_PATH"
        echo -e "  ${GREEN}✓${NC} macOS AMD64 build complete"
        
        # Create DMG installer
        create_dmg "$MACOS_APP_PATH" "macos_video_loom_${VERSION_NUM}_amd64_installer"
    fi
    
    # Try to build for both architectures if on macOS (optional)
    # Note: Building for amd64 from arm64 may require Rosetta or additional setup
    # Uncomment the following block if you want to attempt universal builds:
    # if [ "$CURRENT_ARCH" = "arm64" ]; then
    #     echo "  Building for darwin/amd64 (Intel)..."
    #     if wails build -platform darwin/amd64 -clean 2>/dev/null; then
    #         cp -r build/bin/video_loom_v2.app "$DIST_DIR/macos_video_loom_${VERSION_NUM}_amd64.app"
    #         echo -e "  ${GREEN}✓${NC} macOS AMD64 build complete"
    #     else
    #         echo -e "  ${YELLOW}⚠${NC} macOS AMD64 build skipped (cross-compilation may require additional setup)"
    #     fi
    # fi
else
    echo -e "  ${YELLOW}⚠${NC} macOS build skipped (not on macOS)"
fi

echo ""

# Build for Windows
echo -e "${YELLOW}[2/3] Building for Windows...${NC}"
if command -v x86_64-w64-mingw32-gcc &> /dev/null || [ "$CURRENT_OS" = "MINGW" ] || [ "$CURRENT_OS" = "MSYS" ]; then
    echo "  Building for windows/amd64..."
    if wails build -platform windows/amd64 -clean 2>/dev/null; then
        # Find the .exe file
        if [ -f "build/bin/video_loom_v2.exe" ]; then
            cp build/bin/video_loom_v2.exe "$DIST_DIR/win32_video_loom_${VERSION_NUM}.exe"
            echo -e "  ${GREEN}✓${NC} Windows build complete"
        else
            echo -e "  ${YELLOW}⚠${NC} Windows .exe not found in build/bin/"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Windows build failed (may require cross-compilation tools)"
        echo "    Install: brew install mingw-w64 (on macOS) or use Windows to build"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Windows build skipped (cross-compilation tools not available)"
    echo "    To build for Windows:"
    echo "    - On macOS: brew install mingw-w64"
    echo "    - On Linux: sudo apt-get install gcc-mingw-w64-x86-64"
    echo "    - Or build directly on Windows"
fi

echo ""

# Build for Linux
echo -e "${YELLOW}[3/3] Building for Linux...${NC}"
if [ "$CURRENT_OS" = "Linux" ]; then
    echo "  Building for linux/amd64..."
    wails build -platform linux/amd64 -clean
    if [ -f "build/bin/video_loom_v2" ]; then
        cp build/bin/video_loom_v2 "$DIST_DIR/linux_video_loom_${VERSION_NUM}"
        chmod +x "$DIST_DIR/linux_video_loom_${VERSION_NUM}"
        echo -e "  ${GREEN}✓${NC} Linux build complete"
    else
        echo -e "  ${YELLOW}⚠${NC} Linux binary not found in build/bin/"
    fi
elif [ "$CURRENT_OS" = "Darwin" ]; then
    # Try to cross-compile for Linux from macOS
    echo "  Attempting Linux cross-compilation..."
    if command -v x86_64-linux-gnu-gcc &> /dev/null; then
        if wails build -platform linux/amd64 -clean 2>/dev/null; then
            if [ -f "build/bin/video_loom_v2" ]; then
                cp build/bin/video_loom_v2 "$DIST_DIR/linux_video_loom_${VERSION_NUM}"
                chmod +x "$DIST_DIR/linux_video_loom_${VERSION_NUM}"
                echo -e "  ${GREEN}✓${NC} Linux build complete"
            fi
        else
            echo -e "  ${YELLOW}⚠${NC} Linux cross-compilation failed"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Linux build skipped (cross-compilation tools not available)"
        echo "    To build for Linux:"
        echo "    - Install cross-compilation tools for your platform"
        echo "    - Or build directly on Linux"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Linux build skipped (not on Linux)"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Build Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# List what was built
if [ -d "$DIST_DIR" ]; then
    echo -e "${GREEN}Distributables created in:${NC} $DIST_DIR"
    echo ""
    echo "Files:"
    ls -lh "$DIST_DIR" | tail -n +2 | awk '{print "  " $9 " (" $5 ")"}'
    echo ""
    
    # Count builds
    MACOS_COUNT=$(ls -1 "$DIST_DIR"/*.app 2>/dev/null | wc -l | tr -d ' ')
    MACOS_DMG_COUNT=$(ls -1 "$DIST_DIR"/*.dmg 2>/dev/null | wc -l | tr -d ' ')
    WINDOWS_COUNT=$(ls -1 "$DIST_DIR"/*.exe 2>/dev/null | wc -l | tr -d ' ')
    LINUX_COUNT=$(ls -1 "$DIST_DIR"/linux_* 2>/dev/null | wc -l | tr -d ' ')
    
    TOTAL=$((MACOS_COUNT + WINDOWS_COUNT + LINUX_COUNT))
    
    echo -e "${GREEN}Total builds: ${TOTAL}${NC}"
    [ "$MACOS_COUNT" -gt 0 ] && echo -e "  ${GREEN}✓${NC} macOS app: $MACOS_COUNT"
    [ "$MACOS_DMG_COUNT" -gt 0 ] && echo -e "  ${GREEN}✓${NC} macOS DMG installer: $MACOS_DMG_COUNT"
    [ "$WINDOWS_COUNT" -gt 0 ] && echo -e "  ${GREEN}✓${NC} Windows: $WINDOWS_COUNT"
    [ "$LINUX_COUNT" -gt 0 ] && echo -e "  ${GREEN}✓${NC} Linux: $LINUX_COUNT"
    
    if [ "$TOTAL" -eq 0 ]; then
        echo -e "${YELLOW}⚠${NC} No builds were created. Check the errors above."
        exit 1
    fi
else
    echo -e "${RED}Error: Distribution directory was not created.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Build complete!${NC}"
echo ""
echo "To install and test:"
if [ "$MACOS_DMG_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}macOS Installer (DMG):${NC}"
    echo "    1. Open: $DIST_DIR/*.dmg"
    echo "    2. Drag Video Loom to Applications folder"
    echo "    3. Open from Applications"
elif [ "$MACOS_COUNT" -gt 0 ]; then
    echo "  macOS: open \"$DIST_DIR/macos_video_loom_${VERSION_NUM}_*.app\""
fi
if [ "$WINDOWS_COUNT" -gt 0 ]; then
    echo "  Windows: Run \"$DIST_DIR/win32_video_loom_${VERSION_NUM}.exe\""
fi
if [ "$LINUX_COUNT" -gt 0 ]; then
    echo "  Linux: ./$DIST_DIR/linux_video_loom_${VERSION_NUM}"
fi

