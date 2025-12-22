package utils

import (
	"fmt"
	"math/rand"
	"strings"
)

// TimelineUtils provides timeline-related utility functions
type TimelineUtils struct {
	timeUtils *TimeUtils
}

// NewTimelineUtils creates a new TimelineUtils instance
func NewTimelineUtils() *TimelineUtils {
	return &TimelineUtils{
		timeUtils: &TimeUtils{},
	}
}

// TimelineSegment represents a single timeline segment
type TimelineSegment struct {
	Video int    `json:"video"`
	Start string `json:"start"`
	End   string `json:"end"`
}

// ParseTimeline parses timeline text into array of segments
func (t *TimelineUtils) ParseTimeline(timelineText string) ([]TimelineSegment, error) {
	var segments []TimelineSegment
	lines := strings.Split(timelineText, "\n")

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}

		parts := strings.Split(line, ",")
		if len(parts) != 3 {
			return nil, fmt.Errorf("invalid timeline format: expected 'video,start,end', got: %s", line)
		}

		var video int
		_, err := fmt.Sscanf(strings.TrimSpace(parts[0]), "%d", &video)
		if err != nil {
			return nil, fmt.Errorf("invalid video number: %s", parts[0])
		}

		segments = append(segments, TimelineSegment{
			Video: video,
			Start: strings.TrimSpace(parts[1]),
			End:   strings.TrimSpace(parts[2]),
		})
	}

	return segments, nil
}

// ValidateTimeline validates timeline format and bounds
func (t *TimelineUtils) ValidateTimeline(timelineText string, videoDurations map[int]int) error {
	trimmed := strings.TrimSpace(timelineText)
	trimmed = strings.ReplaceAll(trimmed, "\n", "")
	trimmed = strings.ReplaceAll(trimmed, "\t", "")
	trimmed = strings.ReplaceAll(trimmed, " ", "")

	if trimmed == "" {
		return fmt.Errorf("invalid timeline - timeline cannot be empty")
	}

	segments, err := t.ParseTimeline(timelineText)
	if err != nil {
		return err
	}

	for _, segment := range segments {
		startSeconds, err := t.timeUtils.ConvertDurationToSeconds(segment.Start)
		if err != nil {
			return fmt.Errorf("invalid start time format: %s", segment.Start)
		}

		endSeconds, err := t.timeUtils.ConvertDurationToSeconds(segment.End)
		if err != nil {
			return fmt.Errorf("invalid end time format: %s", segment.End)
		}

		if startSeconds >= endSeconds {
			return fmt.Errorf("invalid timeline - start time is equal/after end time")
		}

		if duration, exists := videoDurations[segment.Video]; exists {
			if endSeconds > duration {
				return fmt.Errorf("invalid timeline - end time exceeds video duration")
			}
		} else {
			return fmt.Errorf("invalid timeline - video %d not found", segment.Video)
		}
	}

	return nil
}

// GenerateRandomSegments generates random timeline segments
func (t *TimelineUtils) GenerateRandomSegments(numSegments, minPerSegment, numVideos int) string {
	var result strings.Builder
	prev := 0
	start := "0:00:00"

	for i := 0; i < numSegments; i++ {
		nextVideoNum := t.generateNextVideoNum(numVideos, prev)
		marginInSec := rand.Intn(61) - 30 // -30 to 30 seconds
		totalSeconds := (i*minPerSegment)*60 + minPerSegment*60 + marginInSec
		end := t.timeUtils.ConvertSecondsToDuration(totalSeconds)

		result.WriteString(fmt.Sprintf("%d,%s,%s\n", nextVideoNum, start, end))

		prev = nextVideoNum
		start = end
	}

	return result.String()
}

func (t *TimelineUtils) generateNextVideoNum(numVideos, prev int) int {
	num := rand.Intn(numVideos) + 1
	if num == prev {
		return t.generateNextVideoNum(numVideos, prev)
	}
	return num
}

// GenerateYouTubeTimestamp converts timeline to YouTube format
func (t *TimelineUtils) GenerateYouTubeTimestamp(timelineText string, labels []string, offset *int) (string, error) {
	segments, err := t.ParseTimeline(timelineText)
	if err != nil {
		return "", err
	}

	var result strings.Builder

	if offset != nil && *offset > 0 {
		result.WriteString("0:00:00 Intro\n")
	}

	for _, segment := range segments {
		if segment.Video < 1 || segment.Video > len(labels) {
			continue
		}
		label := labels[segment.Video-1]

		time := segment.Start
		if offset != nil {
			startSeconds, err := t.timeUtils.ConvertDurationToSeconds(segment.Start)
			if err != nil {
				continue
			}
			time = t.timeUtils.ConvertSecondsToDuration(startSeconds + *offset)
		}

		result.WriteString(fmt.Sprintf("%s %s\n", time, label))
	}

	return result.String(), nil
}
