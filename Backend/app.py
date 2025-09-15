# # app.py (complete updated file)

# import os

# # --- Ensure moviepy/ffmpeg/tempfile uses a directory with space ---
# TMP_DIR = "/home/digi2/Downloads/tmp"
# os.makedirs(TMP_DIR, exist_ok=True)
# # Make Python/tempfile use this directory
# os.environ["TMPDIR"] = TMP_DIR

# # Now import heavy libs (after TMPDIR set)
# from io import BytesIO
# import threading
# import time
# import requests

# import streamlit as st
# import torch
# import soundfile as sf
# from PIL import Image

# # --- Local modules ---
# from modules.audio_handler import convert_to_wav, resample_audio_to_16k, extract_audio_from_video
# from modules.utils import download_transcript
# from modules.huggingface_model import load_wav2vec2_model
# from modules.validators import (
#     is_valid_audio_url,
#     is_valid_video_url,
#     is_valid_image_url,
#     is_valid_document_url
# )
# from modules.speech_utils import is_speech_present
# from modules.image_handler import generate_image_caption
# from modules.document_handler import extract_text_from_document

# # --- Voice assistant modules ---
# # NOTE: assistant.run_voice_assistant_in_thread must not call Streamlit UI functions directly.
# from assistant import handle_voice_command, run_voice_assistant_in_thread, init_voice_assistant_controls
# from speech import take_command, talk, match_file_by_name_debug

# # --- file picker used by assistant too (pyautogui helper) ---
# from modules import file_picker

# # -------------------------------------------------------
# # CONFIG
# # -------------------------------------------------------
# DOWNLOADS_PATH = "/home/digi2/Downloads"

# # -------------------------------------------------------
# # PAGE CONFIG & STYLES
# # -------------------------------------------------------
# st.set_page_config(page_title="AI Multimedia Transcriber", layout="wide")
# st.title("🎤🖼️📄 AI Multimedia Transcriber (Audio / Video / Image / Document)")

# # Load custom CSS (if exists)
# try:
#     with open("static/css/style.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# except FileNotFoundError:
#     pass

# # -------------------------------------------------------
# # SESSION DEFAULTS
# # -------------------------------------------------------
# if "active_tab" not in st.session_state:
#     st.session_state["active_tab"] = "audio"  # "audio" | "video" | "image" | "document"

# if "last_voice_command" not in st.session_state:
#     st.session_state["last_voice_command"] = ""

# if "voice_audio_file_path" not in st.session_state:
#     st.session_state["voice_audio_file_path"] = None

# if "voice_video_file_path" not in st.session_state:
#     st.session_state["voice_video_file_path"] = None

# if "auto_transcribe_audio" not in st.session_state:
#     st.session_state["auto_transcribe_audio"] = False

# # -------------------------------------------------------
# # Small status strip & simple tab buttons (so we can programmatically switch)
# # -------------------------------------------------------
# cols = st.columns([1, 3, 2])
# with cols[0]:
#     st.markdown(
#         f"<div style='padding:8px 12px;border-radius:8px;background:#F0F2F6;display:inline-block;'>"
#         f"🔀 Active Tab: <b>{st.session_state['active_tab'].capitalize()}</b>"
#         f"</div>",
#         unsafe_allow_html=True,
#     )
# with cols[1]:
#     lvc = st.session_state.get("last_voice_command", "")
#     if lvc:
#         st.markdown(
#             f"<div style='padding:8px 12px;border-radius:8px;background:#F8F9FB;display:inline-block;margin-left:6px;'>"
#             f"🗣️ Last voice command: <code>{lvc}</code>"
#             f"</div>",
#             unsafe_allow_html=True,
#         )

# # Render a clickable tab bar (buttons). Buttons set session_state["active_tab"].
# tab_bar_cols = st.columns(4)
# if tab_bar_cols[0].button("🎤 Audio", key="btn_tab_audio"):
#     st.session_state["active_tab"] = "audio"
# if tab_bar_cols[1].button("🎬 Video", key="btn_tab_video"):
#     st.session_state["active_tab"] = "video"
# if tab_bar_cols[2].button("📷 Image", key="btn_tab_image"):
#     st.session_state["active_tab"] = "image"
# if tab_bar_cols[3].button("📄 Document", key="btn_tab_document"):
#     st.session_state["active_tab"] = "document"

# # Optional manual override radio (keeps in sync)
# with st.expander("Manual Tab Switch (override)"):
#     _ = st.radio(
#         "Select tab",
#         ["audio", "video", "image", "document"],
#         horizontal=True,
#         index=["audio", "video", "image", "document"].index(st.session_state["active_tab"]),
#         key="active_tab",
#     )

# # -------------------------------------------------------
# # ASR Model loader (cached)
# # -------------------------------------------------------
# @st.cache_resource
# def get_asr():
#     return load_wav2vec2_model()

# def transcribe_audio_bytes(audio_bytes: BytesIO, progress_prefix="Transcribing"):
#     """
#     Transcribe audio from BytesIO using cached Wav2Vec2 model.
#     """
#     audio_bytes.seek(0)
#     wav_io = resample_audio_to_16k(audio_bytes)
#     if wav_io is None:
#         raise RuntimeError("Failed to convert/resample audio to 16k WAV.")

#     wav_io.seek(0)
#     with sf.SoundFile(wav_io) as f:
#         audio_data = f.read(dtype="float32")
#         samplerate = f.samplerate

#     processor, model = get_asr()
#     inputs = processor(audio_data, sampling_rate=samplerate, return_tensors="pt", padding=True).input_values

#     predicted_ids = []
#     chunk_size = 16000 * 5  # 5-second chunks
#     start = 0
#     total_len = inputs.shape[1]

#     progress_bar = st.progress(0)
#     progress_text = st.empty()

#     while start < total_len:
#         end = min(start + chunk_size, total_len)
#         input_chunk = inputs[:, start:end]
#         with torch.no_grad():
#             logits = model(input_chunk).logits
#         preds = torch.argmax(logits, dim=-1)
#         predicted_ids.extend(
#             preds.squeeze().tolist() if isinstance(preds.squeeze().tolist(), list) else [preds.squeeze().tolist()]
#         )
#         start = end
#         pct = min(int(start / total_len * 100), 100)
#         progress_bar.progress(pct)
#         progress_text.text(f"⏳ {progress_prefix}... {pct}%")

#     try:
#         transcript = processor.decode(predicted_ids)
#     except Exception:
#         import torch as _torch
#         transcript = processor.batch_decode(_torch.tensor([predicted_ids]))[0]

#     progress_bar.progress(100)
#     progress_text.text(f"✅ {progress_prefix} complete")
#     return transcript.strip()

# # -------------------------------------------------------
# # Voice Assistant Controls (Start/Stop) - sidebar
# # -------------------------------------------------------
# init_voice_assistant_controls()

# # -------------------------------------------------------
# # Helper: listen-once button for filename (UI-driven)
# # -------------------------------------------------------
# def ui_listen_for_filename(file_type="audio"):
#     """
#     Trigger a single microphone capture (non-background) to listen for a filename.
#     This avoids continuously blocking on each rerun.
#     """
#     try:
#         spoken = take_command(timeout=5, phrase_time_limit=6)
#     except Exception as e:
#         st.error(f"Microphone error: {e}")
#         return None

#     if not spoken:
#         st.warning("No voice input detected.")
#         return None

#     st.session_state["last_voice_command"] = spoken

#     if file_type == "audio":
#         matched = match_file_by_name_debug(spoken, file_type="audio")
#         if matched:
#             st.success(f"Matched audio file: {matched}")
#             st.session_state["voice_audio_file_path"] = matched
#             # put the result into session_state so audio tab will pick it up
#             st.session_state["auto_transcribe_audio"] = True
#             # switch to audio tab
#             st.session_state["active_tab"] = "audio"
#     elif file_type == "video":
#         matched = match_file_by_name_debug(spoken, file_type="video")
#         if matched:
#             st.success(f"Matched video file: {matched}")
#             st.session_state["voice_video_file_path"] = matched
#             st.session_state["active_tab"] = "video"

# # -------------------------------------------------------
# # Tab content rendering (reactive to session_state["active_tab"])
# # -------------------------------------------------------

# # AUDIO TAB
# if st.session_state["active_tab"] == "audio":
#     st.header("Audio Transcriber")

#     # Button: Listen for filename (one-time)
#     col_listen = st.columns([1, 3, 2])
#     with col_listen[0]:
#         if st.button("🎧 Listen for audio filename (once)", key="listen_audio_btn"):
#             ui_listen_for_filename(file_type="audio")

#     # If assistant or UI has put a file path into session_state, load it
#     audio_file_bytes = None
#     voice_path = st.session_state.get("voice_audio_file_path")
#     if voice_path and os.path.exists(voice_path):
#         audio_file_bytes = convert_to_wav(BytesIO(open(voice_path, "rb").read()))
#         # reset voice path only after showing so repeated clicks won't auto-run forever (you can change this)
#         # we'll leave it set until transcription completes
#         st.info(f"Loaded voice-picked file: {os.path.basename(voice_path)}")

#     # Manual upload / URL fallback
#     uploaded_audio = st.file_uploader(
#         "Upload Audio File",
#         type=["wav","mp3","m4a","ogg","flac","aac"],
#         key="audio_uploader"
#     )
#     audio_url = st.text_input("Or enter audio URL", key="audio_url")

#     if uploaded_audio:
#         audio_file_bytes = convert_to_wav(BytesIO(uploaded_audio.read()))
#         st.audio(audio_file_bytes)

#     elif audio_url and is_valid_audio_url(audio_url.strip()):
#         try:
#             resp = requests.get(audio_url.strip())
#             audio_file_bytes = convert_to_wav(BytesIO(resp.content))
#             st.audio(audio_file_bytes)
#         except Exception as e:
#             st.error(f"❌ Failed to load audio from URL: {e}")

#     # If a voice-picked file exists and auto_transcribe flag is true, transcribe now
#     if audio_file_bytes and st.session_state.get("auto_transcribe_audio", False):
#         try:
#             transcript = transcribe_audio_bytes(audio_file_bytes, progress_prefix="Transcribing audio")
#             st.text_area("✅ Transcript", transcript, height=300)
#             download_transcript(transcript, filename="audio_transcript.txt")
#         except Exception as e:
#             st.error(f"⚠️ Transcription failed: {e}")
#         finally:
#             # reset auto flag and voice path after done
#             st.session_state["auto_transcribe_audio"] = False
#             st.session_state["voice_audio_file_path"] = None

#     # Manual Transcribe button (if user prefers)
#     if audio_file_bytes and st.button("Transcribe Audio (Manual)"):
#         try:
#             transcript = transcribe_audio_bytes(audio_file_bytes, progress_prefix="Transcribing audio")
#             st.text_area("✅ Transcript", transcript, height=300)
#             download_transcript(transcript, filename="audio_transcript.txt")
#         except Exception as e:
#             st.error(f"⚠️ Transcription failed: {e}")

# else:
#     # show hint when other tab active
#     st.info("Switch to the Audio tab (top bar or manual radio) to use the Audio Transcriber.")




# # VIDEO TAB
# if st.session_state["active_tab"] == "video":
#     st.header("Video Transcriber")

#     # Listen for video filename (one-time)
#     col_listen_v = st.columns([1, 3, 2])
#     with col_listen_v[0]:
#         if st.button("🎬 Listen for video filename (once)", key="listen_video_btn"):
#             ui_listen_for_filename(file_type="video")

#     video_file_bytes = st.session_state.get("video_bytes", None)
#     voice_video_path = st.session_state.get("voice_video_file_path", None)

#     # If voice video path provided by voice file picker, load it
#     if voice_video_path and os.path.exists(voice_video_path):
#         video_file_bytes = BytesIO(open(voice_video_path, "rb").read())
#         st.info(f"Loaded voice-picked video: {os.path.basename(voice_video_path)}")

#     uploaded_video = st.file_uploader(
#         "Upload Video File",
#         type=["mp4", "mov", "mkv", "avi", "webm"],
#         key="video_uploader"
#     )
#     video_url = st.text_input("Or enter video URL", key="video_url")

#     if uploaded_video:
#         video_file_bytes = BytesIO(uploaded_video.read())

#     elif video_url and is_valid_video_url(video_url.strip()):
#         try:
#             resp = requests.get(video_url.strip())
#             video_file_bytes = BytesIO(resp.content)
#         except Exception as e:
#             st.error(f"❌ Failed to load video from URL: {e}")

#     elif st.session_state.get("video_bytes"):
#         video_file_bytes = st.session_state.get("video_bytes")

#     if video_file_bytes:
#         st.video(video_file_bytes)
#         try:
#             audio_bytes = extract_audio_from_video(video_file_bytes)
#             if audio_bytes is None:
#                 st.warning("⚠️ No audio track found in this video.")
#             else:
#                 st.audio(audio_bytes)
#                 if not is_speech_present(audio_bytes):
#                     st.warning("⚠️ No speech detected in video audio.")
#                 else:
#                     if st.button("Transcribe Video Audio"):
#                         transcript = transcribe_audio_bytes(audio_bytes, progress_prefix="Transcribing video audio")
#                         st.text_area("✅ Transcript", transcript, height=300)
#                         download_transcript(transcript, filename="video_transcript.txt")
#         except Exception as e:
#             st.error(f"⚠️ Failed to extract audio / process video: {e}")

# else:
#     st.info("Switch to the Video tab (top bar or manual radio) to use the Video Transcriber.")

# # IMAGE TAB
# if st.session_state["active_tab"] == "image":
#     st.header("Image Transcriber")
#     image_file = None

#     uploaded_image = st.file_uploader(
#         "Upload Image",
#         type=["jpg", "jpeg", "png", "bmp", "gif", "webp"],
#         key="image_uploader"
#     )
#     image_url = st.text_input("Or enter image URL", key="image_input_url")

#     if uploaded_image:
#         image_file = Image.open(uploaded_image).convert("RGB")
#     elif image_url and is_valid_image_url(image_url.strip()):
#         try:
#             resp = requests.get(image_url.strip())
#             image_file = Image.open(BytesIO(resp.content)).convert("RGB")
#         except Exception as e:
#             st.error(f"❌ Failed to load image from URL: {e}")
#     elif st.session_state.get("image_bytes"):
#         image_file = Image.open(st.session_state.get("image_bytes")).convert("RGB")

#     if image_file:
#         st.image(image_file, caption="📷 Uploaded Image", use_column_width=False)
#         if st.button("Generate Caption & Description"):
#             try:
#                 caption_text = generate_image_caption(image_file)
#                 st.markdown(f"**📝 Caption:** {caption_text}")
#                 st.markdown(f"📄 **Detailed Description:**\n{caption_text}")
#                 try:
#                     talk("Image caption generated.")
#                 except Exception:
#                     pass
#             except Exception as e:
#                 st.error(f"⚠️ Image captioning failed: {e}")
# else:
#     st.info("Switch to the Image tab (top bar or manual radio) to use the Image Transcriber.")


# # DOCUMENT TAB
# if st.session_state["active_tab"].lower() == "document":
#     st.subheader("📄 Document Transcriber")
#     doc_text = None

#     # --- Upload or URL input ---
#     uploaded_doc = st.file_uploader(
#         "Upload a document", 
#         type=["pdf", "docx", "txt"], 
#         key="doc_uploader"
#     )
#     doc_url = st.text_input("Or enter document URL", key="doc_url")

#     # --- Case 1: Uploaded document ---
#     if uploaded_doc is not None:
#         try:
#             # Save to disk (avoids BytesIO extraction issues)
#             doc_path = os.path.join("uploads", uploaded_doc.name)
#             os.makedirs("uploads", exist_ok=True)
#             with open(doc_path, "wb") as f:
#                 f.write(uploaded_doc.getbuffer())

#             st.success(f"📂 Document uploaded: {uploaded_doc.name}")
#             with st.spinner("🔍 Extracting text..."):
#                 doc_text = extract_text_from_document(doc_path)  # ✅ Path-based extraction
#         except Exception as e:
#             st.error(f"⚠️ Document extraction failed: {e}")

#     # --- Case 2: Document via URL ---
#     elif doc_url and is_valid_document_url(doc_url.strip()):
#         try:
#             resp = requests.get(doc_url.strip())
#             if resp.status_code == 200:
#                 doc_path = os.path.join("uploads", "url_document")
#                 with open(doc_path, "wb") as f:
#                     f.write(resp.content)
#                 with st.spinner("🔍 Extracting text from URL..."):
#                     doc_text = extract_text_from_document(doc_path)
#             else:
#                 st.error("⚠️ Failed to fetch document from URL.")
#         except Exception as e:
#             st.error(f"⚠️ Document extraction failed: {e}")

#     # --- Case 3: Previous session document ---
#     elif st.session_state.get("doc_bytes"):
#         try:
#             doc_path = os.path.join("uploads", "session_document")
#             with open(doc_path, "wb") as f:
#                 f.write(st.session_state["doc_bytes"].getvalue())
#             with st.spinner("🔍 Extracting text from session file..."):
#                 doc_text = extract_text_from_document(doc_path)
#         except Exception as e:
#             st.error(f"⚠️ Document extraction failed: {e}")

#     # --- Display Extracted Text ---
#     if doc_text:
#         st.text_area("📄 Extracted Document Text", doc_text, height=400)
#         download_transcript(doc_text, filename="document_text.txt")

# else:
#     st.info("Switch to the Document tab to use the Document Transcriber.")


#-------------------------------------------------------------------------------------------------------------------------

# app.py (UPDATED)
# import os
# from io import BytesIO
# import threading
# import time
# import requests
# import textwrap

# import streamlit as st
# import torch
# import soundfile as sf
# from PIL import Image

# # Ensure moviepy/ffmpeg temp dir (reduce failures)
# TMP_DIR = os.environ.get("TMPDIR", os.path.expanduser("~/tmp_streamlit"))
# os.makedirs(TMP_DIR, exist_ok=True)
# os.environ["TMPDIR"] = TMP_DIR

# # ----------------------------
# # Local modules (must exist)
# # ----------------------------
# from modules.audio_handler import convert_to_wav, resample_audio_to_16k, extract_audio_from_video, load_audio_file, download_audio_from_url, load_video_file, download_video_from_url
# from modules.validators import is_valid_audio_url, is_valid_video_url, is_valid_image_url, is_valid_document_url
# from modules.speech_utils import is_speech_present
# from modules.image_handler import generate_image_caption
# from modules.document_handler import extract_text_from_document
# from modules.huggingface_model import load_wav2vec2_model, load_image_caption_model
# # voice & speech UI helpers
# import speech as speech_mod
# import assistant as assistant_mod
# import ai_agent as ai_agent_mod  # uses Gemini; wrapped in try/except inside
# from modules.utils import download_transcript

# # ----------------------------
# # Page config
# # ----------------------------
# st.set_page_config(page_title="Accessible Media (Audio/Video/Image/Document)", layout="wide")
# st.title("Accessible Media — Manual & Voice Interfaces")

# # -------------------------------------------------------
# # Session state defaults
# # -------------------------------------------------------
# if "active_tab" not in st.session_state:
#     st.session_state["active_tab"] = "audio"
# if "last_voice_command" not in st.session_state:
#     st.session_state["last_voice_command"] = ""
# if "voice_assistant_running" not in st.session_state:
#     st.session_state["voice_assistant_running"] = False
# if "auto_transcribe_audio" not in st.session_state:
#     st.session_state["auto_transcribe_audio"] = False
# if "voice_audio_file_path" not in st.session_state:
#     st.session_state["voice_audio_file_path"] = None
# if "voice_video_file_path" not in st.session_state:
#     st.session_state["voice_video_file_path"] = None
# if "doc_highlight_index" not in st.session_state:
#     st.session_state["doc_highlight_index"] = 0
# if "doc_lines" not in st.session_state:
#     st.session_state["doc_lines"] = []
# if "audio_bytes" not in st.session_state:
#     st.session_state["audio_bytes"] = None
# if "video_bytes" not in st.session_state:
#     st.session_state["video_bytes"] = None
# if "image_bytes" not in st.session_state:
#     st.session_state["image_bytes"] = None
# if "doc_bytes" not in st.session_state:
#     st.session_state["doc_bytes"] = None

# # -------------------------------------------------------
# # Small utilities
# # -------------------------------------------------------
# def safe_set_state(key, value):
#     try:
#         st.session_state[key] = value
#     except Exception:
#         # if background thread cannot write to session, fallback to printing
#         print(f"[safe_set_state] cannot set {key}")

# def load_bytes_from_url(url: str) -> BytesIO:
#     """
#     Download a URL into an in-memory BytesIO. Raises on network errors.
#     """
#     resp = requests.get(url, timeout=20)
#     resp.raise_for_status()
#     return BytesIO(resp.content)

# # -------------------------------------------------------
# # ASR model loader (cached)
# # -------------------------------------------------------
# @st.cache_resource
# def get_asr_models():
#     """Return processor, model for Wav2Vec2 and BLIP models for images."""
#     # load_wav2vec2_model and load_image_caption_model should be cached in their modules as appropriate
#     wav_proc, wav_model = load_wav2vec2_model()
#     _, _ = load_image_caption_model()  # warm image caption models as needed
#     return wav_proc, wav_model

# # -------------------------------------------------------
# # Transcription helper (in-memory)
# # -------------------------------------------------------
# def transcribe_audio_bytes_in_memory(audio_bytes: BytesIO, progress_prefix="Transcribing"):
#     """
#     Transcribe BytesIO audio using Wav2Vec2. Expects audio_bytes to be readable.
#     """
#     audio_bytes.seek(0)
#     wav16 = resample_audio_to_16k(audio_bytes)
#     if wav16 is None:
#         raise RuntimeError("Unable to resample/convert to 16k WAV for ASR.")
#     wav16.seek(0)
#     with sf.SoundFile(wav16) as f:
#         audio = f.read(dtype="float32")
#         sr = f.samplerate

#     processor, model = get_asr_models()
#     inputs = processor(audio, sampling_rate=sr, return_tensors="pt", padding=True).input_values

#     # chunking by frames to avoid OOM
#     chunk_frames = 16000 * 5  # 5s chunks
#     start = 0
#     parts = []
#     progress_bar = st.progress(0)
#     progress_text = st.empty()
#     total = inputs.shape[1]
#     while start < total:
#         end = min(start + chunk_frames, total)
#         chunk = inputs[:, start:end]
#         with torch.no_grad():
#             logits = model(chunk).logits
#         pred_ids = torch.argmax(logits, dim=-1)
#         # pred_ids is shape (1, seq)
#         # decode chunk and append
#         try:
#             decoded = processor.batch_decode(pred_ids)[0]
#         except Exception:
#             decoded = processor.decode(pred_ids.squeeze().tolist())
#         parts.append(decoded)
#         start = end
#         pct = int(min(100, start / total * 100))
#         progress_bar.progress(pct)
#         progress_text.text(f"⏳ {progress_prefix}... {pct}%")
#     progress_bar.progress(100)
#     progress_text.text("✅ Complete")
#     return " ".join([p.strip() for p in parts]).strip()

# # -------------------------------------------------------
# # Document reading + line-by-line highlight + TTS summary
# # -------------------------------------------------------
# def display_and_read_document_from_bytes(doc_bytes: BytesIO, filename: str = "document"):
#     """
#     Extract text from document bytes (PDF/DOCX/TXT), display it with a line-by-line highlighter,
#     then produce a 5-6 line Gemini summary and speak it.
#     Operates in-memory only (no persistent disk write).
#     """
#     # extract_text_from_document supports file-like objects (we expect BytesIO and filename)
#     try:
#         # Ensure BytesIO pointer at start
#         doc_bytes.seek(0)
#         # Our extract_text_from_document expects (file_obj, filename) if updated earlier; if not, handle both cases
#         try:
#             text = extract_text_from_document(doc_bytes, filename)
#         except TypeError:
#             # fall back to older signature (file_path); attempt to load via PyPDF2/docx from BytesIO directly here
#             # Implement an in-place extractor:
#             from io import BytesIO
#             from PyPDF2 import PdfReader
#             import docx
#             name = filename.lower()
#             if name.endswith(".pdf"):
#                 reader = PdfReader(doc_bytes)
#                 pages = []
#                 for p in reader.pages:
#                     ptext = p.extract_text() or ""
#                     pages.append(ptext)
#                 text = "\n".join(pages)
#             elif name.endswith(".docx"):
#                 doc = docx.Document(doc_bytes)
#                 text = "\n".join([p.text for p in doc.paragraphs])
#             elif name.endswith(".txt"):
#                 doc_bytes.seek(0)
#                 text = doc_bytes.read().decode("utf-8", errors="ignore")
#             else:
#                 raise RuntimeError("Unsupported document type for extraction.")
#         text = text.strip()
#         if not text:
#             st.warning("No extractable text found in document.")
#             return
#     except Exception as e:
#         st.error(f"Document extraction failed: {e}")
#         return

#     # Split into lines for highlighting
#     lines = [ln for ln in text.splitlines() if ln.strip() != ""]
#     if not lines:
#         st.warning("Document contained no readable lines.")
#         return

#     # store lines in session for highlight control
#     st.session_state["doc_lines"] = lines
#     st.session_state["doc_highlight_index"] = 0

#     placeholder = st.empty()

#     # Function to render with current highlight index
#     def render_highlight(idx):
#         rendered = []
#         for i, ln in enumerate(lines):
#             if i == idx:
#                 # highlight style (accessible)
#                 rendered.append(f"<div style='background: #fff3cd; padding:8px; border-left:4px solid #f39c12; border-radius:4px; margin-bottom:4px;'>"
#                                 f"<strong>{ln}</strong></div>")
#             else:
#                 rendered.append(f"<div style='padding:6px; margin-bottom:2px;'>{ln}</div>")
#         placeholder.markdown("\n".join(rendered), unsafe_allow_html=True)

#     # Show controls to step through / auto-read
#     ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1,1,1])
#     with ctrl_col1:
#         if st.button("Play (speak) document"):
#             # speak whole document line-by-line and highlight
#             for idx, ln in enumerate(lines):
#                 st.session_state["doc_highlight_index"] = idx
#                 render_highlight(idx)
#                 # speak the line (non-blocking to UI? we call talk which tries TTS)
#                 try:
#                     speech_mod.talk(ln)
#                 except Exception:
#                     pass
#                 time.sleep(0.06)  # small pacing
#     with ctrl_col2:
#         if st.button("Auto-scroll & speak (slow)"):
#             for idx, ln in enumerate(lines):
#                 st.session_state["doc_highlight_index"] = idx
#                 render_highlight(idx)
#                 try:
#                     speech_mod.talk(ln)
#                 except Exception:
#                     pass
#                 time.sleep(0.5)
#     with ctrl_col3:
#         if st.button("Stop / Reset highlight"):
#             st.session_state["doc_highlight_index"] = 0
#             render_highlight(0)

#     # show full text for convenience below
#     st.text_area("📄 Extracted Text", "\n".join(lines), height=300)

#     # Generate Gemini summary (5-6 lines) and speak it
#     try:
#         summary_prompt = textwrap.shorten(text, width=4000, placeholder="")  # limit input
#         summary_prompt = f"Summarize the following document in 5–6 short lines. Be concise and clear:\n\n{summary_prompt}"
#         try:
#             ai_answer = ai_agent_mod.ask_ai(summary_prompt)
#             # ai_agent may return very long text; keep to ~5 sentences
#             if ai_answer:
#                 # trim to 5-6 lines (split by sentences)
#                 sentences = [s.strip() for s in ai_answer.replace("\n", " ").split(". ") if s.strip()]
#                 summary_lines = ". ".join(sentences[:6]).strip()
#             else:
#                 summary_lines = "No AI summary available."
#         except Exception as e:
#             summary_lines = "[Gemini unavailable — unable to generate summary.]"
#     except Exception:
#         summary_lines = "[Summary generation failed.]"

#     # show summary and speak it
#     st.markdown("**🔎 Gemini Summary (brief):**")
#     st.markdown(f"> {summary_lines}")
#     try:
#         speech_mod.talk(f"Document summary: {summary_lines}")
#     except Exception:
#         pass

# # -------------------------------------------------------
# # Simple toolbar & voice assistant controls
# # -------------------------------------------------------
# st.sidebar.title("Voice Assistant")
# start_voice = st.sidebar.button("Start assistant (background)")
# stop_voice = st.sidebar.button("Stop assistant")
# # also allow the user to listen once for a command
# listen_once = st.sidebar.button("Listen once (process command)")

# if start_voice:
#     if not st.session_state["voice_assistant_running"]:
#         # start assistant background thread via assistant_mod (it uses safe_set_session internally)
#         try:
#             assistant_mod.init_voice_assistant_controls()  # ensure controls present
#         except Exception:
#             pass
#         # start thread
#         evt = threading.Event()
#         t = threading.Thread(target=assistant_mod.run_voice_assistant_in_thread, args=(evt,), daemon=True)
#         t.start()
#         safe_set_state("assistant_stop_event", evt)
#         safe_set_state("assistant_thread", t)
#         st.session_state["voice_assistant_running"] = True
#         st.sidebar.success("Voice assistant started.")
#     else:
#         st.sidebar.info("Assistant already running.")

# if stop_voice:
#     if st.session_state["voice_assistant_running"]:
#         evt = st.session_state.get("assistant_stop_event")
#         if evt:
#             evt.set()
#         st.session_state["voice_assistant_running"] = False
#         st.sidebar.info("Voice assistant stopped.")
#     else:
#         st.sidebar.info("Assistant was not running.")

# if listen_once:
#     # capture mic input once, run it through speech.take_command() -> then try to apply intent
#     cmd = speech_mod.take_command(timeout=6, phrase_time_limit=7)
#     if cmd:
#         st.session_state["last_voice_command"] = cmd
#         st.success(f"Detected: {cmd}")
#         # try to switch tab if requested
#         tab = speech_mod.switch_tab_from_command(cmd)
#         if tab:
#             st.session_state["active_tab"] = tab
#             st.success(f"Switched to {tab} tab (voice).")
#         else:
#             # attempt file pick actions (audio/video/image/document)
#             # we attempt audio/video first
#             # get filename candidate
#             matched_audio = speech_mod.match_file_by_name(cmd, file_type="audio")
#             if matched_audio:
#                 st.success(f"Matched audio: {matched_audio}")
#                 # load in-memory and set flag to auto transcribe
#                 st.session_state["audio_bytes"] = convert_to_wav(BytesIO(open(matched_audio, "rb").read()))
#                 st.session_state["auto_transcribe_audio"] = True
#                 st.session_state["active_tab"] = "audio"
#             else:
#                 matched_video = speech_mod.match_file_by_name(cmd, file_type="video")
#                 if matched_video:
#                     st.success(f"Matched video: {matched_video}")
#                     st.session_state["video_bytes"] = BytesIO(open(matched_video, "rb").read())
#                     st.session_state["active_tab"] = "video"
#                 else:
#                     matched_image = speech_mod.match_file_by_name(cmd, file_type="image")
#                     if matched_image:
#                         st.success(f"Matched image: {matched_image}")
#                         st.session_state["image_bytes"] = BytesIO(open(matched_image, "rb").read())
#                         st.session_state["active_tab"] = "image"
#                     else:
#                         matched_doc = speech_mod.match_file_by_name(cmd, file_type="document")
#                         if matched_doc:
#                             st.success(f"Matched document: {matched_doc}")
#                             st.session_state["doc_bytes"] = BytesIO(open(matched_doc, "rb").read())
#                             st.session_state["active_tab"] = "document"
#                         else:
#                             st.info("No matching file found in Downloads for that command.")

# # -------------------------------------------------------
# # Tab bar as buttons (also set active_tab)
# # -------------------------------------------------------
# tabs_cols = st.columns([1,1,1,1])
# if tabs_cols[0].button("Audio"):
#     st.session_state["active_tab"] = "audio"
# if tabs_cols[1].button("Video"):
#     st.session_state["active_tab"] = "video"
# if tabs_cols[2].button("Image"):
#     st.session_state["active_tab"] = "image"
# if tabs_cols[3].button("Document"):
#     st.session_state["active_tab"] = "document"

# # -------------------------------------------------------
# # AUDIO TAB
# # -------------------------------------------------------
# if st.session_state["active_tab"] == "audio":
#     st.header("Audio — Upload or URL (Manual) / Voice pick (Hands-free)")

#     # Voice-picked bytes (from listen_once flow)
#     audio_bytes = st.session_state.get("audio_bytes")

#     # Uploader / URL fields
#     uploaded_audio = st.file_uploader("Upload audio file", type=["wav","mp3","m4a","ogg","flac","aac"], key="aupload")
#     audio_url = st.text_input("Or enter audio URL", key="audio_url_input")

#     # URL handling (download into memory and convert)
#     if audio_url:
#         if is_valid_audio_url(audio_url.strip()):
#             try:
#                 audio_bytes = download_audio_from_url(audio_url.strip())
#                 if audio_bytes:
#                     st.audio(audio_bytes)
#                     st.success("Loaded audio from URL.")
#             except Exception as e:
#                 st.error(f"Failed to load audio URL: {e}")
#         else:
#             st.warning("Provided URL is not a valid audio link, or unreachable.")

#     # Uploaded handling
#     if uploaded_audio:
#         try:
#             audio_bytes = convert_to_wav(BytesIO(uploaded_audio.read()))
#             st.audio(audio_bytes)
#         except Exception as e:
#             st.error(f"Failed to read uploaded audio: {e}")

#     # If audio bytes present and auto flag true -> auto transcribe
#     if audio_bytes and st.session_state.get("auto_transcribe_audio", False):
#         try:
#             st.info("Auto-transcribing audio...")
#             transcript = transcribe_audio_bytes_in_memory(audio_bytes, progress_prefix="Transcribing audio (auto)")
#             st.text_area("Transcript", transcript, height=300)
#             download_transcript(transcript, filename="audio_transcript.txt")
#         except Exception as e:
#             st.error(f"Transcription failed: {e}")
#         finally:
#             st.session_state["auto_transcribe_audio"] = False
#             st.session_state["audio_bytes"] = None

#     # Manual transcribe button
#     if audio_bytes and st.button("Transcribe now"):
#         try:
#             transcript = transcribe_audio_bytes_in_memory(audio_bytes, progress_prefix="Transcribing audio")
#             st.text_area("Transcript", transcript, height=300)
#             download_transcript(transcript, filename="audio_transcript.txt")
#         except Exception as e:
#             st.error(f"Transcription failed: {e}")

# # -------------------------------------------------------
# # VIDEO TAB
# # -------------------------------------------------------
# elif st.session_state["active_tab"] == "video":
#     st.header("Video — Upload or URL (Manual) / Voice pick")

#     # bytes
#     video_bytes = st.session_state.get("video_bytes")

#     uploaded_video = st.file_uploader("Upload video file", type=["mp4","mov","mkv","avi","webm"], key="vupload")
#     video_url = st.text_input("Or enter video URL", key="video_url_input")

#     if video_url:
#         if is_valid_video_url(video_url.strip()):
#             try:
#                 video_bytes = download_video_from_url(video_url.strip())
#                 if video_bytes:
#                     st.success("Loaded video from URL.")
#             except Exception as e:
#                 st.error(f"Failed to download video URL: {e}")
#         else:
#             st.warning("Provided URL is not a valid video link or unreachable.")

#     if uploaded_video:
#         try:
#             video_bytes = BytesIO(uploaded_video.read())
#             st.video(video_bytes)
#         except Exception as e:
#             st.error(f"Failed to read uploaded video: {e}")

#     if video_bytes:
#         st.video(video_bytes)
#         # extract audio in-memory
#         try:
#             audio_from_video = extract_audio_from_video(video_bytes)
#             if audio_from_video is None:
#                 st.warning("No audio track found in this video.")
#             else:
#                 st.audio(audio_from_video)
#                 # detect speech
#                 has_speech, ratio = True, None
#                 try:
#                     has_speech, ratio = is_speech_present(audio_from_video)
#                 except Exception:
#                     has_speech = True
#                 if not has_speech:
#                     st.warning("This video appears to contain no speech.")
#                 else:
#                     if st.button("Transcribe video audio"):
#                         try:
#                             transcript = transcribe_audio_bytes_in_memory(audio_from_video, progress_prefix="Transcribing video audio")
#                             st.text_area("Transcript", transcript, height=300)
#                             download_transcript(transcript, filename="video_transcript.txt")
#                         except Exception as e:
#                             st.error(f"Video transcription failed: {e}")
#         except Exception as e:
#             st.error(f"Failed to extract/process video: {e}")

# # -------------------------------------------------------
# # IMAGE TAB
# # -------------------------------------------------------
# elif st.session_state["active_tab"] == "image":
#     st.header("Image — Upload or URL (Manual) / Voice pick")

#     image_bytes = st.session_state.get("image_bytes")
#     uploaded_image = st.file_uploader("Upload image file", type=["jpg","jpeg","png","bmp","gif","webp"], key="iupload")
#     image_url = st.text_input("Or enter image URL", key="image_url_input")

#     if image_url:
#         if is_valid_image_url(image_url.strip()):
#             try:
#                 image_bytes = load_bytes_from_url(image_url.strip())
#                 st.success("Loaded image from URL.")
#             except Exception as e:
#                 st.error(f"Failed to load image URL: {e}")
#         else:
#             st.warning("Provided URL is not a valid image link.")

#     if uploaded_image:
#         try:
#             image_bytes = BytesIO(uploaded_image.read())
#         except Exception as e:
#             st.error(f"Failed to read uploaded image: {e}")

#     if image_bytes:
#         try:
#             image_obj = Image.open(BytesIO(image_bytes.getvalue())).convert("RGB")
#             st.image(image_obj, caption="Uploaded image", use_column_width=False)
#             if st.button("Generate caption & description"):
#                 caption = generate_image_caption(image_obj)
#                 st.markdown(f"**📝 Caption:** {caption}")
#                 # also produce a short plain description (could be same as caption)
#                 st.markdown(f"**📄 Description:**\n{caption}")
#                 try:
#                     speech_mod.talk("Image caption generated.")
#                 except Exception:
#                     pass
#         except Exception as e:
#             st.error(f"Failed to display/process image: {e}")

# # -------------------------------------------------------
# # DOCUMENT TAB
# # -------------------------------------------------------
# elif st.session_state["active_tab"] == "document":
#     st.header("Document — Upload or URL (Manual) / Voice pick")

#     doc_bytes = st.session_state.get("doc_bytes")
#     uploaded_doc = st.file_uploader("Upload document (PDF/DOCX/TXT)", type=["pdf","docx","txt"], key="dupload")
#     doc_url = st.text_input("Or enter document URL", key="doc_url_input")

#     if doc_url:
#         if is_valid_document_url(doc_url.strip()):
#             try:
#                 doc_bytes = load_bytes_from_url(doc_url.strip())
#                 st.success("Loaded document from URL.")
#             except Exception as e:
#                 st.error(f"Failed to download document URL: {e}")
#         else:
#             st.warning("Provided URL is not a valid document link.")

#     if uploaded_doc:
#         try:
#             doc_bytes = BytesIO(uploaded_doc.read())
#             st.success("Uploaded document.")
#         except Exception as e:
#             st.error(f"Failed to read uploaded document: {e}")

#     if doc_bytes:
#         # display filename input to tell extractor the type
#         doc_name = st.text_input("Document filename (e.g. cosmos.pdf) — helps extraction", value="document.pdf")
#         if st.button("Extract, highlight & read document"):
#             display_and_read_document_from_bytes(doc_bytes, filename=doc_name)

# # -------------------------------------------------------
# # Footer/help
# # -------------------------------------------------------
# st.markdown("---")
# st.markdown(
#     "Tips: Use **Listen once** in the sidebar to speak commands (e.g. 'Audio Tab', 'upload george.mp3 file'). "
#     "If continuous assistant is used, it will listen in background — but you can also use the single 'Listen once' to ensure immediate tab switching."
# )



#-------------------------------------------------------------------------------------------------------------------------------------

# app.py (FULL updated file)
import torch
import io
from modules.document_handler import extract_text_from_document, highlight_text_live

import os
os.environ["TMPDIR"] = os.environ.get("TMPDIR", "/tmp")  # let system decide; override early if you want

from io import BytesIO
import threading
import time
import queue
import requests
import re
import traceback
# import openai 

import streamlit as st
from PIL import Image
import soundfile as sf

# Local modules (assumed memory-based implementations)
from modules.audio_handler import (
    load_audio_file,
    download_audio_from_url,
    convert_to_wav,
    resample_audio_to_16k,
)
from modules.video_utils import extract_audio_from_video
from modules.image_handler import load_image, generate_image_caption
from modules.document_handler import extract_text_from_document
from modules.validators import (
    is_valid_audio_url,
    is_valid_video_url,
    is_valid_image_url,
    is_valid_document_url,
)
from modules.speech_utils import is_speech_present
from modules.huggingface_model import load_wav2vec2_model, load_image_caption_model
import modules.file_picker as file_picker  # used by UI voice file pickers

# Optional AI summarizer
try:
    import ai_agent  # ai_agent.ask_ai(text) -> summary (5-6 lines)
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False

# TTS (best-effort)
try:
    import pyttsx3

    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 160)
except Exception:
    tts_engine = None


# ----------------------------
# Utility helpers (in-memory only)
# ----------------------------
def speak_text(text: str):
    """Best-effort speak (pyttsx3). Non-fatal on failure."""
    if not text:
        return
    if tts_engine is None:
        return
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception:
        # non-fatal
        pass


def safe_requests_get(url: str, timeout: int = 15) -> bytes:
    """Download URL content into bytes — returns bytes or raises."""
    resp = requests.get(url, stream=True, timeout=timeout)
    resp.raise_for_status()
    return resp.content


def youtube_extract_audio_bytes(url: str) -> BytesIO:
    """
    Try to extract audio from YouTube-like URLs using yt_dlp into BytesIO.
    If yt_dlp isn't available or fails, raises Exception.
    """
    try:
        import yt_dlp
    except Exception as e:
        raise RuntimeError("yt_dlp not available") from e

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": "-",  # pipe
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "wav", "preferredquality": "192"}
        ],
        "noplaylist": True,
        "cachedir": False,
    }

    buf = BytesIO()
    # Use a temporary file approach but keep final result in memory
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # We'll download into a temp file because streaming piping to memory is complicated;
        # but we avoid keeping it permanently by reading into memory and deleting temp file.
        with ydl:
            # create a temp file and let yt_dlp write into it (internal behavior)
            result = ydl.extract_info(url, download=True)
            # seek into the downloaded file path
            # Unfortunately, exact behavior differs by backend — raise if not found
            # In many environments, ydl will produce a local file in cwd; find latest .wav/.mp3
            raise RuntimeError("yt_dlp extraction succeeded but in-memory path not implemented here")
    # If we reach here, fallback
    raise RuntimeError("YouTube audio extraction not implemented in this environment")


# ----------------------------
# Voice command queue + listener thread
# ----------------------------
VOICE_QUEUE = queue.Queue()
VOICE_THREAD = None
VOICE_THREAD_STOP = threading.Event()


def voice_listener_loop(stop_event: threading.Event, put_queue: queue.Queue):
    """
    Background loop: listen once at a time using speech.take_command (if available).
    Puts recognized raw text into put_queue. This avoids updating streamlit session_state from background threads.
    """
    try:
        # import local speech utilities if available
        from speech import take_command, talk as _talk
    except Exception:
        # If speech module not available, exit thread
        return

    # initial announcement (best-effort)
    try:
        _talk("Voice assistant started.")
    except Exception:
        pass

    while not stop_event.is_set():
        try:
            cmd = take_command(timeout=6, phrase_time_limit=8)
            if cmd:
                put_queue.put(cmd)
        except Exception:
            # swallow exceptions so thread continues
            pass
        time.sleep(0.2)


def start_voice_listener():
    global VOICE_THREAD, VOICE_THREAD_STOP
    if VOICE_THREAD and VOICE_THREAD.is_alive():
        return False
    VOICE_THREAD_STOP.clear()
    VOICE_THREAD = threading.Thread(target=voice_listener_loop, args=(VOICE_THREAD_STOP, VOICE_QUEUE), daemon=True)
    VOICE_THREAD.start()
    return True


def stop_voice_listener():
    global VOICE_THREAD, VOICE_THREAD_STOP
    if VOICE_THREAD and VOICE_THREAD.is_alive():
        VOICE_THREAD_STOP.set()
        VOICE_THREAD.join(timeout=2)
        return True
    return False


# ----------------------------
# UI helpers for polling voice queue
# ----------------------------
def process_voice_queue_one():
    """
    If there's a queued voice command, pop one and handle it (main thread safe).
    Supports: tab switching, open downloads, upload file pick, play/transcribe commands.
    """
    try:
        cmd = VOICE_QUEUE.get_nowait()
    except queue.Empty:
        return

    cmd_l = cmd.lower().strip()
    st.session_state["last_voice_command"] = cmd

    # open downloads folder request
    if "open download" in cmd_l or "open downloads" in cmd_l or "open download folder" in cmd_l:
        # Try to open OS Downloads folder (best-effort)
        dl = os.path.expanduser("~/Downloads")
        try:
            if os.name == "nt":
                os.startfile(dl)
            elif os.uname().sysname == "Darwin":
                os.system(f"open '{dl}'")
            else:
                # linux
                os.system(f"xdg-open '{dl}' &")
        except Exception:
            pass
        return

    # Tab switching commands
    for tab_key, keywords in {
        "audio": ["audio tab", "switch to audio", "go to audio", "audio"],
        "video": ["video tab", "switch to video", "go to video", "video"],
        "image": ["image tab", "switch to image", "go to image", "image"],
        "document": ["document tab", "switch to document", "go to document", "document", "docs"],
    }.items():
        for kw in keywords:
            if kw in cmd_l:
                st.session_state["active_tab"] = tab_key
                return

    # Upload file requests like "upload george.mp3 file" or "upload cosmos.pdf"
    # We'll attempt to pick from downloads with file_picker
    # Determine type by extension in command
    m = re.search(r"([^\s]+?\.(mp3|wav|m4a|flac|mp4|mov|mkv|jpg|jpeg|png|gif|pdf|docx|txt))", cmd_l)
    if m:
        filename = m.group(1)
        # decide type
        if filename.lower().endswith((".mp3", ".wav", ".m4a", ".flac")):
            path = file_picker.pick_file_from_command(f"upload {filename}", downloads_path=os.path.expanduser("~/Downloads"))
            if path:
                # load into memory and set session state
                st.session_state["voice_audio_file_path"] = path
                st.session_state["auto_transcribe_audio"] = True
                st.session_state["active_tab"] = "audio"
            else:
                # no match
                pass
            return
        if filename.lower().endswith((".mp4", ".mkv", ".mov", ".avi", ".webm")):
            path = file_picker.pick_video_from_command(f"upload {filename}", downloads_path=os.path.expanduser("~/Downloads"))
            if path:
                st.session_state["voice_video_file_path"] = path
                st.session_state["active_tab"] = "video"
            return
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
            path = file_picker.pick_image_from_command(f"upload {filename}", downloads_path=os.path.expanduser("~/Downloads"))
            if path:
                st.session_state["voice_image_file_path"] = path
                st.session_state["active_tab"] = "image"
            return
        if filename.lower().endswith((".pdf", ".docx", ".txt")):
            path = file_picker.pick_document_from_command(f"upload {filename}", downloads_path=os.path.expanduser("~/Downloads"))
            if path:
                st.session_state["voice_doc_file_path"] = path
                st.session_state["active_tab"] = "document"
            return

    # Play / run commands e.g., "play audio", "run document"
    if "play audio" in cmd_l or "transcribe audio" in cmd_l:
        st.session_state["active_tab"] = "audio"
        st.session_state["auto_transcribe_audio"] = True
        return
    if "play video" in cmd_l or "transcribe video" in cmd_l:
        st.session_state["active_tab"] = "video"
        st.session_state["auto_transcribe_video"] = True
        return
    if "run image" in cmd_l or "transcribe image" in cmd_l:
        st.session_state["active_tab"] = "image"
        st.session_state["auto_transcribe_image"] = True
        return
    if "run document" in cmd_l or "read document" in cmd_l:
        st.session_state["active_tab"] = "document"
        st.session_state["auto_read_document"] = True
        return

    # fallback: show last command
    return


# ----------------------------
# Streamlit App UI
# ----------------------------
st.set_page_config(page_title="Accessible Media (Manual + Voice)", layout="wide")
st.title("Accessible Media — Manual & Voice Interfaces")

# session defaults
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "audio"
if "last_voice_command" not in st.session_state:
    st.session_state["last_voice_command"] = ""
if "voice_audio_file_path" not in st.session_state:
    st.session_state["voice_audio_file_path"] = None
if "voice_video_file_path" not in st.session_state:
    st.session_state["voice_video_file_path"] = None
if "voice_image_file_path" not in st.session_state:
    st.session_state["voice_image_file_path"] = None
if "voice_doc_file_path" not in st.session_state:
    st.session_state["voice_doc_file_path"] = None

# top controls: start/stop voice listener
with st.sidebar:
    st.header("Voice Assistant Controls")
    if st.button("Start Voice Assistant"):
        started = start_voice_listener()
        if started:
            st.success("Voice assistant started (listening).")
        else:
            st.info("Voice assistant already running.")
    if st.button("Stop Voice Assistant"):
        stopped = stop_voice_listener()
        if stopped:
            st.info("Voice assistant stopped.")
        else:
            st.info("Voice assistant was not running.")

# On each rerun, process up to a couple voice commands from the queue
for _ in range(3):
    process_voice_queue_one()


# --- Top tab buttons
tab_cols = st.columns([1, 1, 1, 1])
if tab_cols[0].button("🎧 Audio"):
    st.session_state["active_tab"] = "audio"
if tab_cols[1].button("🎬 Video"):
    st.session_state["active_tab"] = "video"
if tab_cols[2].button("📷 Image"):
    st.session_state["active_tab"] = "image"
if tab_cols[3].button("📄 Document"):
    st.session_state["active_tab"] = "document"

st.write(f"Active tab: **{st.session_state['active_tab']}**")
if st.session_state.get("last_voice_command"):
    st.caption(f"Last voice command: {st.session_state['last_voice_command']}")

# small helper to display errors safely
def show_error(msg):
    st.error(msg)


# ----------------------------
# Shared transcription function (Wav2Vec2) — chunk decode safe
# ----------------------------
@st.cache_resource
def get_asr():
    # returns (processor, model)
    return load_wav2vec2_model()


def transcribe_audio_bytes(audio_bytes: BytesIO, progress_prefix="Transcribing"):
    """
    audio_bytes: BytesIO containing WAV or audio; function resamples to 16k and transcribes.
    Returns string transcript.
    """
    audio_bytes.seek(0)
    # resample to 16k & mono
    wav_io = resample_audio_to_16k(audio_bytes)
    if wav_io is None:
        raise RuntimeError("Failed to resample audio to 16k.")

    wav_io.seek(0)
    with sf.SoundFile(wav_io) as f:
        audio_data = f.read(dtype="float32")
        samplerate = f.samplerate

    processor, model = get_asr()
    inputs = processor(audio_data, sampling_rate=samplerate, return_tensors="pt", padding=True).input_values

    chunk_size = 16000 * 5
    start = 0
    total_len = inputs.shape[1]
    transcript_parts = []

    progress_bar = st.progress(0)
    progress_text = st.empty()

    while start < total_len:
        end = min(start + chunk_size, total_len)
        input_chunk = inputs[:, start:end]
        with torch.no_grad():
            logits = model(input_chunk).logits
        preds = torch.argmax(logits, dim=-1)
        # decode this chunk immediately and append
        try:
            piece = processor.batch_decode(preds)[0]
        except Exception:
            import torch as _torch
            piece = processor.batch_decode(_torch.tensor(preds))[0]
        transcript_parts.append(piece)
        start = end
        pct = min(int(start / total_len * 100), 100)
        progress_bar.progress(pct)
        progress_text.text(f"⏳ {progress_prefix}... {pct}%")

    progress_bar.progress(100)
    progress_text.text(f"✅ {progress_prefix} complete")
    return " ".join([p.strip() for p in transcript_parts]).strip()


# ----------------------------
# AUDIO TAB
# ----------------------------
if st.session_state["active_tab"] == "audio":
    st.header("Audio — Upload or URL (Manual)")

    # Voice-picked file auto handling
    audio_bytes = None
    voice_path = st.session_state.get("voice_audio_file_path")
    if voice_path and os.path.exists(voice_path):
        try:
            audio_bytes = BytesIO(open(voice_path, "rb").read())
            # do not save to disk; we only read into memory
            st.info(f"Loaded audio from Downloads: {os.path.basename(voice_path)}")
        except Exception:
            audio_bytes = None

    uploaded_audio = st.file_uploader("Upload audio file (or let voice assistant pick from Downloads)", type=["wav","mp3","m4a","ogg","flac","aac"])
    audio_url = st.text_input("Or paste an audio URL (direct audio link)", value="", key="audio_url_input")

    if uploaded_audio:
        audio_bytes = BytesIO(uploaded_audio.read())

    elif audio_url:
        audio_url = audio_url.strip()
        # Try to handle typical cases. If youtube link, yt_dlp would be needed
        try:
            if "youtube.com" in audio_url or "youtu.be" in audio_url:
                # Attempt to extract via yt_dlp (best-effort)
                try:
                    audio_bytes = youtube_extract_audio_bytes(audio_url)
                except Exception:
                    show_error("YouTube links require yt_dlp support on the server. Please paste a direct audio link.")
            else:
                if not is_valid_audio_url(audio_url):
                    # Attempt to still fetch and try to read if content-type is non-audio but bytes contain audio
                    raw = safe_requests_get(audio_url)
                    audio_bytes = BytesIO(raw)
                else:
                    raw = safe_requests_get(audio_url)
                    audio_bytes = BytesIO(raw)
        except Exception as e:
            show_error(f"Failed to fetch audio URL: {e}")

    if audio_bytes:
        # convert to wav BytesIO for stable playback/transcription
        try:
            wav = convert_to_wav(audio_bytes)
            st.audio(wav)
            # Auto-transcribe if voice assistant or user requested
            if st.session_state.pop("auto_transcribe_audio", False):
                with st.spinner("Transcribing audio..."):
                    transcript = transcribe_audio_bytes(wav, progress_prefix="Transcribing audio")
                    st.text_area("Transcript", transcript, height=300)
                    st.download_button("⬇️ Download Transcript", transcript, "audio_transcript.txt")
        except Exception as e:
            show_error(f"Audio processing failed: {e}")

    # Manual button
    if audio_bytes and st.button("Transcribe (Manual)"):
        try:
            wav = convert_to_wav(audio_bytes)
            transcript = transcribe_audio_bytes(wav, progress_prefix="Transcribing audio")
            st.text_area("Transcript", transcript, height=300)
            st.download_button("⬇️ Download Transcript", transcript, "audio_transcript.txt")
        except Exception as e:
            show_error(f"Transcription failed: {e}")


# ----------------------------
# VIDEO TAB
# ----------------------------
elif st.session_state["active_tab"] == "video":
    st.header("Video — Upload or URL (Manual)")

    video_bytes = None
    voice_video_path = st.session_state.get("voice_video_file_path")
    if voice_video_path and os.path.exists(voice_video_path):
        try:
            video_bytes = BytesIO(open(voice_video_path, "rb").read())
            st.info(f"Loaded video from Downloads: {os.path.basename(voice_video_path)}")
        except Exception:
            video_bytes = None

    uploaded_video = st.file_uploader(
        "Upload video file (or let voice assistant pick from Downloads)",
        type=["mp4", "mov", "mkv", "avi", "webm"]
    )
    video_url = st.text_input("Or paste a video URL (YouTube or direct)", value="", key="video_url_input")

    if uploaded_video:
        video_bytes = BytesIO(uploaded_video.read())
    elif video_url:
        video_url = video_url.strip()
        try:
            if "youtube.com" in video_url or "youtu.be" in video_url:
                try:
                    video_audio = youtube_extract_audio_bytes(video_url)
                    audio_bytes = video_audio
                except Exception:
                    show_error("YouTube links require yt_dlp support. Please provide a direct video link.")
                    audio_bytes = None
            else:
                raw = safe_requests_get(video_url)
                video_bytes = BytesIO(raw)
        except Exception as e:
            show_error(f"Failed to fetch video URL: {e}")

    if video_bytes:
        st.video(video_bytes)  # Show video player only

        with st.spinner("Extracting audio & transcribing..."):
            success, audio_result = extract_audio_from_video(video_bytes)

            if success:
                audio_path = audio_result  # always .wav file path
                st.success("✅ Audio extracted successfully.")

                try:
                    # Load into BytesIO for resampling
                    with open(audio_path, "rb") as f:
                        audio_io = BytesIO(f.read())
                    wav = resample_audio_to_16k(audio_io)

                    # Transcribe
                    transcript = transcribe_audio_bytes(wav, progress_prefix="Transcribing video")
                    st.text_area("Transcript", transcript, height=300)
                    st.download_button("⬇️ Download Transcript", transcript, "video_transcript.txt")

                except Exception as e:
                    st.error(f"Transcription failed: {e}")
            else:
                st.error(f"Video processing failed: {audio_result}")




# ----------------------------
# IMAGE TAB
# ----------------------------
elif st.session_state["active_tab"] == "image":
    st.header("Image — Upload or URL (Manual)")

    image_obj = None
    voice_image_path = st.session_state.get("voice_image_file_path")

    # Load from Downloads (voice assistant)
    if voice_image_path and os.path.exists(voice_image_path):
        try:
            image_obj = Image.open(voice_image_path).convert("RGB")
            st.info(f"Loaded image from Downloads: {os.path.basename(voice_image_path)}")
        except Exception:
            image_obj = None

    # Upload or URL
    uploaded_image = st.file_uploader(
        "Upload an image (or let voice assistant pick from Downloads)",
        type=["jpg", "jpeg", "png", "bmp", "gif", "webp"]
    )
    image_url = st.text_input("Or paste an image URL", value="", key="image_url_input")

    if uploaded_image:
        image_obj = Image.open(uploaded_image).convert("RGB")
    elif image_url:
        image_url = image_url.strip()
        try:
            raw = safe_requests_get(image_url)
            image_obj = Image.open(BytesIO(raw)).convert("RGB")
        except Exception as e:
            show_error(f"Failed to fetch image URL: {e}")

    # ✅ Compress before showing & captioning
    if image_obj:
        try:
            max_size = (800, 800)
            image_obj.thumbnail(max_size, Image.LANCZOS)

            compressed_bytes = io.BytesIO()
            image_obj.save(compressed_bytes, format="JPEG", quality=70)
            compressed_bytes.seek(0)

            # Show compressed image
            st.image(image_obj, caption="Uploaded Image", use_column_width=False)

            if st.button("Generate Caption"):
                with st.spinner("Generating caption..."):
                    try:
                        caption = generate_image_caption(image_obj)
                        st.markdown(f"**📝 Caption:** {caption}")
                        speak_text(caption)  # speak only caption
                    except Exception as e:
                        show_error(f"Image captioning failed: {e}")
        except Exception as e:
            show_error(f"Image processing failed: {e}")




# # ----------------------------
# # DOCUMENT TAB
# # ----------------------------
# elif st.session_state["active_tab"] == "document":
#     st.header("Document — Upload or URL (Manual)")
#     doc_text = None
#     document_bytes = None
#     filename = None

#     # Voice-picked file in downloads
#     voice_doc_path = st.session_state.get("voice_doc_file_path")
#     if voice_doc_path and os.path.exists(voice_doc_path):
#         try:
#             document_bytes = BytesIO(open(voice_doc_path, "rb").read())
#             filename = os.path.basename(voice_doc_path)
#             st.info(f"Loaded document from Downloads: {filename}")
#         except Exception:
#             document_bytes = None

#     uploaded_doc = st.file_uploader("Upload a document (PDF/DOCX/TXT)", type=["pdf","docx","txt"])
#     doc_url = st.text_input("Or paste a document URL", value="", key="doc_url_input")

#     if uploaded_doc:
#         document_bytes = BytesIO(uploaded_doc.read())
#         filename = uploaded_doc.name
#     elif doc_url:
#         doc_url = doc_url.strip()
#         try:
#             raw = safe_requests_get(doc_url)
#             # If URL points to pdf/docx/txt based on extension, pass bytes to parser
#             if is_valid_document_url(doc_url) or re.search(r"\.(pdf|docx|txt)$", doc_url, re.IGNORECASE):
#                 document_bytes = BytesIO(raw)
#                 filename = os.path.basename(doc_url.split("?")[0])
#             else:
#                 # treat as HTML page: extract visible text with BeautifulSoup fallback
#                 try:
#                     from bs4 import BeautifulSoup

#                     soup = BeautifulSoup(raw, "html.parser")
#                     # naive main content extraction
#                     article = soup.find("article") or soup.find("main") or soup
#                     text = " ".join([p.get_text(strip=True) for p in article.find_all("p")])[:20000]
#                     document_bytes = BytesIO(text.encode("utf-8"))
#                     filename = "webpage.txt"
#                 except Exception:
#                     document_bytes = BytesIO(raw)  # let extractor attempt
#                     filename = "document_from_url"
#         except Exception as e:
#             show_error(f"Failed to fetch document URL: {e}")

#     # If we have document bytes, extract text in-memory (no disk writes)
#     if document_bytes is not None:
#         try:
#             # our extract_text_from_document expects (file_obj, filename)
#             doc_text = extract_text_from_document(document_bytes, filename or "uploaded_document")
#         except Exception as e:
#             show_error(f"Document parsing failed: {e}\n{traceback.format_exc()}")

#     # Display extracted text with highlight & TTS controls
#     if doc_text:
#         st.success("Document text extracted successfully.")
#         # split into lines/paragraphs for highlighting
#         lines = [ln.strip() for ln in re.split(r"\n{1,}", doc_text) if ln.strip()]
#         placeholder = st.empty()
#         # Show initial (first 2000 chars) collapsed
#         st.text_area("Extracted Text (full)", doc_text, height=300)

#         # Summarize using Gemini or fallback
#         summary = None
#         try:
#             if AI_AVAILABLE:
#                 # ask Gemini to produce a brief 5-6 line summary
#                 try:
#                     summary = ai_agent.ask_ai(
#                         f"Summarize the following document in 5-6 brief lines:\n\n{doc_text[:3000]}"
#                     )
#                 except Exception:
#                     summary = None
#             if not summary:
#                 # fallback: take first 5 sentences
#                 sents = re.split(r'(?<=[.!?])\s+', doc_text)
#                 summary = " ".join(sents[:5]).strip()
#         except Exception:
#             summary = "Summary unavailable."

#         st.markdown("### 📌 Brief Summary (5-6 lines)")
#         st.write(summary)
#         # Speak the summary
#         if st.button("🔊 Speak Summary"):
#             speak_text(summary)

#         # Read & highlight button
#         if st.button("▶️ Read document aloud with line-by-line highlight"):
#             # iterate lines and highlight + speak
#             try:
#                 for i, line in enumerate(lines):
#                     # show highlighted current line
#                     display_html = ""
#                     for j, l in enumerate(lines):
#                         if j == i:
#                             display_html += f"<mark style='background:#fffb8f'>{l}</mark>\n\n"
#                         else:
#                             display_html += f"{l}\n\n"
#                     placeholder.markdown(display_html, unsafe_allow_html=True)
#                     # speak the current line
#                     speak_text(line)
#                     # small pause — adjust as needed
#                     time.sleep(0.08)
#                 placeholder.markdown("<i>✅ Finished reading document.</i>", unsafe_allow_html=True)
#             except Exception as e:
#                 show_error(f"Reading/Highlighting failed: {e}")

#         # Also provide a download of extracted text
#         st.download_button("⬇️ Download extracted text", doc_text, file_name="document_text.txt")
#     else:
#         st.info("Upload a PDF/DOCX/TXT or paste a URL to extract and read aloud the document.")


# ----------------------------
# DOCUMENT TAB
# ----------------------------
import streamlit as st
import time
import threading
import re
import os
from io import BytesIO
from modules.document_handler import extract_text_from_document
from modules.utils import safe_requests_get, is_valid_document_url, show_error
from modules.gemini_client import ask_gemini  # Gemini summarization
from modules.tts_handler import speak_text  # Offline TTS

# Session states for reading control
if "doc_reading" not in st.session_state:
    st.session_state.doc_reading = False
if "doc_stop_flag" not in st.session_state:
    st.session_state.doc_stop_flag = False
if "doc_pause_flag" not in st.session_state:
    st.session_state.doc_pause_flag = False

elif st.session_state["active_tab"] == "document":
    st.header("Document — Upload or URL (Manual)")
    doc_text = None
    document_bytes = None
    filename = None

    # Voice-picked file in Downloads
    voice_doc_path = st.session_state.get("voice_doc_file_path")
    if voice_doc_path and os.path.exists(voice_doc_path):
        try:
            document_bytes = BytesIO(open(voice_doc_path, "rb").read())
            filename = os.path.basename(voice_doc_path)
            st.info(f"Loaded document from Downloads: {filename}")
        except Exception:
            document_bytes = None

    uploaded_doc = st.file_uploader("Upload a document (PDF/DOCX/TXT)", type=["pdf","docx","txt"])
    doc_url = st.text_input("Or paste a document URL", value="", key="doc_url_input")

    if uploaded_doc:
        document_bytes = BytesIO(uploaded_doc.read())
        filename = uploaded_doc.name
    elif doc_url:
        doc_url = doc_url.strip()
        try:
            raw = safe_requests_get(doc_url)
            if is_valid_document_url(doc_url) or re.search(r"\.(pdf|docx|txt)$", doc_url, re.IGNORECASE):
                document_bytes = BytesIO(raw)
                filename = os.path.basename(doc_url.split("?")[0])
            else:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(raw, "html.parser")
                article = soup.find("article") or soup.find("main") or soup
                text = " ".join([p.get_text(strip=True) for p in article.find_all("p")])[:20000]
                document_bytes = BytesIO(text.encode("utf-8"))
                filename = "webpage.txt"
        except Exception as e:
            show_error(f"Failed to fetch document URL: {e}")

    # Extract text
    if document_bytes is not None:
        try:
            doc_text = extract_text_from_document(document_bytes)
        except Exception as e:
            show_error(f"Document parsing failed: {e}")

    if doc_text:
        st.success("Document text extracted successfully.")
        placeholder = st.empty()

        # Display collapsed full text
        st.text_area("Extracted Text (full)", doc_text, height=300)

        # Summarize via Gemini
        summary = "Summary unavailable."
        try:
            summary = ask_gemini(f"Summarize the following document in 5-6 brief lines:\n\n{doc_text[:3000]}")
        except Exception as e:
            show_error(f"Gemini summarization failed: {e}")

        st.markdown("### 📌 Brief Summary (5-6 lines)")
        st.write(summary)

        if st.button("🔊 Speak Summary"):
            speak_text(summary)

        # Line-by-line highlighting & TTS with pause/stop
        lines = [ln.strip() for ln in re.split(r"\n{1,}", doc_text) if ln.strip()]

        col1, col2, col3 = st.columns(3)
        if col1.button("▶️ Start Reading"):
            st.session_state.doc_reading = True
            st.session_state.doc_stop_flag = False
            st.session_state.doc_pause_flag = False

            def read_document():
                for i, line in enumerate(lines):
                    if st.session_state.doc_stop_flag:
                        break
                    while st.session_state.doc_pause_flag:
                        time.sleep(0.2)
                    display_html = ""
                    for j, l in enumerate(lines):
                        if j == i:
                            display_html += f"<mark style='background:#fffb8f'>{l}</mark>\n\n"
                        else:
                            display_html += f"{l}\n\n"
                    placeholder.markdown(display_html, unsafe_allow_html=True)
                    speak_text(line)
                    time.sleep(0.1)  # adjust delay per line
                placeholder.markdown("<i>✅ Finished reading document.</i>", unsafe_allow_html=True)
                st.session_state.doc_reading = False

            threading.Thread(target=read_document, daemon=True).start()

        if col2.button("⏸️ Pause"):
            st.session_state.doc_pause_flag = True

        if col3.button("▶️ Continue"):
            st.session_state.doc_pause_flag = False

        if st.button("⏹️ Stop Reading"):
            st.session_state.doc_stop_flag = True
            st.session_state.doc_pause_flag = False
            st.session_state.doc_reading = False

        st.download_button("⬇️ Download extracted text", doc_text, file_name="document_text.txt")

    else:
        st.info("Upload a PDF/DOCX/TXT or paste a URL to extract and read aloud the document.")



# ----------------------------
# End of page
# ----------------------------
st.markdown("---")
st.caption("Built for accessibility: Manual (upload/UI) and Voice-based workflows. Files are processed in-memory (not saved).")

