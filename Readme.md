# 🎵 Musigent — AI Jingle & Music Agent (Real‑World Suno API + Multi‑Agent System)

*An advanced multi‑agent AI system that generates copyright‑safe jingles, background music, and persona‑based audio using real external APIs.*

Musigent is built as the **Capstone Project for the Kaggle 5‑Day Agents Intensive**, using a fully modular **multi‑agent architecture** enhanced with:

- **Real Suno Music Generation API**
- **Google Geolocation API (UTC timestamp + rate‑limit enforcement)**
- **Daily anti‑spam user limits**
- **Short‑term (per‑minute) request throttling**
- **Persistent memory** with user‑time tracking

---

# 🚀 Key Features

### ✅ **1. Real Jingle Generator (Suno API Integrated)**
- Generates **real audio** using Suno’s official API.
- Jingle creation pipeline:
  **Planner → Composer (Suno API) → Quality → Memory → Final Output**
- Handles API errors, 429 insufficient credits, malformed responses, etc.

---

### ✅ **2. Anti‑Spam Protection**
Two‑level protection built into the system:

#### **A. Per‑day Limit**
- Each username can generate **max 5 jingles per UTC day**.

#### **B. Per‑minute Limit**
- Each username can send **max 5 jingle requests per minute**.
- Uses:
  - **Google Geolocation timestamp**
  - **UTC normalization**
  - **MemoryStore with timestamps**

No unnecessary calls are sent to Suno if limits are exceeded.

---

### ✅ **3. Time + Geolocation Tool**
- Fetches current UTC time from:
  - Primary: **Google Geolocation API**
  - Fallback: Python `datetime.utcnow()`
- Used for:
  - Rate‑limit logic  
  - Audit logs  
  - Reproducibility  

---

### ✅ **4. Multi‑Agent Architecture**
- **PlannerAgent** → builds jingle plan (style, tempo, persona)
- **ComposerAgent** → calls **real Suno API**
- **QualityAgent** → evaluates structure + originality
- **JingleAgent** → domain‑specific plan builder
- **MemoryStore** → logs all interactions with timestamps

---

# 🧠 Updated Architecture Diagram

Full multi‑agent pipeline including REAL Suno + Google API:

```
User Request
      │
      ▼
PlannerAgent ──► JingleAgent (optional)
      │
      ▼
ComposerAgent (Suno API)
      │
      ▼
QualityAgent
      │
      ▼
TimeTool (Google Geolocation API)
      │
      ▼
MemoryStore (JSON)
      │
      ▼
Final Response
```

---

# 📡 Kaggle Notebook

👉 **[Musigent Kaggle Notebook (GitHub version)](https://github.com/mzchimeh/musigent/blob/main/notebooks/musigent-notebook.ipynb)**

This notebook contains:
- Full pipeline demonstration  
- Suno API integration  
- Rate‑limit test cell  
- Factory reset instructions  
- Example jingle generations  

---

# 📂 Project Structure

```
musigent/
│
├── musigent/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── composer.py         # Calls real Suno API
│   │   ├── quality.py
│   │   ├── jingle.py
│   │   └── time.py             # Google Geolocation → UTC
│   │
│   ├── tools.py                # SunoTool + SpotifyTool wrappers
│   ├── memory.py               # JSON memory + limits
│   ├── runner.py               # Master orchestration logic
│
├── assets/
│   └── architecture.png
│
├── notebooks/
│   └── musigent-notebook.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

---

# ▶️ Running Locally

### Install dependencies
```
pip install -r requirements.txt
```

### Set API keys
```
export SUNO_API_KEY="your_key_here"
export GOOGLE_API_KEY="your_key_here"
```

### Run FastAPI demo
```
uvicorn app:app --reload
```

---

# 🧪 Example Usage

```
from musigent.runner import MusigentRunner

runner = MusigentRunner()

resp = runner.handle_jingle_survey(
    brand_name="TechNova",
    company_field="AI tools",
    customer_persona="startup founders",
    vibe="energetic",
    username="demo_user",
)

print(resp)
```

---

# ❗ Suno API Error 429 — Insufficient Credits

If you see:

```
ERROR — INSUFFICIENT CREDITS. PLEASE CHARGE YOUR ACCOUNT!
```

It means:

- ✔️ Your jingle pipeline **worked perfectly**
- ✔️ A real API request was sent
- ✔️ Suno responded successfully  
- ❌ Your Suno account needs more credits  

A clean formatted message is appended automatically.

---

# 🔧 Future Improvements

- Cloud deployment (Google Cloud Agent Engine)
- True Spotify OAuth taste modeling
- Vector‑memory upgrade
- Full Web UI
- Automatic persona creation using Suno Persona API

---

# 🤝 Contributions

PRs are welcome.  
This project was built as part of the **Kaggle Agents Intensive Capstone**.

---

### **MZ — Powered by Musigent**  
*November 2025*
