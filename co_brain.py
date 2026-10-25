from Automation.Automation_Brain import Auto_main_brain, clear_file
from NetHyTechSTT.listen import listen
from Brain.personality import jarvis_speak
import threading
from Brain.brain import Main_Brain, JarvisBrain
from Brain.intent_classifier import classifier  # SmartIntentClassifier singleton

# ── Instantiate once, OUTSIDE the loop so memory persists across turns ──
brain = JarvisBrain()
from Tools.app_launcher import open_app
from Tools.app_closer import close_app
from Tools.screen_control import handle_screen_command
from Tools.screen_intelligence import analyze_screen
from Tools.camera_control import open_camera_interface, close_camera_interface, click_photo, start_recording, stop_recording
from Tools.window_control import minimize_window, minimize_active_window, show_all_windows, open_start_menu
from Tools.browser_control import search_youtube, search_google, open_youtube
from Tools.notes_control import is_notes_mode, start_notes, stop_notes, type_text
from Tools.clipboard_control import copy_selection, paste
from Tools.spotify_control import (
    play_song, play_album, search_song, open_spotify_only,
    pause_music, resume_music, increase_volume, decrease_volume,
    next_track, previous_track
)

WAKE_WORD = "jarvis"

def check_inputs():
    import time
    output_text = ""
    while True:
        time.sleep(0.1)  # Small delay for reliable input processing
        with open("input.txt","r") as file:
            input_text = file.read().lower().strip()

        if input_text != output_text and input_text:
            output_text = input_text
            print(f"[DEBUG] Raw input: {output_text}")

            # ============================================
            # MUSIC COMMANDS (NO WAKE WORD REQUIRED)
            # These run BEFORE the wake word gate for seamless control
            # ============================================

            # Play song: "play believer" or "play shape of you"
            if output_text.startswith("play "):
                song_name = output_text.replace("play ", "").strip()
                if song_name:
                    success, msg = play_song(song_name)
                    if success:
                        jarvis_speak(msg, mood="success")
                continue

            # Stop music: "stop" or "stop song" or "stop the song"
            if output_text in ["stop", "stop song", "stop the song", "stop music", "stop the music"]:
                success, msg = pause_music()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # Resume: "resume" or "continue music"
            if output_text in ["resume", "continue", "continue music", "resume music"]:
                success, msg = resume_music()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # Volume up: "increase volume" or "volume up"
            if output_text in ["increase volume", "volume up", "louder", "increase the volume"]:
                success, msg = increase_volume()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # Volume down: "decrease volume" or "lower volume"
            if output_text in ["decrease volume", "lower volume", "volume down", "lower the volume", "decrease the volume"]:
                success, msg = decrease_volume()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # Search: "search believer"
            if output_text.startswith("search "):
                song_name = output_text.replace("search ", "").strip()
                if song_name:
                    success, msg = search_song(song_name)
                    if success:
                        jarvis_speak(msg, mood="success")
                continue

            # Next/Previous (no wake word)
            if output_text in ["next", "next song", "skip"]:
                success, msg = next_track()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if output_text in ["previous", "previous song", "go back"]:
                success, msg = previous_track()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # NOTES MODE (NO WAKE WORD)
            # ============================================
            if is_notes_mode():
                type_text(output_text)
                continue

            # ============================================
            # WAKE WORD GATE (FOR OTHER COMMANDS)
            # ============================================
            if not output_text.startswith(WAKE_WORD):
                print(f"[DEBUG] No wake word, ignoring.")
                continue

            # Strip wake word
            cmd = output_text.replace(WAKE_WORD, "", 1).strip()
            print(f"[DEBUG] Command after stripping wake word: {cmd}")

            # ============================================
            # PRIORITY 1: EXIT
            # ============================================
            if cmd in ["exit", "stop", "quit", "terminate", "shutdown"]:
                jarvis_speak("Shutting down.", mood="neutral")
                break

            # ============================================
            # PRIORITY 2: NOTES MODE TOGGLE
            # ============================================
            if cmd in ["start taking notes", "start notes", "take notes"]:
                success, msg = open_app("notepad")
                if success:
                    start_notes()
                    jarvis_speak("Notes mode started.", mood="success")
                continue

            if cmd in ["stop taking notes", "stop notes"]:
                stop_notes()
                jarvis_speak("Notes mode stopped.", mood="success")
                continue

            # ============================================
            # PRIORITY 3: CLOSE APP
            # ============================================
            if cmd == "close camera":
                success, msg = close_camera_interface()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd.startswith("close "):
                app_name = cmd.replace("close ", "").strip()
                if "window" not in app_name:
                    success, msg = close_app(app_name)
                    if success:
                        jarvis_speak(msg, mood="success")
                    continue

            # ============================================
            # PRIORITY 4: MINIMIZE
            # ============================================
            if cmd in ["minimize window", "minimize this", "minimize"]:
                success, msg = minimize_active_window()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd.startswith("minimize "):
                app_name = cmd.replace("minimize ", "").strip()
                success, msg = minimize_window(app_name)
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 5: OPEN APP
            # ============================================
            if cmd == "open camera":
                success, msg = open_camera_interface()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd in ["open start menu", "start menu"]:
                success, msg = open_start_menu()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd in ["open youtube", "youtube"]:
                success, msg = open_youtube()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd.startswith("open "):
                app_name = cmd.replace("open ", "").strip()
                success, msg = open_app(app_name)
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 6: SYSTEM CONTROLS
            # ============================================
            if cmd in ["show all windows", "show all tabs", "task view"]:
                success, msg = show_all_windows()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 7: BROWSER SEARCH
            # ============================================
            if cmd.startswith("search youtube for "):
                query = cmd.replace("search youtube for ", "").strip()
                success, msg = search_youtube(query)
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd.startswith("search google for "):
                query = cmd.replace("search google for ", "").strip()
                success, msg = search_google(query)
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 8: SPOTIFY (WAKE WORD REQUIRED)
            # ============================================
            if cmd in ["open spotify"]:
                success, msg = open_spotify_only()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd.startswith("play album "):
                album_name = cmd.replace("play album ", "").strip()
                if album_name:
                    success, msg = play_album(album_name)
                    if success:
                        jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 9: CAMERA ACTIONS
            # ============================================
            if cmd in ["click", "take picture", "capture photo"]:
                success, msg = click_photo()
                if success:
                    jarvis_speak(msg, mood="success")
                    continue
                elif cmd != "click":
                    continue  # Silent for camera-specific commands

            if cmd in ["start recording", "record video"]:
                success, msg = start_recording()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd in ["stop recording", "stop video"]:
                success, msg = stop_recording()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 9: SCREEN CONTROL
            # ============================================
            success, msg = handle_screen_command(cmd)
            if success:
                jarvis_speak(msg, mood="success")
                continue

            # ============================================
            # PRIORITY 10: CLIPBOARD
            # ============================================
            if cmd in ["copy", "copy this"]:
                success, msg = copy_selection()
                if success:
                    jarvis_speak(msg, mood="success")
                continue

            if cmd in ["paste", "paste this"]:
                success, msg = paste()
                if success:
                    jarvis_speak(msg, mood="success")
                continue
            # ============================================
            # PRIORITY 11: AUTOMATION
            # ============================================
            if "play music" in cmd or "weather" in cmd:
                Auto_main_brain(cmd)
                continue

            # ============================================
            # PRIORITY 12: SMART INTENT CLASSIFIER (offline, <5ms)
            # Runs BEFORE the LLM — no network call needed.
            # ============================================
            clf_result = classifier.classify(cmd)

            if clf_result["intent"] != "unknown":
                intent  = clf_result["intent"]
                action  = clf_result["action"]
                message = clf_result["message"]
                data    = clf_result["data"]

                print(f"[DEBUG] Classifier hit: intent='{intent}' action='{action}'")

                # ── Screen intelligence: analyze the desktop only on request ──
                if intent == "screen_question":
                    question = data.get("question", cmd)
                    jarvis_speak("Analyzing your screen now, sir.", mood="neutral")
                    success, answer = analyze_screen(question)
                    jarvis_speak(
                        answer,
                        mood="success" if success else "neutral"
                    )
                    continue

                # ── Route classifier intents to existing tool functions ──

                if intent == "open_app":
                    app = data.get("app", "").strip()
                    success, msg = open_app(app)
                    jarvis_speak(msg if success else message, mood="success" if success else "neutral")

                elif intent == "close_app":
                    app = data.get("app", "").strip()
                    success, msg = close_app(app)
                    jarvis_speak(msg if success else message, mood="success" if success else "neutral")

                elif intent == "play_music":
                    song = data.get("song", "").strip()
                    if action == "play_album":
                        success, msg = play_album(song)
                    else:
                        success, msg = play_song(song)
                    jarvis_speak(msg if success else message, mood="success" if success else "neutral")

                elif intent == "web_search":
                    query = data.get("query", "").strip()
                    success, msg = search_google(query)
                    jarvis_speak(msg if success else message, mood="success" if success else "neutral")

                elif intent == "system_vol":
                    if action == "volume_up":
                        success, msg = increase_volume()
                    elif action == "volume_down":
                        success, msg = decrease_volume()
                    elif action == "mute":
                        success, msg = pause_music()   # reuse pause as mute proxy
                    else:
                        success, msg = resume_music()  # unmute
                    jarvis_speak(msg if success else message, mood="success" if success else "neutral")

                elif intent == "notes":
                    if action == "start_notes":
                        success, msg = open_app("notepad")
                        if success:
                            start_notes()
                        jarvis_speak(message, mood="success")
                    elif action == "stop_notes":
                        stop_notes()
                        jarvis_speak(message, mood="success")

                elif intent == "reset_memory":
                    result = brain.reset_memory()
                    jarvis_speak(result["message"], mood="success")

                elif intent == "screenshot":
                    # Capture the desktop, not the webcam.
                    success, msg = handle_screen_command("screenshot")
                    jarvis_speak(
                        msg,
                        mood="success" if success else "neutral",
                )

                elif intent == "weather":
                    # Delegate to automation brain which handles weather
                    Auto_main_brain(cmd)

                elif intent == "system_control":
                    # System actions (shutdown/restart/lock/sleep) — speak the
                    # message; actual OS calls can be wired in Tools/ later.
                    jarvis_speak(message, mood="neutral")
                    print(f"[DEBUG] System control action requested: {action}")

                else:
                    # Any other classifier hit we don't have a specific handler for:
                    # speak the pre-built message and move on.
                    jarvis_speak(message, mood="neutral")

                continue  # ← skip LLM entirely

            # ============================================
            # PRIORITY 13: BRAIN META-COMMANDS
            # These MUST come before the LLM fallback.
            # ============================================

            # Voice hook: wipe conversation memory
            if cmd in ["reset memory", "clear memory", "forget everything"]:
                result = brain.reset_memory()
                jarvis_speak(result["message"], mood="success")
                continue

            # Voice hook: echo the last thing the user said
            if cmd in ["what did i say", "what was my last message", "repeat my last"]:
                last = brain.recall_last()
                if last:
                    jarvis_speak(f"Your last message was: {last}", mood="neutral")
                else:
                    jarvis_speak("No previous messages found, sir.", mood="neutral")
                continue

            # Voice hook: report memory usage
            if cmd in ["brain status", "memory status", "how is your memory"]:
                status = brain.status()
                jarvis_speak(status, mood="neutral")
                continue

            # ============================================
            # PRIORITY 13: LLM FALLBACK (JarvisBrain)
            # ============================================
            print("[DEBUG] Sending to JarvisBrain")

            try:
                result = brain.think(cmd)

                # Route on intent: if the LLM decided this is a tool call,
                # log it — future versions can dispatch to tool handlers here.
                if result.get("intent") == "tool_call":
                    print(f"[BRAIN] Tool call detected → action: {result.get('action')}")

                # Always speak the natural-language message
                jarvis_speak(result.get("message", "I have no response, sir."))

            except Exception as e:
                print(f"[ERROR] JarvisBrain failed: {e}")

            continue

def Jarvis():
    clear_file()
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=check_inputs)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
