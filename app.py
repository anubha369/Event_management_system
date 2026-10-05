import streamlit as st
from recommender import Recommender

st.set_page_config(page_title="Opportunity Hub", layout="wide")


@st.cache_resource
def load():
    return Recommender("Opportunity_Hub_Shifted.csv")


rec = load()

st.title("Opportunity Hub")
st.caption("Apni skills daal, tere liye sahi opportunities milengi.")

with st.sidebar:
    domain = st.selectbox("Domain", rec.domains())
    skills = st.multiselect("Skills", rec.skills())
    year = st.selectbox("Year", rec.years())
    branch = st.selectbox("Branch", rec.branches())
    mode = st.selectbox("Mode", ["Any", "Online", "Offline", "Hybrid"])
    top_n = st.slider("Kitne results", 5, 20, 10)
    go = st.button("Recommend", type="primary")

if go:
    if not skills:
        st.warning("Kam se kam ek skill chun.")
    else:
        res = rec.recommend(domain, ", ".join(skills), year, branch, mode, top_n)
        if res.empty:
            st.info("Koi match nahi mila. Mode ya year ka filter dheela kar.")
        for _, r in res.iterrows():
            with st.container(border=True):
                st.subheader(r['title'])
                st.caption(f"{r['organization']} · {r['category']} · "
                           f"{r['mode']} · Deadline: {r['deadline']}")
                score = min(float(r['score']), 1.0)
                st.progress(score, text=f"Match: {score:.0%}")
                st.write("Matched:", r['matched'] or "-")
                st.write("Missing:", r['missing'] or "-")
                st.link_button("Apply", r['application_url'])
