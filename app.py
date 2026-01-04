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

==================== CUSTOM CSS - MODERN STYLING ====================
st.markdown("""

<style> /* Main container */ .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); } /* Card styling */ .card { background: white; border-radius: 16px; padding: 24px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid #f0f0f0; transition: transform 0.3s ease, box-shadow 0.3s ease; margin-bottom: 20px; } .card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12); } /* Paper item styling */ .paper-item { background: #f8fafc; border-left: 4px solid #667eea; border-radius: 12px; padding: 20px; margin: 12px 0; transition: all 0.2s ease; } .paper-item:hover { background: #f1f5f9; border-left-color: #764ba2; } /* Title styling */ .paper-title { color: #1e293b; font-size: 18px; font-weight: 600; margin-bottom: 8px; line-height: 1.4; } /* Authors styling */ .paper-authors { color: #64748b; font-size: 14px; margin-bottom: 12px; font-style: italic; } /* Abstract styling */ .paper-abstract { color: #475569; font-size: 14px; line-height: 1.6; margin: 12px 0; padding: 12px; background: white; border-radius: 8px; border-left: 3px solid #e2e8f0; } /* Badge styling */ .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; margin-right: 8px; margin-bottom: 8px; } .badge-primary { background: #e0e7ff; color: #3730a3; } .badge-secondary { background: #f1f5f9; color: #475569; } .badge-success { background: #dcfce7; color: #166534; } /* Button styling */ .stButton > button { border-radius: 12px; padding: 10px 24px; font-weight: 500; transition: all 0.3s ease; } .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); } /* Header styling */ .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; border-radius: 0 0 24px 24px; margin-bottom: 32px; } /* Metric cards */ .metric-card { background: white; border-radius: 16px; padding: 20px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05); text-align: center; border: 1px solid #f1f5f9; } .metric-value { font-size: 32px; font-weight: 700; color: #1e293b; margin: 8px 0; } .metric-label { font-size: 14px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; } /* Search input */ .stTextInput > div > div > input { border-radius: 12px; border: 2px solid #e2e8f0; padding: 12px 16px; font-size: 14px; } .stTextInput > div > div > input:focus { border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); } /* Selectbox styling */ .stSelectbox > div > div > div { border-radius: 12px; border: 2px solid #e2e8f0; } /* Expander styling */ .streamlit-expanderHeader { border-radius: 12px; background: #f8fafc; border: 1px solid #e2e8f0; font-weight: 600; } /* Loading spinner */ .stSpinner > div { border-top-color: #667eea !important; } </style>
""", unsafe_allow_html=True)

==================== HEADER ====================
st.markdown("""

<div class="main-header"> <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px;"> <h1 style="margin: 0; font-size: 42px; font-weight: 700; line-height: 1.2;">📈 Finance Research Hub</h1> <p style="margin: 12px 0 0 0; font-size: 18px; opacity: 0.9; font-weight: 400;"> Discover, classify, and explore cutting-edge finance research papers </p> </div> </div> """, unsafe_allow_html=True)
==================== BILINGUAL KEYWORD DATABASE (ENGLISH + CHINESE) ====================
FINANCE_KEYWORD_DATABASE = {
"Computational Finance": {
"keywords": [
# English keywords
"deep learning", "neural networks", "machine learning", "AI", "artificial intelligence",
"gradient descent", "backpropagation", "convolutional", "recurrent", "transformer",
"PDE", "partial differential equation", "numerical methods", "finite difference", "finite element",
"Monte Carlo", "simulation", "stochastic", "high-dimensional", "computational",
"algorithm", "optimization", "parallel computing", "GPU", "CUDA",
"quantum computing", "quantum algorithms", "VQE", "quantum annealing",
"reinforcement learning", "Q-learning", "deep Q-network", "policy gradient",
"time series forecasting", "sequence models", "LSTM", "GRU", "attention",
# Chinese keywords
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
        # English keywords
        "stochastic calculus", "Ito", "Stratonovich", "Brownian motion", "martingale",
        "partial differential equation", "PDE", "Black-Scholes", "option pricing", "risk-neutral",
        "measure theory", "probability", "stochastic processes", "Levy processes", "jump diffusion",
        "Malliavin calculus", "Heston model", "SABR", "local volatility", "stochastic volatility",
        "optimal stopping", "optimal control", "Hamilton-Jacobi-Bellman", "dynamic programming",
        "portfolio optimization", "Markowitz", "mean-variance", "efficient frontier",
        "interest rate models", "Vasicek", "CIR", "HJM", "LIBOR market model",
        # Chinese keywords
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
        # English keywords
        "portfolio optimization", "asset allocation", "diversification", "efficient frontier",
        "mean-variance", "Markowitz", "Black-Litterman", "risk parity", "minimum variance",
        "tactical asset allocation", "strategic asset allocation", "rebalancing", "turnover",
        "tracking error", "active share", "index tracking", "enhanced indexing",
        "factor investing", "smart beta", "risk factors", "style factors",
        "hedge funds", "mutual funds", "ETF", "exchange-traded funds", "fund management",
        "performance measurement", "Sharpe ratio", "Sortino ratio", "information ratio",
        # Chinese keywords
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
        # English keywords
        "value at risk", "VaR", "expected shortfall", "ES", "CVaR", "conditional value at risk",
        "stress testing", "scenario analysis", "backtesting", "historical simulation",
        "credit risk", "default risk", "counterparty risk", "credit value adjustment", "CVA",
        "market risk", "volatility risk", "interest rate risk", "currency risk",
        "liquidity risk", "funding liquidity", "market liquidity", "bid-ask spread",
        "operational risk", "model risk", "legal risk", "compliance risk",
        "systemic risk", "too big to fail", "contagion", "network risk",
        # Chinese keywords
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

"Pricing of Securities": {
    "keywords": [
        # English keywords
        "option pricing", "Black-Scholes", "binomial tree", "trinomial tree", "finite difference",
        "Monte Carlo pricing", "least squares Monte Carlo", "LSM", "American options",
        "exotic options", "barrier options", "Asian options", "lookback options", "digital options",
        "interest rate derivatives", "swaps", "swaptions", "caps", "floors",
        "credit derivatives", "CDS", "credit default swaps", "CDO", "collateralized debt obligations",
        "fixed income pricing", "bond pricing", "yield curve", "term structure", "duration",
        # Chinese keywords
        "期权定价", "布莱克-斯科尔斯", "二叉树", "三叉树", "有限差分",
        "蒙特卡洛定价", "最小二乘蒙特卡洛", "美式期权", "奇异期权",
        "障碍期权", "亚式期权", "回望期权", "数字期权", "利率衍生品",
        "互换", "互换期权", "利率上限", "利率下限", "信用衍生品",
        "信用违约互换", "担保债务凭证", "固定收益定价", "债券定价",
        "收益率曲线", "期限结构", "久期"
    ],
    "weight": 0.85,
    "color": "#ef4444",
    "icon": "💰"
},

"Financial Econometrics": {
    "keywords": [
        # English keywords
        "time series analysis", "ARIMA", "ARMA", "ARCH", "GARCH", "EGARCH", "TGARCH",
        "vector autoregression", "VAR", "cointegration", "error correction model", "ECM",
        "unit root tests", "Dickey-Fuller", "Phillips-Perron", "KPSS",
        "volatility modeling", "realized volatility", "high-frequency data", "microstructure noise",
        "panel data", "fixed effects", "random effects", "dynamic panel", "GMM",
        "event study", "abnormal returns", "cumulative abnormal returns", "CAR",
        # Chinese keywords
        "时间序列分析", "ARIMA", "ARMA", "ARCH", "GARCH", "EGARCH", "TGARCH",
        "向量自回归", "协整", "误差修正模型", "单位根检验",
        "迪基-富勒", "菲利普斯-佩龙", "KPSS检验", "波动率建模",
        "实现波动率", "高频数据", "微观结构噪声", "面板数据",
        "固定效应", "随机效应", "动态面板", "广义矩估计",
        "事件研究", "异常收益", "累计异常收益"
    ],
    "weight": 0.85,
    "color": "#06b6d4",
    "icon": "📈"
},

"Market Microstructure": {
    "keywords": [
        # English keywords
        "limit order book", "market orders", "limit orders", "order flow", "order imbalance",
        "bid-ask spread", "market depth", "liquidity", "illiquidity", "market impact",
        "price impact", "temporary impact", "permanent impact", "Kyle's lambda",
        "high-frequency trading", "algorithmic trading", "market making", "statistical arbitrage",
        "latency", "tick size", "minimum price variation", "decimalization",
        # Chinese keywords
        "限价订单簿", "市价订单", "限价订单", "订单流", "订单不平衡",
        "买卖价差", "市场深度", "流动性", "非流动性", "市场冲击",
        "价格冲击", "暂时冲击", "永久冲击", "凯尔Lambda",
        "高频交易", "算法交易", "做市", "统计套利",
        "延迟", "最小报价单位", "十进制化"
    ],
    "weight": 0.8,
    "color": "#f97316",
    "icon": "⚡"
},

"Green Finance": {
    "keywords": [
        # English keywords
        "green finance", "green bonds", "green loans", "green credit", "sustainable finance",
        "environmental finance", "eco-finance", "green investment", "ESG investment",
        "environmental, social and governance", "green banking", "green insurance",
        "green financial products", "green securities", "green transition finance",
        "low-carbon finance", "circular economy finance", "biodiversity finance",
        "natural capital", "green fintech", "sustainability-linked loans",
        "green mortgage", "energy efficiency finance", "pollution control finance",
        "sustainable investing", "responsible investing", "impact investing",
        # Chinese keywords
        "绿色金融", "绿色债券", "绿色贷款", "绿色信贷", "可持续金融",
        "环境金融", "生态金融", "绿色投资", "ESG投资", "环境社会治理",
        "绿色银行", "绿色保险", "绿色金融产品", "绿色证券", "绿色转型金融",
        "低碳金融", "循环经济金融", "生物多样性金融", "自然资本",
        "绿色金融科技", "可持续发展挂钩贷款", "绿色抵押贷款",
        "能效金融", "污染防治金融", "责任投资", "影响力投资"
    ],
    "weight": 0.85,
    "color": "#22c55e",
    "icon": "🌿"
},

"Climate Finance": {
    "keywords": [
        # English keywords
        "climate finance", "climate change finance", "climate risk finance", "climate adaptation finance",
        "climate mitigation finance", "carbon pricing", "carbon markets", "emissions trading",
        "carbon credits", "carbon offsets", "clean development mechanism", "CDM",
        "climate bonds", "climate funds", "green climate fund", "GCF",
        "adaptation finance", "mitigation finance", "climate resilient finance",
        "transition finance", "decarbonization finance", "net-zero finance",
        "carbon tax", "climate policy", "Paris Agreement finance",
        "loss and damage finance", "climate vulnerability", "extreme weather finance",
        "sea level rise finance", "climate-smart finance", "carbon border adjustment",
        # Chinese keywords
        "气候金融", "气候变化金融", "气候风险金融", "气候适应金融",
        "气候减缓金融", "碳定价", "碳市场", "碳排放交易",
        "碳信用", "碳抵消", "清洁发展机制", "气候债券",
        "气候基金", "绿色气候基金", "适应融资", "减缓融资",
        "气候韧性金融", "转型金融", "脱碳金融", "净零金融",
        "碳税", "气候政策", "巴黎协定融资", "损失损害融资",
        "气候脆弱性", "极端天气金融", "海平面上升金融"
    ],
    "weight": 0.85,
    "color": "#0ea5e9",
    "icon": "🌍"
},

"Sustainable Finance": {
    "keywords": [
        # English keywords
        "ESG", "environmental social governance", "sustainable investing", "responsible investing",
        "green bonds", "climate bonds", "sustainability-linked bonds", "social bonds",
        "sustainable development goals", "SDG finance", "social finance", "impact bonds",
        "ethical investing", "sustainability reporting", "ESG integration", "ESG metrics",
        "sustainability performance", "corporate sustainability", "ESG disclosure",
        "sustainable banking", "ESG rating", "sustainability accounting",
        # Chinese keywords
        "ESG", "环境社会治理", "可持续投资", "责任投资", "社会责任投资",
        "绿色债券", "气候债券", "可持续发展挂钩债券", "社会债券",
        "可持续发展目标", "SDG融资", "社会金融", "影响力债券",
        "伦理投资", "可持续发展报告", "ESG整合", "ESG指标",
        "可持续发展绩效", "企业可持续发展", "ESG信息披露",
        "可持续银行", "ESG评级", "可持续发展会计"
    ],
    "weight": 0.8,
    "color": "#10b981",
    "icon": "🌱"
},

"FinTech & Blockchain": {
    "keywords": [
        # English keywords
        "blockchain", "distributed ledger", "smart contracts", "Ethereum", "solidity",
        "cryptocurrency", "Bitcoin", "Ethereum", "DeFi", "decentralized finance",
        "stablecoins", "CBDC", "central bank digital currency", "digital currency",
        "tokenization", "NFT", "non-fungible tokens", "security tokens",
        "crypto exchanges", "crypto wallets", "hot wallet", "cold wallet",
        "digital assets", "crypto lending", "yield farming", "liquidity mining",
        "web3", "metaverse finance", "DAO", "decentralized autonomous organization",
        # Chinese keywords
        "区块链", "分布式账本", "智能合约", "以太坊", "加密货币",
        "比特币", "去中心化金融", "稳定币", "央行数字货币",
        "数字货币", "代币化", "非同质化代币", "证券型代币",
        "加密货币交易所", "加密货币钱包", "热钱包", "冷钱包",
        "数字资产", "加密借贷", "收益 farming", "流动性挖矿",
        "Web3", "元宇宙金融", "去中心化自治组织"
    ],
    "weight": 0.8,
    "color": "#6366f1",
    "icon": "🔗"
},

"Banking & Financial Institutions": {
    "keywords": [
        # English keywords
        "commercial banks", "investment banks", "central banks", "bank regulation", "Basel",
        "capital adequacy", "liquidity coverage ratio", "LCR", "net stable funding ratio", "NSFR",
        "bank lending", "credit creation", "interbank market", "bank runs", "deposit insurance",
        "shadow banking", "financial intermediation", "bank profitability", "non-performing loans",
        "financial stability", "systemically important banks", "too big to fail", "bank consolidation",
        "bank governance", "corporate governance", "risk management", "compliance",
        # Chinese keywords
        "商业银行", "投资银行", "中央银行", "银行监管", "巴塞尔协议",
        "资本充足率", "流动性覆盖率", "净稳定资金比例", "银行信贷",
        "信用创造", "银行间市场", "银行挤兑", "存款保险", "影子银行",
        "金融中介", "银行盈利能力", "不良贷款", "金融稳定",
        "系统重要性银行", "太大而不能倒", "银行合并", "银行治理",
        "公司治理", "风险管理", "合规"
    ],
    "weight": 0.85,
    "color": "#8b4513",
    "icon": "🏦"
},

"Corporate Finance": {
    "keywords": [
        # English keywords
        "capital structure", "Modigliani-Miller", "dividend policy", "payout policy", "share repurchase",
        "mergers and acquisitions", "M&A", "takeovers", "corporate governance", "board of directors",
        "agency theory", "principal-agent problem", "executive compensation", "CEO pay",
        "corporate investment", "capital budgeting", "NPV", "internal rate of return", "IRR",
        "working capital management", "cash management", "inventory management", "accounts receivable",
        "financial distress", "bankruptcy", "restructuring", "turnaround management",
        "corporate valuation", "DCF", "discounted cash flow", "enterprise value",
        # Chinese keywords
        "资本结构", "莫迪利亚尼-米勒", "股利政策", "派息政策", "股票回购",
        "兼并与收购", "并购", "接管", "公司治理", "董事会",
        "代理理论", "委托代理问题", "高管薪酬", "首席执行官薪酬",
        "公司投资", "资本预算", "净现值", "内部收益率",
        "营运资本管理", "现金管理", "存货管理", "应收账款",
        "财务困境", "破产", "重组", "扭亏管理", "公司估值",
        "折现现金流", "企业价值"
    ],
    "weight": 0.8,
    "color": "#4169e1",
    "icon": "🏢"
},

"Behavioral Finance": {
    "keywords": [
        # English keywords
        "behavioral finance", "cognitive biases", "overconfidence", "loss aversion", "herding behavior",
        "prospect theory", "mental accounting", "anchoring", "framing effect", "disposition effect",
        "market anomalies", "calendar effects", "momentum", "value effect", "size effect",
        "investor sentiment", "noise trading", "limits to arbitrage", "bubbles", "crashes",
        "emotions in finance", "psychology of investing", "neurofinance", "experimental finance",
        # Chinese keywords
        "行为金融", "认知偏差", "过度自信", "损失厌恶", "羊群行为",
        "前景理论", "心理账户", "锚定效应", "框架效应", "处置效应",
        "市场异象", "日历效应", "动量效应", "价值效应", "规模效应",
        "投资者情绪", "噪声交易", "套利限制", "泡沫", "崩盘",
        "金融情绪", "投资心理学", "神经金融", "实验金融"
    ],
    "weight": 0.8,
    "color": "#ec4899",
    "icon": "🧠"
}
==================== UTILITY FUNCTIONS ====================
def extract_keywords(text):
"""Extract meaningful keywords from text"""
if not text:
return []
# Handle both English and Chinese
text = text.lower()
# Remove special characters but keep Chinese characters
text = re.sub(r'[^\w\s\u4e00-\u9fff\-\.]', ' ', text)
words = text.split()

# English stopwords
stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
keywords = [word for word in words if len(word) > 1 and word not in stopwords]

return keywords
def enhanced_classify_with_confidence(text, top_k=5):
"""Enhanced classification function with keyword-based scoring (bilingual support)"""
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
    # Default categories if no match found
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
"""Enhanced classification specifically for CNKI papers with Chinese keyword detection"""
text = f"{title} {' '.join(keywords)} {category_code}"
# Special rules for Chinese finance papers
chinese_keyword_mapping = {
    # Green Finance keywords in Chinese
    "绿色金融": "Green Finance",
    "绿色债券": "Green Finance",
    "绿色信贷": "Green Finance",
    "绿色投资": "Green Finance",
    "ESG": "Green Finance",
    "环境社会治理": "Green Finance",
    
    # Climate Finance keywords in Chinese
    "气候金融": "Climate Finance",
    "碳金融": "Climate Finance",
    "碳交易": "Climate Finance",
    "碳市场": "Climate Finance",
    "碳排放": "Climate Finance",
    "碳中和": "Climate Finance",
    
    # Banking keywords in Chinese
    "商业银行": "Banking & Financial Institutions",
    "银行": "Banking & Financial Institutions",
    "银行业": "Banking & Financial Institutions",
    "金融科技": "FinTech & Blockchain",
    "数字货币": "FinTech & Blockchain",
    "区块链": "FinTech & Blockchain",
    
    # Risk Management keywords in Chinese
    "风险管理": "Risk Management",
    "风险": "Risk Management",
    "信用风险": "Risk Management",
    
    # Portfolio Management keywords in Chinese
    "投资组合": "Portfolio Management",
    "资产配置": "Portfolio Management",
    
    # Mathematical Finance keywords in Chinese
    "金融工程": "Mathematical Finance",
    "量化金融": "Mathematical Finance",
    "金融数学": "Mathematical Finance",
}

# Check for specific Chinese keywords first
for chinese_keyword, category in chinese_keyword_mapping.items():
    if chinese_keyword in text:
        return category

# Fall back to general keyword matching
categories = calculate_category_scores(text, top_k=1)
if categories:
    return categories[0][0]

return "General Finance"
def load_excel_data(file_path):
"""Load and process Excel data from CNKI export with enhanced Chinese classification"""
try:
# Read the Excel file
df = pd.read_excel(file_path, sheet_name=None)
    all_papers = []
    
    # Process each sheet
    for sheet_name, sheet_df in df.items():
        # Standardize column names
        sheet_df.columns = sheet_df.columns.str.strip()
        
        # Check which type of data we have
        if 'Title-题名' in sheet_df.columns and 'Author-作者' in sheet_df.columns:
            # Journal/Conference papers format
            for idx, row in sheet_df.iterrows():
                # Skip empty rows
                if pd.isna(row.get('Title-题名')):
                    continue
                
                # Process authors
                authors_str = str(row.get('Author-作者', ''))
                authors = [author.strip() for author in authors_str.split(',') if author.strip()]
                
                # Process keywords
                keywords_str = str(row.get('关键词', ''))
                keywords = [kw.strip() for kw in keywords_str.split(';;') if kw.strip()]
                
                # Create paper object
                paper = {
                    'title': str(row.get('Title-题名', '')),
                    'authors': authors,
                    'source': str(row.get('Source-文献来源', row.get('Source-报纸名', ''))),
                    'year': int(row.get('Year-年', row.get('Year-学位年度', 2024))) if not pd.isna(row.get('Year-年', row.get('Year-学位年度', pd.NaT))) else 2024,
                    'keywords': keywords,
                    'category_code': str(row.get('中图分类号', '')),
                    'type': 'journal' if 'Source-文献来源' in row else 'newspaper',
                    'abstract': '',  # CNKI exports don't usually include abstracts
                    'arxiv_id': f"CNKI_{sheet_name}_{idx}",
                    'arxiv_url': '',
                    'pdf_url': '',
                    'word_count': len(str(row.get('Title-题名', '')).split()) * 20,  # Estimate for Chinese
                    'published': f"{row.get('Year-年', 2024)}-01-01" if pd.notna(row.get('Year-年', pd.NaT)) else '2024-01-01'
                }
                
                # Enhanced classification for Chinese papers
                paper['category'] = enhanced_classification_for_cnki(
                    paper['title'],
                    paper['keywords'],
                    paper['category_code']
                )
                
                # Add publication details for journals
                if paper['type'] == 'journal':
                    paper['volume'] = str(row.get('Roll-卷', '')) if pd.notna(row.get('Roll-卷', '')) else ''
                    paper['issue'] = str(row.get('Period-期', '')) if pd.notna(row.get('Period-期', '')) else ''
                    paper['pages'] = str(row.get('PageCount-页码', row.get('Page-页码', ''))) if pd.notna(row.get('PageCount-页码', row.get('Page-页码', pd.NaT))) else ''
                
                # Add publication date for newspapers
                elif paper['type'] == 'newspaper':
                    paper['pub_date'] = str(row.get('PubTime-出版日期', '')) if pd.notna(row.get('PubTime-出版日期', pd.NaT)) else ''
                    paper['edition'] = str(row.get('Edition-版次', '')) if pd.notna(row.get('Edition-版次', '')) else ''
                
                # Generate abstract if missing
                if not paper.get('abstract', '') and paper['keywords']:
                    paper['abstract'] = f"研究主题: {', '.join(paper['keywords'][:5])}. 发表于{paper['source']} ({paper['year']})."
                
                all_papers.append(paper)
        
        elif '导师' in sheet_df.columns:
            # Thesis format
            for idx, row in sheet_df.iterrows():
                if pd.isna(row.get('Title-文献题名')):
                    continue
                
                # Process keywords
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
                    'word_count': len(str(row.get('Title-文献题名', '')).split()) * 80,  # Thesis estimate
                    'published': f"{row.get('Year-学位年度', 2024)}-01-01" if pd.notna(row.get('Year-学位年度')) else '2024-01-01',
                    'advisor': str(row.get('导师', ''))
                }
                
                # Enhanced classification for Chinese papers
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
==================== LOAD RESEARCH PAPERS ====================
@st.cache_data
def load_research_papers():
"""Load research papers from both JSON and Excel sources"""
all_papers = []
# Try to load from JSON file first
try:
    with open('research_papers.json', 'r', encoding='utf-8') as f:
        json_papers = json.load(f)
        all_papers.extend(json_papers)
except FileNotFoundError:
    st.info("No research_papers.json file found. Using Excel data only.")
except Exception as e:
    st.warning(f"Could not load JSON file: {e}")

# Try to load from Excel file
try:
    excel_papers = load_excel_data('CNKI-20260104152201560.xls')
    all_papers.extend(excel_papers)
except FileNotFoundError:
    st.info("No Excel file found. Using existing data only.")
except Exception as e:
    st.warning(f"Could not load Excel file: {e}")

if not all_papers:
    st.error("No research papers loaded. Please ensure you have either research_papers.json or CNKI Excel file.")
    return pd.DataFrame(), []

# Convert to DataFrame
papers_df = pd.DataFrame(all_papers)

# Process dates
if 'published' in papers_df.columns:
    papers_df['published_date'] = pd.to_datetime(papers_df['published'], errors='coerce')
    papers_df['date_display'] = papers_df['published_date'].dt.strftime('%b %d, %Y')

# Ensure year column exists
if 'year' not in papers_df.columns and 'published_date' in papers_df.columns:
    papers_df['year'] = papers_df['published_date'].dt.year.fillna(2024)

# Assign colors for display - updated with new categories
category_colors = {
    'Computational Finance': '#667eea',
    'Mathematical Finance': '#f59e0b',
    'Portfolio Management': '#10b981',
    'Risk Management': '#8b5cf6',
    'Pricing of Securities': '#ef4444',
    'Financial Econometrics': '#06b6d4',
    'Market Microstructure': '#f97316',
    'Green Finance': '#22c55e',
    'Climate Finance': '#0ea5e9',
    'Sustainable Finance': '#10b981',
    'FinTech & Blockchain': '#6366f1',
    'Banking & Financial Institutions': '#8b4513',
    'Corporate Finance': '#4169e1',
    'Behavioral Finance': '#ec4899',
    'General Finance': '#764ba2',
    'Unknown': '#94a3b8'
}

papers_df['category_color'] = papers_df['category'].map(category_colors).fillna('#94a3b8')

return papers_df, all_papers
papers_df, papers_list = load_research_papers()

==================== RESEARCH LIBRARY ====================
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

# Statistics with Chinese papers count
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
    
    col_sort, col_source = st.columns(2)
    with col_sort:
        sort_by = st.selectbox(
            "Sort by", 
            ["Newest First", "Oldest First", "Title (A-Z)", "Title (Z-A)", "Category"],
            key="sort_filter"
        )
    
    with col_source:
        source_filter = st.multiselect(
            "Filter by Source",
            options=sorted(papers_df['source'].dropna().unique().tolist()) if 'source' in papers_df.columns else [],
            default=[],
            help="Select specific journals/sources"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Apply filters
filtered_df = papers_df.copy()

if not papers_df.empty:
    if search_query:
        mask = (
            filtered_df['title'].str.contains(search_query, case=False, na=False) |
            filtered_df['abstract'].str.contains(search_query, case=False, na=False) |
            filtered_df['authors'].apply(lambda x: search_query.lower() in str(x).lower() if x else False) |
            filtered_df['keywords'].apply(lambda x: search_query.lower() in str(x).lower() if x else False)
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
    
    if source_filter:
        filtered_df = filtered_df[filtered_df['source'].isin(source_filter)]
    
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
    elif sort_by == "Category":
        filtered_df = filtered_df.sort_values('category')

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
    # Category distribution for filtered results
    if 'category' in filtered_df.columns:
        category_counts = filtered_df['category'].value_counts()
        if len(category_counts) > 0:
            st.markdown("""
            <div style="margin: 20px 0; padding: 16px; background: #f8fafc; border-radius: 12px;">
                <div style="font-size: 14px; color: #64748b; margin-bottom: 8px;">📊 Category Distribution in Results</div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            """, unsafe_allow_html=True)
            
            for category, count in category_counts.head(8).items():
                color = filtered_df[filtered_df['category'] == category]['category_color'].iloc[0] if not filtered_df[filtered_df['category'] == category].empty else '#667eea'
                st.markdown(f"""
                <span style="background: {color}20; color: {color}; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 500; display: inline-block; margin: 2px;">
                    {category}: {count}
                </span>
                """, unsafe_allow_html=True)
            
            if len(category_counts) > 8:
                st.markdown(f"""
                <span style="background: #e2e8f0; color: #64748b; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 500; display: inline-block; margin: 2px;">
                    +{len(category_counts) - 8} more
                </span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 32px 0 16px 0;">
        <div>
            <h3 style="color: #1e293b; font-size: 20px; font-weight: 600; margin: 0;">
                📄 Found {len(filtered_df)} papers
            </h3>
            <p style="color: #64748b; font-size: 14px; margin: 4px 0 0 0;">
                Showing papers from {filtered_df['year'].min() if 'year' in filtered_df.columns else 'N/A'} to {filtered_df['year'].max() if 'year' in filtered_df.columns else 'N/A'}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display each paper
    for idx, paper in filtered_df.iterrows():
        # Determine paper type badge with Chinese indicator
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
        elif paper_type == 'uploaded':
            paper_type_badge += '<span class="badge badge-secondary">📤 Uploaded</span>'
        else:
            paper_type_badge += '<span class="badge badge-secondary">📄 Paper</span>'
        
        # Format keywords display
        keywords_html = ""
        if paper.get('keywords'):
            keywords_list = paper['keywords'][:5] if isinstance(paper['keywords'], list) else str(paper['keywords']).split(',')[:5]
            keywords_html = f"""
            <div style="margin: 8px 0;">
                <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">🏷️ Keywords:</div>
                <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                    {''.join([f'<span style="background: #e2e8f0; color: #475569; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{kw}</span>' for kw in keywords_list])}
                </div>
            </div>
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
                <span class="badge badge-secondary">
                    📝 ~{paper.get('word_count', 0)} words
                </span>
            </div>
            
            {keywords_html}
            
            <div class="paper-abstract">
                <div style="font-weight: 600; color: #475569; margin-bottom: 8px; font-size: 13px;">
                    ABSTRACT / DESCRIPTION
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
                    🤖 Re-classify
                </button>
                
                <button onclick="showPaperDetails('{paper.get('title', '').replace("'", "\\'")}', '{paper.get('category', '').replace("'", "\\'")}', '{paper.get('source', '').replace("'", "\\'")}')" style="
                    background: #e0e7ff;
                    color: #3730a3;
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
                " onmouseover="this.style.background='#c7d2fe'; this.style.transform='translateY(-1px)'"
                onmouseout="this.style.background='#e0e7ff'; this.style.transform='translateY(0)'">
                    ℹ️ Details
                </button>
            </div>
        </div>
        """
        
        st.markdown(paper_html, unsafe_allow_html=True)
==================== ENHANCED CLASSIFIER WITH BILINGUAL SUPPORT ====================
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
                🤖 AI Classification Results
            </h3>
            <p style="margin: 0; color: #64748b; font-size: 14px;">
                Based on keyword analysis of title and abstract (Supports English & Chinese)
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
                    <div style="display: flex; flex-wrap: wrap; gap: 6px; max-height: 100px; overflow-y: auto; padding: 4px;">
                        {''.join([f'<span style="background: {top_category["color"]}20; color: {top_category["color"]}; padding: 4px 10px; border-radius: 16px; font-size: 12px; font-weight: 500; margin: 2px;">{kw}</span>' for kw in top_category["matched_keywords"][:10]])}
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
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span>Algorithm:</span>
                        <span style="font-weight: 600;">Bilingual Keyword-based</span>
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

# All categories
st.markdown("### 📊 All Category Scores")
cols = st.columns(min(len(top_results), 5))
for idx, (col, result) in enumerate(zip(cols, top_results)):
    with col:
        st.markdown(f"""
        <div style="background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; text-align: center; height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
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
==================== STATISTICS DASHBOARD ====================
def display_statistics():
"""Display statistics dashboard with bilingual insights"""
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

# Quick stats with bilingual breakdown
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
    if 'source' in papers_df.columns:
        unique_sources = papers_df['source'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{unique_sources}</div>
            <div class="metric-label">Sources</div>
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
        
        # Get colors for each category
        colors = []
        for category in category_counts['Category']:
            colors.append(FINANCE_KEYWORD_DATABASE.get(category, {}).get('color', '#94a3b8'))
        
        fig = go.Figure(data=[go.Pie(
            labels=category_counts['Category'],
            values=category_counts['Count'],
            hole=.4,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='outside',
            hoverinfo='label+value+percent',
            hovertemplate='<b>%{label}</b><br>Papers: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show top categories
        top_categories = category_counts.head(5)
        st.markdown("""
        <div style="margin-top: 20px; padding: 16px; background: #f8fafc; border-radius: 12px;">
            <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">🏆 Top 5 Categories</div>
        """, unsafe_allow_html=True)
        
        for idx, row in top_categories.iterrows():
            color = FINANCE_KEYWORD_DATABASE.get(row['Category'], {}).get('color', '#94a3b8')
            percentage = (row['Count'] / len(papers_df)) * 100
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {color};"></div>
                    <span style="font-size: 14px; color: #475569;">{row['Category']}</span>
                </div>
                <div>
                    <span style="font-weight: 600; font-size: 14px; color: #1e293b;">{row['Count']}</span>
                    <span style="font-size: 12px; color: #64748b; margin-left: 4px;">({percentage:.1f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown("""
    <div class="card" style="margin-top: 24px;">
        <h3 style="color: #1e293b; font-size: 18px; font-weight: 600; margin-bottom: 20px;">
            📅 Publication Trend by Language
        </h3>
    """, unsafe_allow_html=True)
    
    if 'year' in papers_df.columns and 'arxiv_id' in papers_df.columns:
        # Add language column
        papers_df['language'] = papers_df['arxiv_id'].apply(
            lambda x: 'Chinese' if str(x).startswith(('CNKI', 'THESIS')) else 'English'
        )
        
        # Group by year and language
        yearly_counts = papers_df.groupby(['year', 'language']).size().reset_index(name='Count')
        
        fig = go.Figure()
        
        # Add traces for each language
        colors = {'Chinese': '#ef4444', 'English': '#10b981'}
        
        for language in ['Chinese', 'English']:
            language_data = yearly_counts[yearly_counts['language'] == language]
            if not language_data.empty:
                fig.add_trace(go.Bar(
                    x=language_data['year'],
                    y=language_data['Count'],
                    name=language,
                    marker_color=colors[language],
                    opacity=0.8,
                    hovertemplate='<b>%{x}</b><br>%{y} ' + language + ' papers<extra></extra>'
                ))
        
        fig.update_layout(
            height=400,
            xaxis_title="Year",
            yaxis_title="Number of Papers",
            hovermode='x unified',
            barmode='stack',
            margin=dict(t=30, b=50, l=50, r=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Language distribution
        language_dist = papers_df['language'].value_counts()
        st.markdown("""
        <div style="margin-top: 20px; padding: 16px; background: #f8fafc; border-radius: 12px;">
            <div style="font-size: 14px; color: #64748b; margin-bottom: 12px;">🌐 Language Distribution</div>
        """, unsafe_allow_html=True)
        
        total = len(papers_df)
        for language, count in language_dist.items():
            percentage = (count / total) * 100
            color = colors.get(language, '#94a3b8')
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {color};"></div>
                    <span style="font-size: 14px; color: #475569;">{language} Papers</span>
                </div>
                <div>
                    <span style="font-weight: 600; font-size: 14px; color: #1e293b;">{count}</span>
                    <span style="font-size: 12px; color: #64748b; margin-left: 4px;">({percentage:.1f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
==================== SIDEBAR ====================
st.sidebar.markdown("""

<div style="padding: 20px 0;"> <div style="text-align: center; margin-bottom: 32px;"> <div style="font-size: 32px; margin-bottom: 8px;">📈</div> <div style="font-size: 18px; font-weight: 600; color: #1e293b;">Finance Research Hub</div> <div style="font-size: 12px; color: #64748b; margin-top: 4px;">v4.0 • Bilingual Edition</div> </div> </div> """, unsafe_allow_html=True)
Navigation
st.sidebar.header("🧭 Navigation")
app_mode = st.sidebar.radio(
"",
["📚 Research Library", "🤖 Enhanced Classifier", "📊 Analytics"],
help="Switch between different features",
label_visibility="collapsed"
)

Quick actions
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

Import Data Section
st.sidebar.markdown("---")
st.sidebar.header("📤 Import Data")

uploaded_file = st.sidebar.file_uploader(
"Upload Excel/CSV file",
type=['xls', 'xlsx', 'csv'],
help="Upload CNKI export files or custom research data"
)

if uploaded_file is not None:
try:
# Save uploaded file temporarily
with open(f"temp_{uploaded_file.name}", "wb") as f:
f.write(uploaded_file.getbuffer())
    # Load the uploaded file
    if uploaded_file.name.endswith(('.xls', '.xlsx')):
        uploaded_papers = load_excel_data(f"temp_{uploaded_file.name}")
    else:  # CSV
        df = pd.read_csv(uploaded_file)
        # Convert CSV to paper format
        uploaded_papers = []
        for idx, row in df.iterrows():
            paper = {
                'title': str(row.get('Title', row.get('Title-题名', ''))),
                'authors': str(row.get('Authors', row.get('Author-作者', ''))).split(','),
                'source': str(row.get('Source', row.get('Source-文献来源', ''))),
                'year': int(row.get('Year', row.get('Year-年', 2024))) if pd.notna(row.get('Year', row.get('Year-年', pd.NaT))) else 2024,
                'abstract': str(row.get('Abstract', row.get('摘要', ''))),
                'keywords': str(row.get('Keywords', row.get('关键词', ''))).split(';'),
                'type': 'uploaded'
            }
            uploaded_papers.append(paper)
    
    if uploaded_papers:
        st.sidebar.success(f"✅ Successfully loaded {len(uploaded_papers)} papers from {uploaded_file.name}")
        
        # Option to add to existing data
        if st.sidebar.button("Add to Library", use_container_width=True):
            # Reload function to clear cache
            st.cache_data.clear()
            st.rerun()
except Exception as e:
    st.sidebar.error(f"Error loading file: {e}")
Info section
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ System Info")

if not papers_df.empty:
# Latest paper info
latest_paper = papers_df.sort_values('published_date', ascending=False).iloc[0]
paper_language = "🇨🇳 Chinese" if str(latest_paper.get('arxiv_id', '')).startswith(('CNKI', 'THESIS')) else "🇺🇸 English"
st.sidebar.markdown(f"""
<div style="background: #f8fafc; padding: 16px; border-radius: 12px; border-left: 4px solid #667eea; margin-bottom: 16px;">
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
Database info
total_categories = len(FINANCE_KEYWORD_DATABASE)
total_keywords = sum(len(data['keywords']) for data in FINANCE_KEYWORD_DATABASE.values())

st.sidebar.markdown(f"""

<div style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-top: 16px;"> <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">📊 Database Statistics</div> <div style="font-size: 12px; color: #475569;"> <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"> <span>Finance Categories:</span> <span style="font-weight: 600;">{total_categories}</span> </div> <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"> <span>Total Keywords:</span> <span style="font-weight: 600;">{total_keywords}</span> </div> <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"> <span>Language Support:</span> <span style="font-weight: 600;">Bilingual</span> </div> <div style="display: flex; justify-content: space-between;"> <span>New Categories:</span> <span style="font-weight: 600; color: #22c55e;">Green/Climate</span> </div> </div> </div> """, unsafe_allow_html=True)
Categories quick view
st.sidebar.markdown("""

<div style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-top: 16px;"> <div style="font-size: 13px; color: #64748b; margin-bottom: 8px;">🏷️ Quick Categories</div> <div style="display: flex; flex-wrap: wrap; gap: 4px;"> <span style="background: #22c55e20; color: #22c55e; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 500;">🌿 Green</span> <span style="background: #0ea5e920; color: #0ea5e9; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 500;">🌍 Climate</span> <span style="background: #667eea20; color: #667eea; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 500;">💻 Comp</span> <span style="background: #f59e0b20; color: #f59e0b; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 500;">📐 Math</span> <span style="background: #8b5cf620; color: #8b5cf6; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 500;">⚠️ Risk</span> <span style="background: #6366f120; color: #6366f1; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 500;">🔗 FinTech</span> </div> </div> """, unsafe_allow_html=True)
==================== MAIN APP ROUTING ====================
if app_mode == "📚 Research Library":
display_research_library()

elif app_mode == "🤖 Enhanced Classifier":
display_enhanced_classifier()

elif app_mode == "📊 Analytics":
display_statistics()

==================== FOOTER ====================
st.markdown("""

<div style="margin-top: 64px; padding: 32px 0; text-align: center; color: #94a3b8; border-top: 1px solid #e2e8f0;"> <div style="font-size: 14px; margin-bottom: 8px;"> Finance Research Hub • v4.0 • Bilingual Edition • Made with ❤️ for researchers </div> <div style="font-size: 12px; color: #64748b; margin-bottom: 16px;"> Supports English & Chinese papers • {len(FINANCE_KEYWORD_DATABASE)} finance categories • Advanced classification </div> <div style="display: flex; justify-content: center; gap: 24px; margin-top: 16px;"> <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">📚 Documentation</a> <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">🐙 GitHub</a> <a href="#" style="color: #64748b; text-decoration: none; font-size: 13px;">📧 Contact</a> </div> </div> """, unsafe_allow_html=True)
Add JavaScript for classification and paper details
st.markdown("""

<script> function classifyPaper(title, abstract) { // Create notification const notification = document.createElement('div'); notification.innerHTML = ` <div style=" position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px 24px; border-radius: 12px; box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3); z-index: 9999; display: flex; align-items: center; gap: 16px; animation: slideIn 0.3s ease; max-width: 400px; "> <div style="font-size: 24px;">🤖</div> <div style="flex: 1;"> <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">Classification Started</div> <div style="font-size: 12px; opacity: 0.9; line-height: 1.4;"> Redirecting to classifier with paper:<br> <strong>${title.substring(0, 50)}...</strong> </div> </div> </div> `; document.body.appendChild(notification); // Store paper info in localStorage localStorage.setItem('paper_to_classify', JSON.stringify({ title: title, abstract: abstract, timestamp: new Date().toISOString() })); // Switch to classifier tab const event = new CustomEvent('switchToClassifier', { detail: { title: title, abstract: abstract } }); window.dispatchEvent(event); setTimeout(() => { notification.style.animation = 'slideOut 0.3s ease'; setTimeout(() => notification.remove(), 300); }, 3000); } function showPaperDetails(title, category, source) { const notification = document.createElement('div'); notification.innerHTML = ` <div style=" position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 16px 24px; border-radius: 12px; box-shadow: 0 8px 30px rgba(16, 185, 129, 0.3); z-index: 9999; display: flex; align-items: center; gap: 16px; animation: slideIn 0.3s ease; max-width: 400px; "> <div style="font-size: 24px;">📄</div> <div style="flex: 1;"> <div style="font-weight: 600; font-size: 14px; margin-bottom: 4px;">Paper Details</div> <div style="font-size: 12px; opacity: 0.9; line-height: 1.4;"> <strong>${title.substring(0, 40)}...</strong><br> Category: ${category}<br> Source: ${source} </div> </div> </div> `; document.body.appendChild(notification); setTimeout(() => { notification.style.animation = 'slideOut 0.3s ease'; setTimeout(() => notification.remove(), 300); }, 3000); } // Add animations const style = document.createElement('style'); style.innerHTML = ` @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } } @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } } `; document.head.appendChild(style); // Listen for classification events window.addEventListener('switchToClassifier', function(e) { // This would switch tabs in a real implementation console.log('Switching to classifier with:', e.detail); }); </script>
""", unsafe_allow_html=True)
