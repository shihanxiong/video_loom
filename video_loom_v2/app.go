package main

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"time"

	"video_loom_v2/internal/utils"
)

// App struct
type App struct {
	ctx context.Context

	// State
	videoList      []string
	intro          string
	outro          string
	audioTrack     int
	ffmpegPreset   string
	timelineText   string
	status         string
	outputDir      string
	outputFileName string

	// Utils
	timeUtils     *utils.TimeUtils
	fileUtils     *utils.FileUtils
	sysUtils      *utils.SysUtils
	videoUtils    *utils.VideoUtils
	audioUtils    *utils.AudioUtils
	timelineUtils *utils.TimelineUtils

	// Mutex for thread safety
	mu sync.RWMutex
}

// ShowMessage shows a message (logs it for now, can be enhanced with UI notifications)
func (a *App) ShowMessage(title, message string, dialogType string) error {
	// For now, just update status. In a real implementation, you'd use a UI notification system
	a.SetStatus(fmt.Sprintf("%s: %s", title, message))
	return nil
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{
		videoList:     make([]string, 0),
		audioTrack:    1,
		ffmpegPreset:  "medium",
		outputDir:     ".",
		timeUtils:     &utils.TimeUtils{},
		fileUtils:     &utils.FileUtils{},
		sysUtils:      &utils.SysUtils{},
		videoUtils:    utils.NewVideoUtils(),
		audioUtils:    utils.NewAudioUtils(),
		timelineUtils: utils.NewTimelineUtils(),
		status:        "ready",
	}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	a.outputDir, _ = os.Getwd()
}

// GetVersion returns the application version
func (a *App) GetVersion() string {
	changelogPath := filepath.Join(a.outputDir, "..", "changelog.md")
	return a.fileUtils.GetLatestVersionFromChangelog(changelogPath)
}

// GetStatus returns the current status
func (a *App) GetStatus() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.status
}

// SetStatus sets the current status
func (a *App) SetStatus(status string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.status = status
}

// GetVideoList returns the list of imported videos
func (a *App) GetVideoList() []string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.videoList
}

// AddVideos adds videos to the list (max 4)
func (a *App) AddVideos(videoPaths []string) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	if len(a.videoList)+len(videoPaths) > 4 {
		return fmt.Errorf("maximum 4 videos allowed")
	}

	for _, path := range videoPaths {
		if _, err := os.Stat(path); err != nil {
			return fmt.Errorf("video file not found: %s", path)
		}
		a.videoList = append(a.videoList, path)
	}

	return nil
}

// RemoveVideo removes a video from the list
func (a *App) RemoveVideo(index int) error {
	a.mu.Lock()
	defer a.mu.Unlock()

	if index < 0 || index >= len(a.videoList) {
		return fmt.Errorf("invalid video index")
	}

	a.videoList = append(a.videoList[:index], a.videoList[index+1:]...)
	return nil
}

// ClearVideoList clears all videos
func (a *App) ClearVideoList() {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.videoList = make([]string, 0)
	a.intro = ""
	a.outro = ""
}

// SetIntro sets the intro video path
func (a *App) SetIntro(introPath string) error {
	if introPath != "" {
		if _, err := os.Stat(introPath); err != nil {
			return fmt.Errorf("intro file not found: %s", introPath)
		}
	}
	a.mu.Lock()
	defer a.mu.Unlock()
	a.intro = introPath
	return nil
}

// GetIntro returns the intro video path
func (a *App) GetIntro() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.intro
}

// SetOutro sets the outro video path
func (a *App) SetOutro(outroPath string) error {
	if outroPath != "" {
		if _, err := os.Stat(outroPath); err != nil {
			return fmt.Errorf("outro file not found: %s", outroPath)
		}
	}
	a.mu.Lock()
	defer a.mu.Unlock()
	a.outro = outroPath
	return nil
}

// GetOutro returns the outro video path
func (a *App) GetOutro() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.outro
}

// SetAudioTrack sets the selected audio track
func (a *App) SetAudioTrack(track int) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.audioTrack = track
}

// GetAudioTrack returns the selected audio track
func (a *App) GetAudioTrack() int {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.audioTrack
}

// SetFFmpegPreset sets the FFmpeg preset
func (a *App) SetFFmpegPreset(preset string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.ffmpegPreset = preset
}

// GetFFmpegPreset returns the FFmpeg preset
func (a *App) GetFFmpegPreset() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.ffmpegPreset
}

// SetTimeline sets the timeline text
func (a *App) SetTimeline(timeline string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.timelineText = timeline
}

// GetTimeline returns the timeline text
func (a *App) GetTimeline() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.timelineText
}

// GetVideoInfo returns video information (duration, resolution)
func (a *App) GetVideoInfo(videoPath string) (map[string]interface{}, error) {
	duration, err := a.videoUtils.GetVideoDuration(videoPath)
	if err != nil {
		return nil, err
	}

	width, height, err := a.videoUtils.GetVideoResolution(videoPath)
	if err != nil {
		return nil, err
	}

	return map[string]interface{}{
		"duration": duration,
		"width":    width,
		"height":   height,
	}, nil
}

// GetVideoDurations returns durations for all imported videos
func (a *App) GetVideoDurations() (map[int]int, error) {
	a.mu.RLock()
	defer a.mu.RUnlock()

	durations := make(map[int]int)
	for i, video := range a.videoList {
		duration, err := a.videoUtils.GetVideoDuration(video)
		if err != nil {
			return nil, err
		}
		durations[i+1] = duration
	}

	return durations, nil
}

// ValidateTimeline validates the timeline
func (a *App) ValidateTimeline() error {
	a.mu.RLock()
	timelineText := a.timelineText
	a.mu.RUnlock()

	if timelineText == "" {
		return fmt.Errorf("timeline cannot be empty")
	}

	durations, err := a.GetVideoDurations()
	if err != nil {
		return err
	}

	return a.timelineUtils.ValidateTimeline(timelineText, durations)
}

// GenerateRandomSegments generates random timeline segments
func (a *App) GenerateRandomSegments(numSegments, minPerSegment, numVideos int) (string, error) {
	if numVideos < 1 || numVideos > 4 {
		return "", fmt.Errorf("number of videos must be between 1 and 4")
	}
	return a.timelineUtils.GenerateRandomSegments(numSegments, minPerSegment, numVideos), nil
}

// GenerateYouTubeTimestamp generates YouTube timestamp format
func (a *App) GenerateYouTubeTimestamp(labels []string) (string, error) {
	a.mu.RLock()
	timelineText := a.timelineText
	intro := a.intro
	a.mu.RUnlock()

	var offset *int
	if intro != "" {
		duration, err := a.videoUtils.GetVideoDuration(intro)
		if err == nil {
			offset = &duration
		}
	}

	return a.timelineUtils.GenerateYouTubeTimestamp(timelineText, labels, offset)
}

// GenerateAudioPreview generates MP3 preview from selected video
func (a *App) GenerateAudioPreview() (string, error) {
	a.mu.RLock()
	videoList := a.videoList
	audioTrack := a.audioTrack
	a.mu.RUnlock()

	if len(videoList) == 0 {
		return "", fmt.Errorf("no videos imported")
	}

	if audioTrack < 1 || audioTrack > len(videoList) {
		return "", fmt.Errorf("invalid audio track")
	}

	videoInput := videoList[audioTrack-1]
	audioPreviewOutput := fmt.Sprintf("audio_preview_%d.mp3", audioTrack)

	a.SetStatus("Generating audio preview, please wait...")
	err := a.audioUtils.GenerateMP3FromMP4(videoInput, audioPreviewOutput, "ultrafast")
	if err != nil {
		a.SetStatus("Error generating audio preview")
		return "", err
	}

	a.SetStatus(fmt.Sprintf("Audio preview generated for audio track %d", audioTrack))
	return audioPreviewOutput, nil
}

// RemoveAudioPreview removes the audio preview file
func (a *App) RemoveAudioPreview() error {
	a.mu.RLock()
	audioTrack := a.audioTrack
	a.mu.RUnlock()

	audioPreviewFile := fmt.Sprintf("audio_preview_%d.mp3", audioTrack)
	err := os.Remove(audioPreviewFile)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	a.SetStatus(fmt.Sprintf("Audio preview deleted for audio track %d", audioTrack))
	return nil
}

// HasAudioPreview checks if audio preview exists
func (a *App) HasAudioPreview() bool {
	a.mu.RLock()
	audioTrack := a.audioTrack
	a.mu.RUnlock()

	audioPreviewFile := fmt.Sprintf("audio_preview_%d.mp3", audioTrack)
	_, err := os.Stat(audioPreviewFile)
	return err == nil
}

// GenerateVideo generates the final video
func (a *App) GenerateVideo() error {
	a.mu.RLock()
	videoList := a.videoList
	timelineText := a.timelineText
	audioTrack := a.audioTrack
	ffmpegPreset := a.ffmpegPreset
	intro := a.intro
	outro := a.outro
	outputDir := a.outputDir
	a.mu.RUnlock()

	if len(videoList) == 0 {
		return fmt.Errorf("no videos imported")
	}

	if timelineText == "" {
		return fmt.Errorf("timeline cannot be empty")
	}

	startTime := time.Now()
	a.SetStatus("Starting video processing...")

	// Clean up temp files
	a.fileUtils.CleanUpTempFiles()

	// Calculate output resolution
	maxWidth, maxHeight := 0, 0
	for _, video := range videoList {
		width, height, err := a.videoUtils.GetVideoResolution(video)
		if err != nil {
			return err
		}
		if width > maxWidth {
			maxWidth = width
		}
		if height > maxHeight {
			maxHeight = height
		}
	}

	a.SetStatus(fmt.Sprintf("Output resolution determined at %d x %d", maxWidth, maxHeight))

	// Get video durations
	durations, err := a.GetVideoDurations()
	if err != nil {
		return err
	}

	// Validate timeline
	if err := a.timelineUtils.ValidateTimeline(timelineText, durations); err != nil {
		a.SetStatus(fmt.Sprintf("Timeline validation error: %s", err.Error()))
		return err
	}

	a.SetStatus("Timeline validated")

	// Parse timeline
	segments, err := a.timelineUtils.ParseTimeline(timelineText)
	if err != nil {
		return err
	}

	// Trim videos
	trimmedVideos := make([]string, 0)
	for idx, segment := range segments {
		trimmedOutput := filepath.Join(outputDir, fmt.Sprintf("trimmed_%d.mp4", idx))
		videoIndex := segment.Video - 1
		if videoIndex < 0 || videoIndex >= len(videoList) {
			return fmt.Errorf("invalid video number in timeline: %d", segment.Video)
		}

		err := a.videoUtils.TrimMP4ByTimestamp(
			videoList[videoIndex],
			segment.Start,
			segment.End,
			maxWidth,
			maxHeight,
			ffmpegPreset,
			trimmedOutput,
		)
		if err != nil {
			return fmt.Errorf("error trimming video: %w", err)
		}
		trimmedVideos = append(trimmedVideos, trimmedOutput)
	}

	a.SetStatus("Completed trimming videos")

	// Concatenate videos (if more than one segment)
	var outputFile string
	if len(trimmedVideos) > 1 {
		outputFile, err = a.videoUtils.ConcatenateVideos(trimmedVideos, outputDir, "output.mp4", ffmpegPreset)
		if err != nil {
			return fmt.Errorf("error concatenating videos: %w", err)
		}
		a.SetStatus("Completed concatenating trimmed videos")
	} else if len(trimmedVideos) == 1 {
		outputFile = trimmedVideos[0]
	} else {
		return fmt.Errorf("no video segments to process")
	}

	// Process audio
	outputSound := filepath.Join(outputDir, "audio.aac")
	videoInput := videoList[audioTrack-1]
	err = a.audioUtils.GenerateAACFromMP4(videoInput, outputSound, ffmpegPreset)
	if err != nil {
		return fmt.Errorf("error processing audio: %w", err)
	}
	a.SetStatus(fmt.Sprintf("Completed processing audio from video %d", audioTrack))

	// Combine video and audio
	outputFileName := fmt.Sprintf("%s.mp4", a.timeUtils.GetCurrentTimestamp())
	finalFile, err := a.videoUtils.CombineMP4AACToMP4(outputFile, outputSound, outputDir, outputFileName, ffmpegPreset)
	if err != nil {
		return fmt.Errorf("error combining video and audio: %w", err)
	}
	a.SetStatus("Video is processed and ready for use")

	// Add intro and outro if present
	if intro != "" || outro != "" {
		videos := make([]string, 0)
		if intro != "" {
			videos = append(videos, intro)
		}
		videos = append(videos, finalFile)
		if outro != "" {
			videos = append(videos, outro)
		}

		if len(videos) > 1 {
			finalOutputName := fmt.Sprintf("%s_with_intro_outro.mp4", a.timeUtils.GetCurrentTimestamp())
			_, err = a.videoUtils.ConcatenateVideos(videos, outputDir, finalOutputName, ffmpegPreset)
			if err != nil {
				return fmt.Errorf("error adding intro/outro: %w", err)
			}
		}
	}

	elapsed := time.Since(startTime)
	a.SetStatus(fmt.Sprintf("Video is ready! Took %.2f seconds", elapsed.Seconds()))

	return nil
}

// SetOutputDirectory sets the output directory
func (a *App) SetOutputDirectory(dir string) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.outputDir = dir
}

// GetOutputDirectory returns the output directory
func (a *App) GetOutputDirectory() string {
	a.mu.RLock()
	defer a.mu.RUnlock()
	return a.outputDir
}
