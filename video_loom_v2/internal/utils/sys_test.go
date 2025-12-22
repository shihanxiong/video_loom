package utils

import (
	"runtime"
	"testing"
)

func TestSysUtils_IsWin32(t *testing.T) {
	su := &SysUtils{}
	result := su.IsWin32()
	expected := runtime.GOOS == "windows"

	if result != expected {
		t.Errorf("IsWin32() = %v, want %v", result, expected)
	}
}

func TestSysUtils_IsMacOS(t *testing.T) {
	su := &SysUtils{}
	result := su.IsMacOS()
	expected := runtime.GOOS == "darwin"

	if result != expected {
		t.Errorf("IsMacOS() = %v, want %v", result, expected)
	}
}

func TestSysUtils_IsLinux(t *testing.T) {
	su := &SysUtils{}
	result := su.IsLinux()
	expected := runtime.GOOS == "linux"

	if result != expected {
		t.Errorf("IsLinux() = %v, want %v", result, expected)
	}
}
