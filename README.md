# 🎵 Musigent — AI Music Creative Agent
*A multi-agent AI system that generates copyright-safe jingles, background music, and personalized music personas.*

Musigent is a creative AI agent system built for the **Kaggle 5-Day Agents Intensive Capstone Project**, powered by 
a multi-agent architecture using Planner, Composer, and Quality evaluation agents. It helps content creators, 
brands, and social media users generate **original, copyright-safe audio tailored to their needs.

---

##  Features

## 1. Jingle Generator
Create short, catchy, brand-ready audio logos.

## 2. Background Music Composer**
Generate copyright-safe ambient or cinematic tracks for:
- YouTube videos  
- Instagram reels  
- TikTok posts  
- Podcasts  

## 3. Personal Music Persona
Analyze a user's taste (mocked Spotify integration) and:
- Build a music persona  
- Compose a personalized track  
- Suggest a style based on preferences  

## 4. Multi-Agent Reasoning Pipeline**
Musigent uses:
- **PlannerAgent** → interprets request, defines structure  
- **ComposerAgent** → generates (mock) audio  
- **QualityAgent** → evaluates originality + style match  
- **MemoryStore** → keeps track of interactions  

---

## 🧠 Architecture Overview

The system follows a clean multi-agent flow:

User Request → PlannerAgent → ComposerAgent → QualityAgent → Final Output


If you cloned the repo, the architecture diagram is here:

assets/architecture.png


---

## 🛠️ Technologies Used

- **Python 3.11**
- **FastAPI** (for simple API demo)
- **Uvicorn** (local dev server)
- **Pydantic** (request/response models)
- **Mock Suno + Spotify Tools** (extendable to real APIs)
- **Simple JSON Memory Store**
- **Kaggle Notebook Integration**
- **GitHub Version Control**

---

## 📂 Project Structure

musigent/
│
├── agents/
│ ├── planner.py # Decides style, tempo, strategy
│ ├── composer.py # Generates (mocked) music
│ └── quality.py # LLM-like evaluation scoring
│
├── tools.py # Mock Suno + Spotify tool wrappers
├── memory.py # JSON-based long-term memory
├── runner.py # Full pipeline orchestrator
│
assets/
│ └── architecture.png # System architecture diagram
│
notebooks/
│ └── demo.ipynb # Kaggle-ready demonstration notebook
│
app.py # FastAPI demo service
requirements.txt # Dependencies
README.md # You are here


---

## ▶️ How to Run Locally

1. Install dependencies**
```
pip install -r requirements.txt
```

2. Start FastAPI
```
uvicorn app:app --reload
```
3. Open in browser
```
http://127.0.0.1:8000/docs
```

You can test the /generate endpoint directly.
```
from musigent.runner import MusigentRunner

runner = MusigentRunner()

runner.handle_request(
    mode="jingle",
    prompt="modern startup jingle",
    duration_sec=15
)
```
This returns:

**A- The plan**

**B- The (mocked) generated audio**

**C- The evaluation score**

# 📡 On Kaggle

**To use this project inside a Kaggle notebook:**
```
!git clone https://github.com/mzchimeh/musigent.git
import sys
sys.path.append("/kaggle/working/musigent")

from musigent.runner import MusigentRunner
runner = MusigentRunner()
runner.handle_request("bgm", "soft ambient background", 30)
```

# Future Work
Planned improvements include:

1- Integration with real Suno API for audio generation

2- Integration with Spotify OAuth for true taste modeling

3- Enhanced originality scoring

4- Fully hosted web UI

5- Optional vector database for richer memory retention

6- Deployment via Google Cloud’s Agent Engine

# 🤝 Contributions

Feel free to fork the repo and submit pull requests.
This project was created as part of the Kaggle Agents Intensive Capstone Challenge.

# ⭐ Acknowledgements

Thanks to:

Kaggle & Google DeepMind for the Agents Intensive program

OpenAI & Suno for inspiring creative AI tools

The entire Kaggle community

============
### MZ - 11/2025
