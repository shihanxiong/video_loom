import {
  AddVideos,
  ClearVideoList,
  GenerateAudioPreview,
  GenerateRandomSegments,
  GenerateVideo,
  GenerateYouTubeTimestamp,
  GetAudioTrack,
  GetFFmpegPreset,
  GetIntro,
  GetOutro,
  GetStatus,
  GetTimeline,
  GetVersion,
  GetVideoList,
  HasAudioPreview,
  RemoveAudioPreview,
  RemoveVideo,
  SetAudioTrack,
  SetFFmpegPreset,
  SetIntro,
  SetOutro,
  SetStatus,
  SetTimeline,
  ShowMessage,
  ValidateTimeline,
} from '../wailsjs/go/main/App';
// Note: File path resolution will be handled by the backend

export class App {
  private videoList: string[] = [];
  private videoPlayers: HTMLVideoElement[] = [];
  private isPlaying: boolean = false;
  private currentTime: number = 0;
  private maxDuration: number = 0;
  private audioTrack: number = 1;
  private ffmpegPreset: string = 'medium';
  private statusUpdateInterval: number | null = null;

  async init() {
    await this.loadState();
    this.setupUI();
    this.setupEventListeners();
    this.startStatusUpdates();
  }

  private async loadState() {
    try {
      this.videoList = await GetVideoList();
      this.audioTrack = await GetAudioTrack();
      this.ffmpegPreset = await GetFFmpegPreset();
      const timeline = await GetTimeline();
      const version = await GetVersion();

      document.title = `Video Loom - ${version}`;
      const timelineTextarea = document.getElementById('timeline-text') as HTMLTextAreaElement;
      if (timelineTextarea) {
        timelineTextarea.value = timeline;
      }
    } catch (error) {
      console.error('Error loading state:', error);
    }
  }

  private setupUI() {
    const app = document.getElementById('app');
    if (!app) return;

    app.innerHTML = `
            <div class="app-container">
                <header class="app-header">
                    <h1>Video Loom</h1>
                    <div class="version" id="version"></div>
                </header>

                <div class="main-content">
                    <!-- Video Import Section -->
                    <section class="section video-import-section">
                        <div class="button-group">
                            <button id="import-videos-btn" class="btn btn-primary">Import Videos</button>
                            <button id="view-video-list-btn" class="btn btn-secondary">View Video List (0 of 4)</button>
                            <button id="play-pause-btn" class="btn btn-primary" disabled>Play All Videos</button>
                        </div>
                    </section>

                    <!-- Intro/Outro Section -->
                    <section class="section intro-outro-section">
                        <div class="button-group">
                            <button id="import-intro-btn" class="btn btn-secondary">Add Intro</button>
                            <button id="import-outro-btn" class="btn btn-secondary">Add Outro</button>
                        </div>
                    </section>

                    <!-- Video Preview Section -->
                    <section class="section video-preview-section">
                        <div id="video-container" class="video-container"></div>
                    </section>

                    <!-- Video Controls Section -->
                    <section class="section video-controls-section">
                        <div class="controls-row">
                            <button id="skip-minus-30" class="btn btn-small">-30s</button>
                            <button id="skip-minus-10" class="btn btn-small">-10s</button>
                            <button id="skip-minus-5" class="btn btn-small">-5s</button>
                            <div class="time-display">
                                <span id="current-time">0:00:00</span>
                                <input type="range" id="progress-slider" class="progress-slider" min="0" max="0" value="0">
                                <span id="total-time">0:00:00</span>
                            </div>
                            <button id="skip-plus-5" class="btn btn-small">+5s</button>
                            <button id="skip-plus-10" class="btn btn-small">+10s</button>
                            <button id="skip-plus-30" class="btn btn-small">+30s</button>
                            <button id="copy-timestamp-btn" class="btn btn-small">Copy Timestamp</button>
                        </div>
                    </section>

                    <!-- Settings Section -->
                    <section class="section settings-section">
                        <div class="settings-grid">
                            <div class="setting-group">
                                <label>Audio Track:</label>
                                <select id="audio-track-select" class="select">
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                </select>
                                <button id="generate-audio-preview-btn" class="btn btn-secondary">Generate Preview</button>
                                <button id="remove-audio-preview-btn" class="btn btn-secondary" disabled>Remove Preview</button>
                            </div>
                            <div class="setting-group">
                                <label>Process Speed:</label>
                                <select id="ffmpeg-preset-select" class="select">
                                    <option value="ultrafast">Ultrafast</option>
                                    <option value="superfast">Superfast</option>
                                    <option value="veryfast">Veryfast</option>
                                    <option value="faster">Faster</option>
                                    <option value="fast">Fast</option>
                                    <option value="medium" selected>Medium</option>
                                    <option value="slow">Slow</option>
                                    <option value="slower">Slower</option>
                                    <option value="veryslow">Veryslow</option>
                                </select>
                            </div>
                        </div>
                    </section>

                    <!-- Timeline Section -->
                    <section class="section timeline-section">
                        <label for="timeline-text">Timeline:</label>
                        <textarea id="timeline-text" class="timeline-textarea" rows="10" 
                                  placeholder="Format: video_number,start_time,end_time&#10;Example:&#10;1,0:00:00,0:10:00&#10;2,0:10:00,0:15:05"></textarea>
                        <div class="timeline-actions">
                            <button id="validate-timeline-btn" class="btn btn-secondary">Validate Timeline</button>
                            <button id="create-random-segments-btn" class="btn btn-secondary">Create Random Segments</button>
                            <button id="export-youtube-timestamp-btn" class="btn btn-secondary">Export YouTube Timestamp</button>
                        </div>
                    </section>

                    <!-- Status Section -->
                    <section class="section status-section">
                        <div class="status-display">
                            <strong>Status:</strong> <span id="status-text">ready</span>
                        </div>
                    </section>

                    <!-- Toolbar Section -->
                    <section class="section toolbar-section">
                        <div class="button-group">
                            <button id="generate-video-btn" class="btn btn-primary btn-large" disabled>Generate Video</button>
                            <button id="quit-btn" class="btn btn-secondary btn-large">Quit</button>
                        </div>
                    </section>
                </div>
            </div>

            <!-- Modals -->
            <div id="video-list-modal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>View Video List</h2>
                        <button class="modal-close" id="close-video-list-modal">&times;</button>
                    </div>
                    <div class="modal-body" id="video-list-content"></div>
                    <div class="modal-footer">
                        <button id="clear-video-list-btn" class="btn btn-danger">Clear Video List</button>
                        <button id="close-video-list-modal-btn" class="btn btn-secondary">Close</button>
                    </div>
                </div>
            </div>

            <div id="random-segments-modal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>Create Random Segments</h2>
                        <button class="modal-close" id="close-random-segments-modal">&times;</button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label>Number of videos:</label>
                            <input type="number" id="random-num-videos" min="1" max="4" value="4" class="input">
                        </div>
                        <div class="form-group">
                            <label>Number of segments:</label>
                            <input type="number" id="random-num-segments" min="1" value="5" class="input">
                        </div>
                        <div class="form-group">
                            <label>Minutes per segment:</label>
                            <input type="number" id="random-min-per-segment" min="1" value="2" class="input">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button id="confirm-random-segments-btn" class="btn btn-primary">Confirm</button>
                        <button id="cancel-random-segments-btn" class="btn btn-secondary">Cancel</button>
                    </div>
                </div>
            </div>

            <div id="youtube-timestamp-modal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>Export YouTube Timestamp</h2>
                        <button class="modal-close" id="close-youtube-timestamp-modal">&times;</button>
                    </div>
                    <div class="modal-body" id="youtube-labels-content"></div>
                    <div class="modal-footer">
                        <button id="copy-youtube-timestamp-btn" class="btn btn-primary">Copy to Clipboard</button>
                        <button id="cancel-youtube-timestamp-btn" class="btn btn-secondary">Cancel</button>
                    </div>
                </div>
            </div>
        `;

    this.updateUI();
  }

  private setupEventListeners() {
    // Video import
    document.getElementById('import-videos-btn')?.addEventListener('click', () => this.importVideos());
    document.getElementById('view-video-list-btn')?.addEventListener('click', () => this.showVideoListModal());
    document.getElementById('play-pause-btn')?.addEventListener('click', () => this.togglePlayPause());

    // Intro/Outro
    document.getElementById('import-intro-btn')?.addEventListener('click', () => this.importIntro());
    document.getElementById('import-outro-btn')?.addEventListener('click', () => this.importOutro());

    // Video controls
    document.getElementById('skip-minus-30')?.addEventListener('click', () => this.skip(-30));
    document.getElementById('skip-minus-10')?.addEventListener('click', () => this.skip(-10));
    document.getElementById('skip-minus-5')?.addEventListener('click', () => this.skip(-5));
    document.getElementById('skip-plus-5')?.addEventListener('click', () => this.skip(5));
    document.getElementById('skip-plus-10')?.addEventListener('click', () => this.skip(10));
    document.getElementById('skip-plus-30')?.addEventListener('click', () => this.skip(30));
    document.getElementById('copy-timestamp-btn')?.addEventListener('click', () => this.copyTimestamp());

    const progressSlider = document.getElementById('progress-slider') as HTMLInputElement;
    progressSlider?.addEventListener('input', (e) => {
      const value = parseInt((e.target as HTMLInputElement).value);
      this.seek(value);
    });

    // Settings
    document.getElementById('audio-track-select')?.addEventListener('change', (e) => {
      const track = parseInt((e.target as HTMLSelectElement).value);
      this.setAudioTrack(track);
    });
    document.getElementById('ffmpeg-preset-select')?.addEventListener('change', (e) => {
      const preset = (e.target as HTMLSelectElement).value;
      this.setFFmpegPreset(preset);
    });
    document.getElementById('generate-audio-preview-btn')?.addEventListener('click', () => this.generateAudioPreview());
    document.getElementById('remove-audio-preview-btn')?.addEventListener('click', () => this.removeAudioPreview());

    // Timeline
    document.getElementById('timeline-text')?.addEventListener('input', (e) => {
      const text = (e.target as HTMLTextAreaElement).value;
      SetTimeline(text);
    });
    document.getElementById('validate-timeline-btn')?.addEventListener('click', () => this.validateTimeline());
    document
      .getElementById('create-random-segments-btn')
      ?.addEventListener('click', () => this.showRandomSegmentsModal());
    document
      .getElementById('export-youtube-timestamp-btn')
      ?.addEventListener('click', () => this.showYouTubeTimestampModal());

    // Toolbar
    document.getElementById('generate-video-btn')?.addEventListener('click', () => this.generateVideo());
    document.getElementById('quit-btn')?.addEventListener('click', () => window.close());

    // Modals
    document
      .getElementById('close-video-list-modal')
      ?.addEventListener('click', () => this.closeModal('video-list-modal'));
    document
      .getElementById('close-video-list-modal-btn')
      ?.addEventListener('click', () => this.closeModal('video-list-modal'));
    document.getElementById('clear-video-list-btn')?.addEventListener('click', () => this.clearVideoList());
    document
      .getElementById('close-random-segments-modal')
      ?.addEventListener('click', () => this.closeModal('random-segments-modal'));
    document
      .getElementById('cancel-random-segments-btn')
      ?.addEventListener('click', () => this.closeModal('random-segments-modal'));
    document
      .getElementById('confirm-random-segments-btn')
      ?.addEventListener('click', () => this.confirmRandomSegments());
    document
      .getElementById('close-youtube-timestamp-modal')
      ?.addEventListener('click', () => this.closeModal('youtube-timestamp-modal'));
    document
      .getElementById('cancel-youtube-timestamp-btn')
      ?.addEventListener('click', () => this.closeModal('youtube-timestamp-modal'));
    document.getElementById('copy-youtube-timestamp-btn')?.addEventListener('click', () => this.copyYouTubeTimestamp());

    // Close modals on outside click
    document.querySelectorAll('.modal').forEach((modal) => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          this.closeModal(modal.id);
        }
      });
    });
  }

  private async importVideos() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/mp4,.mp4';
    input.multiple = true;
    input.style.display = 'none';
    document.body.appendChild(input);

    input.onchange = async (e) => {
      const files = (e.target as HTMLInputElement).files;
      if (files && files.length > 0) {
        try {
          const paths: string[] = [];
          for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const path = (file as any).path || file.name;
            paths.push(path);
          }
          await AddVideos(paths);
          await this.refreshVideoList();
          this.updateUI();
        } catch (error) {
          console.error('Error importing videos:', error);
          await this.showError('Failed to import videos');
        } finally {
          document.body.removeChild(input);
        }
      }
    };

    input.click();
  }

  private async refreshVideoList() {
    this.videoList = await GetVideoList();
    this.renderVideoPlayers();
  }

  private renderVideoPlayers() {
    const container = document.getElementById('video-container');
    if (!container) return;

    container.innerHTML = '';
    this.videoPlayers = [];

    this.videoList.forEach((videoPath, index) => {
      const videoWrapper = document.createElement('div');
      videoWrapper.className = 'video-wrapper';
      videoWrapper.innerHTML = `
                <video id="video-${index}" class="video-player" controls>
                    <source src="file://${videoPath}" type="video/mp4">
                </video>
                <div class="video-label">Video ${index + 1}</div>
            `;
      container.appendChild(videoWrapper);

      const video = document.getElementById(`video-${index}`) as HTMLVideoElement;
      if (video) {
        video.addEventListener('loadedmetadata', () => {
          if (index === 0) {
            this.maxDuration = video.duration;
            this.updateProgressSlider();
          }
        });
        video.addEventListener('timeupdate', () => {
          if (index === 0) {
            this.currentTime = video.currentTime;
            this.updateTimeDisplay();
          }
        });
        this.videoPlayers.push(video);
      }
    });
  }

  private async togglePlayPause() {
    if (this.isPlaying) {
      this.pauseAll();
    } else {
      this.playAll();
    }
  }

  private playAll() {
    this.videoPlayers.forEach((player) => {
      player.play().catch((err) => console.error('Error playing video:', err));
    });
    this.isPlaying = true;
    const btn = document.getElementById('play-pause-btn');
    if (btn) btn.textContent = 'Pause All Videos';
  }

  private pauseAll() {
    this.videoPlayers.forEach((player) => {
      player.pause();
    });
    this.isPlaying = false;
    const btn = document.getElementById('play-pause-btn');
    if (btn) btn.textContent = 'Play All Videos';
  }

  private seek(time: number) {
    this.videoPlayers.forEach((player) => {
      player.currentTime = time;
    });
    this.currentTime = time;
    this.updateTimeDisplay();
  }

  private skip(seconds: number) {
    const newTime = Math.max(0, Math.min(this.maxDuration, this.currentTime + seconds));
    this.seek(newTime);
  }

  private updateTimeDisplay() {
    const currentTimeEl = document.getElementById('current-time');
    const slider = document.getElementById('progress-slider') as HTMLInputElement;

    if (currentTimeEl) {
      currentTimeEl.textContent = this.formatTime(this.currentTime);
    }
    if (slider) {
      slider.value = this.currentTime.toString();
    }
  }

  private updateProgressSlider() {
    const slider = document.getElementById('progress-slider') as HTMLInputElement;
    const totalTimeEl = document.getElementById('total-time');

    if (slider) {
      slider.max = this.maxDuration.toString();
    }
    if (totalTimeEl) {
      totalTimeEl.textContent = this.formatTime(this.maxDuration);
    }
  }

  private formatTime(seconds: number): string {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }

  private copyTimestamp() {
    const timestamp = this.formatTime(this.currentTime);
    navigator.clipboard.writeText(timestamp).then(() => {
      this.updateStatus('Timestamp copied to clipboard');
    });
  }

  private async setAudioTrack(track: number) {
    await SetAudioTrack(track);
    this.audioTrack = track;
    await this.updateAudioPreviewButtons();
  }

  private async setFFmpegPreset(preset: string) {
    await SetFFmpegPreset(preset);
    this.ffmpegPreset = preset;
  }

  private async generateAudioPreview() {
    try {
      this.updateStatus('Generating audio preview, please wait...');
      await GenerateAudioPreview();
      await this.updateAudioPreviewButtons();
    } catch (error) {
      console.error('Error generating audio preview:', error);
      await this.showError('Failed to generate audio preview');
    }
  }

  private async removeAudioPreview() {
    try {
      await RemoveAudioPreview();
      await this.updateAudioPreviewButtons();
    } catch (error) {
      console.error('Error removing audio preview:', error);
    }
  }

  private async updateAudioPreviewButtons() {
    const hasPreview = await HasAudioPreview();
    const generateBtn = document.getElementById('generate-audio-preview-btn') as HTMLButtonElement;
    const removeBtn = document.getElementById('remove-audio-preview-btn') as HTMLButtonElement;

    if (generateBtn) generateBtn.disabled = hasPreview;
    if (removeBtn) removeBtn.disabled = !hasPreview;
  }

  private async validateTimeline() {
    try {
      await ValidateTimeline();
      await this.updateStatus('Timeline validated successfully');
    } catch (error: any) {
      await this.showError(error.message || 'Timeline validation failed');
    }
  }

  private showRandomSegmentsModal() {
    document.getElementById('random-segments-modal')?.classList.add('active');
  }

  private async confirmRandomSegments() {
    const numVideos = parseInt((document.getElementById('random-num-videos') as HTMLInputElement).value);
    const numSegments = parseInt((document.getElementById('random-num-segments') as HTMLInputElement).value);
    const minPerSegment = parseInt((document.getElementById('random-min-per-segment') as HTMLInputElement).value);

    try {
      const timeline = await GenerateRandomSegments(numSegments, minPerSegment, numVideos);
      const textarea = document.getElementById('timeline-text') as HTMLTextAreaElement;
      if (textarea) {
        textarea.value = timeline;
        await SetTimeline(timeline);
      }
      this.closeModal('random-segments-modal');
      await this.updateStatus('Random segments generated');
    } catch (error: any) {
      await this.showError(error.message || 'Failed to generate random segments');
    }
  }

  private async showYouTubeTimestampModal() {
    const content = document.getElementById('youtube-labels-content');
    if (!content) return;

    content.innerHTML = '';
    for (let i = 0; i < this.videoList.length; i++) {
      const formGroup = document.createElement('div');
      formGroup.className = 'form-group';
      formGroup.innerHTML = `
                <label>Label ${i + 1}:</label>
                <input type="text" id="youtube-label-${i}" class="input" placeholder="Enter label for video ${i + 1}">
            `;
      content.appendChild(formGroup);
    }

    document.getElementById('youtube-timestamp-modal')?.classList.add('active');
  }

  private async copyYouTubeTimestamp() {
    const labels: string[] = [];
    for (let i = 0; i < this.videoList.length; i++) {
      const input = document.getElementById(`youtube-label-${i}`) as HTMLInputElement;
      labels.push(input?.value || `Video ${i + 1}`);
    }

    try {
      const timestamp = await GenerateYouTubeTimestamp(labels);
      await navigator.clipboard.writeText(timestamp);
      this.closeModal('youtube-timestamp-modal');
      await this.updateStatus('YouTube timestamp copied to clipboard');
    } catch (error: any) {
      await this.showError(error.message || 'Failed to generate YouTube timestamp');
    }
  }

  private async importIntro() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/mp4,.mp4';
    input.style.display = 'none';
    document.body.appendChild(input);

    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        try {
          const path = (file as any).path || file.name;
          await SetIntro(path);
          this.updateUI();
        } catch (error) {
          console.error('Error importing intro:', error);
        } finally {
          document.body.removeChild(input);
        }
      }
    };
    input.click();
  }

  private async importOutro() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/mp4,.mp4';
    input.style.display = 'none';
    document.body.appendChild(input);

    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        try {
          const path = (file as any).path || file.name;
          await SetOutro(path);
          this.updateUI();
        } catch (error) {
          console.error('Error importing outro:', error);
        } finally {
          document.body.removeChild(input);
        }
      }
    };
    input.click();
  }

  private async showVideoListModal() {
    const content = document.getElementById('video-list-content');
    if (!content) return;

    content.innerHTML = '';

    // Videos
    this.videoList.forEach((video, index) => {
      const item = document.createElement('div');
      item.className = 'video-list-item';
      item.innerHTML = `
                <span>Video ${index + 1}: ${video.split(/[/\\]/).pop()}</span>
                <button class="btn btn-small btn-danger" data-index="${index}">Remove</button>
            `;
      item.querySelector('button')?.addEventListener('click', async () => {
        await this.removeVideo(index);
      });
      content.appendChild(item);
    });

    // Intro
    const intro = await GetIntro();
    if (intro) {
      const item = document.createElement('div');
      item.className = 'video-list-item';
      item.innerHTML = `
                <span>Intro: ${intro.split(/[/\\]/).pop()}</span>
                <button class="btn btn-small btn-danger" id="remove-intro-btn">Remove</button>
            `;
      item.querySelector('button')?.addEventListener('click', async () => {
        await SetIntro('');
        this.updateUI();
        this.showVideoListModal();
      });
      content.appendChild(item);
    }

    // Outro
    const outro = await GetOutro();
    if (outro) {
      const item = document.createElement('div');
      item.className = 'video-list-item';
      item.innerHTML = `
                <span>Outro: ${outro.split(/[/\\]/).pop()}</span>
                <button class="btn btn-small btn-danger" id="remove-outro-btn">Remove</button>
            `;
      item.querySelector('button')?.addEventListener('click', async () => {
        await SetOutro('');
        this.updateUI();
        this.showVideoListModal();
      });
      content.appendChild(item);
    }

    document.getElementById('video-list-modal')?.classList.add('active');
  }

  private async removeVideo(index: number) {
    try {
      await RemoveVideo(index);
      await this.refreshVideoList();
      this.updateUI();
      this.showVideoListModal();
    } catch (error) {
      console.error('Error removing video:', error);
    }
  }

  private async clearVideoList() {
    await ClearVideoList();
    await this.refreshVideoList();
    this.updateUI();
    this.closeModal('video-list-modal');
  }

  private async generateVideo() {
    const btn = document.getElementById('generate-video-btn') as HTMLButtonElement;
    if (btn) btn.disabled = true;

    try {
      await GenerateVideo();
    } catch (error: any) {
      await this.showError(error.message || 'Failed to generate video');
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  private async updateUI() {
    // Update video list button
    const viewBtn = document.getElementById('view-video-list-btn');
    if (viewBtn) {
      viewBtn.textContent = `View Video List (${this.videoList.length} of 4)`;
    }

    // Update play/pause button
    const playPauseBtn = document.getElementById('play-pause-btn') as HTMLButtonElement;
    if (playPauseBtn) {
      playPauseBtn.disabled = this.videoList.length === 0;
    }

    // Update generate button
    const generateBtn = document.getElementById('generate-video-btn') as HTMLButtonElement;
    if (generateBtn) {
      generateBtn.disabled = this.videoList.length === 0;
    }

    // Update audio track select
    const audioTrackSelect = document.getElementById('audio-track-select') as HTMLSelectElement;
    if (audioTrackSelect) {
      audioTrackSelect.innerHTML = '';
      for (let i = 1; i <= this.videoList.length; i++) {
        const option = document.createElement('option');
        option.value = i.toString();
        option.textContent = i.toString();
        if (i === this.audioTrack) option.selected = true;
        audioTrackSelect.appendChild(option);
      }
    }

    // Update FFmpeg preset
    const presetSelect = document.getElementById('ffmpeg-preset-select') as HTMLSelectElement;
    if (presetSelect) {
      presetSelect.value = this.ffmpegPreset;
    }

    await this.updateAudioPreviewButtons();
  }

  private closeModal(modalId: string) {
    document.getElementById(modalId)?.classList.remove('active');
  }

  private async updateStatus(message: string) {
    const statusEl = document.getElementById('status-text');
    if (statusEl) {
      statusEl.textContent = message;
    }
    // Also update backend status
    try {
      await SetStatus(message);
    } catch (error) {
      console.error('Error setting status:', error);
    }
  }

  private async showError(message: string) {
    await ShowMessage('Error', message, 'error');
    await this.updateStatus(`Error: ${message}`);
  }

  private startStatusUpdates() {
    if (this.statusUpdateInterval !== null) {
      clearInterval(this.statusUpdateInterval);
    }
    this.statusUpdateInterval = window.setInterval(async () => {
      try {
        const status = await GetStatus();
        const statusEl = document.getElementById('status-text');
        if (statusEl) {
          statusEl.textContent = status;
        }
      } catch (error) {
        console.error('Error updating status:', error);
      }
    }, 1000);
  }
}
