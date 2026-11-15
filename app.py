import streamlit as st
from deep_translator import GoogleTranslator, MyMemoryTranslator
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io

st.set_page_config(page_title="WordWeave", page_icon="🧵", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
<style>
/* App background - dark teal gradient */
.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 50%, #00c6a9 100%);
}

/* Hide default Streamlit chrome */
header[data-testid="stHeader"] { background: transparent; }
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

.main-title {
    text-align: center;
    color: #ffffff;
    font-size: 46px;
    font-weight: 800;
    padding: 20px 0 5px 0;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.4);
}
.sub-title {
    text-align: center;
    color: #d8fff5;
    font-size: 18px;
    margin-bottom: 25px;
}

/* Card container */
.card {
    background: rgba(20, 30, 48, 0.65);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}

/* Labels */
.stSelectbox label, .stTextArea label, .stRadio label, .stFileUploader label {
    color: #aef9e4 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* Text area */
.stTextArea textarea {
    border-radius: 12px;
    border: 2px solid #00c6a9;
    background-color: #0e1620;
    color: #ffffff;
    font-size: 16px;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: #0e1620;
    border: 2px solid #00c6a9;
    border-radius: 12px;
    color: #ffffff;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    padding: 10px 28px;
    font-size: 16px;
    transition: 0.25s;
    width: 100%;
}
div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 18px rgba(238,9,121,0.5);
}

/* Result box */
.result-box {
    background: rgba(255,255,255,0.95);
    border-left: 6px solid #00c6a9;
    border-radius: 10px;
    padding: 18px;
    font-size: 18px;
    color: #14213d;
    min-height: 80px;
}

/* Audio player */
audio { width: 100%; }

/* File uploader box */
section[data-testid="stFileUploadDropzone"] {
    background-color: #0e1620;
    border: 2px dashed #00c6a9;
    border-radius: 12px;
}

/* Section divider text */
.section-label {
    color: #aef9e4;
    font-weight: 700;
    font-size: 16px;
    margin: 10px 0 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="main-title">🧵 WordWeave</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Weave your words across languages — type, speak, translate & listen 🎙️🌍🔊</div>', unsafe_allow_html=True)

# ---------- Languages ----------
LANGUAGES = {
    "Auto Detect": "auto", "English": "en", "Urdu": "ur", "Arabic": "ar",
    "French": "fr", "Spanish": "es", "German": "de", "Chinese (Simplified)": "zh-CN",
    "Hindi": "hi", "Turkish": "tr", "Russian": "ru", "Japanese": "ja",
    "Korean": "ko", "Italian": "it", "Portuguese": "pt", "Bengali": "bn"
}

# ---------- Cached helpers (avoid repeated calls -> no rate-limit errors) ----------
# MyMemory (fallback) needs regional codes, e.g. "ur-PK" instead of "ur"
MYMEMORY_CODES = {
    "en": "en-GB", "ur": "ur-PK", "ar": "ar-SA", "fr": "fr-FR", "es": "es-ES",
    "de": "de-DE", "zh-CN": "zh-CN", "hi": "hi-IN", "tr": "tr-TR", "ru": "ru-RU",
    "ja": "ja-JP", "ko": "ko-KR", "it": "it-IT", "pt": "pt-PT", "bn": "bn-IN",
}


@st.cache_data(show_spinner=False, ttl=3600)
def translate_text(text: str, src: str, tgt: str) -> str:
    """Translate with caching; falls back to MyMemory if Google rate-limits us."""
    try:
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except Exception as google_err:
        # Retrying a rate-limit block right away doesn't help, so go to the fallback.
        try:
            mm_src = MYMEMORY_CODES.get("en" if src == "auto" else src)  # no auto-detect
            mm_tgt = MYMEMORY_CODES.get(tgt)
            return MyMemoryTranslator(source=mm_src, target=mm_tgt).translate(text)
        except Exception as mm_err:
            raise RuntimeError(
                f"Google: {google_err} | Fallback (MyMemory): {mm_err}"
            ) from mm_err


@st.cache_data(show_spinner=False, ttl=3600)
def text_to_speech(text: str, lang: str) -> bytes:
    """Generate MP3 bytes once per (text, language); reruns reuse the cache."""
    buf = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buf)
    return buf.getvalue()


# ---------- Session State ----------
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------- Layout ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("🔤 Source Language", list(LANGUAGES.keys()), index=0)
with col2:
    target_lang_options = [l for l in LANGUAGES.keys() if l != "Auto Detect"]
    target_lang = st.selectbox("🎯 Target Language", target_lang_options, index=target_lang_options.index("Urdu"))

# ---------- Live Voice Recording ----------
st.markdown('<div class="section-label">🎙️ Record Your Voice</div>', unsafe_allow_html=True)
audio = mic_recorder(
    start_prompt="🔴 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav",
    key="recorder"
)

if audio is not None:
    recognizer = sr.Recognizer()
    try:
        audio_bytes = io.BytesIO(audio["bytes"])
        with sr.AudioFile(audio_bytes) as source:
            audio_data = recognizer.record(source)
        recog_lang = LANGUAGES[source_lang] if LANGUAGES[source_lang] != "auto" else "en-US"
        text_from_speech = recognizer.recognize_google(audio_data, language=recog_lang)
        st.session_state.input_text = text_from_speech
        st.success(f"✅ Recognized: {text_from_speech}")
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio. Please try again.")
    except sr.RequestError as e:
        st.error(f"❌ Speech recognition service error: {e}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ---------- Voice Message Upload ----------
st.markdown('<div class="section-label">🎵 Voice Input — upload a voice message to convert speech to text</div>', unsafe_allow_html=True)
audio_file = st.file_uploader("Upload audio", type=["wav", "flac", "aiff", "mp3", "m4a", "ogg"], label_visibility="collapsed")

if audio_file is not None:
    if st.button("🎤 Convert Uploaded Audio to Text"):
        recognizer = sr.Recognizer()
        try:
            file_ext = audio_file.name.split(".")[-1].lower()
            if file_ext in ["wav", "aiff", "flac"]:
                audio_source = audio_file
            else:
                # Convert mp3/m4a/ogg/etc. to wav using pydub
                from pydub import AudioSegment
                sound = AudioSegment.from_file(audio_file, format=file_ext)
                wav_buffer = io.BytesIO()
                sound.export(wav_buffer, format="wav")
                wav_buffer.seek(0)
                audio_source = wav_buffer

            with sr.AudioFile(audio_source) as source:
                audio_data = recognizer.record(source)
            recog_lang = LANGUAGES[source_lang] if LANGUAGES[source_lang] != "auto" else "en-US"
            text_from_speech = recognizer.recognize_google(audio_data, language=recog_lang)
            st.session_state.input_text = text_from_speech
            st.success(f"✅ Recognized: {text_from_speech}")
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition service error: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------- Text Input ----------
input_text = st.text_area("✍️ Enter text to translate", height=150,
                           value=st.session_state.input_text,
                           placeholder="Type, paste, or use voice input above...")

translate_btn = st.button("🚀 Translate Now")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Translation Logic ----------
if translate_btn:
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text to translate.")
    else:
        try:
            src_code = LANGUAGES[source_lang]
            tgt_code = LANGUAGES[target_lang]
            with st.spinner("Translating..."):
                st.session_state.translated_text = translate_text(input_text.strip(), src_code, tgt_code)
        except Exception as e:
            st.error(f"Translation failed: {e}")

# ---------- Output ----------
if st.session_state.translated_text:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ✅ Translated Text")
    st.markdown(f'<div class="result-box">{st.session_state.translated_text}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.code(st.session_state.translated_text, language=None)
        st.caption("👆 Use the copy icon above to copy text")

    with col2:
        try:
            tts_lang = LANGUAGES[target_lang].split("-")[0]
            st.audio(text_to_speech(st.session_state.translated_text, tts_lang), format="audio/mp3")
            st.caption("🔊 Listen to pronunciation")
        except Exception:
            st.caption("🔇 Text-to-speech not available for this language")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    "<div style='text-align:center; color:#d8fff5; margin-top:20px;'>🧵 WordWeave — Made with Streamlit & Google Translate API</div>",
    unsafe_allow_html=True
)