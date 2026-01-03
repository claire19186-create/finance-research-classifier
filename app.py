import streamlit as st
import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import io
from datetime import datetime
import time
import re
from collections import Counter

st.set_page_config(
    page_title="Finance Research Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS - MODERN STYLING ====================
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Paper item styling */
    .paper-item {
        background: #f8fafc;
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.2s ease;
    }
    
    .paper-item:hover {
        background: #f1f5f9;
        border-left-color: #764ba2;
    }
    
    /* Title styling */
    .paper-title {
        color: #1e293b;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    
    /* Authors styling */
    .paper-authors {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 12px;
        font-style: italic;
    }
    
    /* Abstract styling */
    .paper-abstract {
        color: #475569;
        font-size: 14px;
        line-height: 1.6;
        margin: 12px 0;
        padding: 12px;
        background: white;
        border-radius: 8px;
        border-left: 3px solid #e2e8f0;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .badge-primary {
        background: #e0e7ff;
        color: #3730a3;
    }
    
    .badge-secondary {
        background: #f1f5f9;
        color: #475569;
    }
    
    .badge-success {
        background: #dcfce7;
        color: #166534;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px 0;
        border-radius: 0 0 24px 24px;
        margin-bottom: 32px;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
        text-align: center;
        border: 1px solid #f1f5f9;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #1e293b;
        margin: 8px 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Search input */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 12px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        font-weight: 600;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
        <h1 style="margin: 0; font-size: 42px; font-weight: 700; line-height: 1.2;">📈 Finance Research Hub</h1>
        <p style="margin: 12px 0 0 0; font-size: 18px; opacity: 0.9; font-weight: 400;">
            Discover, classify, and explore cutting-edge finance research papers
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== ENHANCED KEYWORD DATABASE ====================
FINANCE_KEYWORD_DATABASE = {
    "Computational Finance": {
        "keywords": [
            "deep learning", "neural networks", "machine learning", "AI", "artificial intelligence",
            "gradient descent", "backpropagation", "convolutional", "recurrent", "transformer",
            "PDE", "partial differential equation", "numerical methods", "finite difference", "finite element",
            "Monte Carlo", "simulation", "stochastic", "high-dimensional", "computational",
            "algorithm", "optimization", "parallel computing", "GPU", "CUDA",
            "quantum computing", "quantum algorithms", "VQE", "quantum annealing",
            "reinforcement learning", "Q-learning", "deep Q-network", "policy gradient",
            "time series forecasting", "sequence models", "LSTM", "GRU", "attention"
        ],
        "weight": 1.0,
        "color": "#667eea",
        "icon": "💻"
    },
    
    "Mathematical Finance": {
        "keywords": [
            "stochastic calculus", "Ito", "Stratonovich", "Brownian motion", "martingale",
            "partial differential equation", "PDE", "Black-Scholes", "option pricing", "risk-neutral",
            "measure theory", "probability", "stochastic processes", "Levy processes", "jump diffusion",
            "Malliavin calculus", "Heston model", "SABR", "local volatility", "stochastic volatility",
            "optimal stopping", "optimal control", "Hamilton-Jacobi-Bellman", "dynamic programming",
            "portfolio optimization", "Markowitz", "mean-variance", "efficient frontier",
            "interest rate models", "Vasicek", "CIR", "HJM", "LIBOR market model"
        ],
        "weight": 0.95,
        "color": "#f59e0b",
        "icon": "📐"
    },
    
    "Portfolio Management": {
        "keywords": [
            "portfolio optimization", "asset allocation", "diversification", "efficient frontier",
            "mean-variance", "Markowitz", "Black-Litterman", "risk parity", "minimum variance",
            "tactical asset allocation", "strategic asset allocation", "rebalancing", "turnover",
            "tracking error", "active share", "index tracking", "enhanced indexing",
            "factor investing", "smart beta", "risk factors", "style factors",
            "hedge funds", "mutual funds", "ETF", "exchange-traded funds", "fund management",
            "performance measurement", "Sharpe ratio", "Sortino ratio", "information ratio"
        ],
        "weight": 0.9,
        "color": "#10b981",
        "icon": "📊"
    },
    
    "Risk Management": {
        "keywords": [
            "value at risk", "VaR", "expected shortfall", "ES", "CVaR", "conditional value at risk",
            "stress testing", "scenario analysis", "backtesting", "historical simulation",
            "credit risk", "default risk", "counterparty risk", "credit value adjustment", "CVA",
            "market risk", "volatility risk", "interest rate risk", "currency risk",
            "liquidity risk", "funding liquidity", "market liquidity", "bid-ask spread",
            "operational risk", "model risk", "legal risk", "compliance risk",
            "systemic risk", "too big to fail", "contagion", "network risk"
        ],
        "weight": 0.9,
        "color": "#8b5cf6",
        "icon": "⚠️"
    },
    
    "Pricing of Securities": {
        "keywords": [
            "option pricing", "Black-Scholes", "binomial tree", "trinomial tree", "finite difference",
            "Monte Carlo pricing", "least squares Monte Carlo", "LSM", "American options",
            "exotic options", "barrier options", "Asian options", "lookback options", "digital options",
            "interest rate derivatives", "swaps", "swaptions", "caps", "floors",
            "credit derivatives", "CDS", "credit default swaps", "CDO", "collateralized debt obligations",
            "fixed income pricing", "bond pricing", "yield curve", "term structure", "duration"
        ],
        "weight": 0.85,
        "color": "#ef4444",
        "icon": "💰"
    },
    
    "Financial Econometrics": {
        "keywords": [
            "time series analysis", "ARIMA", "ARMA", "ARCH", "GARCH", "EGARCH", "TGARCH",
            "vector autoregression", "VAR", "cointegration", "error correction model", "ECM",
            "unit root tests", "Dickey-Fuller", "Phillips-Perron", "KPSS",
            "volatility modeling", "realized volatility", "high-frequency data", "microstructure noise",
            "panel data", "fixed effects", "random effects", "dynamic panel", "GMM",
            "event study", "abnormal returns", "cumulative abnormal returns", "CAR"
        ],
        "weight": 0.85,
        "color": "#06b6d4",
        "icon": "📈"
    },
    
    "Market Microstructure": {
        "keywords": [
            "limit order book", "market orders", "limit orders", "order flow", "order imbalance",
            "bid-ask spread", "market depth", "liquidity", "illiquidity", "market impact",
            "price impact", "temporary impact", "permanent impact", "Kyle's lambda",
            "high-frequency trading", "algorithmic trading", "market making", "statistical arbitrage",
            "latency", "tick size", "minimum price variation", "decimalization"
        ],
        "weight": 0.8,
        "color": "#f97316",
        "icon": "⚡"
    },
    
    "Sustainable Finance": {
        "keywords": [
            "ESG", "environmental social governance", "sustainable investing", "responsible investing",
            "green bonds", "climate bonds", "sustainability-linked bonds",
            "carbon pricing", "carbon credits", "emissions trading", "cap and trade",
            "climate risk", "physical risk", "transition risk", "TCFD", "climate stress testing",
            "impact investing", "social impact bonds", "development finance"
        ],
        "weight": 0.75,
        "color": "#22c55e",
        "icon": "🌱"
    },
    
    "FinTech & Blockchain": {
        "keywords": [
            "blockchain", "distributed ledger", "smart contracts", "Ethereum", "solidity",
            "cryptocurrency", "Bitcoin", "Ethereum", "DeFi", "decentralized finance",
            "stablecoins", "CBDC", "central bank digital currency", "digital currency",
            "tokenization", "NFT", "non-fungible tokens", "security tokens",
            "crypto exchanges", "crypto wallets", "hot wallet", "cold wallet"
        ],
        "weight": 0.8,
        "color": "#6366f1",
        "icon": "🔗"
    }
}

# ==================== UTILITY FUNCTIONS ====================
def extract_keywords(text):
    """Extract meaningful keywords from text"""
    if not text:
        return []
    
    text = text.lower()
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    words = text.split()
    
    stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    keywords = [word for word in words if len(word) > 2 and word not in stopwords]
    
    return keywords

def calculate_category_scores(text, top_k=5):
    """Calculate classification scores based on keyword matching"""
    if not text:
        return []
    
    text_lower = text.lower()
    scores = {}
    
    for category, data in FINANCE_KEYWORD_DATABASE.items():
        score = 0
        matched_keywords = []
        
        for keyword in data['keywords']:
            if keyword.lower() in text_lower:
                score += 1
                matched_keywords.append(keyword)
        
        weighted_score = score * data['weight']
        
        if weighted_score > 0:
            scores[category] = {
                'score': weighted_score,
                'confidence': min(100, weighted_score * 10),
                'matched_keywords': matched_keywords[:10],
                'total_matches': len(matched_keywords),
                'icon': data['icon'],
                'color': data['color']
            }
    
    sorted_categories = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
    return sorted_categories[:top_k]

def enhanced_classify_with_confidence(text, top_k=5):
    """Enhanced classification function with keyword-based scoring"""
    category_scores = calculate_category_scores(text, top_k)
    
    results = []
    for category, data in category_scores:
        results.append({
            "category": category,
            "confidence": data['confidence'],
            "score": data['score'],
            "icon": data['icon'],
            "color": data['color'],
            "matched_keywords": data['matched_keywords'],
            "total_matches": data['total_matches']
        })
    
    if not results:
        default_categories = ["Computational Finance", "Mathematical Finance", "Financial Econometrics"]
        for category in default_categories[:top_k]:
            results.append({
                "category": category,
                "confidence": 30.0,
                "score": 3.0,
                "icon": FINANCE_KEYWORD_DATABASE[category]['icon'],
                "color": FINANCE_KEYWORD_DATABASE[category]['color'],
                "matched_keywords": [],
                "total_matches": 0
            })
    
    return results

# ==================== LOAD RESEARCH PAPERS ====================
@st.cache_data
def load_research_papers():
    try:
        with open('research_papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        papers_df = pd.DataFrame(papers)
        
        if 'published' in papers_df.columns:
            papers_df['published_date'] = pd.to_datetime(papers_df['published'])
            papers_df['date_display'] = papers_df['published_date'].dt.strftime('%b %d, %Y')
        
        category_colors = {
            'Computational Finance': '#667eea',
            'General Finance': '#764ba2',
            'Mathematical Finance': '#f59e0b',
            'Portfolio Management': '#10b981',
            'Pricing of Securities': '#ef4444',
            'Risk Management': '#8b5cf6'
        }
        papers_df['category_color'] = papers_df['category'].map(category_colors)
        
        return papers_df, papers
    except Exception as e:
        st.error(f"Error loading research papers: {e}")
        return pd.DataFrame(), []

papers_df, papers_list = load_research_papers()

# ==================== RESEARCH LIBRARY ====================
def display_research_library():
    """Display the research library interface"""
    
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1e293b; font-size: 28px; font-weight: 700; margin-bottom: 8px;">
            📚 Research Library
        </h2>
        <p style="color: #64748b; font-size: 16px; margin-bottom: 24px;">
            Browse and explore finance research papers from arXiv
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    if not papers_df.empty:
        stats_cols = st.columns(4)
        with stats_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(papers_df)}</div>
                <div class="metric-label">Total Papers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[1]:
            unique_categories = papers_df['category'].nunique() if 'category' in papers_df.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{unique_categories}</div>
                <div class="metric-label">Categories</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[2]:
            if 'year' in papers_df.columns:
                recent_year = papers_df['year'].max()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{recent_year}</div>
                    <div class="metric-label">Latest Year</div>
                </div>
                """, unsafe_allow_html=True)
        
        with stats_cols[3]:
            if 'authors' in papers_df.columns:
                avg_authors = papers_df['authors'].apply(lambda x: len(x) if isinstance(x, list) else 1).mean()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="font-size: 28px;">{avg_authors:.1f}</div>
                    <div class="metric-label">Avg Authors</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Search and Filter
    with st.container():
        st.markdown("""
        <div class="card" style="margin-top: 24px;">
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin-bottom: 20px;">
                🔍 Search & Filter Papers
            </h3>
        """, unsafe_allow_html=True)
        
        search_cols = st.columns([3, 1, 1, 1])
        with search_cols[0]:
            search_query = st.text_input(
                "Search papers by title, authors, or abstract",
                placeholder="Type keywords to search...",
                key="library_search"
            )
        
        with search_cols[1]:
            if 'category' in papers_df.columns:
                categories = sorted(papers_df['category'].dropna().unique().tolist())
                selected_category = st.selectbox("Category", ["All Categories"] + categories, key="category_filter")
        
        with search_cols[2]:
            if 'year' in papers_df.columns:
                years = sorted(papers_df['year'].dropna().unique().tolist(), reverse=True)
                selected_year = st.selectbox("Year", ["All Years"] + [str(y) for y in years], key="year_filter")
        
        with search_cols[3]:
            sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Title (A-Z)", "Title (Z-A)"], key="sort_filter")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = papers_df.copy()
    
    if not papers_df.empty:
        if search_query:
            mask = (
                filtered_df['title'].str.contains(search_query, case=False, na=False) |
                filtered_df['abstract'].str.contains(search_query, case=False, na=False) |
                filtered_df['authors'].apply(lambda x: search_query.lower() in str(x).lower() if x else False)
            )
            filtered_df = filtered_df[mask]
        
        if 'category' in filtered_df.columns and selected_category != "All Categories":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        if 'year' in filtered_df.columns and selected_year != "All Years":
            filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
        
        if sort_by == "Newest First":
            if 'published_date' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('published_date', ascending=False)
        elif sort_by == "Oldest First":
            if 'published_date' in filtered_df.columns:
                filtered_df = filtered_df.sort_values('published_date', ascending=True)
        elif sort_by == "Title (A-Z)":
            filtered_df = filtered_df.sort_values('title')
        elif sort_by == "Title (Z-A)":
            filtered_df = filtered_df.sort_values('title', ascending=False)
    
    # Display Results
    if filtered_df.empty:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 48px 24px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔍</div>
            <h3 style="color: #475569; margin-bottom: 8px;">No papers found</h3>
            <p style="color: #94a3b8;">Try adjusting your search or filter criteria</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 32px 0 16px 0;">
            <div>
                <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin: 0;">
                    📄 Found {len(filtered_df)} papers
                </h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each paper
        for idx, paper in filtered_df.iterrows():
            paper_html = f"""
            <div class="paper-item">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div style="flex: 1;">
                        <div class="paper-title">
                            <span style="color: #667eea; margin-right: 8px;">📄</span>
                            {paper.get('title', 'Untitled')}
                        </div>
                        <div class="paper-authors">
                            👥 {', '.join(paper.get('authors', [])) if isinstance(paper.get('authors', []), list) else paper.get('authors', 'Unknown')}
                        </div>
                    </div>
                    <div style="text-align: right; min-width: 120px;">
                        <span class="badge badge-primary" style="background-color: {paper.get('category_color', '#e0e7ff')}20; color: {paper.get('category_color', '#3730a3')}; border: 1px solid {paper.get('category_color', '#3730a3')}40;">
                            {paper.get('category', 'Unknown')}
                        </span>
                    </div>
                </div>
                
                <div style="display: flex; gap: 12px; margin-bottom: 12px; flex-wrap: wrap;">
                    <span class="badge badge-secondary">
                        📅 {paper.get('date_display', 'Unknown date')}
                    </span>
                    <span class="badge badge-secondary">
                        🏷️ arXiv: {paper.get('arxiv_id', 'N/A')}
                    </span>
                    <span class="badge badge-secondary">
                        📝 {paper.get('word_count', 0)} words
                    </span>
                </div>
                
                <div class="paper-abstract">
                    <div style="font-weight: 600; color: #475569; margin-bottom: 8px; font-size: 13px;">
                        ABSTRACT
                    </div>
                    {paper.get('abstract', 'No abstract available')}
                </div>
                
                <div style="display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap;">
            """
            
            if 'arxiv_url' in paper and paper['arxiv_url']:
                paper_html += f"""
                    <a href="{paper['arxiv_url']}" target="_blank" style="
                        background: #e0e7ff;
                        color: #3730a3;
                        text-decoration: none;
                        padding: 6px 16px;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 500;
                        display: inline-flex;
                        align-items: center;
                        gap: 6px;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.background='#c7d2fe'; this.style.transform='translateY(-1px)'"
                    onmouseout="this.style.background='#e0e7ff'; this.style.transform='translateY(0)'">
                        📄 arXiv
                    </a>
                """
            
            if 'pdf_url' in paper and paper['pdf_url']:
                paper_html += f"""
                    <a href="{paper['pdf_url']}" target="_blank" style="
                        background: #fee2e2;
                        color: #991b1b;
                        text-decoration: none;
                        padding: 6px 16px;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 500;
                        display: inline-flex;
                        align-items: center;
                        gap: 6px;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.background='#fecaca'; this.style.transform='translateY(-1px)'"
                    onmouseout="this.style.background='#fee2e2'; this.style.transform='translateY(0)'">
                        📥 PDF
                    </a>
                """
            
            paper_html += f"""
                    <button onclick="classifyPaper('{paper.get('title', '').replace("'", "\\'")}', '{paper.get('abstract', '').replace("'", "\\'")}')" style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        padding: 6px 16px;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 500;
                        cursor: pointer;
                        display: inline-flex;
                        align-items: center;
                        gap: 6px;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(102, 126, 234, 0.3)'"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                        🤖 Classify
                    </button>
                </div>
            </div>
            """
            
            st.markdown(paper_html, unsafe_allow_html=True)

# ==================== ENHANCED CLASSIFIER ====================
def display_classification_results(top_results, paper_title="", abstract_text=""):
    """Display enhanced classification results"""
    
    if not top_results:
        st.info("No classification results available.")
        return
    
    top_category = top_results[0]
    
    if top_category["confidence"] > 70:
        confidence_color = "#10b981"
        confidence_level = "High"
    elif top_category["confidence"] > 40:
        confidence_color = "#f59e0b"
        confidence_level = "Medium"
    else:
        confidence_color = "#ef4444"
        confidence_level = "Low"
    
    # Display results
    st.markdown(f"""
    <div class="card" style="margin: 24px 0;">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
            <div style="font-size: 36px; color: {top_category['color']};">
                {top_category['icon']}
            </div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 8px 0; color: #1e293b; font-size: 20px;">
                    AI Classification Results
                </h3>
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Based on keyword analysis of abstract and title
                </p>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
            <div>
                <div style="background: {confidence_color}10; padding: 20px; border-radius: 12px; border-left: 4px solid {confidence_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div>
                            <div style="font-size: 14px; color: #64748b; margin-bottom: 4px;">Primary Classification</div>
                            <div style="font-size: 24px; font-weight: 700; color: {top_category['color']};">
                                {top_category['category']}
                            </div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 32px; font-weight: 700; color: {confidence_color};">
                                {top_category['confidence']:.1f}%
                            </div>
                            <div style="font-size: 12px; color: {confidence_color};">
                                {confidence_level} Confidence
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 16px;">
                        <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">Matched Keywords:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                            {''.join([f'<span style="background: {top_category["color"]}20; color: {top_category["color"]}; padding: 4px 10px; border-radius: 16px; font-size: 12px; font-weight: 500;">{kw}</span>' for kw in top_category["matched_keywords"][:8]])}
                        </div>
                    </div>
                </div>
            </div>
            
            <div>
                <div style="background: #f8fafc; padding: 20px; border-radius: 12px;">
                    <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">Classification Details</div>
                    <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span>Total Keywords Matched:</span>
                            <span style="font-weight: 600;">{top_category['total_matches']}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span>Classification Score:</span>
                            <span style="font-weight: 600;">{top_category['score']:.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Algorithm:</span>
                            <span style="font-weight: 600;">Keyword-based</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(top_category["confidence"] / 100, text=f"Model Confidence: {top_category['confidence']:.1f}%")
    
    # All categories
    st.markdown("### 📊 All Category Scores")
    cols = st.columns(len(top_results))
    for idx, (col, result) in enumerate(zip(cols, top_results)):
        with col:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 8px; color: {result['color']}">
                    {result['icon']}
                </div>
                <div style="font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 8px;">
                    {result['category']}
                </div>
                <div style="font-size: 20px; font-weight: 700; color: {result['color']}; margin-bottom: 4px;">
                    {result['confidence']:.1f}%
                </div>
                <div style="font-size: 11px; color: #64748b;">
                    {result['total_matches']} keywords matched
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_enhanced_classifier():
    """Display the enhanced classifier interface"""
    
    st.markdown("""
    <div class="card" style="margin-bottom: 32px;">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
            <div style="font-size: 48px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🤖
            </div>
            <div>
                <h2 style="color: #1e293b; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;">
                    Enhanced AI Classifier
                </h2>
                <p style="color: #64748b; margin: 0; font-size: 16px;">
                    Classify finance papers using advanced keyword analysis with 400+ specialized keywords
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin-bottom: 20px;">
                📝 Input Paper Details
            </h3>
        """, unsafe_allow_html=True)
        
        paper_title = st.text_area(
            "Paper Title",
            placeholder="Enter the research paper title...",
            height=60,
            key="classifier_title"
        )
        
        paper_abstract = st.text_area(
            "Abstract / Summary",
            placeholder="Paste the abstract or summary of the paper...",
            height=200,
            key="classifier_abstract"
        )
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            top_k = st.slider("Number of categories", 3, 10, 5, key="top_k_slider")
        with col_opt2:
            min_confidence = st.slider("Minimum confidence (%)", 20, 100, 30, key="min_confidence")
        
        classify_button = st.button(
            "🚀 Run Enhanced Classification",
            type="primary",
            use_container_width=True,
            key="enhanced_classify_button"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        total_keywords = sum(len(data['keywords']) for data in FINANCE_KEYWORD_DATABASE.values())
        st.markdown(f"""
        <div class="card">
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin-bottom: 20px;">
                📚 Classification Database
            </h3>
            
            <div style="margin-bottom: 24px;">
                <div style="font-size: 14px; color: #64748b; margin-bottom: 8px;">Database Statistics</div>
                <div style="background: #f8fafc; padding: 16px; border-radius: 12px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #475569;">Categories:</span>
                        <span style="font-weight: 600; color: #667eea;">{len(FINANCE_KEYWORD_DATABASE)}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #475569;">Total Keywords:</span>
                        <span style="font-weight: 600; color: #667eea;">{total_keywords}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #475569;">Avg per Category:</span>
                        <span style="font-weight: 600; color: #667eea;">{total_keywords // len(FINANCE_KEYWORD_DATABASE)}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if classify_button and (paper_title or paper_abstract):
        with st.spinner("🔍 Analyzing text with enhanced keyword database..."):
            time.sleep(1)
            
            combined_text = f"{paper_title} {paper_abstract}"
            classification_results = enhanced_classify_with_confidence(combined_text, top_k=top_k)
            
            filtered_results = [
                r for r in classification_results 
                if r['confidence'] >= min_confidence
            ]
            
            if filtered_results:
                display_classification_results(filtered_results, paper_title, paper_abstract)
                
                st.markdown("---")
                st.markdown("#### 📥 Export Classification Results")
                
                export_data = {
                    "title": paper_title,
                    "abstract": paper_abstract[:500],
                    "timestamp": datetime.now().isoformat(),
                    "classification_results": [
                        {
                            "category": r["category"],
                            "confidence": r["confidence"],
                            "matched_keywords": r["matched_keywords"],
                            "total_matches": r["total_matches"]
                        }
                        for r in filtered_results
                    ]
                }
                
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    st.download_button(
                        label="📁 Download JSON",
                        data=json.dumps(export_data, indent=2),
                        file_name=f"classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col_exp2:
                    st.download_button(
                        label="📊 Download CSV",
                        data=pd.DataFrame(filtered_results).to_csv(index=False),
                        file_name=f"classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.warning(f"No categories found with confidence ≥ {min_confidence}%")
    elif classify_button:
        st.error("Please enter at least a title or abstract to classify.")

# ==================== STATISTICS DASHBOARD ====================
def display_statistics():
    """Display statistics dashboard"""
    
    if papers_df.empty:
        st.warning("No research papers loaded.")
        return
    
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1e293b; font-size: 28px; font-weight: 700; margin-bottom: 8px;">
            📊 Research Analytics
        </h2>
        <p style="color: #64748b; font-size: 16px; margin-bottom: 24px;">
            Insights and trends from the research collection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_papers = len(papers_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #667eea;">{total_papers}</div>
            <div class="metric-label">Total Papers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_authors = papers_df['authors'].apply(lambda x: len(x) if isinstance(x, list) else 1).sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #764ba2;">{total_authors}</div>
            <div class="metric-label">Total Authors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_words = papers_df['word_count'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #10b981;">{total_words:,}</div>
            <div class="metric-label">Total Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_words = papers_df['word_count'].mean() if 'word_count' in papers_df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{avg_words:.0f}</div>
            <div class="metric-label">Avg Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("""
        <div class="card" style="margin-top: 24px;">
            <h3 style="color: #1e293b; font-size: 18px; font-weight: 600; margin-bottom: 20px;">
                📈 Category Distribution
            </h3>
        """, unsafe_allow_html=True)
        
        if 'category' in papers_df.columns:
            category_counts = papers_df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            colors = px.colors.qualitative.Plotly[:len(category_counts)]
            
            fig = go.Figure(data=[go.Pie(
                labels=category_counts['Category'],
                values=category_counts['Count'],
                hole=.4,
                marker_colors=colors,
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig.update_layout(
                height=400,
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with chart_col2:
        st.markdown("""
        <div class="card" style="margin-top: 24px;">
            <h3 style="color: #1e293b; font-size: 18px; font-weight: 600; margin-bottom: 20px;">
                📅 Publication Trend
            </h3>
        """, unsafe_allow_html=True)
        
        if 'year' in papers_df.columns:
            yearly_counts = papers_df['year'].value_counts().sort_index().reset_index()
            yearly_counts.columns = ['Year', 'Count']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=yearly_counts['Year'],
                y=yearly_counts['Count'],
                mode='lines+markers',
                line=dict(color='#667eea', width=4),
                marker=dict(size=10, color='white', line=dict(width=2, color='#667eea')),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)',
                name='Papers Published'
            ))
            
            fig.update_layout(
                height=400,
                xaxis_title="Year",
                yaxis_title="Number of Papers",
                hovermode='x unified',
                margin=dict(t=30, b=50, l=50, r=30)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
st.sidebar.markdown("""
<div style="padding: 20px 0;">
    <div style="text-align: center; margin-bottom: 32px;">
        <div style="font-size: 32px; margin-bottom: 8px;">📈</div>
        <div style="font-size: 18px; font-weight: 600; color: #1e293b;">Finance Research Hub</div>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">v3.0 • Professional Edition</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.header("🧭 Navigation")
app_mode = st.sidebar.radio(
    "",
    ["📚 Research Library", "🤖 Enhanced Classifier", "📊 Analytics"],
    help="Switch between different features",
    label_visibility="collapsed"
)

# Quick actions
st.sidebar.markdown("---")
st.sidebar.header("⚡ Quick Actions")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

if st.sidebar.button("📥 Export All Papers", use_container_width=True):
    if not papers_df.empty:
        csv = papers_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"finance_papers_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Info section
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ Info")

if not papers_df.empty:
    latest_paper = papers_df.sort_values('published_date', ascending=False).iloc[0]
    st.sidebar.markdown(f"""
    <div style="background: #f8fafc; padding: 16px; border-radius: 12px; border-left: 4px solid #667eea;">
        <div style="font-size: 13px; color: #64748b; margin-bottom: 4px;">Latest Paper</div>
        <div style="font-size: 14px; font-weight: 500; color: #1e293b; margin-bottom: 8px;">
            {latest_paper.get('title', 'Untitled')[:60]}...
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8;">
            <span>📅 {latest_paper.get('date_display', 'Unknown')}</span>
            <span>{latest_paper.get('category', 'Unknown')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN APP ROUTING ====================
if app_mode == "📚 Research Library":
    display_research_library()
    
elif app_mode == "🤖 Enhanced Classifier":
    display_enhanced_classifier()
    
elif app_mode == "📊 Analytics":
    display_statistics()

# ==================== FOOTER ====================
st.markdown("""
<div style="margin-top: 64px; padding: 32px 0; text-align: center; color: #94a3b8; border-top: 1px solid #e2e8f0;">
    <div style="font-size: 14px; margin-bottom: 8px;">
        Finance Research Hub • v3.0 • Made with ❤️ for researchers
    </div>
    <div style="display: flex; justify-content: center; gap: 24px; margin-top: 16px;">
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">📚 Documentation</a>
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">🐙 GitHub</a>
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Add JavaScript for classification
st.markdown("""
<script>
function classifyPaper(title, abstract) {
    // Create notification
    const notification = document.createElement('div');
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
            z-index: 9999;
            display: flex;
            align-items: center;
            gap: 16px;
            animation: slideIn 0.3s ease;
            max-width: 400px;
        ">
            <div style="font-size: 24px;">🤖</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">Classification Started</div>
                <div style="font-size: 12px; opacity: 0.9; line-height: 1.4;">
                    Redirecting to classifier with paper:<br>
                    <strong>${title.substring(0, 50)}...</strong>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(notification);
    
    // Store paper info in localStorage
    localStorage.setItem('paper_to_classify', JSON.stringify({
        title: title,
        abstract: abstract,
        timestamp: new Date().toISOString()
    }));
    
    // Switch to classifier tab
    const event = new CustomEvent('switchToClassifier', {
        detail: { title: title, abstract: abstract }
    });
    window.dispatchEvent(event);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.innerHTML = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)