import streamlit as st
import pandas as pd
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
    page_title="Finance Research Hub - 金融研究平台",
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
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;">
        <h1 style="margin: 0; font-size: 42px; font-weight: 700; line-height: 1.2;">📈 Finance Research Hub - 金融研究平台</h1>
        <p style="margin: 12px 0 0 0; font-size: 18px; opacity: 0.9; font-weight: 400;">
            Discover, classify, and explore cutting-edge finance research papers | 发现、分类和探索前沿金融研究论文
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== BILINGUAL KEYWORD DATABASE ====================
# English-Chinese bilingual keyword database
FINANCE_KEYWORD_DATABASE = {
    "Computational Finance": {
        "keywords_en": [
            "deep learning", "neural networks", "machine learning", "AI", "artificial intelligence",
            "gradient descent", "backpropagation", "convolutional", "recurrent", "transformer",
            "PDE", "partial differential equation", "numerical methods", "finite difference", "finite element",
            "Monte Carlo", "simulation", "stochastic", "high-dimensional", "computational",
            "algorithm", "optimization", "parallel computing", "GPU", "CUDA",
            "quantum computing", "quantum algorithms", "VQE", "quantum annealing",
            "reinforcement learning", "Q-learning", "deep Q-network", "policy gradient",
            "time series forecasting", "sequence models", "LSTM", "GRU", "attention"
        ],
        "keywords_zh": [
            "深度学习", "神经网络", "机器学习", "人工智能", "AI",
            "梯度下降", "反向传播", "卷积", "循环", "变压器",
            "偏微分方程", "PDE", "数值方法", "有限差分", "有限元",
            "蒙特卡洛", "模拟", "随机", "高维", "计算",
            "算法", "优化", "并行计算", "GPU", "CUDA",
            "量子计算", "量子算法", "量子退火", "变分量子算法",
            "强化学习", "Q学习", "深度Q网络", "策略梯度",
            "时间序列预测", "序列模型", "长短期记忆", "门控循环单元", "注意力机制"
        ],
        "weight": 1.0,
        "color": "#667eea",
        "icon": "💻"
    },
    
    "Mathematical Finance": {
        "keywords_en": [
            "stochastic calculus", "Ito", "Stratonovich", "Brownian motion", "martingale",
            "partial differential equation", "PDE", "Black-Scholes", "option pricing", "risk-neutral",
            "measure theory", "probability", "stochastic processes", "Levy processes", "jump diffusion",
            "Malliavin calculus", "Heston model", "SABR", "local volatility", "stochastic volatility",
            "optimal stopping", "optimal control", "Hamilton-Jacobi-Bellman", "dynamic programming",
            "portfolio optimization", "Markowitz", "mean-variance", "efficient frontier",
            "interest rate models", "Vasicek", "CIR", "HJM", "LIBOR market model"
        ],
        "keywords_zh": [
            "随机微积分", "伊藤", "斯特拉托诺维奇", "布朗运动", "鞅",
            "偏微分方程", "布莱克-斯科尔斯", "期权定价", "风险中性",
            "测度论", "概率", "随机过程", "列维过程", "跳跃扩散",
            "马利亚万计算", "赫斯顿模型", "SABR模型", "局部波动率", "随机波动率",
            "最优停止", "最优控制", "哈密顿-雅可比-贝尔曼", "动态规划",
            "投资组合优化", "马科维茨", "均值-方差", "有效前沿",
            "利率模型", "瓦西塞克", "CIR模型", "HJM模型", "LIBOR市场模型"
        ],
        "weight": 0.95,
        "color": "#f59e0b",
        "icon": "📐"
    },
    
    "Portfolio Management": {
        "keywords_en": [
            "portfolio optimization", "asset allocation", "diversification", "efficient frontier",
            "mean-variance", "Markowitz", "Black-Litterman", "risk parity", "minimum variance",
            "tactical asset allocation", "strategic asset allocation", "rebalancing", "turnover",
            "tracking error", "active share", "index tracking", "enhanced indexing",
            "factor investing", "smart beta", "risk factors", "style factors",
            "hedge funds", "mutual funds", "ETF", "exchange-traded funds", "fund management",
            "performance measurement", "Sharpe ratio", "Sortino ratio", "information ratio"
        ],
        "keywords_zh": [
            "投资组合优化", "资产配置", "分散化", "有效前沿",
            "均值-方差", "马科维茨", "布莱克-利特曼", "风险平价", "最小方差",
            "战术资产配置", "战略资产配置", "再平衡", "换手率",
            "跟踪误差", "主动份额", "指数跟踪", "增强指数",
            "因子投资", "智能贝塔", "风险因子", "风格因子",
            "对冲基金", "共同基金", "交易所交易基金", "基金管理",
            "绩效衡量", "夏普比率", "索提诺比率", "信息比率"
        ],
        "weight": 0.9,
        "color": "#10b981",
        "icon": "📊"
    },
    
    "Risk Management": {
        "keywords_en": [
            "value at risk", "VaR", "expected shortfall", "ES", "CVaR", "conditional value at risk",
            "stress testing", "scenario analysis", "backtesting", "historical simulation",
            "credit risk", "default risk", "counterparty risk", "credit value adjustment", "CVA",
            "market risk", "volatility risk", "interest rate risk", "currency risk",
            "liquidity risk", "funding liquidity", "market liquidity", "bid-ask spread",
            "operational risk", "model risk", "legal risk", "compliance risk",
            "systemic risk", "too big to fail", "contagion", "network risk"
        ],
        "keywords_zh": [
            "风险价值", "VaR", "预期损失", "ES", "条件风险价值", "CVaR",
            "压力测试", "情景分析", "回测", "历史模拟",
            "信用风险", "违约风险", "交易对手风险", "信用估值调整", "CVA",
            "市场风险", "波动率风险", "利率风险", "汇率风险",
            "流动性风险", "资金流动性", "市场流动性", "买卖价差",
            "操作风险", "模型风险", "法律风险", "合规风险",
            "系统性风险", "大而不能倒", "传染风险", "网络风险"
        ],
        "weight": 0.9,
        "color": "#8b5cf6",
        "icon": "⚠️"
    },
    
    "Pricing of Securities": {
        "keywords_en": [
            "option pricing", "Black-Scholes", "binomial tree", "trinomial tree", "finite difference",
            "Monte Carlo pricing", "least squares Monte Carlo", "LSM", "American options",
            "exotic options", "barrier options", "Asian options", "lookback options", "digital options",
            "interest rate derivatives", "swaps", "swaptions", "caps", "floors",
            "credit derivatives", "CDS", "credit default swaps", "CDO", "collateralized debt obligations",
            "fixed income pricing", "bond pricing", "yield curve", "term structure", "duration"
        ],
        "keywords_zh": [
            "期权定价", "布莱克-斯科尔斯", "二叉树", "三叉树", "有限差分",
            "蒙特卡洛定价", "最小二乘蒙特卡洛", "LSM", "美式期权",
            "奇异期权", "障碍期权", "亚式期权", "回望期权", "数字期权",
            "利率衍生品", "互换", "互换期权", "利率上限", "利率下限",
            "信用衍生品", "信用违约互换", "CDS", "债务抵押债券", "CDO",
            "固定收益定价", "债券定价", "收益率曲线", "期限结构", "久期"
        ],
        "weight": 0.85,
        "color": "#ef4444",
        "icon": "💰"
    },
    
    "Financial Econometrics": {
        "keywords_en": [
            "time series analysis", "ARIMA", "ARMA", "ARCH", "GARCH", "EGARCH", "TGARCH",
            "vector autoregression", "VAR", "cointegration", "error correction model", "ECM",
            "unit root tests", "Dickey-Fuller", "Phillips-Perron", "KPSS",
            "volatility modeling", "realized volatility", "high-frequency data", "microstructure noise",
            "panel data", "fixed effects", "random effects", "dynamic panel", "GMM",
            "event study", "abnormal returns", "cumulative abnormal returns", "CAR"
        ],
        "keywords_zh": [
            "时间序列分析", "ARIMA", "ARMA", "ARCH", "GARCH", "EGARCH", "TGARCH",
            "向量自回归", "VAR", "协整", "误差修正模型", "ECM",
            "单位根检验", "迪基-富勒", "菲利普斯-佩龙", "KPSS",
            "波动率建模", "已实现波动率", "高频数据", "市场微观结构噪声",
            "面板数据", "固定效应", "随机效应", "动态面板", "广义矩估计",
            "事件研究", "异常收益", "累积异常收益", "CAR"
        ],
        "weight": 0.85,
        "color": "#06b6d4",
        "icon": "📈"
    },
    
    "Market Microstructure": {
        "keywords_en": [
            "limit order book", "market orders", "limit orders", "order flow", "order imbalance",
            "bid-ask spread", "market depth", "liquidity", "illiquidity", "market impact",
            "price impact", "temporary impact", "permanent impact", "Kyle's lambda",
            "high-frequency trading", "algorithmic trading", "market making", "statistical arbitrage",
            "latency", "tick size", "minimum price variation", "decimalization"
        ],
        "keywords_zh": [
            "限价订单簿", "市价订单", "限价订单", "订单流", "订单不平衡",
            "买卖价差", "市场深度", "流动性", "非流动性", "市场冲击",
            "价格冲击", "暂时冲击", "永久冲击", "凯尔λ",
            "高频交易", "算法交易", "做市", "统计套利",
            "延迟", "最小报价单位", "最小价格变动", "十进制报价"
        ],
        "weight": 0.8,
        "color": "#f97316",
        "icon": "⚡"
    },
    
    "Sustainable Finance": {
        "keywords_en": [
            "ESG", "environmental social governance", "sustainable investing", "responsible investing",
            "green bonds", "climate bonds", "sustainability-linked bonds",
            "carbon pricing", "carbon credits", "emissions trading", "cap and trade",
            "climate risk", "physical risk", "transition risk", "TCFD", "climate stress testing",
            "impact investing", "social impact bonds", "development finance"
        ],
        "keywords_zh": [
            "ESG", "环境社会和治理", "可持续投资", "责任投资",
            "绿色债券", "气候债券", "可持续发展挂钩债券",
            "碳定价", "碳信用", "排放交易", "限额与交易",
            "气候风险", "物理风险", "转型风险", "气候相关财务披露", "气候压力测试",
            "影响力投资", "社会效益债券", "发展金融"
        ],
        "weight": 0.75,
        "color": "#22c55e",
        "icon": "🌱"
    },
    
    "FinTech & Blockchain": {
        "keywords_en": [
            "blockchain", "distributed ledger", "smart contracts", "Ethereum", "solidity",
            "cryptocurrency", "Bitcoin", "Ethereum", "DeFi", "decentralized finance",
            "stablecoins", "CBDC", "central bank digital currency", "digital currency",
            "tokenization", "NFT", "non-fungible tokens", "security tokens",
            "crypto exchanges", "crypto wallets", "hot wallet", "cold wallet"
        ],
        "keywords_zh": [
            "区块链", "分布式账本", "智能合约", "以太坊", "Solidity",
            "加密货币", "比特币", "以太坊", "去中心化金融", "DeFi",
            "稳定币", "央行数字货币", "CBDC", "数字货币",
            "通证化", "非同质化代币", "NFT", "证券型代币",
            "加密货币交易所", "加密货币钱包", "热钱包", "冷钱包"
        ],
        "weight": 0.8,
        "color": "#6366f1",
        "icon": "🔗"
    },
    
    "Corporate Finance": {
        "keywords_en": [
            "capital structure", "dividend policy", "mergers and acquisitions", "M&A", "takeovers",
            "initial public offering", "IPO", "venture capital", "private equity",
            "corporate governance", "agency theory", "corporate restructuring", "financial distress",
            "working capital management", "cash management", "capital budgeting", "investment decisions"
        ],
        "keywords_zh": [
            "资本结构", "股利政策", "并购", "兼并收购", "接管",
            "首次公开发行", "IPO", "风险投资", "私募股权",
            "公司治理", "代理理论", "公司重组", "财务困境",
            "营运资本管理", "现金管理", "资本预算", "投资决策"
        ],
        "weight": 0.8,
        "color": "#ec4899",
        "icon": "🏢"
    },
    
    "Behavioral Finance": {
        "keywords_en": [
            "investor psychology", "market anomalies", "momentum", "value effect", "growth effect",
            "overconfidence", "herding behavior", "loss aversion", "prospect theory",
            "behavioral biases", "cognitive biases", "emotional biases", "disposition effect",
            "market sentiment", "investor sentiment", "noise trading", "irrational exuberance"
        ],
        "keywords_zh": [
            "投资者心理", "市场异象", "动量效应", "价值效应", "成长效应",
            "过度自信", "羊群行为", "损失厌恶", "前景理论",
            "行为偏差", "认知偏差", "情绪偏差", "处置效应",
            "市场情绪", "投资者情绪", "噪声交易", "非理性繁荣"
        ],
        "weight": 0.75,
        "color": "#14b8a6",
        "icon": "🧠"
    }
}

# ==================== UTILITY FUNCTIONS ====================
def detect_language(text):
    """Detect if text is Chinese or English"""
    if not text:
        return "en"
    
    # Simple Chinese character detection
    zh_char_count = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    total_chars = len(text.replace(" ", "").replace("\n", ""))
    
    if total_chars > 0 and zh_char_count / total_chars > 0.3:
        return "zh"
    else:
        return "en"

def extract_keywords_english(text):
    """Extract keywords from English text"""
    if not text:
        return []
    
    text = text.lower()
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    words = text.split()
    
    stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    keywords = [word for word in words if len(word) > 2 and word not in stopwords]
    
    return keywords

def calculate_category_scores_bilingual(text, top_k=5):
    """Calculate classification scores for both Chinese and English text"""
    if not text:
        return []
    
    language = detect_language(text)
    text_lower = text.lower()
    scores = {}
    
    for category, data in FINANCE_KEYWORD_DATABASE.items():
        score = 0
        matched_keywords = []
        
        # Check both English and Chinese keywords
        if language == "zh":
            # Chinese keywords
            for keyword in data['keywords_zh']:
                if keyword in text:
                    score += 1
                    matched_keywords.append(f"{keyword} (中)")
            
            # Also check English keywords for bilingual papers
            for keyword in data['keywords_en']:
                if keyword.lower() in text_lower:
                    score += 0.5  # Lower weight for English keywords in Chinese text
                    matched_keywords.append(f"{keyword} (英)")
        
        else:  # English
            for keyword in data['keywords_en']:
                if keyword.lower() in text_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            # Also check Chinese keywords for bilingual papers
            for keyword in data['keywords_zh']:
                if keyword in text:
                    score += 0.5  # Lower weight for Chinese keywords in English text
                    matched_keywords.append(f"{keyword} (中)")
        
        # Apply category weight
        weighted_score = score * data['weight']
        
        if weighted_score > 0:
            scores[category] = {
                'score': weighted_score,
                'confidence': min(100, weighted_score * 8),
                'matched_keywords': matched_keywords[:10],
                'total_matches': len(matched_keywords),
                'icon': data['icon'],
                'color': data['color'],
                'language': language
            }
    
    sorted_categories = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
    return sorted_categories[:top_k]

def enhanced_classify_with_confidence_bilingual(text, top_k=5):
    """Enhanced bilingual classification function"""
    category_scores = calculate_category_scores_bilingual(text, top_k)
    
    results = []
    for category, data in category_scores:
        results.append({
            "category": category,
            "confidence": data['confidence'],
            "score": data['score'],
            "icon": data['icon'],
            "color": data['color'],
            "matched_keywords": data['matched_keywords'],
            "total_matches": data['total_matches'],
            "language": data['language']
        })
    
    if not results:
        default_categories = ["Computational Finance", "Mathematical Finance", "Financial Econometrics"]
        for category in default_categories[:top_k]:
            results.append({
                "category": category,
                "confidence": 25.0,
                "score": 3.0,
                "icon": FINANCE_KEYWORD_DATABASE[category]['icon'],
                "color": FINANCE_KEYWORD_DATABASE[category]['color'],
                "matched_keywords": [],
                "total_matches": 0,
                "language": "en"
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
        
        # Add language detection
        def detect_paper_language(row):
            title = str(row.get('title', ''))
            abstract = str(row.get('abstract', ''))
            return detect_language(title + ' ' + abstract)
        
        papers_df['language'] = papers_df.apply(detect_paper_language, axis=1)
        
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
        st.error(f"Error loading research papers: {str(e)[:100]}")
        # Return mock data if file not found
        return create_mock_data(), []

def create_mock_data():
    """Create mock data for demonstration"""
    mock_data = {
        'id': [1, 2, 3],
        'title': [
            "Deep Learning for Stock Price Prediction",
            "基于深度学习的股票价格预测研究",
            "Risk Management in Financial Markets"
        ],
        'authors': [
            ["John Smith", "Jane Doe"],
            ["张三", "李四"],
            ["Robert Johnson"]
        ],
        'year': [2024, 2024, 2023],
        'category': ['Computational Finance', 'Computational Finance', 'Risk Management'],
        'abstract': [
            "This paper explores deep learning techniques for stock price prediction using LSTM networks.",
            "本文使用LSTM神经网络研究股票价格预测的深度学习技术。",
            "An analysis of risk management strategies in volatile financial markets."
        ],
        'word_count': [150, 120, 180],
        'arxiv_id': ['2401.001', '2401.002', '2301.001']
    }
    return pd.DataFrame(mock_data)

papers_df, papers_list = load_research_papers()

# ==================== RESEARCH LIBRARY ====================
def display_research_library():
    """Display the research library interface"""
    
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1e293b; font-size: 28px; font-weight: 700; margin-bottom: 8px;">
            📚 Research Library | 研究文献库
        </h2>
        <p style="color: #64748b; font-size: 16px; margin-bottom: 24px;">
            Browse finance research papers | 浏览金融研究论文
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
            english_papers = len(papers_df[papers_df['language'] == 'en'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #667eea;">{english_papers}</div>
                <div class="metric-label">English Papers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[2]:
            chinese_papers = len(papers_df[papers_df['language'] == 'zh'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: #ef4444;">{chinese_papers}</div>
                <div class="metric-label">中文论文</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[3]:
            if 'year' in papers_df.columns:
                recent_year = papers_df['year'].max()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{recent_year}</div>
                    <div class="metric-label">Latest Year</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Search and Filter
    with st.container():
        st.markdown("""
        <div class="card" style="margin-top: 24px;">
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin-bottom: 20px;">
                🔍 Search & Filter Papers | 搜索和筛选论文
            </h3>
        """, unsafe_allow_html=True)
        
        search_cols = st.columns([3, 1, 1])
        with search_cols[0]:
            search_query = st.text_input(
                "Search papers by title, authors, or abstract | 按标题、作者或摘要搜索",
                placeholder="Type keywords in English or Chinese... | 输入英文或中文关键词...",
                key="library_search"
            )
        
        with search_cols[1]:
            if 'category' in papers_df.columns:
                categories = sorted(papers_df['category'].dropna().unique().tolist())
                selected_category = st.selectbox("Category | 类别", ["All Categories | 所有类别"] + categories, key="category_filter")
        
        with search_cols[2]:
            language_filter = st.selectbox("Language | 语言", ["All | 全部", "English | 英文", "Chinese | 中文"], key="language_filter")
        
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
        
        if 'category' in filtered_df.columns and selected_category != "All Categories | 所有类别":
            # Extract just the category name before the pipe
            category_name = selected_category.split(' | ')[0]
            filtered_df = filtered_df[filtered_df['category'] == category_name]
        
        if language_filter == "English | 英文":
            filtered_df = filtered_df[filtered_df['language'] == 'en']
        elif language_filter == "Chinese | 中文":
            filtered_df = filtered_df[filtered_df['language'] == 'zh']
    
    # Display Results
    if filtered_df.empty:
        st.markdown("""
        <div class="card" style="text-align: center; padding: 48px 24px;">
            <div style="font-size: 48px; margin-bottom: 16px;">🔍</div>
            <h3 style="color: #475569; margin-bottom: 8px;">No papers found | 未找到论文</h3>
            <p style="color: #94a3b8;">Try adjusting your search or filter criteria | 请调整搜索或筛选条件</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 32px 0 16px 0;">
            <div>
                <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin: 0;">
                    📄 Found {len(filtered_df)} papers | 找到{len(filtered_df)}篇论文
                </h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each paper
        for idx, paper in filtered_df.iterrows():
            language_icon = "🇨🇳" if paper.get('language') == 'zh' else "🇬🇧"
            language_label = "中文" if paper.get('language') == 'zh' else "English"
            
            paper_html = f"""
            <div class="paper-item">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div style="flex: 1;">
                        <div class="paper-title">
                            <span style="color: #667eea; margin-right: 8px;">{language_icon}</span>
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
                        {language_icon} {language_label}
                    </span>
                    <span class="badge badge-secondary">
                        📅 {paper.get('year', 'Unknown')}
                    </span>
                    <span class="badge badge-secondary">
                        📝 {paper.get('word_count', 0)} words
                    </span>
                </div>
                
                <div class="paper-abstract">
                    <div style="font-weight: 600; color: #475569; margin-bottom: 8px; font-size: 13px;">
                        ABSTRACT | 摘要
                    </div>
                    {paper.get('abstract', 'No abstract available')}
                </div>
                
                <div style="display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap;">
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
                        🤖 Classify | 分类
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
    language = top_results[0].get('language', 'en')
    
    if top_category["confidence"] > 70:
        confidence_color = "#10b981"
        confidence_level = "High" if language == "en" else "高"
    elif top_category["confidence"] > 40:
        confidence_color = "#f59e0b"
        confidence_level = "Medium" if language == "en" else "中"
    else:
        confidence_color = "#ef4444"
        confidence_level = "Low" if language == "en" else "低"
    
    language_label = "Chinese | 中文" if language == "zh" else "English | 英文"
    
    # Display results
    st.markdown(f"""
    <div class="card" style="margin: 24px 0;">
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
            <div style="font-size: 36px; color: {top_category['color']};">
                {top_category['icon']}
            </div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 8px 0; color: #1e293b; font-size: 20px;">
                    AI Classification Results | AI分类结果
                </h3>
                <p style="margin: 0; color: #64748b; font-size: 14px;">
                    Based on bilingual keyword analysis | 基于双语关键词分析
                    <span style="background: #e2e8f0; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 8px;">
                        {language_label}
                    </span>
                </p>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
            <div>
                <div style="background: {confidence_color}10; padding: 20px; border-radius: 12px; border-left: 4px solid {confidence_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div>
                            <div style="font-size: 14px; color: #64748b; margin-bottom: 4px;">
                                Primary Classification | 主要分类
                            </div>
                            <div style="font-size: 24px; font-weight: 700; color: {top_category['color']};">
                                {top_category['category']}
                            </div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 32px; font-weight: 700; color: {confidence_color};">
                                {top_category['confidence']:.1f}%
                            </div>
                            <div style="font-size: 12px; color: {confidence_color};">
                                {confidence_level} Confidence | {confidence_level}置信度
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 16px;">
                        <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">
                            Matched Keywords | 匹配关键词:
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                            {''.join([f'<span style="background: {top_category["color"]}20; color: {top_category["color"]}; padding: 4px 10px; border-radius: 16px; font-size: 12px; font-weight: 500;">{kw}</span>' for kw in top_category["matched_keywords"][:8]])}
                        </div>
                    </div>
                </div>
            </div>
            
            <div>
                <div style="background: #f8fafc; padding: 20px; border-radius: 12px;">
                    <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">
                        Classification Details | 分类详情
                    </div>
                    <div style="font-size: 12px; color: #475569; line-height: 1.6;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span>Total Keywords Matched | 匹配关键词总数:</span>
                            <span style="font-weight: 600;">{top_category['total_matches']}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span>Classification Score | 分类得分:</span>
                            <span style="font-weight: 600;">{top_category['score']:.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Algorithm | 算法:</span>
                            <span style="font-weight: 600;">Bilingual Keyword-based | 双语关键词</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(top_category["confidence"] / 100, 
                text=f"Model Confidence: {top_category['confidence']:.1f}% | 模型置信度: {top_category['confidence']:.1f}%")
    
    # All categories
    st.markdown("### 📊 All Category Scores | 所有类别得分")
    cols = st.columns(min(5, len(top_results)))
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
                    {result['total_matches']} keywords matched | {result['total_matches']}个关键词匹配
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
                    Enhanced AI Classifier | 增强AI分类器
                </h2>
                <p style="color: #64748b; margin: 0; font-size: 16px;">
                    Classify finance papers in English and Chinese using bilingual keyword analysis | 
                    使用双语关键词分析分类英文和中文金融论文
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
                📝 Input Paper Details | 输入论文详情
            </h3>
        """, unsafe_allow_html=True)
        
        paper_title = st.text_area(
            "Paper Title | 论文标题",
            placeholder="Enter paper title in English or Chinese... | 输入英文或中文论文标题...",
            height=60,
            key="classifier_title"
        )
        
        paper_abstract = st.text_area(
            "Abstract / Summary | 摘要 / 总结",
            placeholder="Paste the abstract or summary in English or Chinese... | 粘贴英文或中文摘要...",
            height=200,
            key="classifier_abstract"
        )
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            top_k = st.slider("Number of categories | 类别数量", 3, 10, 5, key="top_k_slider")
        with col_opt2:
            min_confidence = st.slider("Minimum confidence (%) | 最小置信度(%)", 20, 100, 30, key="min_confidence")
        
        classify_button = st.button(
            "🚀 Run Enhanced Classification | 运行增强分类",
            type="primary",
            use_container_width=True,
            key="enhanced_classify_button"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        total_keywords_en = sum(len(data['keywords_en']) for data in FINANCE_KEYWORD_DATABASE.values())
        total_keywords_zh = sum(len(data['keywords_zh']) for data in FINANCE_KEYWORD_DATABASE.values())
        total_keywords = total_keywords_en + total_keywords_zh
        
        st.markdown(f"""
        <div class="card">
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin-bottom: 20px;">
                📚 Classification Database | 分类数据库
            </h3>
            
            <div style="margin-bottom: 24px;">
                <div style="font-size: 14px; color: #64748b; margin-bottom: 8px;">Database Statistics | 数据库统计</div>
                <div style="background: #f8fafc; padding: 16px; border-radius: 12px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #475569;">Categories | 类别:</span>
                        <span style="font-weight: 600; color: #667eea;">{len(FINANCE_KEYWORD_DATABASE)}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #475569;">English Keywords | 英文关键词:</span>
                        <span style="font-weight: 600; color: #667eea;">{total_keywords_en}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="color: #475569;">Chinese Keywords | 中文关键词:</span>
                        <span style="font-weight: 600; color: #ef4444;">{total_keywords_zh}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #475569;">Total Keywords | 总关键词:</span>
                        <span style="font-weight: 600; color: #10b981;">{total_keywords}</span>
                    </div>
                </div>
            </div>
            
            <div>
                <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">Supported Categories | 支持的类别</div>
                <div style="max-height: 300px; overflow-y: auto;">
        """, unsafe_allow_html=True)
        
        # Display categories
        for category, data in FINANCE_KEYWORD_DATABASE.items():
            st.markdown(f"""
            <div style="background: {data['color']}10; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {data['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="font-size: 16px;">{data['icon']}</div>
                        <div style="font-size: 13px; font-weight: 500; color: #1e293b;">{category}</div>
                    </div>
                    <div style="display: flex; gap: 4px;">
                        <div style="background: #667eea30; color: #667eea; padding: 2px 6px; border-radius: 10px; font-size: 10px; font-weight: 600;">
                            {len(data['keywords_en'])} EN
                        </div>
                        <div style="background: #ef444430; color: #ef4444; padding: 2px 6px; border-radius: 10px; font-size: 10px; font-weight: 600;">
                            {len(data['keywords_zh'])} 中
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div></div>", unsafe_allow_html=True)
    
    if classify_button and (paper_title or paper_abstract):
        with st.spinner("🔍 Analyzing text with bilingual keyword database... | 使用双语关键词数据库分析文本..."):
            time.sleep(1)
            
            combined_text = f"{paper_title} {paper_abstract}"
            classification_results = enhanced_classify_with_confidence_bilingual(
                combined_text, 
                top_k=top_k
            )
            
            filtered_results = [
                r for r in classification_results 
                if r['confidence'] >= min_confidence
            ]
            
            if filtered_results:
                display_classification_results(filtered_results, paper_title, paper_abstract)
                
                st.markdown("---")
                st.markdown("#### 📥 Export Classification Results | 导出分类结果")
                
                export_data = {
                    "title": paper_title,
                    "abstract": paper_abstract[:500],
                    "timestamp": datetime.now().isoformat(),
                    "language": filtered_results[0].get('language', 'en'),
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
                st.warning(f"No categories found with confidence ≥ {min_confidence}% | 未找到置信度≥{min_confidence}%的类别")
    elif classify_button:
        st.error("Please enter at least a title or abstract to classify. | 请至少输入标题或摘要进行分类。")

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
st.sidebar.header("🧭 Navigation | 导航")
app_mode = st.sidebar.radio(
    "",
    ["📚 Research Library", "🤖 Enhanced Classifier", "📊 Analytics"],
    help="Switch between different features | 在不同功能间切换",
    label_visibility="collapsed"
)

# Quick actions
st.sidebar.markdown("---")
st.sidebar.header("⚡ Quick Actions | 快速操作")

if st.sidebar.button("🔄 Refresh Data | 刷新数据", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# ==================== MAIN APP ROUTING ====================
if app_mode == "📚 Research Library":
    display_research_library()
    
elif app_mode == "🤖 Enhanced Classifier":
    display_enhanced_classifier()
    
elif app_mode == "📊 Analytics":
    # Simple analytics
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1e293b; font-size: 28px; font-weight: 700; margin-bottom: 8px;">
            📊 Analytics Dashboard | 分析仪表板
        </h2>
        <p style="color: #64748b; font-size: 16px; margin-bottom: 24px;">
            Database Statistics | 数据库统计
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not papers_df.empty:
        # Category distribution
        st.markdown("### 📈 Category Distribution | 类别分布")
        if 'category' in papers_df.columns:
            category_counts = papers_df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            fig = px.pie(category_counts, values='Count', names='Category', 
                        title="Papers by Category | 按类别分布的论文")
            st.plotly_chart(fig, use_container_width=True)
        
        # Language distribution
        st.markdown("### 🌍 Language Distribution | 语言分布")
        if 'language' in papers_df.columns:
            language_counts = papers_df['language'].value_counts().reset_index()
            language_counts.columns = ['Language', 'Count']
            language_counts['Language'] = language_counts['Language'].map({'en': 'English', 'zh': 'Chinese'})
            
            fig = px.bar(language_counts, x='Language', y='Count',
                        title="Papers by Language | 按语言分布的论文",
                        color='Language',
                        color_discrete_map={'English': '#667eea', 'Chinese': '#ef4444'})
            st.plotly_chart(fig, use_container_width=True)

# ==================== FOOTER ====================
st.markdown("""
<div style="margin-top: 64px; padding: 32px 0; text-align: center; color: #94a3b8; border-top: 1px solid #e2e8f0;">
    <div style="font-size: 14px; margin-bottom: 8px;">
        Finance Research Hub • v4.0 • Bilingual Edition • Made with ❤️ for researchers
    </div>
    <div style="display: flex; justify-content: center; gap: 24px; margin-top: 16px;">
        <span style="color: #64748b; font-size: 13px;">🌍 Support: English & Chinese</span>
        <span style="color: #64748b; font-size: 13px;">📚 Sources: arXiv & Local Database</span>
        <span style="color: #64748b; font-size: 13px;">🤖 AI: Bilingual Classification</span>
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
                <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">Classification Started | 分类开始</div>
                <div style="font-size: 12px; opacity: 0.9; line-height: 1.4;">
                    Analyzing paper with bilingual AI...<br>
                    <strong>${title.substring(0, 50)}...</strong>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(notification);
    
    // Simulate redirect to classifier
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