# Opportunity Hub: Content-Based Recommendation System

Students spend a lot of time hunting for internships, hackathons, and workshops — and often can't even tell which ones they're eligible for. This system recommends opportunities that match a student's skill profile.

**Live demo:** [https://event-management-system-l5kc.onrender.com](https://event-management-system-l5kc.onrender.com)

---

## How It Works

* **Dataset:** A dataset of 5,000 opportunities containing domain, required/preferred skills, eligibility, mode, deadline, and more.
* **Feature Extraction:** Skills are cleaned using a comma-based tokenizer, and TF-IDF vectors are built (94 unique tokens).
* **Cosine Similarity:** The student's profile is transformed into the same TF-IDF vector space to calculate similarity match scores.
* **Boolean Mask Filtering:** Filters are applied for deadline, eligibility year, branch, and mode using boolean masks to keep matrix row indices strictly aligned.
* **Skill Insights:** Each recommendation highlights both matched and missing skills to help students bridge skill gaps.

---

## Tech Stack

* **Language:** Python
* **Data Processing & ML:** pandas, scikit-learn
* **Web Framework / UI:** Streamlit, FastAPI
* **Database:** SQLite (SQLAlchemy)

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Note

> The dataset is synthetic. Dates were shifted forward so deadlines remain valid during the demo.
