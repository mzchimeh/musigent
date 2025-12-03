# 🎵 Musigent — AI Jingle & Music Agent (Real‑World Suno API + Multi‑Agent System)

*A multi‑agent AI system that generates copyright‑safe jingles, background music, and persona‑based audio using real external APIs.*

Musigent is built as the **Capstone Project for the Kaggle 5‑Day Agents Intensive**, using a fully modular **multi‑agent architecture** enhanced with:

- **Real Suno Music Generation API**
- **Google Geolocation API (UTC timestamp + rate‑limit enforcement)**
- **Audd.io Music Recognition API (Copyright Safety Checker)**
- **Daily anti‑spam user limits**
- **Short‑term (per‑minute) request throttling**
- **Persistent memory** with user‑time tracking

---

# 🚀 Key Features

### ✅ **1. Real Jingle Generator (Suno API Integrated)**
- Generates **real audio** using Suno’s official API.
- Jingle creation pipeline:
  **Planner → JingleAgent → Composer (Suno API) → QualityAgent → MemoryStore → Final Output**
- Handles API errors, 429 insufficient credits, malformed responses, etc.

---

### ✅ **2. Copyright Safety Checker (NEW)**
Musigent now includes a **two-stage copyright safety system**:

#### **A. Originality Score (Local Audio Analysis)**
- RMS‑variance algorithm evaluates originality.
- Detects repetitive patterns or low‑variation tracks.
- Returns `None` if audio cannot be analyzed.

#### **B. Audd.io Music Recognition**
- Sends generated audio to Audd.io for copyright matching.
- Reports:
  - `risk_level: low | medium | high`
  - Matching track metadata (if found)
  - Copyright safety score
  - Reasons and cross‑database results

Ensures **copyright‑safe** and publication‑ready music.

---

### ✅ **3. Anti‑Spam Protection**
Two‑level protection:

#### **A. Per‑day Limit**
- Max **5 jingles per user per day**

#### **B. Per‑minute Limit**
- Max **5 jingles per minute**
- Uses **Google Geolocation UTC timestamp** for consistency

No unnecessary Suno API calls when limits are exceeded.

---

### ✅ **4. Time + Geolocation Agent**
- Fetches precise UTC time via **Google Geolocation API**
- Falls back to Python `datetime.utcnow()` when offline
- Supports:
  - Rate limiting
  - Logging
  - Audit tracking

---

### ✅ **5. Multi‑Agent Architecture**
| Agent | Role |
|-------|------|
| **PlannerAgent** | Builds jingle plan (style, tempo, persona) |
| **JingleAgent** | Creates structured jingle prompts |
| **ComposerAgent** | Calls Suno API to generate audio |
| **TimeAgent** | Provides UTC timestamps |
| **QualityAgent** | Originality analysis + copyright safety |
| **MemoryStore** | Persistent JSON database with timestamps |

---

# 🧠 Updated Architecture Diagram

```mermaid
flowchart LR
    classDef dark fill:#1a1a1a,stroke:#888,color:#e6e6e6;
    classDef api fill:#222,stroke:#999,color:#e6e6e6;

    U["User"]:::dark --> J["JingleAgent"]:::dark

    subgraph M["Musigent"]:::dark
        J --> MS["MemoryStore"]:::dark
        MS <--> T["TimeAgent"]:::dark
        T --> Q["QualityAgent (Originality + Copyright)"]:::dark
    end

    J --> SUNO["Suno API"]:::api
    Q --> SUNO:::api

    T --> GAPI["Google Geolocation API"]:::api
    Q --> AUDD["Audd.io Music Recognition API"]:::api

    Q --> MS:::dark
```

---

# 📡 Kaggle Notebook

👉 **[Musigent Kaggle Notebook](https://github.com/mzchimeh/musigent/blob/main/notebooks/musigent-notebook.ipynb)**

---

# 📂 Project Structure

```
musigent/
│
├── musigent/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── composer.py
│   │   ├── quality.py
│   │   ├── jingle.py
│   │   └── time.py
│   │
│   ├── tools.py
│   ├── memory.py
│   ├── runner.py
│   ├── utils/
│   │   └── formatter.py
│
├── assets/
│   ├── MUSIGENT-Architecture-MZ.png
│   └── MUSIGENT-Architecture-MZ-Dark.png
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
```bash
pip install -r requirements.txt
```

### Set API keys
```bash
export SUNO_API_KEY="your_suno_key"
export GOOGLE_API_KEY="your_google_key"
export AUDD_API_KEY="your_audd_key"
```

### Run API server
```bash
uvicorn app:app --reload
```

---

# 🧪 Example Usage

```python
from musigent.runner import MusigentRunner

runner = MusigentRunner()

resp = runner.handle_jingle_survey(
    brand_name="TechNova",
    company_field="AI tools",
    customer_persona="startup founders",
    vibe="energetic",
    username="demo_user"
)

print(resp)
```

---

# ❗ Handling Suno “Insufficient Credits” Error

If you see:

```
ERROR — INSUFFICIENT CREDITS. PLEASE CHARGE YOUR ACCOUNT!
```

It means:

- ✔️ Your multi‑agent pipeline executed correctly  
- ✔️ Suno API was called successfully  
- ❌ You simply need more credits to generate audio  

This is expected behavior in the demo version.

---

# 🔧 Future Improvements

- Full Web UI interface  
- Cloud agent deployment  
- Upgrade memory system to vector embeddings  
- Spotify taste modeling (OAuth)  
- Persona-driven jingle generator  
- Batch jingle production  

---

# 🤝 Contributions

Contributions and PRs are welcome.  
Built as part of the **Kaggle Agents Intensive Capstone**.

---

### **Musigent — by MZ (2025)**
