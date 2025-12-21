package utils

import (
	"os"
	"path/filepath"
	"testing"
)

func TestAudioUtils_GetAudioDuration(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	audio1 := findTestAsset("audio_1.aac")
	audio2 := findTestAsset("audio_2.aac")
	if audio1 == "" || audio2 == "" {
		t.Skip("Test audio files not found, skipping test")
		return
	}

	au := NewAudioUtils()

	// Test audio_1.aac should be 5 seconds
	duration1, err := au.GetAudioDuration(audio1)
	if err != nil {
		t.Fatalf("GetAudioDuration(audio_1.aac) error = %v", err)
	}
	if duration1 != 5 {
		t.Errorf("GetAudioDuration(audio_1.aac) = %d, want 5", duration1)
	}

	// Test audio_2.aac should be 10 seconds
	duration2, err := au.GetAudioDuration(audio2)
	if err != nil {
		t.Fatalf("GetAudioDuration(audio_2.aac) error = %v", err)
	}
	if duration2 != 10 {
		t.Errorf("GetAudioDuration(audio_2.aac) = %d, want 10", duration2)
	}
}

func TestAudioUtils_GenerateMP3FromMP4(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	if testVideo == "" {
		t.Skip("Test video not found, skipping test")
		return
	}

	au := NewAudioUtils()
	outputDir := "test"
	outputPath := filepath.Join(outputDir, "test_generate_mp3_from_mp4.mp3")

	// Create output directory if it doesn't exist
	os.MkdirAll(outputDir, 0755)

	// Clean up if exists
	os.Remove(outputPath)

	err := au.GenerateMP3FromMP4(testVideo, outputPath, "ultrafast")
	if err != nil {
		t.Fatalf("GenerateMP3FromMP4() error = %v", err)
	}

	// Verify output exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Errorf("GenerateMP3FromMP4() output file was not created: %s", outputPath)
	}

	// Clean up
	os.Remove(outputPath)
}

func TestAudioUtils_GenerateAACFromMP4(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	testVideo := findTestAsset("2023_04_15_19_00_49.mp4")
	if testVideo == "" {
		t.Skip("Test video not found, skipping test")
		return
	}

	au := NewAudioUtils()
	outputDir := "test"
	outputPath := filepath.Join(outputDir, "test_generate_aac_from_mp4.aac")

	// Create output directory if it doesn't exist
	os.MkdirAll(outputDir, 0755)

	// Clean up if exists
	os.Remove(outputPath)

	err := au.GenerateAACFromMP4(testVideo, outputPath, "ultrafast")
	if err != nil {
		t.Fatalf("GenerateAACFromMP4() error = %v", err)
	}

	// Verify output exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Errorf("GenerateAACFromMP4() output file was not created: %s", outputPath)
	}

	// Clean up
	os.Remove(outputPath)
}

func TestAudioUtils_ConcatenateAudios(t *testing.T) {
	if !checkFFmpeg(t) {
		return
	}

	audio1 := findTestAsset("audio_1.aac")
	audio2 := findTestAsset("audio_2.aac")
	if audio1 == "" || audio2 == "" {
		t.Skip("Test audio files not found, skipping test")
		return
	}

	au := NewAudioUtils()
	outputDir := "test"
	outputName := "test_concatenate_audios.aac"
	outputPath := filepath.Join(outputDir, outputName)

	// Create output directory if it doesn't exist
	os.MkdirAll(outputDir, 0755)

	// Clean up if exists
	os.Remove(outputPath)

	// Concatenate two audio files (5 + 10 = 15 seconds)
	audios := []string{audio1, audio2}
	_, err := au.ConcatenateAudios(audios, outputDir, outputName)
	if err != nil {
		t.Fatalf("ConcatenateAudios() error = %v", err)
	}

	// Verify output exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		t.Errorf("ConcatenateAudios() output file was not created: %s", outputPath)
	}

	// Verify duration is approximately 15 seconds
	duration, err := au.GetAudioDuration(outputPath)
	if err != nil {
		t.Logf("Warning: Could not verify duration: %v", err)
	} else if duration != 15 {
		t.Errorf("ConcatenateAudios() duration = %d, want 15", duration)
	}

	// Clean up
	os.Remove(outputPath)
}
