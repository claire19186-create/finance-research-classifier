# COMPLETE BILINGUAL FINANCE RESEARCH HUB - FIXED VERSION
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from datetime import datetime
import time
import re
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Finance Research Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== BILINGUAL KEYWORD DATABASE ====================
FINANCE_KEYWORD_DATABASE = {
    "Computational Finance": {
        "keywords": [
            "deep learning", "neural networks", "machine learning", "AI", "artificial intelligence",
            "gradient descent", "backpropagation", "convolutional", "recurrent", "transformer",
            "PDE", "partial differential equation", "numerical methods", "finite difference", "finite element",
            "Monte Carlo", "simulation", "stochastic", "high-dimensional", "computational",
            "algorithm", "optimization", "parallel computing", "GPU", "CUDA",
            "深度学习", "神经网络", "机器学习", "人工智能", "AI",
            "梯度下降", "反向传播", "卷积", "循环神经网络", "Transformer",
            "偏微分方程", "数值方法", "有限差分", "有限元", "蒙特卡洛",
            "模拟", "随机", "高维", "计算金融", "算法",
            "优化", "并行计算", "量子计算", "强化学习", "时间序列预测"
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
            "随机微积分", "伊藤", "布朗运动", "鞅", "偏微分方程",
            "布莱克-斯科尔斯", "期权定价", "风险中性", "测度论", "概率",
            "随机过程", "Levy过程", "跳跃扩散", "Malliavin微积分", "Heston模型",
            "局部波动率", "随机波动率", "最优停止", "最优控制", "动态规划"
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
            "投资组合优化", "资产配置", "分散化", "有效前沿", "均值方差",
            "马科维茨", "风险平价", "最小方差", "战术资产配置", "战略资产配置",
            "再平衡", "换手率", "跟踪误差", "主动份额", "指数跟踪",
            "因子投资", "智能贝塔", "风险因子", "风格因子", "对冲基金"
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
            "风险价值", "VaR", "预期损失", "条件风险价值", "压力测试",
            "情景分析", "回测", "历史模拟", "信用风险", "违约风险",
            "交易对手风险", "信用价值调整", "市场风险", "波动率风险",
            "利率风险", "汇率风险", "流动性风险", "资金流动性", "市场流动性"
        ],
        "weight": 0.9,
        "color": "#8b5cf6",
        "icon": "⚠️"
    },
    
    "Green Finance": {
        "keywords": [
            "green finance", "green bonds", "green loans", "green credit", "sustainable finance",
            "environmental finance", "eco-finance", "green investment", "ESG investment",
            "environmental, social and governance", "green banking", "green insurance",
            "绿色金融", "绿色债券", "绿色贷款", "绿色信贷", "可持续金融",
            "环境金融", "生态金融", "绿色投资", "ESG投资", "环境社会治理",
            "绿色银行", "绿色保险", "绿色金融产品", "绿色证券", "绿色转型金融",
            "低碳金融", "循环经济金融", "生物多样性金融", "自然资本",
            "绿色金融科技", "可持续发展挂钩贷款", "绿色抵押贷款"
        ],
        "weight": 0.85,
        "color": "#22c55e",
        "icon": "🌿"
    },
    
    "Climate Finance": {
        "keywords": [
            "climate finance", "climate change finance", "climate risk finance", "climate adaptation finance",
            "climate mitigation finance", "carbon pricing", "carbon markets", "emissions trading",
            "carbon credits", "carbon offsets", "clean development mechanism", "CDM",
            "气候金融", "气候变化金融", "气候风险金融", "气候适应金融",
            "气候减缓金融", "碳定价", "碳市场", "碳排放交易",
            "碳信用", "碳抵消", "清洁发展机制", "气候债券",
            "气候基金", "绿色气候基金", "适应融资", "减缓融资"
        ],
        "weight": 0.85,
        "color": "#0ea5e9",
        "icon": "🌍"
    },
    
    "Sustainable Finance": {
        "keywords": [
            "ESG", "environmental social governance", "sustainable investing", "responsible investing",
            "green bonds", "climate bonds", "sustainability-linked bonds", "social bonds",
            "sustainable development goals", "SDG finance", "social finance", "impact bonds",
            "ESG", "环境社会治理", "可持续投资", "责任投资", "社会责任投资",
            "绿色债券", "气候债券", "可持续发展挂钩债券", "社会债券",
            "可持续发展目标", "SDG融资", "社会金融", "影响力债券"
        ],
        "weight": 0.8,
        "color": "#10b981",
        "icon": "🌱"
    },
    
    "FinTech & Blockchain": {
        "keywords": [
            "blockchain", "distributed ledger", "smart contracts", "Ethereum", "solidity",
            "cryptocurrency", "Bitcoin", "Ethereum", "DeFi", "decentralized finance",
            "stablecoins", "CBDC", "central bank digital currency", "digital currency",
            "区块链", "分布式账本", "智能合约", "以太坊", "加密货币",
            "比特币", "去中心化金融", "稳定币", "央行数字货币",
            "数字货币", "代币化", "非同质化代币", "证券型代币"
        ],
        "weight": 0.8,
        "color": "#6366f1",
        "icon": "🔗"
    },
    
    "Banking & Financial Institutions": {
        "keywords": [
            "commercial banks", "investment banks", "central banks", "bank regulation", "Basel",
            "capital adequacy", "liquidity coverage ratio", "LCR", "net stable funding ratio", "NSFR",
            "bank lending", "credit creation", "interbank market", "bank runs", "deposit insurance",
            "商业银行", "投资银行", "中央银行", "银行监管", "巴塞尔协议",
            "资本充足率", "流动性覆盖率", "净稳定资金比例", "银行信贷",
            "信用创造", "银行间市场", "银行挤兑", "存款保险", "影子银行",
            "金融中介", "银行盈利能力", "不良贷款", "金融稳定"
        ],
        "weight": 0.85,
        "color": "#8b4513",
        "icon": "🏦"
    },
    
    "Corporate Finance": {
        "keywords": [
            "capital structure", "Modigliani-Miller", "dividend policy", "payout policy", "share repurchase",
            "mergers and acquisitions", "M&A", "takeovers", "corporate governance", "board of directors",
            "agency theory", "principal-agent problem", "executive compensation", "CEO pay",
            "资本结构", "莫迪利亚尼-米勒", "股利政策", "派息政策", "股票回购",
            "兼并与收购", "并购", "接管", "公司治理", "董事会",
            "代理理论", "委托代理问题", "高管薪酬", "首席执行官薪酬",
            "公司投资", "资本预算", "净现值", "内部收益率"
        ],
        "weight": 0.8,
        "color": "#4169e1",
        "icon": "🏢"
    }
}

# ==================== DEBUG - CHECK FILES ====================
def check_files():
    """Check if required files exist"""
    st.sidebar.subheader("🔍 File Check")
    
    # Check Excel file
    excel_file = 'CNKI-20260104152201560.xls'
    if os.path.exists(excel_file):
        st.sidebar.success(f"✅ {excel_file}")
        st.sidebar.caption(f"Size: {os.path.getsize(excel_file)} bytes")
    else:
        st.sidebar.error(f"❌ {excel_file} not found")
    
    # Check JSON file
    json_file = 'research_papers.json'
    if os.path.exists(json_file):
        st.sidebar.success(f"✅ {json_file}")
    else:
        st.sidebar.warning(f"⚠️ {json_file} not found")
    
    # Show current directory
    if st.sidebar.checkbox("Show directory contents"):
        st.sidebar.code(f"CWD: {os.getcwd()}")
        files = os.listdir('.')
        for f in files[:10]:  # Show first 10 files
            st.sidebar.write(f"  - {f}")

# ==================== UTILITY FUNCTIONS ====================
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
                'confidence': min(100, weighted_score * 8),
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
        default_categories = ["General Finance", "Banking & Financial Institutions", "Green Finance"]
        for category in default_categories[:top_k]:
            results.append({
                "category": category,
                "confidence": 20.0,
                "score": 2.0,
                "icon": FINANCE_KEYWORD_DATABASE.get(category, {}).get('icon', '📄'),
                "color": FINANCE_KEYWORD_DATABASE.get(category, {}).get('color', '#764ba2'),
                "matched_keywords": [],
                "total_matches": 0
            })
    
    return results

def enhanced_classification_for_cnki(title, keywords, category_code):
    """Enhanced classification specifically for CNKI papers"""
    text = f"{title} {' '.join(keywords)} {category_code}"
    
    chinese_keyword_mapping = {
        "绿色金融": "Green Finance",
        "绿色债券": "Green Finance",
        "绿色信贷": "Green Finance",
        "绿色投资": "Green Finance",
        "ESG": "Green Finance",
        "气候金融": "Climate Finance",
        "碳金融": "Climate Finance",
        "碳交易": "Climate Finance",
        "碳市场": "Climate Finance",
        "碳排放": "Climate Finance",
        "碳中和": "Climate Finance",
        "商业银行": "Banking & Financial Institutions",
        "银行": "Banking & Financial Institutions",
        "银行业": "Banking & Financial Institutions",
        "金融科技": "FinTech & Blockchain",
        "数字货币": "FinTech & Blockchain",
        "区块链": "FinTech & Blockchain",
        "风险管理": "Risk Management",
        "风险": "Risk Management",
        "信用风险": "Risk Management",
        "投资组合": "Portfolio Management",
        "资产配置": "Portfolio Management",
        "金融工程": "Mathematical Finance",
        "量化金融": "Mathematical Finance",
        "金融数学": "Mathematical Finance",
    }
    
    for chinese_keyword, category in chinese_keyword_mapping.items():
        if chinese_keyword in text:
            return category
    
    categories = calculate_category_scores(text, top_k=1)
    if categories:
        return categories[0][0]
    
    return "General Finance"

# ==================== LOAD EXCEL DATA ====================
def load_excel_data(file_path):
    """Load and process Excel data from CNKI export"""
    try:
        # Try different Excel engines
        try:
            df = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        except:
            try:
                df = pd.read_excel(file_path, sheet_name=None, engine='xlrd')
            except:
                st.error("Cannot read Excel file. Please install: pip install openpyxl xlrd")
                return []
        
        all_papers = []
        
        for sheet_name, sheet_df in df.items():
            sheet_df.columns = sheet_df.columns.str.strip()
            
            # Handle different sheet formats
            if 'Title-题名' in sheet_df.columns:
                for idx, row in sheet_df.iterrows():
                    if pd.isna(row.get('Title-题名')):
                        continue
                    
                    # Extract authors
                    authors_str = str(row.get('Author-作者', ''))
                    authors = [author.strip() for author in authors_str.split(',') if author.strip()]
                    
                    # Extract keywords
                    keywords_str = str(row.get('关键词', ''))
                    keywords = []
                    if isinstance(keywords_str, str):
                        keywords = [kw.strip() for kw in keywords_str.split(';;') if kw.strip()]
                    
                    # Create paper object
                    paper = {
                        'title': str(row.get('Title-题名', '')),
                        'authors': authors,
                        'source': str(row.get('Source-文献来源', row.get('Source-报纸名', ''))),
                        'year': int(row.get('Year-年', 2024)) if not pd.isna(row.get('Year-年')) else 2024,
                        'keywords': keywords,
                        'category_code': str(row.get('中图分类号', '')),
                        'type': 'journal' if 'Source-文献来源' in row else 'newspaper',
                        'abstract': '',
                        'arxiv_id': f"CNKI_{sheet_name}_{idx}",
                        'arxiv_url': '',
                        'pdf_url': '',
                        'word_count': len(str(row.get('Title-题名', '')).split()) * 20,
                        'published': f"{row.get('Year-年', 2024)}-01-01" if pd.notna(row.get('Year-年')) else '2024-01-01'
                    }
                    
                    # Classify the paper
                    paper['category'] = enhanced_classification_for_cnki(
                        paper['title'],
                        paper['keywords'],
                        paper['category_code']
                    )
                    
                    # Create abstract if missing
                    if not paper.get('abstract', '') and paper['keywords']:
                        paper['abstract'] = f"Research Topic: {', '.join(paper['keywords'][:5])}. Published in {paper['source']} ({paper['year']})."
                    
                    all_papers.append(paper)
            
            elif '导师' in sheet_df.columns:  # Thesis format
                for idx, row in sheet_df.iterrows():
                    if pd.isna(row.get('Title-文献题名')):
                        continue
                    
                    keywords_str = str(row.get('关键词', ''))
                    keywords = []
                    if isinstance(keywords_str, str):
                        keywords = [kw.strip() for kw in keywords_str.split(';;') if kw.strip()]
                    
                    paper = {
                        'title': str(row.get('Title-文献题名', '')),
                        'authors': [str(row.get('Author-作者', '')).strip()],
                        'source': str(row.get('Source-文献来源', '')),
                        'year': int(row.get('Year-学位年度', 2024)) if not pd.isna(row.get('Year-学位年度')) else 2024,
                        'keywords': keywords,
                        'category_code': str(row.get('中图分类号', '')),
                        'type': 'thesis',
                        'abstract': f"学位论文: {row.get('Source-文献来源', '')} - 导师: {row.get('导师', '')}",
                        'arxiv_id': f"THESIS_{sheet_name}_{idx}",
                        'arxiv_url': '',
                        'pdf_url': '',
                        'word_count': len(str(row.get('Title-文献题名', '')).split()) * 80,
                        'published': f"{row.get('Year-学位年度', 2024)}-01-01" if pd.notna(row.get('Year-学位年度')) else '2024-01-01',
                        'advisor': str(row.get('导师', ''))
                    }
                    
                    paper['category'] = enhanced_classification_for_cnki(
                        paper['title'],
                        paper['keywords'],
                        paper['category_code']
                    )
                    
                    all_papers.append(paper)
        
        return all_papers
        
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return []

# ==================== LOAD RESEARCH PAPERS ====================
@st.cache_data
def load_research_papers():
    """Load research papers from both JSON and Excel sources"""
    all_papers = []
    
    # Load from JSON if exists
    json_path = 'research_papers.json'
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_papers = json.load(f)
                all_papers.extend(json_papers)
        except:
            pass
    
    # Load from Excel CNKI
    excel_path = 'CNKI-20260104152201560.xls'
    if os.path.exists(excel_path):
        excel_papers = load_excel_data(excel_path)
        if excel_papers:
            all_papers.extend(excel_papers)
    
    # If no papers loaded, create sample data
    if not all_papers:
        st.warning("No papers loaded. Using sample data.")
        all_papers = [
            {
                'title': 'Sample: Green Finance Development in China',
                'authors': ['Zhang Wei', 'Li Ming'],
                'source': 'Finance Research',
                'year': 2024,
                'keywords': ['green finance', 'sustainable development', 'ESG'],
                'category': 'Green Finance',
                'type': 'journal',
                'abstract': 'A study on green finance development in China.',
                'arxiv_id': 'SAMPLE_001',
                'word_count': 5000,
                'published': '2024-01-15'
            }
        ]
    
    # Convert to DataFrame
    papers_df = pd.DataFrame(all_papers)
    
    # Process dates
    if 'published' in papers_df.columns:
        papers_df['published_date'] = pd.to_datetime(papers_df['published'], errors='coerce')
        papers_df['date_display'] = papers_df['published_date'].dt.strftime('%b %d, %Y')
    
    if 'year' not in papers_df.columns and 'published_date' in papers_df.columns:
        papers_df['year'] = papers_df['published_date'].dt.year.fillna(2024)
    
    # Add colors for categories
    category_colors = {
        'Computational Finance': '#667eea',
        'Mathematical Finance': '#f59e0b',
        'Portfolio Management': '#10b981',
        'Risk Management': '#8b5cf6',
        'Green Finance': '#22c55e',
        'Climate Finance': '#0ea5e9',
        'Sustainable Finance': '#10b981',
        'FinTech & Blockchain': '#6366f1',
        'Banking & Financial Institutions': '#8b4513',
        'Corporate Finance': '#4169e1',
        'General Finance': '#764ba2',
        'Unknown': '#94a3b8'
    }
    
    papers_df['category_color'] = papers_df['category'].map(category_colors).fillna('#94a3b8')
    
    return papers_df, all_papers

# ==================== HEADER ====================
st.title("📈 Finance Research Hub")
st.markdown("Discover, classify, and explore cutting-edge finance research papers")

# ==================== LOAD DATA ====================
with st.spinner("Loading research papers..."):
    papers_df, papers_list = load_research_papers()

# ==================== RESEARCH LIBRARY ====================
def display_research_library():
    """Display the research library interface"""
    
    st.header("📚 Research Library")
    st.markdown("Browse and explore finance research papers from arXiv and CNKI")
    
    if not papers_df.empty:
        cnki_papers = len(papers_df[papers_df['arxiv_id'].str.startswith('CNKI') | 
                                    papers_df['arxiv_id'].str.startswith('THESIS')])
        other_papers = len(papers_df) - cnki_papers
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Papers", len(papers_df))
        with col2:
            st.metric("Categories", papers_df['category'].nunique())
        with col3:
            st.metric("Chinese Papers", cnki_papers)
        with col4:
            st.metric("Other Papers", other_papers)
    
    # Search and filter
    with st.expander("🔍 Search & Filter Papers", expanded=True):
        search_cols = st.columns([3, 1, 1])
        with search_cols[0]:
            search_query = st.text_input("Search papers", placeholder="Type keywords...")
        
        with search_cols[1]:
            if 'category' in papers_df.columns:
                categories = ["All"] + sorted(papers_df['category'].dropna().unique().tolist())
                selected_category = st.selectbox("Category", categories)
        
        with search_cols[2]:
            if 'year' in papers_df.columns:
                years = ["All"] + sorted(papers_df['year'].dropna().unique().tolist(), reverse=True)
                selected_year = st.selectbox("Year", years)
    
    # Filter papers
    filtered_df = papers_df.copy()
    
    if search_query:
        mask = (
            filtered_df['title'].str.contains(search_query, case=False, na=False) |
            filtered_df['abstract'].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
    
    # Display papers
    if filtered_df.empty:
        st.info("No papers found matching your criteria.")
    else:
        st.subheader(f"Found {len(filtered_df)} papers")
        
        for idx, paper in filtered_df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{paper.get('title', 'Untitled')}**")
                    st.markdown(f"👥 {', '.join(paper.get('authors', [])) if isinstance(paper.get('authors'), list) else paper.get('authors', 'Unknown')}")
                    
                    if paper.get('keywords'):
                        keywords = paper['keywords'][:5] if isinstance(paper['keywords'], list) else []
                        if keywords:
                            st.markdown(f"🏷️ **Keywords:** {', '.join(keywords)}")
                    
                    if paper.get('abstract'):
                        with st.expander("Abstract"):
                            st.write(paper['abstract'])
                
                with col2:
                    st.markdown(f"<div style='background-color: {paper.get('category_color', '#e0e7ff')}20; padding: 8px; border-radius: 8px; border: 1px solid {paper.get('category_color', '#e0e7ff')}80;'>"
                                f"<small>{paper.get('category', 'Unknown')}</small><br>"
                                f"<small>📅 {paper.get('date_display', 'Unknown')}</small>"
                                f"</div>", unsafe_allow_html=True)
                
                st.divider()

# ==================== ENHANCED CLASSIFIER ====================
def display_enhanced_classifier():
    """Display the enhanced classifier interface"""
    
    st.header("🤖 Bilingual AI Classifier")
    st.markdown("Classify finance papers using bilingual keyword analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        paper_title = st.text_area("Paper Title", placeholder="Enter the research paper title...", height=60)
        paper_abstract = st.text_area("Abstract / Summary", placeholder="Paste the abstract or summary...", height=200)
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            top_k = st.slider("Number of categories", 3, 10, 5)
        with col_opt2:
            min_confidence = st.slider("Minimum confidence (%)", 10, 100, 20)
        
        if st.button("🚀 Run Bilingual Classification", type="primary", use_container_width=True):
            if paper_title or paper_abstract:
                with st.spinner("Classifying..."):
                    time.sleep(1)
                    combined_text = f"{paper_title} {paper_abstract}"
                    results = enhanced_classify_with_confidence(combined_text, top_k)
                    
                    # Filter by confidence
                    filtered_results = [r for r in results if r['confidence'] >= min_confidence]
                    
                    if filtered_results:
                        top_result = filtered_results[0]
                        
                        # Display top result
                        st.subheader("🎯 Primary Classification")
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.markdown(f"### {top_result['icon']} {top_result['category']}")
                            if top_result['matched_keywords']:
                                st.markdown(f"**Matched keywords:** {', '.join(top_result['matched_keywords'][:5])}")
                        
                        with col_b:
                            confidence_color = "green" if top_result['confidence'] > 70 else "orange" if top_result['confidence'] > 40 else "red"
                            st.markdown(f"<h1 style='color: {confidence_color}; text-align: center;'>{top_result['confidence']:.1f}%</h1>", unsafe_allow_html=True)
                            st.progress(top_result['confidence'] / 100)
                        
                        # Display all results
                        st.subheader("📊 All Category Scores")
                        cols = st.columns(min(len(filtered_results), 4))
                        
                        for idx, result in enumerate(filtered_results):
                            with cols[idx % len(cols)]:
                                st.markdown(f"""
                                <div style='border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; text-align: center;'>
                                    <div style='font-size: 24px;'>{result['icon']}</div>
                                    <div style='font-weight: bold;'>{result['category']}</div>
                                    <div style='font-size: 20px; color: {result["color"]};'>{result['confidence']:.1f}%</div>
                                    <div style='font-size: 12px; color: gray;'>{result['total_matches']} matches</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning(f"No categories found with confidence ≥ {min_confidence}%")
            else:
                st.error("Please enter at least a title or abstract.")
    
    with col2:
        st.subheader("📚 Bilingual Database")
        st.metric("Categories", len(FINANCE_KEYWORD_DATABASE))
        
        # Show database info
        with st.expander("View Categories"):
            for category, data in FINANCE_KEYWORD_DATABASE.items():
                st.markdown(f"**{data['icon']} {category}**")
                st.caption(f"{len(data['keywords'])} keywords")

# ==================== STATISTICS DASHBOARD ====================
def display_statistics():
    """Display statistics dashboard"""
    
    st.header("📊 Research Analytics")
    st.markdown("Insights and trends from the bilingual research collection")
    
    if papers_df.empty:
        st.warning("No data available for analytics.")
        return
    
    # Basic stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Papers", len(papers_df))
    with col2:
        st.metric("Chinese Papers", len(papers_df[papers_df['arxiv_id'].str.contains('CNKI|THESIS', na=False)]))
    with col3:
        st.metric("Categories", papers_df['category'].nunique())
    with col4:
        st.metric("Average Year", int(papers_df['year'].mean()) if 'year' in papers_df.columns else 2024)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Category Distribution")
        if 'category' in papers_df.columns:
            category_counts = papers_df['category'].value_counts()
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.subheader("Publication Trend")
        if 'year' in papers_df.columns:
            yearly_counts = papers_df['year'].value_counts().sort_index()
            fig = px.bar(
                x=yearly_counts.index,
                y=yearly_counts.values,
                labels={'x': 'Year', 'y': 'Number of Papers'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    with st.expander("View Raw Data"):
        st.dataframe(papers_df[['title', 'authors', 'category', 'year', 'source']].head(20))

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("📈 Finance Research Hub")
    st.markdown("v4.0 • Bilingual Edition")
    
    st.divider()
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["📚 Research Library", "🤖 Enhanced Classifier", "📊 Analytics"]
    )
    
    st.divider()
    
    # File check
    check_files()
    
    st.divider()
    
    # Quick actions
    if st.button("🔄 Clear Cache & Reload"):
        st.cache_data.clear()
        st.rerun()
    
    # Info
    if not papers_df.empty:
        st.caption(f"📄 {len(papers_df)} papers loaded")
        if 'category' in papers_df.columns:
            st.caption(f"📊 {papers_df['category'].nunique()} categories")

# ==================== MAIN APP ====================
if page == "📚 Research Library":
    display_research_library()
elif page == "🤖 Enhanced Classifier":
    display_enhanced_classifier()
elif page == "📊 Analytics":
    display_statistics()

# ==================== FOOTER ====================
st.divider()
st.caption("Finance Research Hub • v4.0 • Bilingual Edition • Made for researchers")