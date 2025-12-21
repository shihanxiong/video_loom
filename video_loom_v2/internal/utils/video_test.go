package utils

import (
	"os"
	"path/filepath"
	"testing"
)

func TestVideoUtils_GetFFmpegPresetValueForNVENC(t *testing.T) {
	vu := NewVideoUtils()

	tests := []struct {
		input    string
		expected string
	}{
		{"faster", "fast"},
		{"veryslow", "slow"},
		{"medium", "medium"},
		{"ultrafast", "fast"},
		{"superfast", "fast"},
		{"veryfast", "fast"},
		{"fast", "fast"},
		{"slow", "slow"},
		{"slower", "slow"},
		{"not-a-valid-preset", "medium"},
	}

	for _, tt := range tests {
		result := vu.GetFFmpegPresetValueForNVENC(tt.input)
		if result != tt.expected {
			t.Errorf("GetFFmpegPresetValueForNVENC(%s) = %s, want %s", tt.input, result, tt.expected)
		}
	}
}

func TestVideoUtils_GetVideoDuration(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	if testVideo == "" {
		t.Skip("Test video not found, skipping test")
		return
	}

	vu := NewVideoUtils()
	duration, err := vu.GetVideoDuration(testVideo)
	if err != nil {
		t.Fatalf("GetVideoDuration() error = %v", err)
	}

	// The test video should be 15 seconds
	if duration != 15 {
		t.Errorf("GetVideoDuration() = %d, want 15", duration)
	}
}

func TestVideoUtils_GetVideoResolution(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	if testVideo == "" {
		t.Skip("Test video not found, skipping test")
		return
	}

	vu := NewVideoUtils()
	width, height, err := vu.GetVideoResolution(testVideo)
	if err != nil {
		t.Fatalf("GetVideoResolution() error = %v", err)
	}

	// The test video should be 1920x1080
	if width != 1920 || height != 1080 {
		t.Errorf("GetVideoResolution() = %dx%d, want 1920x1080", width, height)
	}
}

func TestVideoUtils_ConcatenateVideos(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	if testVideo == "" {
		t.Skip("Test video not found, skipping test")
		return
	}

	vu := NewVideoUtils()
	outputDir := "test"
	outputName := "test_concatenate_videos.mp4"
	outputPath := filepath.Join(outputDir, outputName)

	// Create output directory if it doesn't exist
	os.MkdirAll(outputDir, 0755)

	// Clean up if exists
	os.Remove(outputPath)

	// Concatenate two copies of the same video (each 15 seconds = 30 seconds total)
	videos := []string{testVideo, testVideo}
	_, err := vu.ConcatenateVideos(videos, outputDir, outputName, "ultrafast")
	if err != nil {
		t.Fatalf("ConcatenateVideos() error = %v", err)
	}

	// Verify output exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Errorf("ConcatenateVideos() output file was not created: %s", outputPath)
	}

	// Verify duration is approximately 30 seconds
	duration, err := vu.GetVideoDuration(outputPath)
	if err != nil {
		t.Logf("Warning: Could not verify duration: %v", err)
	} else if duration != 30 {
		t.Errorf("ConcatenateVideos() duration = %d, want 30", duration)
	}

	// Clean up
	os.Remove(outputPath)
}

func TestVideoUtils_CombineMP4AACToMP4(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	testAudio := findTestAsset("long_duration_audio.aac")
	if testVideo == "" || testAudio == "" {
		t.Skip("Test assets not found, skipping test")
		return
	}

	vu := NewVideoUtils()
	outputDir := "test"
	outputName := "test_combined.mp4"
	outputPath := filepath.Join(outputDir, outputName)

	// Create output directory if it doesn't exist
	os.MkdirAll(outputDir, 0755)

	// Clean up if exists
	os.Remove(outputPath)

	_, err := vu.CombineMP4AACToMP4(testVideo, testAudio, outputDir, outputName, "ultrafast")
	if err != nil {
		t.Fatalf("CombineMP4AACToMP4() error = %v", err)
	}

	// Verify output exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Errorf("CombineMP4AACToMP4() output file was not created: %s", outputPath)
	}

	// Verify duration is approximately 15 seconds (video duration)
	duration, err := vu.GetVideoDuration(outputPath)
	if err != nil {
		t.Logf("Warning: Could not verify duration: %v", err)
	} else if duration != 15 {
		t.Errorf("CombineMP4AACToMP4() duration = %d, want 15", duration)
	}

	// Clean up
	os.Remove(outputPath)
}

func TestVideoUtils_TrimMP4ByTimestamp(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	if testVideo == "" {
		t.Skip("Test video not found, skipping test")
		return
	}

	vu := NewVideoUtils()
	outputDir := "test"
	outputPath := filepath.Join(outputDir, "test_trimmed.mp4")

	// Create output directory if it doesn't exist
	os.MkdirAll(outputDir, 0755)

	// Clean up if exists
	os.Remove(outputPath)

	// Trim from 5 to 10 seconds (5 second clip)
	err := vu.TrimMP4ByTimestamp(testVideo, "0:00:05", "0:00:10", 1920, 1080, "ultrafast", outputPath)
	if err != nil {
		t.Fatalf("TrimMP4ByTimestamp() error = %v", err)
	}

	// Verify output exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Errorf("TrimMP4ByTimestamp() output file was not created: %s", outputPath)
	}

	// Verify duration is approximately 5 seconds
	duration, err := vu.GetVideoDuration(outputPath)
	if err != nil {
		t.Logf("Warning: Could not verify duration: %v", err)
	} else if duration != 5 {
		t.Errorf("TrimMP4ByTimestamp() duration = %d, want 5", duration)
	}

	// Clean up
	os.Remove(outputPath)
}
