package utils

import (
	"os"
	"path/filepath"
	"regexp"
	"testing"
)

func TestFileUtils_EscapeFileName(t *testing.T) {
	fu := &FileUtils{}

	tests := []struct {
		input    string
		expected string
	}{
		{"abc.mp4", `"abc.mp4"`},
		{"", ""},
		{"file with spaces.mp4", `"file with spaces.mp4"`},
		{"test", `"test"`},
	}

	for _, tt := range tests {
		result := fu.EscapeFileName(tt.input)
		if result != tt.expected {
			t.Errorf("EscapeFileName(%s) = %s, want %s", tt.input, result, tt.expected)
		}
	}
}

func TestFileUtils_GetLatestVersionFromChangelog(t *testing.T) {
	fu := &FileUtils{}

	// Try to find changelog.md in parent directories
	changelogPath := ""
	dirs := []string{".", "..", "../..", "../../.."}

	for _, dir := range dirs {
		path := filepath.Join(dir, "changelog.md")
		if _, err := os.Stat(path); err == nil {
			changelogPath = path
			break
		}
	}

	if changelogPath == "" {
		t.Skip("changelog.md not found, skipping test")
	}

	version := fu.GetLatestVersionFromChangelog(changelogPath)

	// Version should match pattern vX.Y.Z, be "Unreleased", or "Hackday"
	matched, _ := regexp.MatchString(`^v[0-9]+\.[0-9]+\.[0-9]+$`, version)
	isUnreleased := version == "Unreleased"
	isHackday := version == "Hackday"

	if !matched && !isUnreleased && !isHackday {
		t.Errorf("GetLatestVersionFromChangelog() = %s, want pattern vX.Y.Z, 'Unreleased', or 'Hackday'", version)
	}
}

func TestFileUtils_CleanUpTempFiles(t *testing.T) {
	fu := &FileUtils{}

	// Create temporary test files
	testFiles := []string{"test_cleanup.mp4", "test_cleanup.mp3", "test_cleanup.aac"}

	// Create test files
	for _, filename := range testFiles {
		file, err := os.Create(filename)
		if err != nil {
			t.Fatalf("Failed to create test file %s: %v", filename, err)
		}
		file.Close()
	}

	// Verify files exist
	for _, filename := range testFiles {
		if _, err := os.Stat(filename); os.IsNotExist(err) {
			t.Fatalf("Test file %s was not created", filename)
		}
	}

	// Clean up
	err := fu.CleanUpTempFiles()
	if err != nil {
		t.Errorf("CleanUpTempFiles() error = %v", err)
	}

	// Verify files are removed
	for _, filename := range testFiles {
		if _, err := os.Stat(filename); !os.IsNotExist(err) {
			t.Errorf("Test file %s was not cleaned up", filename)
		}
	}
}
