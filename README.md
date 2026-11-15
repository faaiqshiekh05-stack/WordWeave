# 🧵 WordWeave

### Weave Your Words Across Languages 🌍

**WordWeave** is a multilingual language translation and voice-assistance application built with **Python and Streamlit**. It lets users type or speak their input, translate it into another language, convert uploaded voice messages into text, and listen to translated text using text-to-speech.

> **Type. Speak. Translate. Listen. — All in one place.**

---

## ✨ Features

### 🌍 Multilingual Translation

Translate text between multiple supported languages using a simple and intuitive interface.

Currently supported:

- 🇬🇧 English
- 🇵🇰 Urdu
- 🇸🇦 Arabic
- 🇫🇷 French
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇨🇳 Chinese (Simplified)
- 🇮🇳 Hindi
- 🇹🇷 Turkish
- 🇷🇺 Russian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇧🇩 Bengali

The source language also supports **automatic detection**.

---

### 🎙️ Live Voice Input

WordWeave allows users to record their voice directly from the application.

The recorded speech is processed using speech recognition and converted into text automatically, which can then be translated.

**Workflow:**

```text
🎙️ Speak
   ↓
📝 Speech → Text
   ↓
🌍 Translate
   ↓
🔊 Listen
```

---

### 🎵 Upload Voice Messages

Users can upload existing audio files and convert the speech into text.

Supported formats include:

- WAV
- FLAC
- AIFF
- MP3
- M4A
- OGG

For supported formats that require conversion, the application processes the audio before speech recognition.

---

### 🔊 Text-to-Speech

After translation, users can listen to the translated result instead of reading it.

This makes WordWeave useful for:

- Language learning
- Pronunciation practice
- Communication
- Travel
- Understanding unfamiliar languages

---

### 🔄 Translation Fallback

WordWeave uses a fallback mechanism to improve translation reliability.

The primary translation service is:

**GoogleTranslator**

If the primary service encounters an error or rate limit, the application attempts to use:

**MyMemoryTranslator**

This helps reduce interruptions when the primary translation service is temporarily unavailable.

---

### ⚡ Smart Caching

WordWeave uses Streamlit's caching functionality for translation and text-to-speech operations.

Previously processed results can be reused instead of repeatedly requesting the same service.

This helps improve:

- Response speed
- User experience
- API/service efficiency
- Repeated translation performance

---

## 🎨 Modern User Interface

WordWeave includes a custom Streamlit interface designed around a modern dark teal visual theme.

### UI Highlights

- 🧵 WordWeave branded header
- 🌊 Dark teal gradient background
- 🪟 Glass-style cards
- 🎯 Clear language selectors
- 🎙️ Voice recording controls
- 📁 Audio upload interface
- 🚀 Large translation action button
- 📋 Easy-to-copy translated text
- 🔊 Built-in audio playback
- 📱 Responsive Streamlit layout

The interface is designed to keep the translation workflow simple:

```text
Select Language
      ↓
Enter / Speak / Upload Audio
      ↓
Translate
      ↓
View Result
      ↓
Listen to Translation
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core application development |
| **Streamlit** | Web application interface |
| **Deep Translator** | Translation services |
| **Google Translate** | Primary translation service |
| **MyMemory** | Translation fallback |
| **gTTS** | Text-to-speech generation |
| **SpeechRecognition** | Speech-to-text processing |
| **streamlit-mic-recorder** | Browser-based voice recording |
| **PyDub** | Audio format conversion |
| **HTML/CSS** | UI customization |

---

## 📁 Project Structure

```text
WordWeave/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `app.py`

Contains the complete Streamlit application, including:

- User interface
- Language selection
- Voice recording
- Audio upload
- Speech recognition
- Translation
- Translation fallback
- Text-to-speech
- Session state
- Caching

### `requirements.txt`

Contains the Python dependencies required to run WordWeave.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/faaiqshiekh05-stack/WordWeave.git
```

Move into the project:

```bash
cd WordWeave
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run WordWeave

```bash
streamlit run app.py
```

Streamlit will start the application locally and provide a browser address.

---

## 💡 How to Use

### Text Translation

1. Select the **source language**.
2. Select the **target language**.
3. Enter your text.
4. Click **Translate Now**.
5. View the translated result.
6. Use the audio player to listen to the translation.

---

### Voice Translation

1. Select your source language.
2. Click **Start Recording**.
3. Speak clearly.
4. Stop the recording.
5. WordWeave converts your speech into text.
6. Click **Translate Now**.
7. Listen to the translated result.

---

### Audio File Translation

1. Select the source language.
2. Upload an audio file.
3. Click **Convert Uploaded Audio to Text**.
4. WordWeave extracts the spoken text.
5. Translate the generated text.
6. Listen to the translated result.

---

## 🧠 Application Architecture

WordWeave follows a simple processing pipeline:

```text
                 ┌─────────────────┐
                 │      User       │
                 └────────┬────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
          Text Input              Voice Input
             │                         │
             │                  Speech Recognition
             │                         │
             └────────────┬────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   Translation │
                  │     Engine    │
                  └───────┬───────┘
                          │
                 Google Translator
                          │
                    Fallback
                          │
                    MyMemory
                          │
                          ▼
                  ┌───────────────┐
                  │   Translation │
                  │     Result    │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Text-to-Speech│
                  └───────┬───────┘
                          │
                          ▼
                    🔊 Audio Output
```

---

## 🎯 Use Cases

WordWeave can be useful for:

- 🌍 Everyday language translation
- 🎓 Language learning
- 🗣️ Pronunciation practice
- ✈️ Travel communication
- 💬 Multilingual communication
- 📚 Understanding foreign-language content
- 🎙️ Converting spoken language into text
- 🔊 Listening to translated text

---

## ⚠️ Notes

WordWeave relies on external translation and speech services. Therefore, functionality can depend on:

- Internet connectivity
- Availability of external services
- Service rate limits
- Supported language capabilities

Translation quality may also vary depending on the language pair and the external translation service.

---

## 🔒 Privacy & Security

WordWeave does not require users to create an account within the current application.

However, because translation and speech-recognition functionality relies on external services, users should avoid submitting highly sensitive or confidential information.

Do not add API keys, passwords, tokens, or other secrets directly to the source code.

---

## 🔮 Future Improvements

Potential future enhancements include:

- 📝 Translation history
- ⭐ Favorite translations
- 📋 One-click copy controls
- 🌐 Additional language support
- 🎤 Improved multilingual speech recognition
- 🔊 More voice options
- 📱 Mobile-focused interface improvements
- 🌐 Deployment as a public web application
- 👤 User accounts
- ☁️ Cloud-based translation history
- 🤖 AI-powered contextual translation

---

## 📸 Screenshots

Add screenshots of the application here after capturing your Streamlit interface.

Example:

```markdown
![WordWeave Interface](screenshots/wordweave-home.png)
```

Recommended screenshots:

- Main translation interface
- Voice recording interface
- Audio upload section
- Translation result
- Text-to-speech output

---

## 📌 Project Status

**Status:** Active Development 🚀

WordWeave is a functional multilingual translation application with text translation, voice recording, speech recognition, audio upload, translation fallback, caching, and text-to-speech capabilities.

---

## 👨‍💻 Author

**Faaiq Qaisar Shahzad**

Computer Science Student | Aspiring AI Engineer | Python Developer | Data Analyst

---

## 📄 License

This project is available for learning, development, and portfolio purposes.

If you reuse or modify this project, please provide appropriate attribution to the original author.

---

### ⭐ Support the Project

If you find WordWeave useful or interesting:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report issues**

💡 **Suggest improvements**

---

## 🧵 WordWeave

**Weave your words across languages.**

> Built with Python 🐍 + Streamlit 🎈
