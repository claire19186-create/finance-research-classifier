# app.py
# Fixed version: safe Plotly import + minor robustness fixes

import streamlit as st
import pandas as pd
import sys
import numpy as np
import json
import io
from datetime import datetime

# ===== OPTIONAL PLOTLY IMPORT =====
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False

# Add src folder to path
sys.path.append('src')

st.set_page_config(
    page_title="Finance Research Classifier",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Finance Research Paper Classifier & Library")
st.success("✅ Finance Research Classifier - Ready")

# ===== VERSION INFO =====
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Streamlit** {st.__version__}")
with col2:
    st.markdown(f"**Pandas** {pd.__version__}")
with col3:
    st.markdown(f"**Numpy** {np.__version__}")

if not PLOTLY_AVAILABLE:
    st.warning("⚠️ Plotly is not installed. Charts will be disabled. Add `plotly` to requirements.txt")

# ===== LOAD RESEARCH PAPERS =====
@st.cache_data
def load_research_papers():
    try:
        with open('research_papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)

        df = pd.DataFrame(papers)

        if 'published' in df.columns:
            df['published_date'] = pd.to_datetime(df['published'], errors='coerce')
            df['year'] = df['published_date'].dt.year

        if 'category' in df.columns:
            df['category_clean'] = df['category'].astype(str).str.replace('_', ' ').str.title()

        return df, papers
    except Exception as e:
        st.error(f"Error loading research papers: {e}")
        return pd.DataFrame(), []

papers_df, papers_list = load_research_papers()

# ===== RESEARCH LIBRARY =====
def display_research_library():
    st.header("📚 Research Library")

    if papers_df.empty:
        st.warning("No research papers found.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Papers", len(papers_df))
    c2.metric("Categories", papers_df['category'].nunique() if 'category' in papers_df else 0)
    c3.metric("Latest Year", int(papers_df['year'].max()) if 'year' in papers_df else '-')

    st.subheader("🔍 Search")
    q = st.text_input("Search title / abstract")

    df = papers_df.copy()
    if q:
        df = df[
            df['title'].str.contains(q, case=False, na=False)
            | df['abstract'].str.contains(q, case=False, na=False)
        ]

    if df.empty:
        st.info("No matching papers")
        return

    for _, paper in df.iterrows():
        with st.expander(paper.get('title', 'Untitled')):
            st.markdown(f"**Authors:** {paper.get('authors', '-')}")
            st.markdown(f"**Year:** {paper.get('year', '-')}")
            st.markdown(f"**Category:** {paper.get('category', '-')}")
            st.write(paper.get('abstract', '')[:600])

# ===== MOCK CLASSIFIER =====
def classify_with_confidence(text, top_k=5):
    categories = [
        "Quantitative Finance", "Behavioral Finance", "Corporate Finance",
        "Asset Pricing", "Banking", "Fintech", "Risk Management"
    ]

    np.random.seed(abs(hash(text)) % 10_000)
    scores = np.random.dirichlet(np.ones(len(categories)))

    idx = np.argsort(scores)[::-1][:top_k]
    return [
        {
            "category": categories[i],
            "confidence": float(scores[i] * 100)
        }
        for i in idx
    ]

# ===== DISPLAY RESULTS =====
def display_results(results):
    st.subheader("🤖 Classification Results")
    df = pd.DataFrame(results)

    st.dataframe(
        df,
        column_config={
            "confidence": st.column_config.ProgressColumn(
                "Confidence (%)", min_value=0, max_value=100, format="%.2f%%"
            )
        },
        use_container_width=True
    )

    if PLOTLY_AVAILABLE:
        fig = px.bar(df, x='category', y='confidence')
        st.plotly_chart(fig, use_container_width=True)

# ===== SIDEBAR =====
st.sidebar.header("📚 Navigation")
mode = st.sidebar.radio("Mode", ["🏠 Classifier", "📚 Research Library"])

# ===== MAIN =====
if mode == "📚 Research Library":
    display_research_library()

else:
    st.header("📄 Text Classifier (Demo)")
    text = st.text_area("Paste abstract here")

    if st.button("Classify") and text:
        results = classify_with_confidence(text)
        display_results(results)

# ===== FOOTER =====
st.markdown("---")
st.caption("Finance Research Classifier • Plotly-safe version")
