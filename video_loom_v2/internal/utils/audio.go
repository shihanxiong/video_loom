package utils

import (
	"encoding/json"
	"os/exec"
	"path/filepath"
	"strconv"
)

// AudioUtils provides audio processing utility functions
type AudioUtils struct {
	sysUtils *SysUtils
}

// NewAudioUtils creates a new AudioUtils instance
func NewAudioUtils() *AudioUtils {
	return &AudioUtils{
		sysUtils: &SysUtils{},
	}
}

// GenerateMP3FromMP4 generates MP3 preview from MP4
func (a *AudioUtils) GenerateMP3FromMP4(mp4Input, mp3Output, ffmpegPresetValue string) error {
	cmd := exec.Command("ffmpeg",
		"-i", mp4Input,
		"-vn",
		"-acodec", "mp3",
		"-preset", ffmpegPresetValue,
		mp3Output,
	)

	if a.sysUtils.IsWin32() {
		SetSysProcAttr(cmd)
	}

	return cmd.Run()
}

// GenerateAACFromMP4 extracts AAC audio from MP4
func (a *AudioUtils) GenerateAACFromMP4(mp4Input, aacOutput, ffmpegPresetValue string) error {
	cmd := exec.Command("ffmpeg",
		"-i", mp4Input,
		"-vn",
		"-acodec", "copy",
		"-shortest",
		"-preset", ffmpegPresetValue,
		aacOutput,
	)

	if a.sysUtils.IsWin32() {
		SetSysProcAttr(cmd)
	}

	return cmd.Run()
}

// GetAudioDuration returns the duration of the audio in seconds
func (a *AudioUtils) GetAudioDuration(audioPath string) (int, error) {
	cmd := exec.Command("ffprobe",
		"-v", "error",
		"-show_entries", "format=duration",
		"-of", "json",
		audioPath,
	)

	output, err := cmd.Output()
	if err != nil {
		return 0, err
	}

	var result struct {
		Format struct {
			Duration string `json:"duration"`
		} `json:"format"`
	}

	if err := json.Unmarshal(output, &result); err != nil {
		return 0, err
	}

	duration, err := strconv.ParseFloat(result.Format.Duration, 64)
	if err != nil {
		return 0, err
	}

	return int(duration), nil
}

// ConcatenateAudios concatenates multiple audio files
func (a *AudioUtils) ConcatenateAudios(audioPaths []string, outputDirectory, outputName string) (string, error) {
	outputFile := filepath.Join(outputDirectory, outputName)

	// Build filter string
	filterString := "concat:"
	for idx, audio := range audioPaths {
		if idx != 0 {
			filterString += "|"
		}
		filterString += audio
	}

	cmd := exec.Command("ffmpeg",
		"-i", filterString,
		"-c", "copy",
		outputFile,
	)

	if a.sysUtils.IsWin32() {
		SetSysProcAttr(cmd)
	}

	return outputFile, cmd.Run()
}
