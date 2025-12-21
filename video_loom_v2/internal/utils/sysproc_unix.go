//go:build !windows
// +build !windows

package utils

import "os/exec"

// SetSysProcAttr sets the SysProcAttr on a command for non-Windows platforms
func SetSysProcAttr(cmd *exec.Cmd) {
	// No-op for non-Windows platforms
}
