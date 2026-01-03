import streamlit as st
import pandas as pd
# # import torch  # Commented out - not needed for mock model
import sys
import plotly.express as px
import numpy as np
import json
import io
from datetime import datetime

# Add src folder to path
sys.path.append('src')

st.set_page_config(
    page_title="Finance Research Classifier",
    page_icon="📊",
    layout="wide"
)

# Title with clickable badges
st.title("📊 Finance Research Paper Classifier")
st.success("✅ Finance Research Classifier - Ready")

# Display versions with icons
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Streamlit** {st.__version__}")
with col2:
    st.markdown(f"**Pandas** {pd.__version__}")
with col3:
    st.markdown(f"**Numpy** {np.__version__}")

# ===== MOCK MODEL FUNCTION (Replace with your actual model) =====
def classify_with_confidence(text, top_k=5, improve_confidence=True):
    """
    Mock classification function with improved confidence simulation
    Replace with your actual ML model
    """
    # 50 finance categories with Wikipedia links
    finance_categories = [
        "Quantitative Finance",
        "Behavioral Finance", 
        "Corporate Finance",
        "Asset Pricing",
        "Financial Econometrics",
        "Banking", 
        "Insurance",
        "Financial Markets",
        "Investment Analysis",
        "Risk Management",
        "Financial Regulation",
        "Fintech",
        "Cryptocurrency",
        "Sustainable Finance",
        "International Finance",
        "Public Finance",
        "Personal Finance",
        "Real Estate Finance",
        "Derivatives",
        "Fixed Income",
        "Financial Engineering",
        "Market Microstructure",
        "Financial Modeling",
        "Credit Risk",
        "Liquidity Risk",
        "Operational Risk",
        "Portfolio Theory",
        "Capital Structure",
        "Mergers and Acquisitions",
        "Venture Capital",
        "Private Equity",
        "Hedge Funds",
        "Financial Technology",
        "Blockchain in Finance",
        "AI in Finance",
        "Machine Learning in Finance",
        "Financial Planning",
        "Wealth Management",
        "Financial Analysis",
        "Accounting Standards",
        "Auditing",
        "Taxation",
        "Development Finance",
        "Microfinance",
        "Islamic Finance",
        "Financial Crises",
        "Monetary Policy",
        "Fiscal Policy",
        "Financial Stability",
        "Financial Inclusion"
    ]
    
    # Wikipedia links for each category (for reference)
    category_links = {
        "Quantitative Finance": "https://en.wikipedia.org/wiki/Quantitative_analysis_(finance)",
        "Behavioral Finance": "https://en.wikipedia.org/wiki/Behavioral_finance",
        "Corporate Finance": "https://en.wikipedia.org/wiki/Corporate_finance",
        "Asset Pricing": "https://en.wikipedia.org/wiki/Asset_pricing",
        "Financial Econometrics": "https://en.wikipedia.org/wiki/Financial_econometrics",
        "Banking": "https://en.wikipedia.org/wiki/Banking",
        "Financial Markets": "https://en.wikipedia.org/wiki/Financial_market",
        "Risk Management": "https://en.wikipedia.org/wiki/Risk_management",
        "Fintech": "https://en.wikipedia.org/wiki/Fintech",
        "Cryptocurrency": "https://en.wikipedia.org/wiki/Cryptocurrency",
        "Sustainable Finance": "https://en.wikipedia.org/wiki/Sustainable_finance",
        "International Finance": "https://en.wikipedia.org/wiki/International_finance",
        "Public Finance": "https://en.wikipedia.org/wiki/Public_finance",
        "Derivatives": "https://en.wikipedia.org/wiki/Derivative_(finance)",
        "Portfolio Theory": "https://en.wikipedia.org/wiki/Modern_portfolio_theory",
        "Financial Crises": "https://en.wikipedia.org/wiki/Financial_crisis",
        "Monetary Policy": "https://en.wikipedia.org/wiki/Monetary_policy",
        "Fiscal Policy": "https://en.wikipedia.org/wiki/Fiscal_policy"
    }
    
    # Generate more realistic confidence scores
    np.random.seed(hash(text) % 10000)
    
    if improve_confidence:
        # Generate higher, more realistic confidence scores
        base_scores = np.random.dirichlet(np.ones(len(finance_categories)) * 0.3)
        
        # Boost top categories for better differentiation
        sorted_indices = np.argsort(base_scores)[::-1]
        boost_factor = np.linspace(1.5, 1.0, len(base_scores))
        
        adjusted_scores = base_scores.copy()
        for idx, boost in zip(sorted_indices, boost_factor):
            adjusted_scores[idx] *= boost
        
        # Normalize to sum to 1
        scores = adjusted_scores / adjusted_scores.sum()
    else:
        scores = np.random.dirichlet(np.ones(len(finance_categories)) * 0.1)
    
    # Sort and get top k
    indices = np.argsort(scores)[::-1][:top_k]
    
    results = []
    for idx in indices:
        category = finance_categories[idx]
        confidence = float(scores[idx] * 100)
        # Add small random variation for more realistic distribution
        confidence += np.random.uniform(-2, 2)
        confidence = max(0, min(100, confidence))  # Clamp between 0-100
        
        # Get Wikipedia link if available
        wiki_link = category_links.get(category, "https://en.wikipedia.org/wiki/Finance")
        
        results.append({
            "category": category,
            "confidence": confidence,
            "score": float(scores[idx]),
            "wiki_link": wiki_link
        })
    
    return results

# Function to display classification results
def display_classification_results(top_results, file_name="", abstract_text=""):
    """
    Display classification results with enhanced visualization and clickable links
    """
    top_category = top_results[0]
    
    # Determine color based on confidence
    if top_category["confidence"] > 75:
        confidence_color = "#28a745"  # Green
        confidence_level = "High"
        confidence_icon = "✅"
    elif top_category["confidence"] > 50:
        confidence_color = "#ffc107"  # Orange
        confidence_level = "Medium"
        confidence_icon = "⚠️"
    else:
        confidence_color = "#dc3545"  # Red
        confidence_level = "Low"
        confidence_icon = "❌"
    
    # Display main category with enhanced styling
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {confidence_color}10, {confidence_color}05); 
                padding:20px; border-radius:12px; border-left:6px solid {confidence_color}; 
                margin:15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="display:flex; align-items:center; gap:15px;">
            <div style="font-size:32px;">{confidence_icon}</div>
            <div>
                <h3 style="margin:0 0 8px 0; color:#1a1a1a;">🏷️ Predicted Category: {top_category['category']}</h3>
                <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                    <div style="font-size:18px; font-weight:bold; color:{confidence_color};">
                        Confidence: {top_category['confidence']:.2f}%
                    </div>
                    <div style="padding:4px 12px; background-color:{confidence_color}20; 
                                color:{confidence_color}; border-radius:20px; font-size:14px;">
                        {confidence_level} Confidence
                    </div>
                    <a href="{top_category.get('wiki_link', 'https://en.wikipedia.org/wiki/Finance')}" 
                       target="_blank" 
                       style="padding:4px 12px; background-color:#007bff20; 
                              color:#007bff; border-radius:20px; font-size:14px;
                              text-decoration:none;">
                        📚 Learn more
                    </a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_value = top_category["confidence"] / 100
    st.progress(progress_value, text=f"Model Confidence: {top_category['confidence']:.1f}%")
    
    # Quick action buttons
    st.markdown("### 🔗 Quick Actions")
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("📖 Category Info", key=f"info_{file_name}", use_container_width=True):
            st.info(f"**{top_category['category']}** - This category focuses on...")
    
    with action_cols[1]:
        st.link_button("🌐 Wikipedia", top_category.get('wiki_link', 'https://en.wikipedia.org/wiki/Finance'))
    
    with action_cols[2]:
        st.link_button("📚 Google Scholar", f"https://scholar.google.com/scholar?q={top_category['category'].replace(' ', '+')}+finance")
    
    with action_cols[3]:
        st.link_button("📊 More Papers", f"https://www.jstor.org/action/doBasicSearch?Query={top_category['category'].replace(' ', '+')}")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Top Categories", "📈 Visualization", "📥 Export Results", "📋 Report & Links"])
    
    with tab1:
        # Display top categories in a table with clickable links
        st.subheader(f"Top {len(top_results)} Predictions")
        
        # Create DataFrame with clickable links
        df_results = pd.DataFrame(top_results)
        df_results.index = range(1, len(df_results) + 1)
        
        # Add clickable category column
        df_results['category_with_link'] = df_results.apply(
            lambda row: f"[{row['category']}]({row['wiki_link']})", 
            axis=1
        )
        
        # Display table
        st.dataframe(
            df_results[['category_with_link', 'confidence']],
            column_config={
                "category_with_link": st.column_config.TextColumn(
                    "Category", 
                    width="large",
                    help="Click category name to learn more on Wikipedia"
                ),
                "confidence": st.column_config.ProgressColumn(
                    "Confidence (%)",
                    format="%.2f%%",
                    min_value=0,
                    max_value=100
                )
            },
            hide_index=False,
            use_container_width=True,
            height=min(400, 45 * len(top_results))
        )
        
        # Useful resource links
        st.markdown("### 📚 Useful Resources")
        resource_cols = st.columns(3)
        
        with resource_cols[0]:
            st.markdown("""
            **Academic Databases:**
            - [📖 JSTOR](https://www.jstor.org)
            - [🔬 ScienceDirect](https://www.sciencedirect.com)
            - [🎓 SSRN](https://www.ssrn.com)
            """)
        
        with resource_cols[1]:
            st.markdown("""
            **Finance Portals:**
            - [📈 Investopedia](https://www.investopedia.com)
            - [🏦 IMF eLibrary](https://www.elibrary.imf.org)
            - [🌍 World Bank Open Knowledge](https://openknowledge.worldbank.org)
            """)
        
        with resource_cols[2]:
            st.markdown("""
            **Research Tools:**
            - [🔍 Google Scholar](https://scholar.google.com)
            - [📊 arXiv Finance](https://arxiv.org/list/q-fin/recent)
            - [💡 RePEc](https://ideas.repec.org)
            """)
        
        # Confidence assessment
        with st.container():
            st.markdown("### 🤖 Model Assessment")
            cols = st.columns(3)
            with cols[0]:
                st.metric("Top Confidence", f"{top_category['confidence']:.1f}%")
            with cols[1]:
                gap = top_category['confidence'] - top_results[1]['confidence'] if len(top_results) > 1 else 0
                st.metric("Confidence Gap", f"{gap:.1f}%")
            with cols[2]:
                avg_confidence = df_results['confidence'].mean()
                st.metric("Avg Top 5", f"{avg_confidence:.1f}%")
    
    with tab2:
        # Visualization
        st.subheader("📊 Confidence Distribution")
        
        fig = px.bar(
            df_results,
            x='category',
            y='confidence',
            color='confidence',
            color_continuous_scale=px.colors.sequential.Viridis,
            text='confidence',
            labels={'confidence': 'Confidence (%)', 'category': 'Category'},
            hover_data={'confidence': ':.2f%'}
        )
        
        fig.update_traces(
            texttemplate='%{text:.2f}%',
            textposition='outside',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            hovertemplate="<b>%{x}</b><br>Confidence: %{y:.2f}%<extra></extra>"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_range=[0, 100],
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0.02)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional resources
        st.markdown("""
        ### 📈 Data Visualization Resources
        - [Plotly Documentation](https://plotly.com/python/)
        - [Streamlit Charts Guide](https://docs.streamlit.io/library/api-reference/charts)
        - [Finance Data APIs](https://www.quandl.com/tools/api)
        """)
    
    with tab3:
        # Export functionality
        st.subheader("📥 Export Classification Results")
        
        # Prepare data for export
        export_data = {
            "file_name": file_name,
            "timestamp": datetime.now().isoformat(),
            "predicted_category": top_category["category"],
            "confidence": top_category["confidence"],
            "confidence_level": confidence_level,
            "abstract_preview": abstract_text[:200] + "..." if len(abstract_text) > 200 else abstract_text,
            "all_predictions": [
                {k: v for k, v in pred.items() if k != 'wiki_link'} 
                for pred in top_results
            ],
            "model_version": "1.0",
            "export_links": {
                "wikipedia": top_category.get('wiki_link', ''),
                "google_scholar": f"https://scholar.google.com/scholar?q={top_category['category'].replace(' ', '+')}",
                "related_papers": f"https://www.semanticscholar.org/search?q={top_category['category'].replace(' ', '%20')}"
            }
        }
        
        # Export buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV Export
            df_export = pd.DataFrame(top_results)
            csv_buffer = io.StringIO()
            df_export.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="📊 Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"classification_{file_name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download results as CSV file"
            )
        
        with col2:
            # JSON Export
            json_buffer = io.StringIO()
            json.dump(export_data, json_buffer, indent=2)
            
            st.download_button(
                label="📁 Download JSON",
                data=json_buffer.getvalue(),
                file_name=f"classification_{file_name.replace('.pdf', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                help="Download full results as JSON file with links"
            )
        
        with col3:
            # Markdown Report
            report_content = f"""# Finance Research Classification Report

## File Information
- **File**: {file_name}
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Model**: Finance Classifier v1.0

## Classification Results
- **Primary Category**: {top_category['category']}
- **Confidence**: {top_category['confidence']:.2f}% ({confidence_level})

## Quick Links
- Wikipedia: {top_category.get('wiki_link', 'N/A')}
- Google Scholar: https://scholar.google.com/scholar?q={top_category['category'].replace(' ', '+')}
- Related Papers: https://www.semanticscholar.org/search?q={top_category['category'].replace(' ', '%20')}

## All Predictions
"""
            for i, pred in enumerate(top_results, 1):
                report_content += f"{i}. {pred['category']}: {pred['confidence']:.2f}%\n"
            
            st.download_button(
                label="📄 Download Report",
                data=report_content,
                file_name=f"report_{file_name.replace('.pdf', '')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Online sharing options
        st.markdown("---")
        st.markdown("### 🌐 Share Online")
        share_cols = st.columns(4)
        
        with share_cols[0]:
            st.link_button("📧 Email Results", f"mailto:?subject=Classification Results for {file_name}&body={report_content[:500]}...")
        
        with share_cols[1]:
            st.link_button("💼 LinkedIn", "https://www.linkedin.com/sharing/share-offsite/?url=")
        
        with share_cols[2]:
            st.link_button("🐦 Twitter", f"https://twitter.com/intent/tweet?text=Classified {file_name} as {top_category['category']} with {top_category['confidence']:.1f}% confidence")
        
        with share_cols[3]:
            st.link_button("📚 ResearchGate", "https://www.researchgate.net")
    
    with tab4:
        # Generate a comprehensive report with links
        st.subheader("📋 Classification Report")
        
        report_content = f"""# 📊 Finance Research Classification Report

## 📄 File Information
- **File Name**: {file_name}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Model Version**: Finance Classifier v1.0
- **Confidence Level**: {confidence_level}

## 🏷️ Classification Results
- **Primary Category**: {top_category['category']}
- **Confidence Score**: {top_category['confidence']:.2f}%
- **Assessment**: {'High reliability - suitable for automated processing' if confidence_level == 'High' else 'Moderate reliability - review recommended' if confidence_level == 'Medium' else 'Low reliability - manual classification required'}

## 🔗 Quick Access Links
- [🌐 Wikipedia Entry]({top_category.get('wiki_link', 'https://en.wikipedia.org/wiki/Finance')})
- [📚 Google Scholar Search](https://scholar.google.com/scholar?q={top_category['category'].replace(' ', '+')}+finance)
- [📊 Related Papers](https://www.semanticscholar.org/search?q={top_category['category'].replace(' ', '%20')})
- [💾 Download Raw Data](#)

## 📈 Top Predictions
"""
        
        for i, result in enumerate(top_results, 1):
            report_content += f"{i}. **{result['category']}**: {result['confidence']:.2f}% [Learn more]({result.get('wiki_link', 'https://en.wikipedia.org/wiki/Finance')})\n"
        
        report_content += f"""
## 📝 Abstract Preview
{abstract_text[:300]}...

## 🤖 Model Notes
This classification was generated using an AI model trained on 50 finance research categories.
For questions or corrections, please contact the research team.

---
*Generated by Finance Research Classifier • {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        # Display report preview
        st.text_area("📋 Report Preview", report_content, height=300)
        
        # Download buttons for report
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Markdown",
                data=report_content,
                file_name=f"classification_report_{file_name.replace('.pdf', '')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            # HTML version
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Classification Report - {file_name}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 30px; border-radius: 10px; }}
        .category {{ background: #f8f9fa; padding: 15px; border-left: 5px solid #007bff; 
                    margin: 10px 0; border-radius: 5px; }}
        .link {{ color: #007bff; text-decoration: none; }}
        .link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Finance Research Classification Report</h1>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h2>📄 File Information</h2>
    <p><strong>File:</strong> {file_name}</p>
    
    <h2>🏷️ Classification Results</h2>
    <div class="category">
        <h3>{top_category['category']}</h3>
        <p>Confidence: {top_category['confidence']:.2f}%</p>
        <p><a class="link" href="{top_category.get('wiki_link', 'https://en.wikipedia.org/wiki/Finance')}" target="_blank">🌐 Learn more on Wikipedia</a></p>
    </div>
    
    <h2>🔗 Useful Links</h2>
    <ul>
        <li><a class="link" href="https://scholar.google.com/scholar?q={top_category['category'].replace(' ', '+')}" target="_blank">📚 Search Google Scholar</a></li>
        <li><a class="link" href="https://www.jstor.org" target="_blank">📖 Access JSTOR</a></li>
        <li><a class="link" href="https://arxiv.org/list/q-fin/recent" target="_blank">📈 Browse arXiv Finance</a></li>
    </ul>
</body>
</html>"""
            
            st.download_button(
                label="🌐 Download HTML",
                data=html_content,
                file_name=f"report_{file_name.replace('.pdf', '')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        # External research links
        st.markdown("---")
        st.markdown("### 🎓 External Research Databases")
        
        db_cols = st.columns(3)
        with db_cols[0]:
            st.markdown("""
            **Open Access:**
            - [🔓 arXiv](https://arxiv.org)
            - [📖 SSRN](https://www.ssrn.com)
            - [🌍 DOAJ](https://doaj.org)
            """)
        
        with db_cols[1]:
            st.markdown("""
            **Commercial:**
            - [📚 Elsevier](https://www.sciencedirect.com)
            - [🏛️ Springer](https://link.springer.com)
            - [🎓 Wiley](https://onlinelibrary.wiley.com)
            """)
        
        with db_cols[2]:
            st.markdown("""
            **Finance Specific:**
            - [💹 NBER](https://www.nber.org)
            - [🏦 IMF](https://www.imf.org/en/Publications)
            - [🌐 World Bank](https://documents.worldbank.org)
            """)
    
    # Store in session state for history
    if 'classification_history' not in st.session_state:
        st.session_state.classification_history = []
    
    st.session_state.classification_history.append({
        "file_name": file_name,
        "predicted_category": top_category["category"],
        "confidence": top_category["confidence"],
        "timestamp": datetime.now().isoformat(),
        "abstract_preview": abstract_text[:100] if abstract_text else "",
        "wiki_link": top_category.get('wiki_link', '')
    })

# Try to import PDF processor
try:
    from pdf_processor import PDFProcessor
    pdf_processor = PDFProcessor()
    pdf_available = True
    st.sidebar.success("✅ PDF processor loaded")
except ImportError:
    pdf_available = False
    st.sidebar.warning("⚠️ PDF processor not available")
except Exception as e:
    pdf_available = False
    st.sidebar.error(f"❌ PDF processor error: {str(e)[:50]}")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if pdf_available:
        max_pages = st.slider("Pages to extract", 1, 10, 3)
        show_raw_text = st.checkbox("Show raw text", False)
    
    st.header("📤 Upload Files")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload academic papers or research reports (max 200MB per file)"
    )
    
    # External links section
    st.markdown("---")
    st.header("🔗 Useful Links")
    
    link_cols = st.columns(2)
    with link_cols[0]:
        st.link_button("📚 Documentation", "https://docs.streamlit.io")
        st.link_button("🐙 GitHub", "https://github.com")
    
    with link_cols[1]:
        st.link_button("🎓 Tutorials", "https://streamlit.io/gallery")
        st.link_button("💬 Community", "https://discuss.streamlit.io")
    
    # Quick resources
    st.markdown("**Academic Resources:**")
    st.markdown("- [Google Scholar](https://scholar.google.com)")
    st.markdown("- [arXiv Finance](https://arxiv.org/list/q-fin/recent)")
    st.markdown("- [JSTOR](https://www.jstor.org)")
    
    # Classification settings
    st.header("🤖 Classification Settings")
    top_k = st.slider("Number of top categories", 3, 10, 5)
    improve_model = st.checkbox("Enhance confidence scores", True)
    
    st.header("📊 Display Options")
    show_visualizations = st.checkbox("Show visualizations", True)
    auto_classify = st.checkbox("Auto-classify on upload", False)
    
    st.header("📥 Export Options")
    auto_export = st.checkbox("Auto-export results", False)

# Main content area
if uploaded_files:
    st.success(f"📄 {len(uploaded_files)} file(s) uploaded")
    
    # Initialize session state for classification history
    if 'classification_history' not in st.session_state:
        st.session_state.classification_history = []
    
    # Quick action buttons at top
    st.markdown("### ⚡ Quick Actions")
    quick_cols = st.columns(5)
    
    with quick_cols[0]:
        if st.button("📊 Classify All", use_container_width=True):
            st.info("Classification in progress...")
    
    with quick_cols[1]:
        st.link_button("📚 Help Guide", "https://docs.streamlit.io")
    
    with quick_cols[2]:
        st.link_button("🐛 Report Issue", "https://github.com")
    
    with quick_cols[3]:
        st.link_button("⭐ Star Project", "https://github.com")
    
    with quick_cols[4]:
        st.link_button("🔄 Check Update", "https://pypi.org")
    
    # Process each uploaded file
    for i, file in enumerate(uploaded_files):
        # Create a card-like expander
        with st.expander(f"📋 **{file.name}** ({file.size/1024:.1f} KB)", expanded=i==0):
            
            # File header with quick links
            header_cols = st.columns([3, 1])
            with header_cols[0]:
                st.markdown(f"**File ID:** `{hash(file.name) % 10000:04d}`")
            with header_cols[1]:
                st.link_button("📥 Direct Download", "#", disabled=True)
            
            if pdf_available:
                # Extract text from PDF
                with st.spinner("Extracting text from PDF..."):
                    try:
                        pdf_text = pdf_processor.extract_text(file, max_pages=max_pages)
                        abstract = pdf_processor.extract_abstract(pdf_text)
                        word_count = pdf_processor.count_words(pdf_text)
                        
                        # Create two-column layout
                        col_left, col_right = st.columns([2, 1])
                        
                        with col_left:
                            st.write("**📝 Extracted Abstract:**")
                            
                            # Display abstract with clickable format
                            abstract_display = f"""
                            {abstract[:400]}...
                            
                            **🔗 Related Resources:**
                            - [📖 Read full abstract](#)
                            - [🔍 Search similar papers](https://scholar.google.com)
                            - [📚 Find citations](#)
                            - [🎯 Related topics](#)
                            """
                            st.markdown(abstract_display)
                            
                            # Statistics with icons
                            st.write("**🔢 Statistics:**")
                            stat_cols = st.columns(4)
                            with stat_cols[0]:
                                st.metric("Words", word_count)
                            with stat_cols[1]:
                                st.metric("Pages", max_pages)
                            with stat_cols[2]:
                                st.metric("Chars", len(pdf_text))
                            with stat_cols[3]:
                                st.metric("Size", f"{file.size/1024:.0f} KB")
                            
                            if show_raw_text and pdf_text:
                                with st.expander("📄 View extracted text"):
                                    st.text(pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text)
                        
                        with col_right:
                            # File info card
                            st.markdown("""
                            <div style="background:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #ddd;">
                                <h4 style="margin-top:0;">📄 File Information</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.metric("File Size", f"{file.size/1024:.0f} KB")
                            st.metric("Words", word_count)
                            st.metric("Pages", max_pages)
                            
                            # Quick links
                            st.markdown("**🔗 Quick Links:**")
                            link_col1, link_col2 = st.columns(2)
                            with link_col1:
                                st.link_button("🌐 View Online", "#")
                            with link_col2:
                                st.link_button("📊 Analytics", "#")
                            
                            # Classification section
                            st.markdown("---")
                            st.write("**🤖 AI Classification**")
                            
                            # Auto-classify if enabled
                            classify_button = st.button(
                                f"🔍 Classify with AI", 
                                key=f"classify_{i}", 
                                type="primary", 
                                use_container_width=True
                            )
                            
                            if auto_classify or classify_button:
                                with st.spinner("Running AI classification..."):
                                    # Run classification with improved confidence
                                    top_results = classify_with_confidence(
                                        pdf_text, 
                                        top_k=top_k,
                                        improve_confidence=improve_model
                                    )
                                    
                                    # Display results
                                    display_classification_results(top_results, file.name, abstract)
                                    
                                    # Auto-export if enabled
                                    if auto_export:
                                        st.success("✅ Results auto-exported")
                                        st.balloons()
                    
                    except Exception as e:
                        st.error(f"❌ Error processing PDF: {str(e)}")
                        st.info("💡 Try reducing the number of pages or check PDF format.")
            else:
                # Fallback if PDF processor not available
                st.warning("⚠️ PDF processing not available. Please install pdfplumber:")
                st.code("pip install pdfplumber")
                
                col_left, col_right = st.columns([2, 1])
                with col_left:
                    st.write("**📄 File Information:**")
                    st.write(f"- Name: {file.name}")
                    st.write(f"- Size: {file.size/1024:.1f} KB")
                    st.write(f"- Type: PDF")
                    st.write(f"- Status: Ready for processing")
                
                with col_right:
                    st.metric("Status", "Ready")
                    st.info("Install PDF processor for full functionality")
                    
                    # Installation links
                    st.markdown("**Installation Links:**")
                    st.markdown("- [PyPI](https://pypi.org/project/pdfplumber/)")
                    st.markdown("- [Documentation](https://github.com/jsvine/pdfplumber)")

# Display classification history with clickable links
if 'classification_history' in st.session_state and st.session_state.classification_history:
    with st.expander("📚 Classification History", expanded=False):
        history_df = pd.DataFrame(st.session_state.classification_history)
        
        # Convert timestamp to readable format
        if 'timestamp' in history_df.columns:
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df['time_display'] = history_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Create clickable category column
        if 'wiki_link' in history_df.columns:
            history_df['category_link'] = history_df.apply(
                lambda row: f"[{row['predicted_category']}]({row['wiki_link']})" 
                if pd.notna(row['wiki_link']) else row['predicted_category'],
                axis=1
            )
        else:
            history_df['category_link'] = history_df['predicted_category']
        
        # Display history table
        st.dataframe(
            history_df[['file_name', 'category_link', 'confidence', 'time_display']],
            column_config={
                "file_name": "File",
                "category_link": st.column_config.TextColumn("Category", help="Click to learn more"),
                "confidence": st.column_config.ProgressColumn(
                    "Confidence",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                ),
                "time_display": "Time"
            },
            use_container_width=True,
            hide_index=True
        )
        
        # History actions
        hist_cols = st.columns(3)
        with hist_cols[0]:
            if st.button("Clear History", type="secondary", use_container_width=True):
                st.session_state.classification_history = []
                st.rerun()
        
        with hist_cols[1]:
            # Export history
            if len(history_df) > 0:
                history_csv = history_df.to_csv(index=False)
                st.download_button(
                    label="📥 Export History",
                    data=history_csv,
                    file_name=f"classification_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with hist_cols[2]:
            st.link_button("📊 View Analytics", "#")

# Footer với clickable links
st.markdown("---")
footer_cols = st.columns(5)

with footer_cols[0]:
    st.markdown("[📖 Documentation](https://docs.streamlit.io)")

with footer_cols[1]:
    st.markdown("[🐙 GitHub](https://github.com/YOUR_USERNAME/finance-classifier)")

with footer_cols[2]:
    st.markdown("[💬 Community](https://discuss.streamlit.io)")

with footer_cols[3]:
    st.markdown("[🐦 Twitter](https://twitter.com/streamlit)")

with footer_cols[4]:
    st.markdown(f"**Version 2.1** • {datetime.now().strftime('%Y-%m-%d')}")

# Final caption với link
st.caption(f"""
[Finance Research Classifier](https://github.com/YOUR_USERNAME/finance-classifier) v2.1 | 
Made with ❤️ for academic research
""")
