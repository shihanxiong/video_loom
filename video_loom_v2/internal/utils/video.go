package utils

import (
	"encoding/json"
	"fmt"
	"os/exec"
	"strconv"
	"strings"
)

// VideoUtils provides video processing utility functions
type VideoUtils struct {
	sysUtils *SysUtils
}

// NewVideoUtils creates a new VideoUtils instance
func NewVideoUtils() *VideoUtils {
	return &VideoUtils{
		sysUtils: &SysUtils{},
	}
}

// VideoInfo contains video metadata
type VideoInfo struct {
	Duration int `json:"duration"`
	Width    int `json:"width"`
	Height   int `json:"height"`
}

// GetVideoDuration returns the duration of the video in seconds
func (v *VideoUtils) GetVideoDuration(videoPath string) (int, error) {
	cmd := exec.Command("ffprobe",
		"-v", "error",
		"-show_entries", "format=duration",
		"-of", "json",
		videoPath,
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

// GetVideoResolution returns the width and height of the video
func (v *VideoUtils) GetVideoResolution(videoPath string) (int, int, error) {
	cmd := exec.Command("ffprobe",
		"-v", "error",
		"-show_entries", "stream=width,height",
		"-of", "csv=p=0",
		videoPath,
	)

	output, err := cmd.Output()
	if err != nil {
		return 0, 0, err
	}

	parts := strings.Split(strings.TrimSpace(string(output)), ",")
	if len(parts) != 2 {
		return 0, 0, fmt.Errorf("invalid resolution format")
	}

	width, err := strconv.Atoi(strings.TrimSpace(parts[0]))
	if err != nil {
		return 0, 0, err
	}

	height, err := strconv.Atoi(strings.TrimSpace(parts[1]))
	if err != nil {
		return 0, 0, err
	}

	return width, height, nil
}

// GetFFmpegPresetValueForNVENC translates CPU presets to NVENC presets
func (v *VideoUtils) GetFFmpegPresetValueForNVENC(ffmpegPresetValue string) string {
	fastPresets := []string{"ultrafast", "superfast", "veryfast", "faster", "fast"}
	slowPresets := []string{"slow", "slower", "veryslow"}

	for _, preset := range fastPresets {
		if ffmpegPresetValue == preset {
			return "fast"
		}
	}

	for _, preset := range slowPresets {
		if ffmpegPresetValue == preset {
			return "slow"
		}
	}

	return "medium"
}

// TrimMP4ByTimestamp trims a video segment with scaling
func (v *VideoUtils) TrimMP4ByTimestamp(videoPath, startTime, endTime string, outputWidth, outputHeight int, ffmpegPresetValue, outputFile string) error {
	var cmd *exec.Cmd

	if v.sysUtils.IsWin32() {
		// Windows GPU-accelerated
		nvencPreset := v.GetFFmpegPresetValueForNVENC(ffmpegPresetValue)
		cmd = exec.Command("ffmpeg",
			"-hwaccel", "cuvid",
			"-c:v", "h264_cuvid",
			"-i", videoPath,
			"-c:v", "h264_nvenc",
			"-ss", startTime,
			"-to", endTime,
			"-vf", fmt.Sprintf("scale_cuda=%d:%d", outputWidth, outputHeight),
			"-c:a", "copy",
			"-preset", nvencPreset,
			outputFile,
		)
	} else {
		// macOS/Linux CPU
		cmd = exec.Command("ffmpeg",
			"-i", videoPath,
			"-ss", startTime,
			"-to", endTime,
			"-vf", fmt.Sprintf("scale=%d:%d", outputWidth, outputHeight),
			"-c:a", "copy",
			"-preset", ffmpegPresetValue,
			outputFile,
		)
	}

	// Hide console window on Windows
	if v.sysUtils.IsWin32() {
		SetSysProcAttr(cmd)
	}

	return cmd.Run()
}

// ConcatenateVideos concatenates multiple videos
func (v *VideoUtils) ConcatenateVideos(videoPaths []string, outputDirectory, outputName, ffmpegPresetValue string) (string, error) {
	outputFile := fmt.Sprintf("%s/%s", outputDirectory, outputName)

	cmd := exec.Command("ffmpeg")
	for _, video := range videoPaths {
		cmd.Args = append(cmd.Args, "-i", video)
	}

	cmd.Args = append(cmd.Args,
		"-filter_complex", fmt.Sprintf("concat=n=%d:v=1:a=1", len(videoPaths)),
		"-c:v", "libx264",
		"-c:a", "aac",
		"-preset", ffmpegPresetValue,
		"-vsync", "2",
		outputFile,
	)

	if v.sysUtils.IsWin32() {
		SetSysProcAttr(cmd)
	}

	return outputFile, cmd.Run()
}

// CombineMP4AACToMP4 combines video and audio streams
func (v *VideoUtils) CombineMP4AACToMP4(sourceVideo, sourceAudio, outputDirectory, outputFile, ffmpegPresetValue string) (string, error) {
	outputFilePath := fmt.Sprintf("%s/%s", outputDirectory, outputFile)

	cmd := exec.Command("ffmpeg",
		"-i", sourceVideo,
		"-i", sourceAudio,
		"-c:v", "copy",
		"-map", "0:v",
		"-map", "1:a",
		"-shortest",
		"-preset", ffmpegPresetValue,
		outputFilePath,
	)

	if v.sysUtils.IsWin32() {
		SetSysProcAttr(cmd)
	}

	return outputFilePath, cmd.Run()
}
