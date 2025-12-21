package utils

import (
	"fmt"
	"time"
)

// TimeUtils provides time-related utility functions
type TimeUtils struct{}

// GetCurrentDate returns the current date in YYYY_MM_DD format
func (t *TimeUtils) GetCurrentDate() string {
	return time.Now().Format("2006_01_02")
}

// GetCurrentTimestamp returns the current timestamp in YYYY_MM_DD_HH_MM_SS format
func (t *TimeUtils) GetCurrentTimestamp() string {
	return time.Now().Format("2006_01_02_15_04_05")
}

// ConvertSecondsToDuration converts seconds to H:MM:SS format
func (t *TimeUtils) ConvertSecondsToDuration(seconds int) string {
	duration := time.Duration(seconds) * time.Second
	hours := int(duration.Hours())
	minutes := int(duration.Minutes()) % 60
	secs := int(duration.Seconds()) % 60
	return fmt.Sprintf("%d:%02d:%02d", hours, minutes, secs)
}

// ConvertDurationToSeconds converts H:MM:SS format to seconds
func (t *TimeUtils) ConvertDurationToSeconds(duration string) (int, error) {
	var hours, minutes, seconds int
	_, err := fmt.Sscanf(duration, "%d:%d:%d", &hours, &minutes, &seconds)
	if err != nil {
		return 0, err
	}
	return hours*3600 + minutes*60 + seconds, nil
}
