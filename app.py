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
import sys

# ==================== PAGE CONFIG ====================
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

# ==================== BILINGUAL KEYWORD DATABASE ====================
FINANCE_KEYWORD_DATABASE = {
    "Computational Finance": {
        "keywords": [
            # English
            "deep learning", "neural networks", "machine learning", "AI", "artificial intelligence",
            "gradient descent", "backpropagation", "convolutional", "recurrent", "transformer",
            "PDE", "partial differential equation", "numerical methods", "finite difference", "finite element",
            "Monte Carlo", "simulation", "stochastic", "high-dimensional", "computational",
            "algorithm", "optimization", "parallel computing", "GPU", "CUDA",
            "quantum computing", "quantum algorithms", "VQE", "quantum annealing",
            "reinforcement learning", "Q-learning", "deep Q-network", "policy gradient",
            "time series forecasting", "sequence models", "LSTM", "GRU", "attention",
            # Chinese
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
            # English
            "stochastic calculus", "Ito", "Stratonovich", "Brownian motion", "martingale",
            "partial differential equation", "PDE", "Black-Scholes", "option pricing", "risk-neutral",
            "measure theory", "probability", "stochastic processes", "Levy processes", "jump diffusion",
            "Malliavin calculus", "Heston model", "SABR", "local volatility", "stochastic volatility",
            "optimal stopping", "optimal control", "Hamilton-Jacobi-Bellman", "dynamic programming",
            "portfolio optimization", "Markowitz", "mean-variance", "efficient frontier",
            "interest rate models", "Vasicek", "CIR", "HJM", "LIBOR market model",
            # Chinese
            "随机微积分", "伊藤", "布朗运动", "鞅", "偏微分方程",
            "布莱克-斯科尔斯", "期权定价", "风险中性", "测度论", "概率",
            "随机过程", "Levy过程", "跳跃扩散", "Malliavin微积分", "Heston模型",
            "局部波动率", "随机波动率", "最优停止", "最优控制", "动态规划",
            "投资组合优化", "马科维茨", "均值方差", "有效前沿", "利率模型"
        ],
        "weight": 0.95,
        "color": "#f59e0b",
        "icon": "📐"
    },
    
    "Portfolio Management": {
        "keywords": [
            # English
            "portfolio optimization", "asset allocation", "diversification", "efficient frontier",
            "mean-variance", "Markowitz", "Black-Litterman", "risk parity", "minimum variance",
            "tactical asset allocation", "strategic asset allocation", "rebalancing", "turnover",
            "tracking error", "active share", "index tracking", "enhanced indexing",
            "factor investing", "smart beta", "risk factors", "style factors",
            "hedge funds", "mutual funds", "ETF", "exchange-traded funds", "fund management",
            "performance measurement", "Sharpe ratio", "Sortino ratio", "information ratio",
            # Chinese
            "投资组合优化", "资产配置", "分散化", "有效前沿", "均值方差",
            "马科维茨", "风险平价", "最小方差", "战术资产配置", "战略资产配置",
            "再平衡", "换手率", "跟踪误差", "主动份额", "指数跟踪",
            "因子投资", "智能贝塔", "风险因子", "风格因子", "对冲基金",
            "共同基金", "交易所交易基金", "基金管理", "业绩衡量", "夏普比率"
        ],
        "weight": 0.9,
        "color": "#10b981",
        "icon": "📊"
    },
    
    "Risk Management": {
        "keywords": [
            # English
            "value at risk", "VaR", "expected shortfall", "ES", "CVaR", "conditional value at risk",
            "stress testing", "scenario analysis", "backtesting", "historical simulation",
            "credit risk", "default risk", "counterparty risk", "credit value adjustment", "CVA",
            "market risk", "volatility risk", "interest rate risk", "currency risk",
            "liquidity risk", "funding liquidity", "market liquidity", "bid-ask spread",
            "operational risk", "model risk", "legal risk", "compliance risk",
            "systemic risk", "too big to fail", "contagion", "network risk",
            # Chinese
            "风险价值", "VaR", "预期损失", "条件风险价值", "压力测试",
            "情景分析", "回测", "历史模拟", "信用风险", "违约风险",
            "交易对手风险", "信用价值调整", "市场风险", "波动率风险",
            "利率风险", "汇率风险", "流动性风险", "资金流动性", "市场流动性",
            "买卖价差", "操作风险", "模型风险", "法律风险", "合规风险",
            "系统性风险", "太大而不能倒", "传染效应", "网络风险"
        ],
        "weight": 0.9,
        "color": "#8b5cf6",
        "icon": "⚠️"
    },
    
    "Green Finance": {
        "keywords": [
            # English
            "green finance", "green bonds", "green loans", "green credit", "sustainable finance",
            "environmental finance", "eco-finance", "green investment", "ESG investment",
            "environmental, social and governance", "green banking", "green insurance",
            "green financial products", "green securities", "green transition finance",
            "low-carbon finance", "circular economy finance", "biodiversity finance",
            "natural capital", "green fintech", "sustainability-linked loans",
            "green mortgage", "energy efficiency finance", "pollution control finance",
            # Chinese
            "绿色金融", "绿色债券", "绿色贷款", "绿色信贷", "可持续金融",
            "环境金融", "生态金融", "绿色投资", "ESG投资", "环境社会治理",
            "绿色银行", "绿色保险", "绿色金融产品", "绿色证券", "绿色转型金融",
            "低碳金融", "循环经济金融", "生物多样性金融", "自然资本",
            "绿色金融科技", "可持续发展挂钩贷款", "绿色抵押贷款",
            "能效金融", "污染防治金融"
        ],
        "weight": 0.85,
        "color": "#22c55e",
        "icon": "🌿"
    },
    
    "Climate Finance": {
        "keywords": [
            # English
            "climate finance", "climate change finance", "climate risk finance", "climate adaptation finance",
            "climate mitigation finance", "carbon pricing", "carbon markets", "emissions trading",
            "carbon credits", "carbon offsets", "clean development mechanism", "CDM",
            "climate bonds", "climate funds", "green climate fund", "GCF",
            "adaptation finance", "mitigation finance", "climate resilient finance",
            "transition finance", "decarbonization finance", "net-zero finance",
            "carbon tax", "climate policy", "Paris Agreement finance",
            # Chinese
            "气候金融", "气候变化金融", "气候风险金融", "气候适应金融",
            "气候减缓金融", "碳定价", "碳市场", "碳排放交易",
            "碳信用", "碳抵消", "清洁发展机制", "气候债券",
            "气候基金", "绿色气候基金", "适应融资", "减缓融资",
            "气候韧性金融", "转型金融", "脱碳金融", "净零金融",
            "碳税", "气候政策", "巴黎协定融资"
        ],
        "weight": 0.85,
        "color": "#0ea5e9",
        "icon": "🌍"
    },
    
    "Sustainable Finance": {
        "keywords": [
            # English
            "ESG", "environmental social governance", "sustainable investing", "responsible investing",
            "green bonds", "climate bonds", "sustainability-linked bonds", "social bonds",
            "sustainable development goals", "SDG finance", "social finance", "impact bonds",
            "ethical investing", "sustainability reporting", "ESG integration", "ESG metrics",
            "sustainability performance", "corporate sustainability", "ESG disclosure",
            # Chinese
            "ESG", "环境社会治理", "可持续投资", "责任投资", "社会责任投资",
            "绿色债券", "气候债券", "可持续发展挂钩债券", "社会债券",
            "可持续发展目标", "SDG融资", "社会金融", "影响力债券",
            "伦理投资", "可持续发展报告", "ESG整合", "ESG指标",
            "可持续发展绩效", "企业可持续发展", "ESG信息披露"
        ],
        "weight": 0.8,
        "color": "#10b981",
        "icon": "🌱"
    },
    
    "FinTech & Blockchain": {
        "keywords": [
            # English
            "blockchain", "distributed ledger", "smart contracts", "Ethereum", "solidity",
            "cryptocurrency", "Bitcoin", "Ethereum", "DeFi", "decentralized finance",
            "stablecoins", "CBDC", "central bank digital currency", "digital currency",
            "tokenization", "NFT", "non-fungible tokens", "security tokens",
            "crypto exchanges", "crypto wallets", "hot wallet", "cold wallet",
            # Chinese
            "区块链", "分布式账本", "智能合约", "以太坊", "加密货币",
            "比特币", "去中心化金融", "稳定币", "央行数字货币",
            "数字货币", "代币化", "非同质化代币", "证券型代币",
            "加密货币交易所", "加密货币钱包", "热钱包", "冷钱包"
        ],
        "weight": 0.8,
        "color": "#6366f1",
        "icon": "🔗"
    },
    
    "Banking & Financial Institutions": {
        "keywords": [
            # English
            "commercial banks", "investment banks", "central banks", "bank regulation", "Basel",
            "capital adequacy", "liquidity coverage ratio", "LCR", "net stable funding ratio", "NSFR",
            "bank lending", "credit creation", "interbank market", "bank runs", "deposit insurance",
            "shadow banking", "financial intermediation", "bank profitability", "non-performing loans",
            "financial stability", "systemically important banks", "too big to fail", "bank consolidation",
            # Chinese
            "商业银行", "投资银行", "中央银行", "银行监管", "巴塞尔协议",
            "资本充足率", "流动性覆盖率", "净稳定资金比例", "银行信贷",
            "信用创造", "银行间市场", "银行挤兑", "存款保险", "影子银行",
            "金融中介", "银行盈利能力", "不良贷款", "金融稳定",
            "系统重要性银行", "太大而不能倒", "银行合并"
        ],
        "weight": 0.85,
        "color": "#8b4513",
        "icon": "🏦"
    },
    
    "Corporate Finance": {
        "keywords": [
            # English
            "capital structure", "Modigliani-Miller", "dividend policy", "payout policy", "share repurchase",
            "mergers and acquisitions", "M&A", "takeovers", "corporate governance", "board of directors",
            "agency theory", "principal-agent problem", "executive compensation", "CEO pay",
            "corporate investment", "capital budgeting", "NPV", "internal rate of return", "IRR",
            "working capital management", "cash management", "inventory management", "accounts receivable",
            # Chinese
            "资本结构", "莫迪利亚尼-米勒", "股利政策", "派息政策", "股票回购",
            "兼并与收购", "并购", "接管", "公司治理", "董事会",
            "代理理论", "委托代理问题", "高管薪酬", "首席执行官薪酬",
            "公司投资", "资本预算", "净现值", "内部收益率",
            "营运资本管理", "现金管理", "存货管理", "应收账款"
        ],
        "weight": 0.8,
        "color": "#4169e1",
        "icon": "🏢"
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
    }
}

# ==================== UTILITY FUNCTIONS ====================
def extract_keywords(text):
    """Extract meaningful keywords from text"""
    if not text:
        return []
    
    text = text.lower()
    text = re.sub(r'[^\w\s\u4e00-\u9fff\-\.]', ' ', text)
    words = text.split()
    
    stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    keywords = [word for word in words if len(word) > 1 and word not in stopwords]
    
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
            
            if 'Title-题名' in sheet_df.columns:
                for idx, row in sheet_df.iterrows():
                    if pd.isna(row.get('Title-题名')):
                        continue
                    
                    authors_str = str(row.get('Author-作者', ''))
                    authors = [author.strip() for author in authors_str.split(',') if author.strip()]
                    
                    keywords_str = str(row.get('关键词', ''))
                    keywords = [kw.strip() for kw in keywords_str.split(';;') if kw.strip()]
                    
                    paper = {
                        'title': str(row.get('Title-题名', '')),
                        'authors': authors,
                        'source': str(row.get('Source-文献来源', row.get('Source-报纸名', ''))),
                        'year': int(row.get('Year-年', row.get('Year-学位年度', 2024))) if not pd.isna(row.get('Year-年', row.get('Year-学位年度', pd.NaT))) else 2024,
                        'keywords': keywords,
                        'category_code': str(row.get('中图分类号', '')),
                        'type': 'journal' if 'Source-文献来源' in row else 'newspaper',
                        'abstract': '',
                        'arxiv_id': f"CNKI_{sheet_name}_{idx}",
                        'arxiv_url': '',
                        'pdf_url': '',
                        'word_count': len(str(row.get('Title-题名', '')).split()) * 20,
                        'published': f"{row.get('Year-年', 2024)}-01-01" if pd.notna(row.get('Year-年', pd.NaT)) else '2024-01-01'
                    }
                    
                    paper['category'] = enhanced_classification_for_cnki(
                        paper['title'],
                        paper['keywords'],
                        paper['category_code']
                    )
                    
                    if not paper.get('abstract', '') and paper['keywords']:
                        paper['abstract'] = f"Research Topic: {', '.join(paper['keywords'][:5])}. Published in {paper['source']} ({paper['year']})."
                    
                    all_papers.append(paper)
            
            elif '导师' in sheet_df.columns:
                for idx, row in sheet_df.iterrows():
                    if pd.isna(row.get('Title-文献题名')):
                        continue
                    
                    keywords_str = str(row.get('关键词', ''))
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
    
    # ========== DEBUG: Kiểm tra file trong thư mục ==========
    st.sidebar.subheader("🔍 File Check")
    
    # Tìm file Excel tự động
    excel_files = [f for f in os.listdir('.') if f.lower().endswith(('.xls', '.xlsx')) and 'cnki' in f.lower()]
    
    if excel_files:
        excel_path = excel_files[0]
        st.sidebar.success(f"✅ Found Excel: {excel_path}")
    else:
        st.sidebar.error("❌ No CNKI Excel file found!")
        st.sidebar.write("Looking for files with 'cnki' in name:")
        for f in os.listdir('.'):
            if f.lower().endswith(('.xls', '.xlsx')):
                st.sidebar.write(f"  - {f}")
        return pd.DataFrame(), []
    
    # Load từ JSON nếu có
    json_path = 'research_papers.json'
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_papers = json.load(f)
                all_papers.extend(json_papers)
                st.sidebar.success(f"✅ Loaded {len(json_papers)} papers from JSON")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not load JSON: {e}")
    
    # Load từ Excel CNKI
    try:
        excel_papers = load_excel_data(excel_path)
        if excel_papers:
            all_papers.extend(excel_papers)
            st.sidebar.success(f"✅ Loaded {len(excel_papers)} papers from Excel")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading Excel: {e}")
    
    # Nếu không có papers, tạo dữ liệu mẫu
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
        'Unknown': '#94a3b8',
        'Pricing of Securities': '#ef4444',
        'Financial Econometrics': '#06b6d4',
        'Market Microstructure': '#f97316'
    }
    
    papers_df['category_color'] = papers_df['category'].map(category_colors).fillna('#94a3b8')
    
    return papers_df, all_papers

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
            Browse and explore finance research papers from arXiv and CNKI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not papers_df.empty:
        cnki_papers = len(papers_df[papers_df['arxiv_id'].str.startswith('CNKI') | papers_df['arxiv_id'].str.startswith('THESIS')])
        other_papers = len(papers_df) - cnki_papers
        
        stats_cols = st.columns(5)
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
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{cnki_papers}</div>
                <div class="metric-label">Chinese Papers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[4]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{other_papers}</div>
                <div class="metric-label">Other Papers</div>
            </div>
            """, unsafe_allow_html=True)
    
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
                placeholder="Type keywords to search (English or Chinese)...",
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
            paper_type_filter = st.selectbox(
                "Paper Type", 
                ["All Types", "Chinese Papers", "Journal", "Newspaper", "Thesis", "Other"],
                key="type_filter"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
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
        
        if paper_type_filter != "All Types":
            if paper_type_filter == "Chinese Papers":
                filtered_df = filtered_df[filtered_df['arxiv_id'].str.startswith(('CNKI', 'THESIS'), na=False)]
            elif paper_type_filter in ["Journal", "Newspaper", "Thesis"]:
                filtered_df = filtered_df[filtered_df['type'] == paper_type_filter.lower()]
            elif paper_type_filter == "Other":
                filtered_df = filtered_df[~filtered_df['arxiv_id'].str.startswith(('CNKI', 'THESIS'), na=False)]
        
        filtered_df = filtered_df.sort_values('published_date', ascending=False) if 'published_date' in filtered_df.columns else filtered_df
    
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
        
        for idx, paper in filtered_df.iterrows():
            paper_type = paper.get('type', 'unknown')
            paper_type_badge = ""
            
            if paper.get('arxiv_id', '').startswith(('CNKI', 'THESIS')):
                paper_type_badge = '<span class="badge badge-secondary" style="background-color: #fee2e2; color: #dc2626;">🇨🇳 Chinese</span>'
            
            if paper_type == 'journal':
                paper_type_badge += '<span class="badge badge-secondary">📖 Journal</span>'
            elif paper_type == 'newspaper':
                paper_type_badge += '<span class="badge badge-secondary">📰 Newspaper</span>'
            elif paper_type == 'thesis':
                paper_type_badge += '<span class="badge badge-secondary">🎓 Thesis</span>'
            else:
                paper_type_badge += '<span class="badge badge-secondary">📄 Paper</span>'
            
            keywords_html = ""
            if paper.get('keywords'):
                keywords_list = paper['keywords'][:3] if isinstance(paper['keywords'], list) else []
                if keywords_list:
                    keywords_html = f"""
                    <div style="margin: 8px 0;">
                        <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">🏷️ Keywords:</div>
                        <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                            {''.join([f'<span style="background: #e2e8f0; color: #475569; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{kw}</span>' for kw in keywords_list])}
                        </div>
                    </div>
                    """
            
            # PDF và arXiv links
            links_html = ""
            if paper.get('arxiv_url'):
                links_html += f"""
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
            
            if paper.get('pdf_url'):
                links_html += f"""
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
                    {paper_type_badge}
                    <span class="badge badge-secondary">
                        📊 {paper.get('source', 'Unknown')}
                    </span>
                </div>
                
                {keywords_html}
                
                <div class="paper-abstract">
                    <div style="font-weight: 600; color: #475569; margin-bottom: 8px; font-size: 13px;">
                        ABSTRACT / DESCRIPTION
                    </div>
                    {paper.get('abstract', 'No abstract available')}
                </div>
                
                <div style="display: flex; gap: 8px; margin-top: 16px;">
                    {links_html}
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
                        🤖 Re-classify
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
    
    st.markdown(f"""
    <div class="card" style="margin: 24px 0;">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
            <div style="font-size: 36px; color: {top_category['color']};">
                {top_category['icon']}
            </div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 8px 0; color: #1e293b; font-size: 20px;">
                    🤖 AI Classification Results
                </h3>
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Based on bilingual keyword analysis (English & Chinese)
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
                        <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">Matched Keywords ({top_category['total_matches']} found):</div>
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
                            <span>Language Support:</span>
                            <span style="font-weight: 600;">English & Chinese</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(top_category["confidence"] / 100, text=f"Model Confidence: {top_category['confidence']:.1f}%")
    
    st.markdown("### 📊 All Category Scores")
    cols = st.columns(min(len(top_results), 5))
    for idx, (col, result) in enumerate(zip(cols, top_results)):
        with col:
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; text-align: center; height: 140px;">
                <div style="font-size: 24px; margin-bottom: 8px; color: {result['color']}">
                    {result['icon']}
                </div>
                <div style="font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 8px; line-height: 1.2;">
                    {result['category']}
                </div>
                <div style="font-size: 20px; font-weight: 700; color: {result['color']}; margin-bottom: 4px;">
                    {result['confidence']:.1f}%
                </div>
                <div style="font-size: 11px; color: #64748b;">
                    {result['total_matches']} matches
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
                    Bilingual AI Classifier
                </h2>
                <p style="color: #64748b; margin: 0; font-size: 16px;">
                    Classify finance papers using bilingual keyword analysis
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
                📝 Input Paper Details (English or Chinese)
            </h3>
        """, unsafe_allow_html=True)
        
        paper_title = st.text_area(
            "Paper Title",
            placeholder="Enter the research paper title (English or Chinese)...",
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
            min_confidence = st.slider("Minimum confidence (%)", 10, 100, 20, key="min_confidence")
        
        classify_button = st.button(
            "🚀 Run Bilingual Classification",
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
                📚 Bilingual Database
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
                        <span style="color: #475569;">Language Support:</span>
                        <span style="font-weight: 600; color: #22c55e;">English & Chinese</span>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 16px;">
                <div style="font-size: 14px; color: #64748b; margin-bottom: 8px;">New Categories:</div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                    <span style="background: #22c55e20; color: #22c55e; padding: 4px 10px; border-radius: 16px; font-size: 12px; font-weight: 500;">🌿 Green Finance</span>
                    <span style="background: #0ea5e920; color: #0ea5e9; padding: 4px 10px; border-radius: 16px; font-size: 12px; font-weight: 500;">🌍 Climate Finance</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if classify_button and (paper_title or paper_abstract):
        with st.spinner("🔍 Analyzing text with bilingual keyword database..."):
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
                        data=json.dumps(export_data, indent=2, ensure_ascii=False),
                        file_name=f"classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col_exp2:
                    results_df = pd.DataFrame(filtered_results)
                    results_df = results_df[['category', 'confidence', 'total_matches']]
                    st.download_button(
                        label="📊 Download CSV",
                        data=results_df.to_csv(index=False),
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
            Insights and trends from the bilingual research collection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_papers = len(papers_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #667eea;">{total_papers}</div>
            <div class="metric-label">Total Papers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        chinese_papers = len(papers_df[papers_df['arxiv_id'].str.startswith(('CNKI', 'THESIS'), na=False)])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">{chinese_papers}</div>
            <div class="metric-label">Chinese Papers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        english_papers = total_papers - chinese_papers
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #10b981;">{english_papers}</div>
            <div class="metric-label">English Papers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        unique_categories = papers_df['category'].nunique() if 'category' in papers_df.columns else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #8b5cf6;">{unique_categories}</div>
            <div class="metric-label">Categories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        if 'year' in papers_df.columns:
            recent_year = papers_df['year'].max()
            st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{recent_year}</div>
            <div class="metric-label">Latest Year</div>
        </div>
        """, unsafe_allow_html=True)
    
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
            
            colors = []
            for category in category_counts['Category']:
                colors.append(FINANCE_KEYWORD_DATABASE.get(category, {}).get('color', '#94a3b8'))
            
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
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">v4.0 • Bilingual Edition</div>
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
st.sidebar.header("ℹ️ System Info")

if not papers_df.empty:
    latest_paper = papers_df.sort_values('published_date', ascending=False).iloc[0]
    paper_language = "🇨🇳 Chinese" if str(latest_paper.get('arxiv_id', '')).startswith(('CNKI', 'THESIS')) else "🇺🇸 English"
    
    st.sidebar.markdown(f"""
    <div style="background: #f8fafc; padding: 16px; border-radius: 12px; border-left: 4px solid #667eea;">
        <div style="font-size: 13px; color: #64748b; margin-bottom: 4px;">Latest Paper</div>
        <div style="font-size: 14px; font-weight: 500; color: #1e293b; margin-bottom: 8px; line-height: 1.4;">
            {latest_paper.get('title', 'Untitled')[:50]}...
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8;">
            <span>📅 {latest_paper.get('date_display', 'Unknown')}</span>
            <span>{paper_language}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Database info
total_categories = len(FINANCE_KEYWORD_DATABASE)
total_keywords = sum(len(data['keywords']) for data in FINANCE_KEYWORD_DATABASE.values())

st.sidebar.markdown(f"""
<div style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-top: 16px;">
    <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">📊 Database Statistics</div>
    <div style="font-size: 12px; color: #475569;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span>Finance Categories:</span>
            <span style="font-weight: 600;">{total_categories}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span>Total Keywords:</span>
            <span style="font-weight: 600;">{total_keywords}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span>Language Support:</span>
            <span style="font-weight: 600;">Bilingual</span>
        </div>
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
        Finance Research Hub • v4.0 • Bilingual Edition • Made with ❤️ for researchers
    </div>
    <div style="font-size: 12px; color: #64748b; margin-bottom: 16px;">
        Supports English & Chinese papers • {len(FINANCE_KEYWORD_DATABASE)} finance categories
    </div>
</div>
""", unsafe_allow_html=True)

# Add JavaScript
st.markdown("""
<script>
function classifyPaper(title, abstract) {
    alert('Switching to classifier with paper: ' + title.substring(0, 50) + '...');
    // In a real implementation, this would switch tabs
}
</script>
""", unsafe_allow_html=True)