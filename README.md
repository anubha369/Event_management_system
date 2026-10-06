# Opportunity Hub: AI-Powered Event & Recommendation System

Opportunity Hub is a comprehensive platform connecting **Students**, **Organizers**, and **Platform Administrators**. It provides AI-driven content recommendation for students, registration predictions for event organizers, platform analytics, risk/anomaly detection for admins, and a Gemini-powered AI chatbot assistant.

---

## 🌟 Comprehensive Feature Map & Specifications for AI/Frontend Developers

If you are generating a frontend app (React, Next.js, Vue, Mobile App, or Streamlit), use this document as the complete blueprint for API contracts, page layouts, components, and data structures.

---

## 1. 🎓 Student Module (Recommendation Engine)

### Problem
Students waste time searching across opportunities without knowing match compatibility, missing required skills, or eligibility compliance.

### AI Model Specification
* **Algorithm:** TF-IDF Vectorizer + Cosine Similarity with custom Comma-Tokenizer (`skill_tokenizer`).
* **Vocabulary Size:** ~94 unique technical skills and tokens.
* **Domain Bonus:** `+0.1` boost to similarity score if exact domain matches.
* **Strict Masking:** Mask out expired deadlines, incompatible student eligibility years, non-matching engineering branches, and modes (`Online`, `Offline`, `Hybrid`).
* **Skill Gap Analysis:** Computes `matched` skills vs `missing` skills dynamically.

### Frontend API Contract

#### `POST /student/recommend`
* **Request Payload (`application/json`):**
  ```json
  {
    "domain": "Web Development",
    "skills": "React, Node.js, JavaScript",
    "year": "3rd Year",
    "branch": "CSE",
    "mode": "Online",
    "top_n": 10
  }
  ```
* **Response Payload (`application/json`):**
  ```json
  {
    "recommendations": [
      {
        "title": "Full Stack Hackathon 2026",
        "organization": "Digital India Community",
        "domain": "Web Development",
        "category": "Hackathon",
        "mode": "Online",
        "deadline": "2026-10-30",
        "required_skills": "Express.js, Node.js, JavaScript, React, MongoDB",
        "application_url": "https://example.org/opportunity/0002",
        "score": 0.88,
        "matched": "javascript, node.js, react",
        "missing": "express.js, mongodb"
      }
    ]
  }
  ```

---

## 2. 📊 Organizer Module (Registration Predictor & Analytics)

### Features
1. **Predictive Registration Estimator:** Machine Learning model (`RandomForest`/`Regression`) that estimates total expected student registrations before an event is published based on event characteristics.
2. **Event Demand & Distribution Tracker:** Provides real-time metrics on event status breakdowns (`PENDING`, `APPROVED`, `REJECTED`) and event mode distribution (`Online`, `Offline`, `Hybrid`).
3. **Platform Performance Dashboard:** High-level totals for users, verified/pending organizers, and total events.

### Frontend API Contracts

#### `POST /organizer/predict-registrations`
* **Request Payload (`application/json`):**
  ```json
  {
    "domain": "Artificial Intelligence",
    "category": "Hackathon",
    "mode": "Online",
    "prize_money_inr": 25000,
    "application_fee_inr": 0,
    "certificate_available": true,
    "team_required": true,
    "min_team_size": 2,
    "max_team_size": 4
  }
  ```
* **Response Payload (`application/json`):**
  ```json
  {
    "predicted_registrations": 485
  }
  ```

#### `GET /organizer/event-demand`
* **Response Payload (`application/json`):**
  ```json
  {
    "total_events": 5000,
    "event_status": {
      "pending": 1008,
      "approved": 3468,
      "rejected": 524
    },
    "mode_distribution": {
      "online": 1719,
      "offline": 1718,
      "hybrid": 1563
    }
  }
  ```

#### `GET /organizer/analytics`
* **Response Payload (`application/json`):**
  ```json
  {
    "platform_statistics": {
      "total_users": 1500,
      "total_organizers": 45,
      "total_events": 5000
    },
    "organizer_statistics": {
      "pending_verification": 5,
      "verified": 40
    },
    "event_statistics": {
      "pending": 1008,
      "approved": 3468,
      "rejected": 524
    }
  }
  ```

---

## 3. 🛡️ Admin Module (Event Risk & Anomaly Detection)

### Features
* **Scam / Risk Detection Model:** Uses an ML Anomaly Detection model (`IsolationForest`) to compute risk scores for newly created events.
* **Automated Triage System:** Flags suspicious listings (`NEEDS REVIEW` vs `NORMAL`) and assigns review priority (`HIGH`, `MEDIUM`, `LOW`) based on anomaly scores.

### Frontend API Contract

#### `POST /admin/event-risk`
* **Request Payload (`application/json`):**
  ```json
  {
    "prize_money_inr": 500000,
    "application_fee_inr": 5000,
    "certificate_available": false,
    "team_required": false
  }
  ```
* **Response Payload (`application/json`):**
  ```json
  {
    "admin_status": "NEEDS REVIEW",
    "risk_score": 82.5,
    "review_priority": "HIGH",
    "anomaly_score": -0.325
  }
  ```

---

## 4. 🤖 AI Chatbot Module (Gemini Assistant)

### Features
* **Conversational Guidance:** Powered by Google Gemini (`gemini-3.8-flash`) to answer student queries, explain skill gaps, and guide event organizers.
* **Context Preservation:** Keeps track of chat threads using `previous_interaction_id`.

### Frontend API Contract

#### `POST /chat`
* **Request Payload (`application/json`):**
  ```json
  {
    "message": "Which skills should I learn for Full Stack Web Development?",
    "previous_interaction_id": "optional_previous_id"
  }
  ```
* **Response Payload (`application/json`):**
  ```json
  {
    "reply": "To excel in Full Stack Web Development, focus on React, Node.js, Express, and MongoDB...",
    "interaction_id": "interaction_xyz123"
  }
  ```

---

## 🗄️ Database Schema & Entities (SQLite / PostgreSQL)

### 1. `users` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | User unique ID |
| `name` | String | Not Null | User full name |
| `email` | String | Unique, Indexed | User email |
| `password_hash` | String | Not Null | Encrypted password |
| `role` | String | Default "USER" | Role (`STUDENT`, `ORGANIZER`, `ADMIN`) |
| `branch` | String | Nullable | Engineering Branch (e.g. `CSE`, `ECE`) |
| `year` | Integer | Nullable | Academic Year (`1`, `2`, `3`, `4`) |
| `status` | String | Default "ACTIVE" | Account Status |

### 2. `organizers` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Organizer record ID |
| `user_id` | Integer | Foreign Key (`users.id`) | Linked user account |
| `organization_name` | String | Not Null | Company or Club Name |
| `verification_status` | String | Default "PENDING" | Status (`PENDING`, `VERIFIED`, `REJECTED`) |

### 3. `events` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Event unique ID |
| `organizer_id` | Integer | Foreign Key (`organizers.id`) | Hosting organizer |
| `title` | String | Not Null | Event Title |
| `domain` | String | Indexed | Domain (e.g., `Web Development`, `AI`) |
| `category` | String | Indexed | Category (`Hackathon`, `Internship`, `Workshop`) |
| `mode` | String | Indexed | `Online`, `Offline`, `Hybrid` |
| `prize_money` | Integer | Default 0 | Prize Pool in INR |
| `application_fee` | Integer | Default 0 | Fee in INR |
| `certificate_available` | Boolean | Default False | Certificate toggle |
| `team_required` | Boolean | Default False | Team participation toggle |
| `status` | String | Default "PENDING" | `PENDING`, `APPROVED`, `REJECTED` |

---

## 🎨 Recommended UI Component Blueprint for Frontend AI Agents

### 1. Student Portal Page (`/student`)
* **Sidebar Controls:** Dropdowns for Domain, Multi-select for Skills, Select for Year, Branch, Mode (`Any/Online/Offline/Hybrid`), and Slider for `Top N Results`.
* **Recommendation Card Component:**
  * **Header:** Title, Organization badge, Domain & Category tags.
  * **Progress Indicator:** Visual Match Percentage Bar (`min(score, 1.0)`).
  * **Skill Chips:** Green chips for `matched` skills, Red/Grey chips for `missing` skills.
  * **Action Button:** External link button redirecting to `application_url`.

### 2. Organizer Portal Page (`/organizer`)
* **Predictor Form Component:** Inputs for Domain, Category, Mode, Fees, Prize Money, and Certificates. Displays estimated registration count badge upon submission.
* **Analytics Component:** Bar graphs and pie charts for Event Status Distribution (`Approved`, `Pending`, `Rejected`) and Mode Distribution.

### 3. Admin Portal Page (`/admin`)
* **Risk Review Dashboard:** Table of events flagged by `/admin/event-risk`.
* **Risk Badges:** High Priority (Red), Medium Priority (Orange), Low Priority (Green).

### 4. Floating Chatbot Widget (`/chat`)
* **UI Component:** Sticky bottom-right chat modal supporting markdown output and input memory.

---

## 🛠️ How to Run Backend APIs

```bash
# Install dependencies
pip install -r requirements.txt

# Seed SQLite database (creates opportunity_hub.db with 5,000 events)
python seed_database.py

# Launch FastAPI server (with Swagger docs at http://127.0.0.1:8000/docs)
uvicorn combined_api:app --reload --port 8000

# Launch Streamlit frontend
streamlit run app.py
```
