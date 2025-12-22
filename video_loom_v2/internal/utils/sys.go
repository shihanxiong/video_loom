package utils

import (
	"runtime"
)

// SysUtils provides system-related utility functions
type SysUtils struct{}

// IsWin32 checks if running on Windows
func (s *SysUtils) IsWin32() bool {
	return runtime.GOOS == "windows"
}

// IsMacOS checks if running on macOS
func (s *SysUtils) IsMacOS() bool {
	return runtime.GOOS == "darwin"
}

// IsLinux checks if running on Linux
func (s *SysUtils) IsLinux() bool {
	return runtime.GOOS == "linux"
}
