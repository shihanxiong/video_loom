//go:build windows
// +build windows

package utils

import (
	"os/exec"
	"syscall"
)

// getSysProcAttr returns system process attributes for Windows
func getSysProcAttr() *syscall.SysProcAttr {
	return &syscall.SysProcAttr{
		HideWindow: true,
	}
}

// SetSysProcAttr sets the SysProcAttr on a command for Windows
func SetSysProcAttr(cmd *exec.Cmd) {
	cmd.SysProcAttr = &syscall.SysProcAttr{
		HideWindow: true,
	}
}
