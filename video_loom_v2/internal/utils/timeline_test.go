package utils

import (
	"strings"
	"testing"
)

func TestTimelineUtils_ParseTimeline(t *testing.T) {
	tu := NewTimelineUtils()

	tests := []struct {
		name     string
		input    string
		expected []TimelineSegment
		wantErr  bool
	}{
		{
			name:  "valid timeline",
			input: "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n3,0:00:10,0:00:15",
			expected: []TimelineSegment{
				{Video: 1, Start: "0:00:01", End: "0:00:05"},
				{Video: 2, Start: "0:00:05", End: "0:00:10"},
				{Video: 3, Start: "0:00:10", End: "0:00:15"},
			},
			wantErr: false,
		},
		{
			name:  "with leading/trailing spaces",
			input: " 1,0:00:01,0:00:05\n2,0:00:05,0:00:10 \n3,0:00:10,0:00:15",
			expected: []TimelineSegment{
				{Video: 1, Start: "0:00:01", End: "0:00:05"},
				{Video: 2, Start: "0:00:05", End: "0:00:10"},
				{Video: 3, Start: "0:00:10", End: "0:00:15"},
			},
			wantErr: false,
		},
		{
			name:  "with spaces in middle",
			input: "1,0:00:01, 0:00:05\n2,0:00:05, 0:00:10\n3,0:00:10,0:00:15",
			expected: []TimelineSegment{
				{Video: 1, Start: "0:00:01", End: "0:00:05"},
				{Video: 2, Start: "0:00:05", End: "0:00:10"},
				{Video: 3, Start: "0:00:10", End: "0:00:15"},
			},
			wantErr: false,
		},
		{
			name:  "with extra empty lines",
			input: "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n\n3,0:00:10,0:00:15\n\n\n",
			expected: []TimelineSegment{
				{Video: 1, Start: "0:00:01", End: "0:00:05"},
				{Video: 2, Start: "0:00:05", End: "0:00:10"},
				{Video: 3, Start: "0:00:10", End: "0:00:15"},
			},
			wantErr: false,
		},
		{
			name:    "invalid format - missing value",
			input:   "1,0:00:01,0:00:05\n2,0:00:10\n3,0:00:10,0:00:15",
			wantErr: true,
		},
		{
			name:    "invalid format - extra value",
			input:   "1,0:00:01,0:00:05,extra",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := tu.ParseTimeline(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParseTimeline() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if len(result) != len(tt.expected) {
					t.Errorf("ParseTimeline() length = %d, want %d", len(result), len(tt.expected))
					return
				}
				for i, seg := range result {
					if seg.Video != tt.expected[i].Video || seg.Start != tt.expected[i].Start || seg.End != tt.expected[i].End {
						t.Errorf("ParseTimeline() segment[%d] = %+v, want %+v", i, seg, tt.expected[i])
					}
				}
			}
		})
	}
}

func TestTimelineUtils_ValidateTimeline(t *testing.T) {
	tu := NewTimelineUtils()
	videoDurations := map[int]int{1: 100, 2: 200, 3: 300}

	tests := []struct {
		name        string
		timeline    string
		expectedErr string
	}{
		{
			name:        "empty timeline",
			timeline:    " \n \n\n   \n\n\n",
			expectedErr: "invalid timeline - timeline cannot be empty",
		},
		{
			name:        "missing timestamp",
			timeline:    "1,0:00:01,0:00:05\n2,0:00:10\n3,0:00:10,0:00:15",
			expectedErr: "invalid timeline format",
		},
		{
			name:        "start time after end time",
			timeline:    "1,0:00:01,0:00:05\n2,0:00:10,0:00:09\n3,0:00:10,0:00:15",
			expectedErr: "invalid timeline - start time is equal/after end time",
		},
		{
			name:        "start time equal to end time",
			timeline:    "1,0:00:01,0:00:05\n2,0:00:10,0:00:10\n3,0:00:10,0:00:15",
			expectedErr: "invalid timeline - start time is equal/after end time",
		},
		{
			name:        "end time exceeds video duration",
			timeline:    "1,0:00:01,0:00:05\n2,0:00:10,0:00:19\n3,0:00:10,0:05:15",
			expectedErr: "invalid timeline - end time exceeds video duration",
		},
		{
			name:        "valid timeline",
			timeline:    "1,0:00:01,0:00:05\n2,0:00:05,0:00:10\n3,0:00:10,0:00:15",
			expectedErr: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tu.ValidateTimeline(tt.timeline, videoDurations)
			if tt.expectedErr == "" {
				if err != nil {
					t.Errorf("ValidateTimeline() error = %v, want nil", err)
				}
			} else {
				if err == nil {
					t.Errorf("ValidateTimeline() error = nil, want error containing '%s'", tt.expectedErr)
				} else if !strings.Contains(err.Error(), tt.expectedErr) {
					t.Errorf("ValidateTimeline() error = %v, want error containing '%s'", err, tt.expectedErr)
				}
			}
		})
	}
}

func TestTimelineUtils_GenerateRandomSegments(t *testing.T) {
	tu := NewTimelineUtils()

	result := tu.GenerateRandomSegments(10, 3, 3)
	lines := strings.Split(strings.TrimSpace(result), "\n")

	if len(lines) != 10 {
		t.Errorf("GenerateRandomSegments() returned %d lines, want 10", len(lines))
	}

	// Verify that consecutive segments use different video numbers
	for i := 1; i < len(lines); i++ {
		parts1 := strings.Split(lines[i-1], ",")
		parts2 := strings.Split(lines[i], ",")
		if len(parts1) > 0 && len(parts2) > 0 {
			if parts1[0] == parts2[0] {
				t.Errorf("GenerateRandomSegments() consecutive segments have same video number: %s and %s", lines[i-1], lines[i])
			}
		}
	}
}

func TestTimelineUtils_GenerateYouTubeTimestamp(t *testing.T) {
	tu := NewTimelineUtils()

	timelineText := "1,0:00:01,0:00:05\n2,0:00:10,0:00:15\n3,0:00:15,0:00:20"
	labels := []string{"Dan", "Hank", "Lindsay"}

	// Test without offset
	result, err := tu.GenerateYouTubeTimestamp(timelineText, labels, nil)
	if err != nil {
		t.Fatalf("GenerateYouTubeTimestamp() error = %v", err)
	}

	expected := "0:00:01 Dan\n0:00:10 Hank\n0:00:15 Lindsay\n"
	if result != expected {
		t.Errorf("GenerateYouTubeTimestamp() = %q, want %q", result, expected)
	}

	// Test with offset
	offset := 1
	result, err = tu.GenerateYouTubeTimestamp(timelineText, labels, &offset)
	if err != nil {
		t.Fatalf("GenerateYouTubeTimestamp() error = %v", err)
	}

	expected = "0:00:00 Intro\n0:00:02 Dan\n0:00:11 Hank\n0:00:16 Lindsay\n"
	if result != expected {
		t.Errorf("GenerateYouTubeTimestamp() with offset = %q, want %q", result, expected)
	}
}
