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

# Add src folder to path
sys.path.append('src')

st.set_page_config(
    page_title="Finance Research Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
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
    
    .paper-title a {
        color: #1e293b;
        text-decoration: none;
    }
    
    .paper-title a:hover {
        color: #667eea;
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
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 500;
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

# Title with modern gradient
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

# ===== LOAD RESEARCH PAPERS FROM JSON =====
@st.cache_data
def load_research_papers():
    try:
        with open('research_papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        # Convert to DataFrame for easier manipulation
        papers_df = pd.DataFrame(papers)
        
        # Convert date columns to datetime
        if 'published' in papers_df.columns:
            papers_df['published_date'] = pd.to_datetime(papers_df['published'])
            papers_df['year_month'] = papers_df['published_date'].dt.strftime('%Y-%m')
            papers_df['date_display'] = papers_df['published_date'].dt.strftime('%b %d, %Y')
        
        # Clean up category names
        if 'category' in papers_df.columns:
            papers_df['category_clean'] = papers_df['category'].str.replace('_', ' ').str.title()
        
        # Add color mapping for categories
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

# Load papers
papers_df, papers_list = load_research_papers()

# ===== RESEARCH LIBRARY FUNCTIONS WITH MODERN DESIGN =====
def display_research_library():
    """Display the research library interface with modern design"""
    
    # Header with stats
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
    
    # Display statistics in modern cards
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
    
    # Search and filter section in a card
    with st.container():
        st.markdown("""
        <div class="card" style="margin-top: 24px;">
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin-bottom: 20px;">
                🔍 Search & Filter Papers
            </h3>
        """, unsafe_allow_html=True)
        
        # Search row
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
                selected_category = st.selectbox(
                    "Category",
                    ["All Categories"] + categories,
                    key="category_filter"
                )
        
        with search_cols[2]:
            if 'year' in papers_df.columns:
                years = sorted(papers_df['year'].dropna().unique().tolist(), reverse=True)
                selected_year = st.selectbox(
                    "Year",
                    ["All Years"] + [str(y) for y in years],
                    key="year_filter"
                )
        
        with search_cols[3]:
            sort_options = {
                "Newest First": "Newest",
                "Oldest First": "Oldest",
                "Title (A-Z)": "Title A-Z",
                "Title (Z-A)": "Title Z-A",
                "Most Authors": "Authors Desc",
                "Fewest Authors": "Authors Asc"
            }
            sort_by = st.selectbox(
                "Sort by",
                list(sort_options.keys()),
                key="sort_filter"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = papers_df.copy()
    
    if not papers_df.empty:
        # Apply search
        if search_query:
            mask = (
                filtered_df['title'].str.contains(search_query, case=False, na=False) |
                filtered_df['abstract'].str.contains(search_query, case=False, na=False) |
                filtered_df['authors'].apply(lambda x: search_query.lower() in str(x).lower() if x else False)
            )
            filtered_df = filtered_df[mask]
        
        # Apply category filter
        if 'category' in filtered_df.columns and selected_category != "All Categories":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        # Apply year filter
        if 'year' in filtered_df.columns and selected_year != "All Years":
            filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
        
        # Apply sorting
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
        elif sort_by == "Most Authors":
            filtered_df['author_count'] = filtered_df['authors'].apply(lambda x: len(x) if isinstance(x, list) else 1)
            filtered_df = filtered_df.sort_values('author_count', ascending=False)
        elif sort_by == "Fewest Authors":
            filtered_df['author_count'] = filtered_df['authors'].apply(lambda x: len(x) if isinstance(x, list) else 1)
            filtered_df = filtered_df.sort_values('author_count', ascending=True)
    
    # Display results
    if filtered_df.empty:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 48px 24px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔍</div>
            <h3 style="color: #475569; margin-bottom: 8px;">No papers found</h3>
            <p style="color: #94a3b8;">Try adjusting your search or filter criteria</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Results header
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 32px 0 16px 0;">
            <div>
                <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin: 0;">
                    📄 Found {len(filtered_df)} papers
                </h3>
                <p style="color: #64748b; margin: 4px 0 0 0; font-size: 14px;">
                    {search_query and f'Searched for: "{search_query}" • ' or ''}
                    {selected_category != "All Categories" and f'Category: {selected_category} • ' or ''}
                    {selected_year != "All Years" and f'Year: {selected_year} • ' or ''}
                    Sorted by: {sort_by}
                </p>
            </div>
            <div style="display: flex; gap: 8px;">
                <button onclick="window.scrollTo(0, 0)" style="
                    background: #f1f5f9;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    color: #475569;
                    cursor: pointer;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                ">
                    ⬆️ Scroll to top
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display papers in a nice format
        for idx, paper in filtered_df.iterrows():
            # Create paper card
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
            
            # Add links
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
            
            if 'doi' in paper and paper['doi']:
                paper_html += f"""
                    <a href="https://doi.org/{paper['doi']}" target="_blank" style="
                        background: #dbeafe;
                        color: #1e40af;
                        text-decoration: none;
                        padding: 6px 16px;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 500;
                        display: inline-flex;
                        align-items: center;
                        gap: 6px;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.background='#bfdbfe'; this.style.transform='translateY(-1px)'"
                    onmouseout="this.style.background='#dbeafe'; this.style.transform='translateY(0)'">
                        🔗 DOI
                    </a>
                """
            
            # Add classify button
            paper_html += f"""
                    <button onclick="classifyPaper('{paper.get('title', '').replace("'", "\\'")}', '{paper.get('abstract', '').replace("'", "\\'")[:500]}')" style="
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
        
        # Add JavaScript for classify button
        st.markdown("""
        <script>
        function classifyPaper(title, abstract) {
            // Store paper data in Streamlit session state
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {
                    title: title,
                    abstract: abstract
                }
            }, '*');
            
            // Show notification
            const notification = document.createElement('div');
            notification.innerHTML = `
                <div style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 24px;
                    border-radius: 12px;
                    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
                    z-index: 9999;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    animation: slideIn 0.3s ease;
                ">
                    <div style="font-size: 20px;">🤖</div>
                    <div>
                        <div style="font-weight: 600; font-size: 14px;">Redirecting to classifier...</div>
                        <div style="font-size: 12px; opacity: 0.9;">Paper: ${title.substring(0, 50)}...</div>
                    </div>
                </div>
            `;
            document.body.appendChild(notification);
            
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

# ===== MODERN STATISTICS DASHBOARD =====
def display_statistics():
    """Display statistics with modern visualization"""
    
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
    
    # Quick stats row
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
        avg_confidence = papers_df['word_count'].mean() if 'word_count' in papers_df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{avg_confidence:.0f}</div>
            <div class="metric-label">Avg Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts row
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Category distribution - Pie chart
        st.markdown("""
        <div class="card" style="margin-top: 24px;">
            <h3 style="color: #1e293b; font-size: 18px; font-weight: 600; margin-bottom: 20px;">
                📈 Category Distribution
            </h3>
        """, unsafe_allow_html=True)
        
        if 'category' in papers_df.columns:
            category_counts = papers_df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            # Create pie chart with custom colors
            colors = px.colors.qualitative.Plotly[:len(category_counts)]
            
            fig = go.Figure(data=[go.Pie(
                labels=category_counts['Category'],
                values=category_counts['Count'],
                hole=.4,
                marker_colors=colors,
                textinfo='label+percent',
                textposition='outside',
                insidetextorientation='radial'
            )])
            
            fig.update_layout(
                height=400,
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with chart_col2:
        # Yearly trend - Line chart
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
                line=dict(color='#667eea', width=4, shape='spline'),
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
                margin=dict(t=30, b=50, l=50, r=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.05)',
                    tickmode='linear'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.05)'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Word count distribution
    st.markdown("""
    <div class="card" style="margin-top: 24px;">
        <h3 style="color: #1e293b; font-size: 18px; font-weight: 600; margin-bottom: 20px;">
            📝 Abstract Length Distribution
        </h3>
    """, unsafe_allow_html=True)
    
    if 'word_count' in papers_df.columns:
        fig = px.histogram(
            papers_df,
            x='word_count',
            nbins=20,
            color_discrete_sequence=['#10b981'],
            opacity=0.8
        )
        
        fig.update_layout(
            height=300,
            xaxis_title="Word Count",
            yaxis_title="Number of Papers",
            bargap=0.1,
            margin=dict(t=30, b=50, l=50, r=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== MODERN SIDEBAR =====
st.sidebar.markdown("""
<div style="padding: 20px 0;">
    <div style="text-align: center; margin-bottom: 32px;">
        <div style="font-size: 32px; margin-bottom: 8px;">📈</div>
        <div style="font-size: 18px; font-weight: 600; color: #1e293b;">Finance Research Hub</div>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">v2.3 • Professional Edition</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.header("🧭 Navigation")
app_mode = st.sidebar.radio(
    "",
    ["📚 Research Library", "🤖 AI Classifier", "📊 Analytics"],
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

# Filter by date
st.sidebar.markdown("---")
st.sidebar.header("📅 Quick Filters")

if 'published_date' in papers_df.columns and not papers_df.empty:
    min_date = papers_df['published_date'].min().date()
    max_date = papers_df['published_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Display info
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

# ===== MAIN CONTENT ROUTING =====
if app_mode == "📚 Research Library":
    display_research_library()
    
elif app_mode == "🤖 AI Classifier":
    # You can add your classifier interface here
    st.markdown("""
    <div class="card" style="text-align: center; padding: 48px 24px;">
        <div style="font-size: 64px; margin-bottom: 24px;">🤖</div>
        <h2 style="color: #1e293b; margin-bottom: 16px;">AI Classifier</h2>
        <p style="color: #64748b; max-width: 600px; margin: 0 auto 32px auto;">
            Upload PDFs or select papers from the library to classify them using AI
        </p>
        <div style="display: flex; gap: 16px; justify-content: center;">
            <button style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 32px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(102, 126, 234, 0.3)'"
            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                📤 Upload PDF
            </button>
            <button style="
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
                padding: 12px 32px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            " onmouseover="this.style.background='#667eea'; this.style.color='white'"
            onmouseout="this.style.background='white'; this.style.color='#667eea'">
                📚 Browse Library
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
elif app_mode == "📊 Analytics":
    display_statistics()

# Footer
st.markdown("""
<div style="margin-top: 64px; padding: 32px 0; text-align: center; color: #94a3b8; border-top: 1px solid #e2e8f0;">
    <div style="font-size: 14px; margin-bottom: 8px;">
        Finance Research Hub • v2.3 • Made with ❤️ for researchers
    </div>
    <div style="display: flex; justify-content: center; gap: 24px; margin-top: 16px;">
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">📚 Documentation</a>
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">🐙 GitHub</a>
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">📧 Contact</a>
        <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">🔒 Privacy</a>
    </div>
</div>
""", unsafe_allow_html=True)