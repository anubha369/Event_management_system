Opportunity Hub: Content-Based Recommendation System


Students spend a lot of time hunting for internships, hackathons, and workshops — and often can't even tell which ones they're eligible for. This system recommends opportunities that match a student's skill profile.
Live demo: <https://event-management-system-l5kc.onrender.com>


How It Works:

* A dataset of 5000 opportunities (domain, required/preferred skills, eligibility, mode, deadline).

* Skills were cleaned using a comma-based tokenizer, and TF-IDF vectors were built (94 unique tokens).

* The student's profile is transformed into the same TF-IDF space.

* Cosine similarity produces a match score.

* Filters applied: deadline, eligibility year, branch, and mode. Filters use a boolean mask so the matrix row indices stay aligned.
* Each result shows both matched and missing skills.

Tech Stack:

Python
pandas
scikit-learn
Streamlit

How to Run:

bash
pip install -r requirements.txt
streamlit run app.py


Note:

The dataset is synthetic. Dates were shifted forward so deadlines remain valid during the demo.