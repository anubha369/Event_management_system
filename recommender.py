import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def skill_tokenizer(text):
    return [t.strip().lower() for t in text.split(',') if t.strip()]


class Recommender:
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        df['combined_features'] = (df['domain'] + ", " +
                                   df['required_skills'] + ", " +
                                   df['required_skills'] + ", " +
                                   df['preferred_skills'])
        self.df = df
        self.tfidf = TfidfVectorizer(tokenizer=skill_tokenizer,
                                     lowercase=False, token_pattern=None)
        self.matrix = self.tfidf.fit_transform(df['combined_features'])
        self.deadline = pd.to_datetime(df['deadline'])
        self.branch_lists = df['eligible_branch'].apply(
            lambda s: [b.strip().lower() for b in s.split(',')])

    # dropdown options data se hi nikalte hain
    def domains(self):
        return sorted(self.df['domain'].unique())

    def years(self):
        return [y for y in sorted(self.df['eligibility_year'].unique())
                if y != "Any Year"]

    def branches(self):
        b = self.df['eligible_branch'].str.split(',').explode().str.strip().unique()
        return sorted(x for x in b if not x.lower().startswith("all"))

    def skills(self):
        return sorted(self.df['required_skills'].str.split(', ').explode().unique())

    def recommend(self, domain, skills, year, branch, mode="Any",
                  top_n=10, domain_bonus=0.1):
        today = pd.Timestamp.today().normalize()
        text = domain + ", " + skills
        sim = cosine_similarity(self.tfidf.transform([text]), self.matrix).ravel()
        sim = sim + domain_bonus * (self.df['domain'] == domain).values

        b = branch.lower()
        mask = self.deadline >= today
        mask &= self.df['eligibility_year'].isin([year, "Any Year"])
        mask &= self.branch_lists.apply(
            lambda l: b in l or any(x.startswith("all") for x in l))
        if mode != "Any":
            mask &= (self.df['mode'] == mode)
        sim[~mask.values] = -1

        top = sim.argsort()[::-1][:50]
        res = self.df.iloc[top][['title', 'organization', 'domain', 'category',
                                 'mode', 'deadline', 'required_skills',
                                 'application_url']].copy()
        res['score'] = sim[top].round(3)
        res = res[res['score'] > 0]
        res = res.drop_duplicates(subset=['title', 'organization']).head(top_n)

        s_set = set(skill_tokenizer(skills))
        res['matched'] = res['required_skills'].apply(
            lambda t: ", ".join(sorted(set(skill_tokenizer(t)) & s_set)))
        res['missing'] = res['required_skills'].apply(
            lambda t: ", ".join(sorted(set(skill_tokenizer(t)) - s_set)))
        return res
