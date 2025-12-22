package utils

import (
	"testing"
	"time"
)

func TestTimeUtils_GetCurrentTimestamp(t *testing.T) {
	tu := &TimeUtils{}
	timestamp := tu.GetCurrentTimestamp()

	// Verify format: YYYY_MM_DD_HH_MM_SS
	if len(timestamp) != 19 {
		t.Errorf("Expected timestamp length 19, got %d: %s", len(timestamp), timestamp)
	}

	// Verify it can be parsed
	_, err := time.Parse("2006_01_02_15_04_05", timestamp)
	if err != nil {
		t.Errorf("Failed to parse timestamp %s: %v", timestamp, err)
	}
}

func TestTimeUtils_GetCurrentDate(t *testing.T) {
	tu := &TimeUtils{}
	date := tu.GetCurrentDate()

	// Verify format: YYYY_MM_DD
	if len(date) != 10 {
		t.Errorf("Expected date length 10, got %d: %s", len(date), date)
	}

	// Verify it can be parsed
	_, err := time.Parse("2006_01_02", date)
	if err != nil {
		t.Errorf("Failed to parse date %s: %v", date, err)
	}
}

func TestTimeUtils_ConvertSecondsToDuration(t *testing.T) {
	tu := &TimeUtils{}

	tests := []struct {
		seconds  int
		expected string
	}{
		{15, "0:00:15"},
		{3601, "1:00:01"},
		{0, "0:00:00"},
		{3661, "1:01:01"},
		{7200, "2:00:00"},
	}

	for _, tt := range tests {
		result := tu.ConvertSecondsToDuration(tt.seconds)
		if result != tt.expected {
			t.Errorf("ConvertSecondsToDuration(%d) = %s, want %s", tt.seconds, result, tt.expected)
		}
	}
}

func TestTimeUtils_ConvertDurationToSeconds(t *testing.T) {
	tu := &TimeUtils{}

	tests := []struct {
		duration string
		expected int
		wantErr  bool
	}{
		{"0:01:15", 75, false},
		{"1:00:01", 3601, false},
		{"0:00:00", 0, false},
		{"2:30:45", 9045, false},
		{"invalid", 0, true},
		{"1:2:3", 3723, false}, // Should handle single digits
	}

	for _, tt := range tests {
		result, err := tu.ConvertDurationToSeconds(tt.duration)
		if (err != nil) != tt.wantErr {
			t.Errorf("ConvertDurationToSeconds(%s) error = %v, wantErr %v", tt.duration, err, tt.wantErr)
			continue
		}
		if !tt.wantErr && result != tt.expected {
			t.Errorf("ConvertDurationToSeconds(%s) = %d, want %d", tt.duration, result, tt.expected)
		}
	}
}
