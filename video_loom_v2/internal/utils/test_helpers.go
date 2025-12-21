package utils

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"
)

// findTestAsset searches for test assets in common locations
func findTestAsset(filename string) string {
	searchPaths := []string{
		"../../video_loom_v1/src/test",
		"../../../video_loom_v1/src/test",
		"../../../../video_loom_v1/src/test",
		"test",
		"../test",
		"../../test",
	}

	for _, path := range searchPaths {
		fullPath := filepath.Join(path, filename)
		if _, err := os.Stat(fullPath); err == nil {
			return fullPath
		}
	}
	return ""
}

// checkFFmpeg checks if ffmpeg and ffprobe are available
func checkFFmpeg(t *testing.T) bool {
	if _, err := exec.LookPath("ffmpeg"); err != nil {
		t.Skip("ffmpeg not found, skipping video tests")
		return false
	}
	if _, err := exec.LookPath("ffprobe"); err != nil {
		t.Skip("ffprobe not found, skipping video tests")
		return false
	}
	return true
}
