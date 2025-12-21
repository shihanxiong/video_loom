package utils

import (
	"os"
	"path/filepath"
	"strings"
)

// FileUtils provides file-related utility functions
type FileUtils struct{}

// CleanUpTempFiles removes temporary MP4, MP3, and AAC files in the current directory
func (f *FileUtils) CleanUpTempFiles() error {
	patterns := []string{"*.mp4", "*.mp3", "*.aac"}
	for _, pattern := range patterns {
		matches, err := filepath.Glob(pattern)
		if err != nil {
			continue
		}
		for _, match := range matches {
			os.Remove(match)
		}
	}
	return nil
}

// EscapeFileName wraps filename in quotes
func (f *FileUtils) EscapeFileName(filename string) string {
	if filename == "" {
		return ""
	}
	return `"` + filename + `"`
}

// GetLatestVersionFromChangelog extracts version from changelog.md
func (f *FileUtils) GetLatestVersionFromChangelog(changelogPath string) string {
	data, err := os.ReadFile(changelogPath)
	if err != nil {
		return "Unknown"
	}

	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		if strings.HasPrefix(line, "###") {
			parts := strings.Fields(line)
			if len(parts) > 1 {
				return parts[1]
			}
		}
	}
	return "Unknown"
}
