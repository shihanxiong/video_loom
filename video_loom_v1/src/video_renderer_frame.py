import os
import pygame
import logging
from tkinter import ttk
from component_interface import ComponentInterface
from pdb import set_trace
import queue
import threading
import tkinter as tk

# Module-level globals for queue processor (must be at module level)
_tkinter_ops_queue = queue.Queue()
_tkinter_ops_processor_scheduled = False
_root_window = None  # Store root window reference for background threads

# Monkey patch tkVideoPlayer to fix fast_seek attribute issue with newer av versions
# and thread-safety issues with event_generate
# This must be done before importing TkinterVideo
try:
    import av
    import threading

    # Patch av.open to wrap containers and handle missing fast_seek/discard_corrupt attributes
    original_av_open = av.open

    def patched_av_open(*args, **kwargs):
        container = original_av_open(*args, **kwargs)

        # Create a wrapper that intercepts attribute setting
        class ContainerWrapper:
            def __init__(self, container):
                object.__setattr__(self, "_container", container)

            def __getattr__(self, name):
                return getattr(self._container, name)

            def __setattr__(self, name, value):
                if name == "_container":
                    object.__setattr__(self, name, value)
                elif name in ("fast_seek", "discard_corrupt"):
                    # Silently ignore setting these on newer av versions that don't support them
                    try:
                        setattr(self._container, name, value)
                    except (AttributeError, TypeError):
                        pass  # Attribute doesn't exist in newer av versions, ignore
                else:
                    setattr(self._container, name, value)

            def __enter__(self):
                self._container.__enter__()
                return self

            def __exit__(self, *args):
                return self._container.__exit__(*args)

        return ContainerWrapper(container)

    # Replace av.open with our patched version globally
    av.open = patched_av_open

    # Now import tkVideoPlayer - it will use our patched av.open
    import tkVideoPlayer.tkvideoplayer as tkvp_module

    # Also patch it in the module's av import if it has one
    if hasattr(tkvp_module, "av"):
        tkvp_module.av.open = patched_av_open

    # Patch event_generate to be thread-safe
    # Save the original event_generate method
    original_event_generate = tkvp_module.TkinterVideo.event_generate

    # Create a queue to pass events from background threads to main thread
    _event_queue = queue.Queue()
    _queue_processor_scheduled = False

    def process_event_queue():
        """Process events from the queue on the main thread"""
        global _queue_processor_scheduled
        _queue_processor_scheduled = False
        try:
            processed = 0
            while processed < 10:  # Process up to 10 events at a time
                try:
                    widget, sequence, kw = _event_queue.get_nowait()
                    try:
                        original_event_generate(widget, sequence, **kw)
                    except Exception as e:
                        # Silently ignore errors - events might not be critical
                        pass
                    processed += 1
                except queue.Empty:
                    break
        except Exception:
            pass
        finally:
            # Schedule next check if queue has more items
            if not _event_queue.empty():
                try:
                    import tkinter as tk

                    root = _root_window
                    if not root:
                        root = tk._default_root
                    if root and hasattr(root, "after"):
                        root.after(10, process_event_queue)
                        _queue_processor_scheduled = True
                except Exception:
                    pass

    def thread_safe_event_generate(self, sequence, **kw):
        """Thread-safe version of event_generate that schedules on main thread"""
        global _queue_processor_scheduled
        # Check if we're on the main thread
        is_main_thread = threading.current_thread() is threading.main_thread()

        if is_main_thread:
            # We're on the main thread, try to call directly
            try:
                return original_event_generate(self, sequence, **kw)
            except RuntimeError as e:
                if (
                    "main thread is not in main loop" in str(e)
                    or "main loop" in str(e).lower()
                ):
                    # Main loop might not be ready yet, schedule it
                    try:
                        root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            root.after(
                                10,
                                lambda: original_event_generate(self, sequence, **kw),
                            )
                    except Exception:
                        pass
                else:
                    raise
        else:
            # We're in a background thread, put event in queue
            try:
                _event_queue.put((self, sequence, kw))
                # Schedule queue processing if not already scheduled
                if not _queue_processor_scheduled:
                    try:
                        # Use stored root window (set from main thread)
                        # Don't call winfo_toplevel() from background thread!
                        root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            root.after(10, process_event_queue)
                            _queue_processor_scheduled = True
                    except Exception:
                        pass
            except Exception:
                pass

    # Replace event_generate with thread-safe version
    tkvp_module.TkinterVideo.event_generate = thread_safe_event_generate

    # Note: _tkinter_ops_queue, _tkinter_ops_processor_scheduled, and _root_window
    # are now defined at module level (above) so they can be accessed by process_tkinter_ops_queue

    def schedule_on_main_thread(func, *args, **kwargs):
        """Schedule a function to run on the main thread"""
        global _tkinter_ops_processor_scheduled
        is_main_thread = threading.current_thread() is threading.main_thread()

        if is_main_thread:
            # Already on main thread, call directly
            try:
                return func(*args, **kwargs)
            except RuntimeError:
                # Main loop might not be ready, schedule it
                _tkinter_ops_queue.put((func, args, kwargs))
                if not _tkinter_ops_processor_scheduled:
                    try:
                        root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            root.after(10, process_tkinter_ops_queue)
                            _tkinter_ops_processor_scheduled = True
                    except Exception:
                        pass
        else:
            # Background thread, queue the operation
            _tkinter_ops_queue.put((func, args, kwargs))
            if not _tkinter_ops_processor_scheduled:
                try:
                    root = _root_window
                    if not root:
                        root = tk._default_root
                    if root and hasattr(root, "after"):
                        root.after(10, process_tkinter_ops_queue)
                        _tkinter_ops_processor_scheduled = True
                except Exception:
                    pass

    # Patch _set_frame_size to be thread-safe (it creates PhotoImage which needs main thread)
    original_set_frame_size = tkvp_module.TkinterVideo._set_frame_size

    def thread_safe_set_frame_size(self):
        """Thread-safe version of _set_frame_size that schedules on main thread and waits"""
        global _tkinter_ops_processor_scheduled
        is_main_thread = threading.current_thread() is threading.main_thread()

        if is_main_thread:
            # Already on main thread, call directly
            try:
                return original_set_frame_size(self)
            except RuntimeError:
                # Main loop might not be ready, schedule it
                _tkinter_ops_queue.put((original_set_frame_size, (self,), {}))
                if not _tkinter_ops_processor_scheduled:
                    try:
                        root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            root.after(10, process_tkinter_ops_queue)
                            _tkinter_ops_processor_scheduled = True
                    except Exception:
                        pass
        else:
            # Background thread - need to wait for completion
            result_container = {"done": False, "exception": None}

            def set_frame_size_wrapper():
                try:
                    logging.info(f"_set_frame_size: Starting for video player")
                    original_set_frame_size(self)
                    logging.info(f"_set_frame_size: Completed successfully")
                except Exception as e:
                    logging.error(f"_set_frame_size: Failed with error: {e}")
                    import traceback

                    logging.debug(traceback.format_exc())
                    result_container["exception"] = e
                finally:
                    result_container["done"] = True

            # Schedule on main thread
            _tkinter_ops_queue.put((set_frame_size_wrapper, (), {}))
            # Always try to start queue processor if not running
            if not _tkinter_ops_processor_scheduled:
                try:
                    # Try multiple ways to get root window
                    root = None
                    # First try stored root
                    if _root_window:
                        root = _root_window
                    # Then try default root
                    if not root:
                        root = tk._default_root
                    # If still no root, try to get it from tkinter's internal state
                    if not root:
                        try:
                            import tkinter

                            root = tkinter._default_root
                        except:
                            pass

                    if root and hasattr(root, "after"):
                        try:
                            root.after(0, process_tkinter_ops_queue)
                            _tkinter_ops_processor_scheduled = True
                            logging.debug(
                                "Scheduled queue processor from _set_frame_size"
                            )
                        except Exception as e:
                            logging.debug(f"Failed to call root.after(): {e}")
                    else:
                        logging.debug(
                            f"No root window available (stored: {_root_window is not None}, default: {tk._default_root is not None})"
                        )
                except Exception as e:
                    logging.debug(f"Failed to schedule queue processor: {e}")
                    import traceback

                    logging.debug(traceback.format_exc())

            # Wait for completion (with timeout)
            import time

            timeout = 2.0  # 2 second timeout (increased)
            start = time.time()
            # Also trigger queue processing while waiting
            while not result_container["done"] and (time.time() - start) < timeout:
                # Try to trigger queue processing
                if not _tkinter_ops_processor_scheduled:
                    try:
                        # Try multiple ways to get root window
                        root = None
                        if _root_window:
                            root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            try:
                                root.after(0, process_tkinter_ops_queue)
                                _tkinter_ops_processor_scheduled = True
                            except:
                                pass
                    except Exception:
                        pass
                # Also try to process queue directly if we're on main thread (shouldn't happen, but safety check)
                try:
                    if threading.current_thread() is threading.main_thread():
                        process_tkinter_ops_queue()
                except:
                    pass
                time.sleep(0.01)

            if not result_container["done"]:
                logging.warning(f"_set_frame_size timed out after {timeout} seconds")
            if result_container["exception"]:
                logging.error(
                    f"_set_frame_size failed: {result_container['exception']}"
                )
                raise result_container["exception"]

    # Replace _set_frame_size with thread-safe version
    tkvp_module.TkinterVideo._set_frame_size = thread_safe_set_frame_size

    # Patch config to be thread-safe
    original_config = tkvp_module.TkinterVideo.config

    def thread_safe_config(self, **kw):
        """Thread-safe version of config"""
        global _tkinter_ops_processor_scheduled
        is_main_thread = threading.current_thread() is threading.main_thread()

        if is_main_thread:
            # Already on main thread, call directly
            try:
                return original_config(self, **kw)
            except RuntimeError:
                # Main loop might not be ready, schedule it
                _tkinter_ops_queue.put((original_config, (self,), kw))
                if not _tkinter_ops_processor_scheduled:
                    try:
                        root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            root.after(10, process_tkinter_ops_queue)
                            _tkinter_ops_processor_scheduled = True
                    except Exception:
                        pass
        else:
            # Background thread - schedule but don't wait (config is usually non-blocking)
            _tkinter_ops_queue.put((original_config, (self,), kw))
            if not _tkinter_ops_processor_scheduled:
                try:
                    root = _root_window
                    if not root:
                        root = tk._default_root
                    if root and hasattr(root, "after"):
                        root.after(0, process_tkinter_ops_queue)
                        _tkinter_ops_processor_scheduled = True
                except Exception:
                    pass

    tkvp_module.TkinterVideo.config = thread_safe_config

    # Patch ImageTk.PhotoImage in the tkvideoplayer module to be thread-safe
    # The module imports: from PIL import ImageTk, Image, ImageOps
    # So ImageTk is available as tkvp_module.ImageTk
    if hasattr(tkvp_module, "ImageTk"):
        original_module_PhotoImage = tkvp_module.ImageTk.PhotoImage

        def module_thread_safe_PhotoImage(*args, **kwargs):
            """Thread-safe PhotoImage that schedules creation on main thread"""
            is_main_thread = threading.current_thread() is threading.main_thread()
            if is_main_thread:
                return original_module_PhotoImage(*args, **kwargs)
            else:
                # Can't create PhotoImage from background thread
                # Schedule it on main thread and wait for result
                result_container = {"result": None, "exception": None, "done": False}

                def create_photoimage():
                    try:
                        logging.debug(f"PhotoImage: Creating from background thread")
                        result_container["result"] = original_module_PhotoImage(
                            *args, **kwargs
                        )
                        logging.debug(f"PhotoImage: Created successfully")
                    except Exception as e:
                        logging.error(f"PhotoImage: Creation failed: {e}")
                        import traceback

                        logging.debug(traceback.format_exc())
                        result_container["exception"] = e
                    finally:
                        result_container["done"] = True

                # Schedule on main thread
                _tkinter_ops_queue.put((create_photoimage, (), {}))
                if not _tkinter_ops_processor_scheduled:
                    try:
                        root = _root_window
                        if not root:
                            root = tk._default_root
                        if root and hasattr(root, "after"):
                            # Use after_idle for immediate processing if possible
                            try:
                                root.after_idle(process_tkinter_ops_queue)
                            except:
                                root.after(0, process_tkinter_ops_queue)
                            _tkinter_ops_processor_scheduled = True
                    except Exception:
                        pass

                # Wait for creation to complete (with timeout)
                import time

                timeout = 2.0  # 2 second timeout
                start = time.time()
                while not result_container["done"] and (time.time() - start) < timeout:
                    time.sleep(0.01)

                if result_container["exception"]:
                    raise result_container["exception"]
                if result_container["result"] is None:
                    raise RuntimeError("PhotoImage creation timed out or failed")
                return result_container["result"]

        tkvp_module.ImageTk.PhotoImage = module_thread_safe_PhotoImage

        # Actually, let's not patch _load - it's too complex. The _set_frame_size patch should be enough.

except Exception as ex:
    # If patching fails, log it but continue
    logging.warning(f"Failed to patch tkVideoPlayer: {ex}")

from tkVideoPlayer import TkinterVideo


# Module-level queue processor function (must be at module level for Tkinter serialization)
def process_tkinter_ops_queue():
    """Process Tkinter operations from the queue on the main thread"""
    global _tkinter_ops_processor_scheduled
    _tkinter_ops_processor_scheduled = False
    try:
        processed = 0
        # Process all available operations (not just 10)
        while True:
            try:
                func, args, kwargs = _tkinter_ops_queue.get_nowait()
                try:
                    func(*args, **kwargs)
                    processed += 1
                except Exception as e:
                    # Log errors for debugging - use info level so we can see them
                    logging.info(f"Error in queued Tkinter operation: {e}")
                    import traceback

                    logging.debug(traceback.format_exc())
            except queue.Empty:
                break
        if processed > 0:
            logging.debug(f"Processed {processed} Tkinter operations from queue")
    except Exception as e:
        logging.info(f"Error processing Tkinter ops queue: {e}")
        import traceback

        logging.debug(traceback.format_exc())
    finally:
        # Always schedule next check to keep processor running continuously
        try:
            root = _root_window
            if not root:
                root = tk._default_root
            if root and hasattr(root, "after"):
                # Schedule next check even if queue is empty (continuous polling every 10ms)
                # Function is now at module level, so Tkinter can serialize it
                root.after(10, process_tkinter_ops_queue)
                _tkinter_ops_processor_scheduled = True
        except Exception as e:
            logging.debug(f"Failed to reschedule queue processor: {e}")


# video renderer
class VideoRendererFrame(ttk.Frame, ComponentInterface):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # status
        self.is_playing = False
        self.videoplayers = []  # Initialize empty list

        # pygame
        pygame.init()
        self.mixer = pygame.mixer

        # Store root window reference immediately for use by background threads
        def start_continuous_queue_processor():
            global _tkinter_ops_processor_scheduled
            try:
                root = _root_window
                if not root:
                    root = tk._default_root
                if root and hasattr(root, "after"):
                    # Start continuous queue processor
                    root.after(0, process_tkinter_ops_queue)
                    _tkinter_ops_processor_scheduled = True
                    logging.debug("Started continuous queue processor")
            except Exception as e:
                logging.debug(f"Failed to start queue processor: {e}")

        # Store root window and start queue processor immediately
        # The root window should already be set by app.py, but verify and start processor
        def start_queue_processor():
            global _tkinter_ops_processor_scheduled, _root_window
            try:
                root = _root_window
                if not root:
                    root = self.winfo_toplevel()
                    if root:
                        _root_window = root
                if not root:
                    root = tk._default_root

                if root and hasattr(root, "after"):
                    # Start the continuous queue processor
                    # Use lambda to ensure function reference is maintained
                    root.after(0, lambda: process_tkinter_ops_queue())
                    _tkinter_ops_processor_scheduled = True
                    logging.info("Started continuous queue processor")
            except Exception as e:
                logging.debug(f"Failed to start queue processor: {e}")

        # Verify root window is set (should be set by app.py)
        global _root_window
        try:
            root = self.winfo_toplevel()
            if root:
                if not _root_window:
                    _root_window = root  # Store if not already set
                    logging.info(f"Stored root window in VideoRendererFrame: {root}")
                # Start queue processor
                if hasattr(root, "after"):
                    root.after(50, start_queue_processor)  # Start after a short delay
        except Exception as e:
            logging.debug(f"Failed to get root window in __init__: {e}")
            # Try again later
            try:
                self.after(200, start_queue_processor)
            except:
                pass

    def refresh(self):
        # dynamically create video player instances
        # First, destroy existing video players
        if hasattr(self, "videoplayers"):
            for videoplayer in self.videoplayers:
                try:
                    videoplayer.stop()
                    videoplayer.destroy()
                except Exception:
                    pass

        self.videoplayers = []
        for i in range(len(self.master.video_list)):
            try:
                videoplayer = TkinterVideo(self, scaled=True, keep_aspect=True)
                video_path = os.path.abspath(self.master.video_list[i])
                logging.info(f"Loading video {i+1}: {video_path}")
                videoplayer.load(video_path)
                videoplayer.grid(row=0, column=i, sticky="NEWS", padx=(10), pady=(20))
                self.videoplayers.append(videoplayer)
                logging.info(f"Video {i+1} loaded and gridded")
            except Exception as e:
                logging.error(f"Error loading video {i+1}: {e}")
                import traceback

                logging.debug(traceback.format_exc())

    def load_audio_preview(self):
        try:
            if (
                self.master.master.settings_component.audio_setting_component.has_audio_preview()
            ):
                self.mixer.music.load(
                    self.master.master.settings_component.audio_setting_component.get_audio_preview()
                )
                if self.is_playing:
                    self.mixer.music.play(
                        start=self.master.video_control_component.progress_value.get()
                    )
                else:
                    self.mixer.music.set_pos(
                        self.master.video_control_component.progress_value.get()
                    )
            else:
                self.mixer.music.stop()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def unload_audio_preview(self):
        try:
            self.mixer.music.unload()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def play_all(self):
        self.is_playing = True
        self.master.master.status_component.set_and_log_status("playing all videos")
        logging.info(f"Playing {len(self.videoplayers)} video(s)")
        for i, videoplayer in enumerate(self.videoplayers):
            try:
                logging.info(f"Calling play() on video player {i+1}")
                videoplayer.play()
                logging.info(f"play() called successfully on video player {i+1}")
            except Exception as e:
                logging.error(f"Error playing video {i+1}: {e}")
                import traceback

                logging.debug(traceback.format_exc())

        # audio
        if (
            self.master.master.settings_component.audio_setting_component.has_audio_preview()
        ):
            self.load_audio_preview()
            if self.mixer.music.get_pos() == -1:
                self.mixer.music.play(
                    start=self.master.video_control_component.progress_value.get()
                )
            else:
                self.mixer.music.set_pos(
                    self.master.video_control_component.progress_value.get()
                )
                self.mixer.music.unpause()

    def pause_all(self):
        self.is_playing = False
        self.master.master.status_component.set_and_log_status("pausing all videos")
        try:
            for videoplayer in self.videoplayers:
                videoplayer.pause()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

        # audio
        if (
            self.master.master.settings_component.audio_setting_component.has_audio_preview()
        ):
            self.mixer.music.pause()

    def seek(self, value):
        # audio
        if (
            self.master.master.settings_component.audio_setting_component.has_audio_preview()
        ):
            self.mixer.music.set_pos(value)
