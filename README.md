# Opportunity Hub: Content-Based Recommendation System

Students ko internships, hackathons, workshops jaisi opportunities dhundhne mein time lagta hai aur kaunsi unke liye eligible hai yeh pata nahi hota. Yeh system student ki skills se match hone wali opportunities recommend karta hai.

**Live demo:** <apna Streamlit link yahan daal>

## Kaise kaam karta hai
1. 5000 opportunities ka dataset (domain, required/preferred skills, eligibility, mode, deadline).
2. Skills ko comma-based tokenizer se clean kiya, TF-IDF vectors banaye (94 unique tokens).
3. Student ki profile ko wahi TF-IDF space mein transform kiya.
4. Cosine similarity se match score nikala.
5. Filters: deadline, eligibility year, branch, mode. Filters mask se lagte hain taaki matrix ke row indices na bigdein.
6. Har result ke saath matched aur missing skills dikhte hain.

## Tech
Python, pandas, scikit-learn, Streamlit

## Chalane ka tarika
```
pip install -r requirements.txt
streamlit run app.py
```

## Note
Dataset synthetic hai. Dates ko aage shift kiya gaya hai taaki demo mein deadlines valid rahein.
