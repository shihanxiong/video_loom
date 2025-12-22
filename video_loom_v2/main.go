package main

import (
	"embed"
	"fmt"
	"net/http"
	"os"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	// Create an instance of the app structure
	app := NewApp()

	// Create application with options
	version := app.GetVersion()

	// Create custom handler for serving video files
	videoHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Extract file path from query parameter
		filePath := r.URL.Query().Get("path")
		if filePath == "" {
			http.Error(w, "Missing path parameter", http.StatusBadRequest)
			return
		}

		// Security: verify the file exists and is accessible
		if _, err := os.Stat(filePath); os.IsNotExist(err) {
			http.Error(w, "File not found", http.StatusNotFound)
			return
		}

		// Set appropriate headers for video streaming
		w.Header().Set("Content-Type", "video/mp4")
		w.Header().Set("Accept-Ranges", "bytes")

		// Serve the file
		http.ServeFile(w, r, filePath)
	})

	err := wails.Run(&options.App{
		Title:  fmt.Sprintf("Video Loom - %s", version),
		Width:  1200,
		Height: 1100,
		AssetServer: &assetserver.Options{
			Assets: assets,
			Middleware: func(next http.Handler) http.Handler {
				return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
					// Handle video file requests
					if r.URL.Path == "/video" {
						videoHandler.ServeHTTP(w, r)
						return
					}
					next.ServeHTTP(w, r)
				})
			},
		},
		BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
		},
	})

	if err != nil {
		println("Error:", err.Error())
	}
}
