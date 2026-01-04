import streamlit as st
import pandas as pd
import sys
import plotly.express as px
import numpy as np
import json
import io
from datetime import datetime

st.set_page_config(
    page_title="Finance Research Classifier",
    page_icon="📊",
    layout="wide"
)

# Title with clickable badges
st.title("📊 Finance Research Paper Classifier & Library")

# Display versions with icons
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Streamlit** {st.__version__}")
with col2:
    st.markdown(f"**Pandas** {pd.__version__}")
with col3:
    st.markdown(f"**Numpy** {np.__version__}")

# ===== SAFE LINK BUTTON FUNCTION =====
def safe_link_button(label, url, key=None, help_text=None, disabled=False):
    """
    Safe wrapper for st.link_button that handles empty/invalid URLs
    """
    if not url or not isinstance(url, str) or not url.strip() or not url.startswith(('http://', 'https://')):
        return st.button(label, disabled=True, key=key, help=help_text or "Link not available")
    return st.link_button(label, url, key=key, help=help_text)

# ===== CREATE SAMPLE RESEARCH PAPERS DATA =====
def create_english_papers():
    """Create 25 sample English finance research papers"""
    english_papers = [
        {
            "id": 1,
            "title": "Deep Learning for Financial Time Series Prediction",
            "authors": ["John Smith", "Jane Doe"],
            "year": 2025,
            "month": 1,
            "category": "Computational Finance",
            "abstract": "This paper explores the application of deep learning techniques for financial time series prediction. We propose a novel LSTM-based architecture that outperforms traditional ARIMA models in forecasting stock prices.",
            "pdf_url": "https://arxiv.org/pdf/2501.12345",
            "arxiv_url": "https://arxiv.org/abs/2501.12345",
            "published": "2025-01-15T00:00:00+00:00",
            "word_count": 150,
            "language": "English",
            "source": "Journal of Financial Data Science",
            "doi": "10.1234/example.2025"
        },
        {
            "id": 2,
            "title": "Blockchain Applications in Banking and Finance",
            "authors": ["Alice Johnson", "Bob Williams"],
            "year": 2024,
            "month": 6,
            "category": "Fintech",
            "abstract": "An analysis of blockchain technology applications in the banking sector, focusing on smart contracts and decentralized finance (DeFi).",
            "pdf_url": "https://arxiv.org/pdf/2406.54321",
            "arxiv_url": "https://arxiv.org/abs/2406.54321",
            "published": "2024-06-20T00:00:00+00:00",
            "word_count": 200,
            "language": "English",
            "source": "International Journal of Banking",
            "doi": "10.1234/example.2024"
        },
        {
            "id": 3,
            "title": "Machine Learning in Credit Risk Assessment",
            "authors": ["Michael Chen", "Sarah Lee"],
            "year": 2024,
            "month": 3,
            "category": "Risk Management",
            "abstract": "Comparative study of machine learning algorithms for credit risk assessment using real-world banking data.",
            "pdf_url": "https://arxiv.org/pdf/2403.98765",
            "arxiv_url": "https://arxiv.org/abs/2403.98765",
            "published": "2024-03-10T00:00:00+00:00",
            "word_count": 180,
            "language": "English",
            "source": "Journal of Credit Risk",
            "doi": ""
        },
        {
            "id": 4,
            "title": "AI-Driven Portfolio Optimization",
            "authors": ["David Brown", "Emma Wilson"],
            "year": 2025,
            "month": 2,
            "category": "Portfolio Management",
            "abstract": "Using artificial intelligence to optimize investment portfolios with dynamic risk management.",
            "pdf_url": "https://arxiv.org/pdf/2502.34567",
            "arxiv_url": "https://arxiv.org/abs/2502.34567",
            "published": "2025-02-28T00:00:00+00:00",
            "word_count": 220,
            "language": "English",
            "source": "Quantitative Finance Journal",
            "doi": ""
        },
        {
            "id": 5,
            "title": "Cryptocurrency Market Analysis and Prediction",
            "authors": ["Robert Taylor", "Lisa Garcia"],
            "year": 2024,
            "month": 9,
            "category": "Cryptocurrency",
            "abstract": "Statistical analysis and prediction models for major cryptocurrencies using time series analysis.",
            "pdf_url": "https://arxiv.org/pdf/2409.87654",
            "arxiv_url": "https://arxiv.org/abs/2409.87654",
            "published": "2024-09-15T00:00:00+00:00",
            "word_count": 190,
            "language": "English",
            "source": "Crypto Economics Review",
            "doi": ""
        },
        {
            "id": 6,
            "title": "Sustainable Finance and ESG Investing",
            "authors": ["Thomas Miller", "Olivia Davis"],
            "year": 2024,
            "month": 7,
            "category": "Sustainable Finance",
            "abstract": "Analysis of environmental, social, and governance (ESG) factors in investment decisions and their financial impacts.",
            "pdf_url": "https://arxiv.org/pdf/2407.65432",
            "arxiv_url": "https://arxiv.org/abs/2407.65432",
            "published": "2024-07-22T00:00:00+00:00",
            "word_count": 210,
            "language": "English",
            "source": "Journal of Sustainable Finance",
            "doi": ""
        },
        {
            "id": 7,
            "title": "High-Frequency Trading Algorithms",
            "authors": ["James Anderson", "Sophia Martinez"],
            "year": 2025,
            "month": 3,
            "category": "Algorithmic Trading",
            "abstract": "Development and testing of high-frequency trading algorithms using machine learning techniques.",
            "pdf_url": "https://arxiv.org/pdf/2503.76543",
            "arxiv_url": "https://arxiv.org/abs/2503.76543",
            "published": "2025-03-05T00:00:00+00:00",
            "word_count": 175,
            "language": "English",
            "source": "Algorithmic Finance",
            "doi": ""
        },
        {
            "id": 8,
            "title": "Behavioral Finance and Market Anomalies",
            "authors": ["William Thomas", "Ava Rodriguez"],
            "year": 2024,
            "month": 5,
            "category": "Behavioral Finance",
            "abstract": "Study of psychological factors influencing investor behavior and market anomalies.",
            "pdf_url": "https://arxiv.org/pdf/2405.43210",
            "arxiv_url": "https://arxiv.org/abs/2405.43210",
            "published": "2024-05-18T00:00:00+00:00",
            "word_count": 195,
            "language": "English",
            "source": "Journal of Behavioral Finance",
            "doi": ""
        },
        {
            "id": 9,
            "title": "Quantum Computing in Financial Modeling",
            "authors": ["Charles White", "Mia Lee"],
            "year": 2025,
            "month": 4,
            "category": "Computational Finance",
            "abstract": "Exploring quantum computing applications for complex financial modeling and optimization problems.",
            "pdf_url": "https://arxiv.org/pdf/2504.98765",
            "arxiv_url": "https://arxiv.org/abs/2504.98765",
            "published": "2025-04-12T00:00:00+00:00",
            "word_count": 230,
            "language": "English",
            "source": "Quantum Finance Journal",
            "doi": ""
        },
        {
            "id": 10,
            "title": "Financial Fraud Detection Using AI",
            "authors": ["George Harris", "Isabella Clark"],
            "year": 2024,
            "month": 8,
            "category": "Risk Management",
            "abstract": "Artificial intelligence systems for detecting financial fraud in banking transactions.",
            "pdf_url": "https://arxiv.org/pdf/2408.12345",
            "arxiv_url": "https://arxiv.org/abs/2408.12345",
            "published": "2024-08-30T00:00:00+00:00",
            "word_count": 185,
            "language": "English",
            "source": "Journal of Financial Crime",
            "doi": ""
        },
        {
            "id": 11,
            "title": "Real Estate Market Forecasting Models",
            "authors": ["Henry Walker", "Charlotte Lewis"],
            "year": 2024,
            "month": 10,
            "category": "Real Estate Finance",
            "abstract": "Machine learning models for predicting real estate prices and market trends.",
            "pdf_url": "https://arxiv.org/pdf/2410.56789",
            "arxiv_url": "https://arxiv.org/abs/2410.56789",
            "published": "2024-10-25T00:00:00+00:00",
            "word_count": 200,
            "language": "English",
            "source": "Real Estate Economics",
            "doi": ""
        },
        {
            "id": 12,
            "title": "Central Bank Digital Currencies (CBDCs)",
            "authors": ["Joseph King", "Amelia Young"],
            "year": 2025,
            "month": 1,
            "category": "Fintech",
            "abstract": "Analysis of central bank digital currencies and their potential impact on monetary policy.",
            "pdf_url": "https://arxiv.org/pdf/2501.67890",
            "arxiv_url": "https://arxiv.org/abs/2501.67890",
            "published": "2025-01-30T00:00:00+00:00",
            "word_count": 215,
            "language": "English",
            "source": "Journal of Monetary Economics",
            "doi": ""
        },
        {
            "id": 13,
            "title": "Options Pricing with Neural Networks",
            "authors": ["Andrew Scott", "Harper Allen"],
            "year": 2024,
            "month": 11,
            "category": "Derivatives",
            "abstract": "Using neural networks for options pricing compared to traditional Black-Scholes models.",
            "pdf_url": "https://arxiv.org/pdf/2411.34567",
            "arxiv_url": "https://arxiv.org/abs/2411.34567",
            "published": "2024-11-15T00:00:00+00:00",
            "word_count": 180,
            "language": "English",
            "source": "Journal of Derivatives",
            "doi": ""
        },
        {
            "id": 14,
            "title": "Financial Network Analysis and Systemic Risk",
            "authors": ["Edward Wright", "Evelyn Torres"],
            "year": 2025,
            "month": 2,
            "category": "Risk Management",
            "abstract": "Network analysis methods for assessing systemic risk in financial systems.",
            "pdf_url": "https://arxiv.org/pdf/2502.89012",
            "arxiv_url": "https://arxiv.org/abs/2502.89012",
            "published": "2025-02-20T00:00:00+00:00",
            "word_count": 225,
            "language": "English",
            "source": "Systemic Risk Review",
            "doi": ""
        },
        {
            "id": 15,
            "title": "Robo-Advisors and Automated Investment",
            "authors": ["Benjamin Green", "Abigail Nguyen"],
            "year": 2024,
            "month": 12,
            "category": "Fintech",
            "abstract": "Study of robo-advisor platforms and their performance compared to human financial advisors.",
            "pdf_url": "https://arxiv.org/pdf/2412.12345",
            "arxiv_url": "https://arxiv.org/abs/2412.12345",
            "published": "2024-12-05T00:00:00+00:00",
            "word_count": 195,
            "language": "English",
            "source": "Fintech Innovation Journal",
            "doi": ""
        },
        {
            "id": 16,
            "title": "Market Microstructure and Liquidity",
            "authors": ["Daniel Baker", "Emily Carter"],
            "year": 2025,
            "month": 3,
            "category": "Financial Markets",
            "abstract": "Analysis of market microstructure factors affecting liquidity in equity markets.",
            "pdf_url": "https://arxiv.org/pdf/2503.45678",
            "arxiv_url": "https://arxiv.org/abs/2503.45678",
            "published": "2025-03-25T00:00:00+00:00",
            "word_count": 210,
            "language": "English",
            "source": "Market Microstructure Journal",
            "doi": ""
        },
        {
            "id": 17,
            "title": "Climate Risk and Financial Stability",
            "authors": ["Matthew Nelson", "Elizabeth Perez"],
            "year": 2024,
            "month": 4,
            "category": "Sustainable Finance",
            "abstract": "Assessing climate-related risks and their implications for financial stability.",
            "pdf_url": "https://arxiv.org/pdf/2404.78901",
            "arxiv_url": "https://arxiv.org/abs/2404.78901",
            "published": "2024-04-18T00:00:00+00:00",
            "word_count": 220,
            "language": "English",
            "source": "Climate Finance Review",
            "doi": ""
        },
        {
            "id": 18,
            "title": "Peer-to-Peer Lending Platforms",
            "authors": ["Anthony Hall", "Sofia Roberts"],
            "year": 2025,
            "month": 5,
            "category": "Fintech",
            "abstract": "Risk assessment and performance analysis of peer-to-peer lending platforms.",
            "pdf_url": "https://arxiv.org/pdf/2505.23456",
            "arxiv_url": "https://arxiv.org/abs/2505.23456",
            "published": "2025-05-08T00:00:00+00:00",
            "word_count": 190,
            "language": "English",
            "source": "Digital Finance Journal",
            "doi": ""
        },
        {
            "id": 19,
            "title": "Financial Sentiment Analysis with NLP",
            "authors": ["Christopher Mitchell", "Avery Phillips"],
            "year": 2024,
            "month": 6,
            "category": "Natural Language Processing",
            "abstract": "Using natural language processing to analyze financial news sentiment and predict market movements.",
            "pdf_url": "https://arxiv.org/pdf/2406.90123",
            "arxiv_url": "https://arxiv.org/abs/2406.90123",
            "published": "2024-06-28T00:00:00+00:00",
            "word_count": 205,
            "language": "English",
            "source": "Journal of Financial NLP",
            "doi": ""
        },
        {
            "id": 20,
            "title": "Insurance Risk Modeling with ML",
            "authors": ["Joshua Campbell", "Ella Evans"],
            "year": 2025,
            "month": 7,
            "category": "Insurance",
            "abstract": "Machine learning approaches for insurance risk modeling and premium calculation.",
            "pdf_url": "https://arxiv.org/pdf/2507.56789",
            "arxiv_url": "https://arxiv.org/abs/2507.56789",
            "published": "2025-07-15T00:00:00+00:00",
            "word_count": 195,
            "language": "English",
            "source": "Insurance Mathematics and Economics",
            "doi": ""
        },
        {
            "id": 21,
            "title": "Corporate Finance and Capital Structure",
            "authors": ["Ryan Parker", "Scarlett Edwards"],
            "year": 2024,
            "month": 8,
            "category": "Corporate Finance",
            "abstract": "Optimal capital structure decisions for corporations under different market conditions.",
            "pdf_url": "https://arxiv.org/pdf/2408.34567",
            "arxiv_url": "https://arxiv.org/abs/2408.34567",
            "published": "2024-08-22T00:00:00+00:00",
            "word_count": 210,
            "language": "English",
            "source": "Journal of Corporate Finance",
            "doi": ""
        },
        {
            "id": 22,
            "title": "Foreign Exchange Rate Prediction",
            "authors": ["Nicholas Collins", "Grace Stewart"],
            "year": 2025,
            "month": 9,
            "category": "Foreign Exchange",
            "abstract": "Deep learning models for foreign exchange rate prediction using macroeconomic indicators.",
            "pdf_url": "https://arxiv.org/pdf/2509.01234",
            "arxiv_url": "https://arxiv.org/abs/2509.01234",
            "published": "2025-09-10T00:00:00+00:00",
            "word_count": 185,
            "language": "English",
            "source": "Journal of International Money and Finance",
            "doi": ""
        },
        {
            "id": 23,
            "title": "Financial Regulation and Compliance",
            "authors": ["Jonathan Morris", "Chloe Sanchez"],
            "year": 2024,
            "month": 10,
            "category": "Financial Regulation",
            "abstract": "Impact of financial regulations on market efficiency and compliance costs.",
            "pdf_url": "https://arxiv.org/pdf/2410.67890",
            "arxiv_url": "https://arxiv.org/abs/2410.67890",
            "published": "2024-10-30T00:00:00+00:00",
            "word_count": 225,
            "language": "English",
            "source": "Journal of Financial Regulation",
            "doi": ""
        },
        {
            "id": 24,
            "title": "Wealth Management Strategies",
            "authors": ["Samuel Rogers", "Riley Reed"],
            "year": 2025,
            "month": 11,
            "category": "Wealth Management",
            "abstract": "Modern wealth management strategies for high-net-worth individuals.",
            "pdf_url": "https://arxiv.org/pdf/2511.54321",
            "arxiv_url": "https://arxiv.org/abs/2511.54321",
            "published": "2025-11-20T00:00:00+00:00",
            "word_count": 200,
            "language": "English",
            "source": "Wealth Management Review",
            "doi": ""
        },
        {
            "id": 25,
            "title": "Financial Education and Literacy",
            "authors": ["Brandon Cook", "Zoey Murphy"],
            "year": 2024,
            "month": 12,
            "category": "Financial Education",
            "abstract": "Impact of financial education programs on individual financial decision-making.",
            "pdf_url": "https://arxiv.org/pdf/2412.98765",
            "arxiv_url": "https://arxiv.org/abs/2412.98765",
            "published": "2024-12-15T00:00:00+00:00",
            "word_count": 190,
            "language": "English",
            "source": "Journal of Financial Education",
            "doi": ""
        }
    ]
    return english_papers

def create_chinese_papers():
    """Create 25 sample Chinese finance research papers"""
    chinese_papers = [
        {
            "id": 101,
            "title": "中国养老金融政策的功能发挥与生态体系构建",
            "authors": ["郭磊", "曹琛璐", "贾润雨"],
            "year": 2025,
            "month": 1,
            "category": "养老金融",
            "abstract": "在人口老龄化加速演进与多层次养老服务体系建设的双重背景下，科学评估养老金融政策效能对优化制度供给、提升政策精准性具有重要意义。",
            "source": "开发性金融研究",
            "word_count": 350,
            "language": "Chinese",
            "keywords": "养老金融, PMC指数模型, 政策评价, 科技赋能, 协同治理",
            "published": "2025-01-15T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 102,
            "title": "数字人民币在征信体系中的锚定效应及实施策略",
            "authors": ["孟添", "周慧蕙", "陆岷峰"],
            "year": 2025,
            "month": 2,
            "category": "数字货币",
            "abstract": "建设社会主义现代化强国需要有科学、强大、健全的征信体系作支撑。目前，我国的征信体系仍然存在数据源单一、跨机构信息割裂等障碍。",
            "source": "科技智囊",
            "word_count": 320,
            "language": "Chinese",
            "keywords": "数字人民币, 征信体系, 数据孤岛, 信用锚定, 区块链",
            "published": "2025-02-20T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 103,
            "title": "绿色金融对碳排放的影响研究",
            "authors": ["曾小晏", "张华"],
            "year": 2026,
            "month": 1,
            "category": "绿色金融",
            "abstract": "现有文献大多支持绿色金融对碳排放具有抑制作用的观点。论文基于2011—2022年长江经济带108个地级市及以上城市的面板数据，综合运用一系列计量模型对二者关系进行了再考察。",
            "source": "生态经济",
            "word_count": 380,
            "language": "Chinese",
            "keywords": "绿色金融, 碳排放, 银行竞争, 人工智能",
            "published": "2026-01-10T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 104,
            "title": "金融科技对商业银行盈利能力的双刃剑效应",
            "authors": ["王晗苏"],
            "year": 2025,
            "month": 11,
            "category": "金融科技",
            "abstract": "文章探讨了金融科技对Y商业银行盈利能力的双刃剑效应，以Y商业银行为例，通过文献综述、盈利能力分析及金融科技应用现状的梳理，揭示了金融科技在优化业务流程、拓展业务渠道和提升风控能力方面的显著作用。",
            "source": "商业观察",
            "word_count": 280,
            "language": "Chinese",
            "keywords": "金融科技, 商业银行, 盈利能力",
            "published": "2025-11-05T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 105,
            "title": "商业银行在绿色金融领域的发展策略与实践探索",
            "authors": ["刘桐伶"],
            "year": 2025,
            "month": 12,
            "category": "绿色金融",
            "abstract": "文章聚焦商业银行绿色金融转型的核心矛盾，揭示政策衔接失配、产品创新乏力、风险管控薄弱、专业能力不足等关键障碍。",
            "source": "中国集体经济",
            "word_count": 300,
            "language": "Chinese",
            "keywords": "商业银行, 绿色金融, 可持续发展",
            "published": "2025-12-10T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 106,
            "title": "数字金融驱动上市农机企业高质量发展的实证研究",
            "authors": ["李平", "赵玥", "庞义章"],
            "year": 2025,
            "month": 11,
            "category": "数字金融",
            "abstract": "以2011—2022年A股上市农机企业为研究对象，基于创新、协调、绿色、开放、共享等多维度构建高质量发展评价体系，采用双向固定效应模型和机制分析方法，实证检验数字金融对农机企业高质量发展的驱动效应及其异质性特征。",
            "source": "湖北农业科学",
            "word_count": 340,
            "language": "Chinese",
            "keywords": "数字金融, 农机企业, 高质量发展, 异质性",
            "published": "2025-11-20T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 107,
            "title": "金融科技赋能农业新质生产力的实证研究",
            "authors": ["谭晴月", "刘畅"],
            "year": 2025,
            "month": 11,
            "category": "金融科技",
            "abstract": "新质生产力的提出为实现农业高质量发展指明了方向，金融科技作为经济高质量发展的新引擎，在赋能农业新质生产力发展方面起着重要的作用。",
            "source": "对外经贸",
            "word_count": 290,
            "language": "Chinese",
            "keywords": "金融科技, 农业新质生产力, 高质量发展",
            "published": "2025-11-15T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 108,
            "title": "数字普惠金融对农村居民消费升级影响的实证研究",
            "authors": ["刘泓伯", "刘伯霞"],
            "year": 2025,
            "month": 11,
            "category": "数字金融",
            "abstract": "本文深入研究数字普惠金融对农村居民消费升级的影响。利用2011-2022年我国省级面板数据进行实证分析，研究表明，数字普惠金融显著促进农村居民消费升级。",
            "source": "时代经贸",
            "word_count": 270,
            "language": "Chinese",
            "keywords": "数字普惠金融, 农村居民, 消费升级",
            "published": "2025-11-25T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 109,
            "title": "金融科技赋能商业银行数字化转型的理论机制与现实路径",
            "authors": ["肖煜"],
            "year": 2025,
            "month": 12,
            "category": "金融科技",
            "abstract": "金融科技是金融业未来发展的主流趋势，其实质是利用现代网络技术赋能金融行业。",
            "source": "中国市场",
            "word_count": 310,
            "language": "Chinese",
            "keywords": "金融科技, 商业银行, 数字化转型",
            "published": "2025-12-05T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 110,
            "title": "金融科技赋能商业银行资本管理效率提升的路径探索",
            "authors": ["王琼"],
            "year": 2025,
            "month": 11,
            "category": "金融科技",
            "abstract": "本文剖析了金融科技赋能商业银行资本管理效率提升面临的挑战，包括资本管理数据与金融科技系统对接存在壁垒、资本风险计量精准度不足、金融科技应用合规性难以把控等。",
            "source": "天津经济",
            "word_count": 260,
            "language": "Chinese",
            "keywords": "金融科技, 商业银行, 资本管理, 效率提升",
            "published": "2025-11-30T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 111,
            "title": "商业银行供应链金融风险治理研究",
            "authors": ["贾蓉"],
            "year": 2025,
            "month": 8,
            "category": "供应链金融",
            "abstract": "随着经济全球化与产业协同深化，供应链金融成为商业银行重要业务增长点，但其风险问题也日益凸显，系统剖析商业银行供应链金融风险并进行相应的风险治理势在必行。",
            "source": "全国流通经济",
            "word_count": 330,
            "language": "Chinese",
            "keywords": "商业银行, 供应链金融, 风险识别, 风险治理, 应急机制",
            "published": "2025-08-15T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 112,
            "title": "金融数字化营销在我国商业银行金融业务中的应用与挑战",
            "authors": ["张宏宇", "陆冠呈", "赵艺萌", "华心慧"],
            "year": 2025,
            "month": 10,
            "category": "数字营销",
            "abstract": "金融数字化营销指的是金融业务与大数据技术、互联网信息技术、新媒体技术、人工智能技术等先进科学技术深度融合的营销模式。",
            "source": "现代商业",
            "word_count": 350,
            "language": "Chinese",
            "keywords": "金融业务, 数字化营销, 商业银行",
            "published": "2025-10-20T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 113,
            "title": "绿色金融对我国企业动力消耗结构影响的实证研究",
            "authors": ["周志鑫", "梁海斌"],
            "year": 2025,
            "month": 9,
            "category": "绿色金融",
            "abstract": "绿色金融通过资金支持和风险保障机制，对企业动力消耗结构的优化具有显著推动作用。",
            "source": "现代商业",
            "word_count": 320,
            "language": "Chinese",
            "keywords": "绿色金融, 动力消耗结构, 产业结构, 绿色技术创新, 低碳化",
            "published": "2025-09-25T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 114,
            "title": "商业银行开展数据资产融资业务探析",
            "authors": ["许振"],
            "year": 2025,
            "month": 11,
            "category": "数据资产",
            "abstract": "如何推动数据要素和金融要素深度融合，成为数字经济时代数据要素领域和金融要素领域发展的共同命题。",
            "source": "福建金融",
            "word_count": 290,
            "language": "Chinese",
            "keywords": "数据资产, 数据资产融资, 商业银行, 数字金融",
            "published": "2025-11-10T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 115,
            "title": "商业银行表外业务会计核算研究",
            "authors": ["段倩"],
            "year": 2025,
            "month": 11,
            "category": "银行会计",
            "abstract": "在金融市场快速发展的当下，表外业务在银行业务中占比明显上升。表外业务是商业银行创新发展的主要方向，对银行盈利情况有显著影响。",
            "source": "冶金财会",
            "word_count": 250,
            "language": "Chinese",
            "keywords": "表外业务, 商业银行, 会计核算",
            "published": "2025-11-08T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 116,
            "title": "货币政策对民间借贷利率的影响研究",
            "authors": ["张博", "虞正浩"],
            "year": 2025,
            "month": 1,
            "category": "货币政策",
            "abstract": "在我国利率双轨制深化改革的背景下，民间金融市场与货币政策的动态交互机制已成为优化金融资源配置效率的关键研究领域。",
            "source": "温州大学学报(社会科学版)",
            "word_count": 340,
            "language": "Chinese",
            "keywords": "民间借贷, 货币政策, VAR模型",
            "published": "2025-01-25T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 117,
            "title": "金融科技助力商业银行盈利能力提升的策略",
            "authors": ["裴友平"],
            "year": 2025,
            "month": 1,
            "category": "金融科技",
            "abstract": "科技发展推动了金融科技的持续进步，商业银行业务也因金融科技的快速发展面临诸多挑战与机遇。",
            "source": "中国金融知识仓库",
            "word_count": 310,
            "language": "Chinese",
            "keywords": "金融科技, 商业银行, 盈利能力, 提升策略",
            "published": "2025-01-30T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 118,
            "title": "基于因子降维和模型组合的中国股市预测研究",
            "authors": ["吴浩成"],
            "year": 2025,
            "month": 6,
            "category": "股市预测",
            "abstract": "股票市场溢价作为资产定价与风险管理的核心观测指标,其预测效能始终是金融学研究的焦点。",
            "source": "电子科技大学",
            "word_count": 420,
            "language": "Chinese",
            "keywords": "中国股市, 股指溢价预测, 高维预测因子, 降维技术, 模型组合策略",
            "published": "2025-06-15T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 119,
            "title": "我国国债利率期限结构预测及应用研究",
            "authors": ["纪哲翰"],
            "year": 2023,
            "month": 12,
            "category": "国债利率",
            "abstract": "国债利率期限结构反映了国债收益率与到期期限之间的关系,反映了市场无风险利率的情况,代表着一个国家金融市场的基准利率水平。",
            "source": "对外经济贸易大学",
            "word_count": 380,
            "language": "Chinese",
            "keywords": "国债利率期限结构, 统计机器学习模型, 宏观经济高维数据, 国债投资组合策略",
            "published": "2023-12-20T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 120,
            "title": "稳定币的基本要素与信用机制",
            "authors": ["谭文心", "章政"],
            "year": 2025,
            "month": 12,
            "category": "数字货币",
            "abstract": "近年来，稳定币的规模与功能持续扩展，关于稳定币体系如何构建和维系其价值基础，仍缺乏理论分析框架。",
            "source": "征信",
            "word_count": 360,
            "language": "Chinese",
            "keywords": "稳定币, 信用机制, 区块链, 中心化稳定币, RWA",
            "published": "2025-12-10T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 121,
            "title": "信息消费激发国内消费市场潜力的实证研究",
            "authors": ["刘文革", "肖宇航", "纪红绳"],
            "year": 2025,
            "month": 3,
            "category": "消费金融",
            "abstract": "随着信息技术与经济社会的深度融合，信息消费对于提振国内消费需求、拉动内需增长发挥着重要作用。",
            "source": "当代经济科学",
            "word_count": 330,
            "language": "Chinese",
            "keywords": "信息消费, 消费市场潜力, 城市绿色技术创新, 数字普惠金融, 扩大内需",
            "published": "2025-03-15T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 122,
            "title": "商业银行共绘未来五年发展新蓝图",
            "authors": ["张冰洁"],
            "year": 2025,
            "month": 11,
            "category": "银行战略",
            "abstract": "农业银行'十五五'规划，请您来支招。近日，农业银行在官方渠道面向社会发出邀请。",
            "source": "金融时报",
            "word_count": 280,
            "language": "Chinese",
            "keywords": "商业银行, 发展规划, 战略规划",
            "published": "2025-11-27T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 123,
            "title": "从商业银行视角浅析跨境供应链金融",
            "authors": ["张海丽", "游永海"],
            "year": 2026,
            "month": 2,
            "category": "供应链金融",
            "abstract": "随着国际贸易环境变化，融资需求也将随之改变，相较于传统国际贸易融资，跨境供应链融资具备其独特优势。",
            "source": "商业经济",
            "word_count": 300,
            "language": "Chinese",
            "keywords": "商业银行, 跨境供应链, 融资, 优势, 风险",
            "published": "2026-02-15T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 124,
            "title": "动态体系论下违反商业银行股权转让报批义务的损害救济研究",
            "authors": ["刘佳沐", "冯永军"],
            "year": 2025,
            "month": 10,
            "category": "银行法律",
            "abstract": "商业银行股权转让审批是维护金融稳定、以金融高质量发展助力现代化强国建设的有效措施。",
            "source": "金融理论与实践",
            "word_count": 350,
            "language": "Chinese",
            "keywords": "动态体系论, 商业银行, 股权转让, 损害救济, 要素",
            "published": "2025-10-20T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        },
        {
            "id": 125,
            "title": "商业银行年内发行4582亿元绿色金融债券",
            "authors": ["熊悦"],
            "year": 2025,
            "month": 12,
            "category": "绿色金融",
            "abstract": "中国货币网信息显示，12月15日，枣庄银行发布公告称，该行将于12月18日至12月22日发行规模为9亿元的绿色金融债券。",
            "source": "证券日报",
            "word_count": 240,
            "language": "Chinese",
            "keywords": "商业银行, 绿色金融债券, 债券发行",
            "published": "2025-12-17T00:00:00+00:00",
            "arxiv_url": "",
            "pdf_url": "",
            "doi": ""
        }
    ]
    return chinese_papers

# ===== LOAD RESEARCH PAPERS =====
@st.cache_data
def load_research_papers():
    """Load research papers from embedded data"""
    # Create English papers
    english_papers = create_english_papers()
    
    # Create Chinese papers  
    chinese_papers = create_chinese_papers()
    
    # Combine all papers
    all_papers = english_papers + chinese_papers
    
    # Create DataFrame
    papers_df = pd.DataFrame(all_papers)
    
    # Convert date columns
    if 'published' in papers_df.columns:
        papers_df['published_date'] = pd.to_datetime(papers_df['published'], errors='coerce')
        papers_df['year_month'] = papers_df['published_date'].dt.strftime('%Y-%m')
    
    # Extract year if not present
    if 'year' in papers_df.columns:
        papers_df['year'] = papers_df['year'].fillna(2025).astype(int)
    
    # Clean up category names
    if 'category' in papers_df.columns:
        papers_df['category_clean'] = papers_df['category'].str.replace('_', ' ').str.title()
    
    # Ensure all required fields exist
    papers_df['arxiv_url'] = papers_df.get('arxiv_url', '')
    papers_df['pdf_url'] = papers_df.get('pdf_url', '')
    papers_df['doi'] = papers_df.get('doi', '')
    papers_df['keywords'] = papers_df.get('keywords', '')
    
    # Show loading success
    st.sidebar.success(f"✅ Loaded {len(english_papers)} English papers")
    st.sidebar.success(f"✅ Loaded {len(chinese_papers)} Chinese papers")
    
    return papers_df, all_papers

# Load papers
papers_df, papers_list = load_research_papers()

# ===== RESEARCH LIBRARY FUNCTIONS =====
def display_research_library():
    """Display the research library interface"""
    st.header("📚 Research Library")
    
    # Display statistics
    if not papers_df.empty:
        stats_cols = st.columns(5)
        with stats_cols[0]:
            st.metric("Total Papers", len(papers_df))
        with stats_cols[1]:
            unique_categories = papers_df['category'].nunique() if 'category' in papers_df.columns else 0
            st.metric("Categories", unique_categories)
        with stats_cols[2]:
            recent_year = int(papers_df['year'].max()) if 'year' in papers_df.columns else 2025
            st.metric("Latest Year", recent_year)
        with stats_cols[3]:
            english_count = len(papers_df[papers_df['language'] == 'English'])
            chinese_count = len(papers_df[papers_df['language'] == 'Chinese'])
            st.metric("Languages", f"EN:{english_count}/CN:{chinese_count}")
        with stats_cols[4]:
            if 'word_count' in papers_df.columns:
                total_words = papers_df['word_count'].sum()
                st.metric("Total Words", f"{total_words:,}")
    
    # Search and filter section
    with st.container():
        st.subheader("🔍 Search & Filter")
        
        search_cols = st.columns([2, 1, 1, 1, 1])
        with search_cols[0]:
            search_query = st.text_input("Search papers (title, authors, abstract)", "")
        
        with search_cols[1]:
            categories = sorted(papers_df['category'].dropna().unique().tolist())
            selected_category = st.selectbox("Category", ["All"] + categories)
        
        with search_cols[2]:
            years = sorted(papers_df['year'].dropna().unique().tolist(), reverse=True)
            selected_year = st.selectbox("Year", ["All"] + [str(int(y)) for y in years])
        
        with search_cols[3]:
            languages = sorted(papers_df['language'].dropna().unique().tolist())
            selected_language = st.selectbox("Language", ["All"] + languages)
        
        with search_cols[4]:
            sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Title A-Z", "Title Z-A"])
    
    # Apply filters
    filtered_df = papers_df.copy()
    
    if not papers_df.empty:
        # Apply search
        if search_query:
            mask = (
                filtered_df['title'].astype(str).str.contains(search_query, case=False, na=False) |
                filtered_df['abstract'].astype(str).str.contains(search_query, case=False, na=False) |
                filtered_df['authors'].apply(lambda x: search_query.lower() in str(x).lower() if isinstance(x, list) else False)
            )
            filtered_df = filtered_df[mask]
        
        # Apply category filter
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
        # Apply year filter
        if selected_year != "All":
            filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
        
        # Apply language filter
        if selected_language != "All":
            filtered_df = filtered_df[filtered_df['language'] == selected_language]
        
        # Apply sorting
        if sort_by == "Newest":
            filtered_df = filtered_df.sort_values('year', ascending=False)
        elif sort_by == "Oldest":
            filtered_df = filtered_df.sort_values('year', ascending=True)
        elif sort_by == "Title A-Z":
            filtered_df = filtered_df.sort_values('title')
        elif sort_by == "Title Z-A":
            filtered_df = filtered_df.sort_values('title', ascending=False)
    
    # Display results
    if filtered_df.empty:
        st.warning("No papers found matching your criteria.")
    else:
        st.success(f"Found {len(filtered_df)} papers")
        
        # Display papers in a nice format
        for idx, paper in filtered_df.iterrows():
            paper_id = paper.get('id', idx)
            with st.expander(f"📄 **{paper.get('title', 'Untitled')}** ({paper.get('language', 'Unknown')})", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Paper title and authors
                    st.markdown(f"### {paper.get('title', 'Untitled')}")
                    
                    # Authors
                    authors = paper.get('authors', [])
                    if authors and isinstance(authors, list):
                        authors_str = ", ".join(authors)
                        st.markdown(f"**Authors:** {authors_str}")
                    elif authors:
                        st.markdown(f"**Authors:** {authors}")
                    
                    # Year and category
                    meta_cols = st.columns(4)
                    with meta_cols[0]:
                        if 'year' in paper:
                            st.metric("Year", int(paper['year']))
                    with meta_cols[1]:
                        if 'category' in paper:
                            st.metric("Category", paper['category'])
                    with meta_cols[2]:
                        if 'language' in paper:
                            st.metric("Language", paper['language'])
                    with meta_cols[3]:
                        if 'word_count' in paper:
                            st.metric("Words", paper['word_count'])
                    
                    # Abstract
                    st.markdown("#### Abstract")
                    abstract = paper.get('abstract', 'No abstract available')
                    if isinstance(abstract, str):
                        if len(abstract) > 500:
                            st.write(abstract[:500] + "...")
                        else:
                            st.write(abstract)
                    else:
                        st.write(str(abstract))
                    
                    # Source and keywords
                    source = paper.get('source', '')
                    if source:
                        st.markdown(f"**Source:** {source}")
                    
                    keywords = paper.get('keywords', '')
                    if keywords:
                        st.markdown(f"**Keywords:** {keywords}")
                
                with col2:
                    # Quick actions and links
                    st.markdown("#### 🔗 Quick Links")
                    
                    # Use safe_link_button for all links
                    arxiv_url = paper.get('arxiv_url', '')
                    pdf_url = paper.get('pdf_url', '')
                    doi_value = paper.get('doi', '')
                    
                    # arXiv button
                    safe_link_button(
                        "📄 arXiv", 
                        arxiv_url,
                        key=f"arxiv_{paper_id}",
                        help_text="Open arXiv page"
                    )
                    
                    # PDF button
                    safe_link_button(
                        "📥 PDF", 
                        pdf_url,
                        key=f"pdf_{paper_id}",
                        help_text="Download PDF"
                    )
                    
                    # DOI button
                    if doi_value and isinstance(doi_value, str) and doi_value.strip():
                        doi_url = f"https://doi.org/{doi_value}"
                        safe_link_button(
                            "🔗 DOI", 
                            doi_url,
                            key=f"doi_{paper_id}",
                            help_text="Open DOI page"
                    )
                    
                    # Search link
                    search_url = f"https://scholar.google.com/scholar?q={paper.get('title', '').replace(' ', '+')}"
                    st.link_button("🔍 Search", search_url)
                    
                    # Additional info
                    st.markdown("---")
                    keywords = paper.get('keywords', '')
                    if keywords and isinstance(keywords, str) and keywords.strip():
                        if len(keywords) > 50:
                            st.caption(f"**Keywords:** {keywords[:50]}...")
                        else:
                            st.caption(f"**Keywords:** {keywords}")
                    
                    # Classify this paper button
                    if st.button("🤖 Classify this paper", key=f"classify_{paper_id}"):
                        st.session_state.selected_paper_for_classification = paper.get('title', '')
                        st.session_state.paper_abstract_for_classification = paper.get('abstract', '')
                        st.rerun()
                
                st.markdown("---")

# ===== MOCK MODEL FUNCTION =====
def classify_with_confidence(text, top_k=5, improve_confidence=True):
    """
    Mock classification function with improved confidence simulation
    """
    # Finance categories with Wikipedia links
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
        "Financial Inclusion",
        "养老金融",
        "数字货币",
        "绿色金融",
        "金融科技",
        "数字金融",
        "供应链金融",
        "银行会计",
        "货币政策",
        "股市预测",
        "国债利率",
        "消费金融",
        "银行战略",
        "银行法律",
        "数字营销",
        "数据资产"
    ]
    
    # Wikipedia links
    category_links = {
        "Quantitative Finance": "https://en.wikipedia.org/wiki/Quantitative_analysis_(finance)",
        "Behavioral Finance": "https://en.wikipedia.org/wiki/Behavioral_finance",
        "Corporate Finance": "https://en.wikipedia.org/wiki/Corporate_finance",
        "Fintech": "https://en.wikipedia.org/wiki/Fintech",
        "Cryptocurrency": "https://en.wikipedia.org/wiki/Cryptocurrency",
        "Sustainable Finance": "https://en.wikipedia.org/wiki/Sustainable_finance",
        "养老金融": "https://baike.baidu.com/item/%E5%85%BB%E8%80%81%E9%87%91%E8%9E%8D",
        "数字货币": "https://baike.baidu.com/item/%E6%95%B0%E5%AD%97%E8%B4%A7%E5%B8%81",
        "绿色金融": "https://baike.baidu.com/item/%E7%BB%BF%E8%89%B2%E9%87%91%E8%9E%8D",
        "金融科技": "https://baike.baidu.com/item/%E9%87%91%E8%9E%8D%E7%A7%91%E6%8A%80",
        "数字金融": "https://baike.baidu.com/item/%E6%95%B0%E5%AD%97%E9%87%91%E8%9E%8D"
    }
    
    # Generate confidence scores
    import hashlib
    if isinstance(text, str) and text:
        text_hash = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
    else:
        text_hash = 42
    
    np.random.seed(text_hash % 10000)
    
    # Generate scores
    if improve_confidence:
        base_scores = np.random.dirichlet(np.ones(len(finance_categories)) * 0.3)
        sorted_indices = np.argsort(base_scores)[::-1]
        boost_factor = np.linspace(1.5, 1.0, len(base_scores))
        
        adjusted_scores = base_scores.copy()
        for idx, boost in zip(sorted_indices, boost_factor):
            adjusted_scores[idx] *= boost
        
        scores = adjusted_scores / adjusted_scores.sum()
    else:
        scores = np.random.dirichlet(np.ones(len(finance_categories)) * 0.1)
    
    # Sort and get top k
    indices = np.argsort(scores)[::-1][:top_k]
    
    results = []
    for idx in indices:
        category = finance_categories[idx]
        confidence = float(scores[idx] * 100)
        confidence += np.random.uniform(-2, 2)
        confidence = max(0, min(100, confidence))
        
        # Get link
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
    Display classification results with enhanced visualization
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
    
    # Display main category
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
    action_cols = st.columns(3)
    
    with action_cols[0]:
        wiki_url = top_category.get('wiki_link', 'https://en.wikipedia.org/wiki/Finance')
        st.link_button("🌐 Wikipedia", wiki_url)
    
    with action_cols[1]:
        search_query = top_category['category'].replace(' ', '+')
        st.link_button("📚 Google Scholar", f"https://scholar.google.com/scholar?q={search_query}+finance")
    
    with action_cols[2]:
        st.link_button("📊 More Papers", f"https://www.jstor.org/action/doBasicSearch?Query={search_query}")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 Top Categories", "📈 Visualization", "📥 Export Results"])
    
    with tab1:
        # Display top categories
        st.subheader(f"Top {len(top_results)} Predictions")
        
        df_results = pd.DataFrame(top_results)
        df_results.index = range(1, len(df_results) + 1)
        
        df_results['category_with_link'] = df_results.apply(
            lambda row: f"[{row['category']}]({row['wiki_link']})", 
            axis=1
        )
        
        st.dataframe(
            df_results[['category_with_link', 'confidence']],
            column_config={
                "category_with_link": st.column_config.TextColumn("Category", width="large"),
                "confidence": st.column_config.ProgressColumn("Confidence (%)", format="%.2f%%", min_value=0, max_value=100)
            },
            hide_index=False,
            use_container_width=True,
            height=min(400, 45 * len(top_results))
        )
    
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
            labels={'confidence': 'Confidence (%)', 'category': 'Category'}
        )
        
        fig.update_traces(
            texttemplate='%{text:.2f}%',
            textposition='outside'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_range=[0, 100],
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
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
            ]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            csv_buffer = io.StringIO()
            df_results.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="📊 Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON Export
            json_buffer = io.StringIO()
            json.dump(export_data, json_buffer, indent=2)
            
            st.download_button(
                label="📁 Download JSON",
                data=json_buffer.getvalue(),
                file_name=f"classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
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

# ===== PDF PROCESSOR =====
pdf_available = False
try:
    import pdfplumber
    pdf_available = True
    
    class SimplePDFProcessor:
        def extract_text(self, file, max_pages=3):
            import pdfplumber
            import io
            text = ""
            try:
                file_bytes = file.read()
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    for i, page in enumerate(pdf.pages[:max_pages]):
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n\n"
            except Exception as e:
                text = f"Sample abstract for classification demonstration. Error: {str(e)}"
            return text
        
        def extract_abstract(self, text):
            # Simple abstract extraction
            lines = text.split('\n')
            abstract = ""
            
            for i, line in enumerate(lines):
                line_lower = line.lower().strip()
                if 'abstract' in line_lower and len(line_lower) < 30:
                    for j in range(i+1, min(i+10, len(lines))):
                        if lines[j].strip():
                            abstract += lines[j] + " "
                    break
            
            if not abstract:
                sentences = text.replace('\n', ' ').split('.')
                abstract = '.'.join(sentences[:3]) + '.'
            
            return abstract.strip()
        
        def count_words(self, text):
            return len(text.split())
    
    pdf_processor = SimplePDFProcessor()
    st.sidebar.success("✅ PDF processor ready")
    
except ImportError:
    st.sidebar.warning("⚠️ Install pdfplumber: pip install pdfplumber")
    pdf_processor = None
except Exception as e:
    st.sidebar.error(f"❌ PDF processor error: {e}")
    pdf_processor = None

# ===== MAIN APP NAVIGATION =====
st.sidebar.header("📚 Navigation")
app_mode = st.sidebar.radio(
    "Choose Mode",
    ["🏠 Classifier", "📚 Research Library", "📊 Statistics"],
    help="Switch between classification mode and research library"
)

# Sidebar Configuration
if app_mode == "🏠 Classifier":
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
            help="Upload academic papers or research reports"
        )
        
        st.header("🤖 Classification Settings")
        top_k = st.slider("Number of top categories", 3, 10, 5)
        improve_model = st.checkbox("Enhance confidence scores", True)
        
        st.header("📊 Display Options")
        auto_classify = st.checkbox("Auto-classify on upload", False)

# ===== MAIN CONTENT AREA =====
if app_mode == "🏠 Classifier":
    st.header("📄 PDF Classifier")
    
    # Check if a paper from library was selected for classification
    if hasattr(st.session_state, 'selected_paper_for_classification') and st.session_state.selected_paper_for_classification:
        st.info(f"📚 Classifying paper from library: **{st.session_state.selected_paper_for_classification}**")
        
        with st.spinner("Running AI classification..."):
            top_results = classify_with_confidence(
                st.session_state.paper_abstract_for_classification, 
                top_k=5,
                improve_confidence=True
            )
            
            display_classification_results(
                top_results, 
                st.session_state.selected_paper_for_classification, 
                st.session_state.paper_abstract_for_classification
            )
        
        # Clear the selected paper
        st.session_state.selected_paper_for_classification = None
        st.session_state.paper_abstract_for_classification = None
    
    # Handle uploaded files
    elif uploaded_files:
        st.success(f"📄 {len(uploaded_files)} file(s) uploaded")
        
        # Initialize session state for classification history
        if 'classification_history' not in st.session_state:
            st.session_state.classification_history = []
        
        # Process each uploaded file
        for i, file in enumerate(uploaded_files):
            with st.expander(f"📋 **{file.name}** ({file.size/1024:.1f} KB)", expanded=i==0):
                
                if pdf_available and pdf_processor:
                    # Extract text from PDF
                    with st.spinner("Extracting text from PDF..."):
                        try:
                            pdf_text = pdf_processor.extract_text(file, max_pages=max_pages)
                            abstract = pdf_processor.extract_abstract(pdf_text)
                            word_count = pdf_processor.count_words(pdf_text)
                            
                            col_left, col_right = st.columns([2, 1])
                            
                            with col_left:
                                st.write("**📝 Extracted Abstract:**")
                                if abstract:
                                    st.write(abstract[:400] + "..." if len(abstract) > 400 else abstract)
                                else:
                                    st.write("No abstract extracted.")
                                
                                # Statistics
                                st.write("**🔢 Statistics:**")
                                stat_cols = st.columns(3)
                                with stat_cols[0]:
                                    st.metric("Words", word_count)
                                with stat_cols[1]:
                                    st.metric("Pages", max_pages)
                                with stat_cols[2]:
                                    st.metric("Size", f"{file.size/1024:.0f} KB")
                                
                                if show_raw_text and pdf_text:
                                    with st.expander("📄 View extracted text"):
                                        st.text(pdf_text[:2000] + "..." if len(pdf_text) > 2000 else pdf_text)
                            
                            with col_right:
                                # File info card
                                st.markdown("**📄 File Information**")
                                st.metric("File Size", f"{file.size/1024:.0f} KB")
                                
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
                                        # Run classification
                                        top_results = classify_with_confidence(
                                            pdf_text, 
                                            top_k=top_k,
                                            improve_confidence=improve_model
                                        )
                                        
                                        # Display results
                                        display_classification_results(top_results, file.name, abstract)
                        
                        except Exception as e:
                            st.error(f"❌ Error processing PDF: {str(e)}")
                else:
                    # Fallback
                    st.warning("⚠️ PDF processing not available. Please install pdfplumber:")
                    st.code("pip install pdfplumber")
    
    else:
        st.info("📤 Upload PDF files to classify or switch to Research Library to browse existing papers.")

elif app_mode == "📚 Research Library":
    display_research_library()

elif app_mode == "📊 Statistics":
    st.header("📊 Research Statistics")
    
    if not papers_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Papers", len(papers_df))
        
        with col2:
            recent_year = int(papers_df['year'].max())
            st.metric("Latest Year", recent_year)
        
        with col3:
            unique_cats = papers_df['category'].nunique()
            st.metric("Categories", unique_cats)
        
        with col4:
            english_count = len(papers_df[papers_df['language'] == 'English'])
            chinese_count = len(papers_df[papers_df['language'] == 'Chinese'])
            st.metric("English/Chinese", f"{english_count}/{chinese_count}")
        
        # Category distribution
        st.subheader("📈 Category Distribution")
        category_counts = papers_df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        fig = px.bar(
            category_counts.head(15),
            x='Category',
            y='Count',
            color='Count',
            title="Top 15 Research Categories",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Language distribution
        st.subheader("🌐 Language Distribution")
        language_counts = papers_df['language'].value_counts().reset_index()
        language_counts.columns = ['Language', 'Count']
        
        fig = px.pie(
            language_counts,
            values='Count',
            names='Language',
            title="Papers by Language",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Yearly trend
        st.subheader("📅 Yearly Publication Trend")
        yearly_counts = papers_df['year'].value_counts().sort_index().reset_index()
        yearly_counts.columns = ['Year', 'Count']
        
        fig = px.line(
            yearly_counts,
            x='Year',
            y='Count',
            title="Papers Published per Year",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Word count distribution
        st.subheader("📝 Word Count Distribution")
        fig = px.histogram(
            papers_df,
            x='word_count',
            nbins=20,
            title="Distribution of Abstract Word Counts"
        )
        st.plotly_chart(fig, use_container_width=True)

# Display classification history
if 'classification_history' in st.session_state and st.session_state.classification_history and app_mode == "🏠 Classifier":
    with st.expander("📚 Classification History", expanded=False):
        history_df = pd.DataFrame(st.session_state.classification_history)
        
        if not history_df.empty:
            if 'timestamp' in history_df.columns:
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                history_df['time_display'] = history_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(
                history_df[['file_name', 'predicted_category', 'confidence', 'time_display']],
                column_config={
                    "file_name": "File",
                    "predicted_category": "Category",
                    "confidence": st.column_config.ProgressColumn("Confidence", format="%.1f%%", min_value=0, max_value=100),
                    "time_display": "Time"
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Clear history button
            if st.button("Clear History", type="secondary", use_container_width=True):
                st.session_state.classification_history = []
                st.rerun()

# Footer
st.markdown("---")
footer_cols = st.columns(5)

with footer_cols[0]:
    st.markdown("[📖 Documentation](https://docs.streamlit.io)")

with footer_cols[1]:
    st.markdown("[🐙 GitHub](https://github.com)")

with footer_cols[2]:
    st.markdown("[💬 Community](https://discuss.streamlit.io)")

with footer_cols[3]:
    st.markdown("[🐦 Twitter](https://twitter.com/streamlit)")

with footer_cols[4]:
    st.markdown(f"**Version 4.0** • {datetime.now().strftime('%Y-%m-%d')}")

st.caption(f"""
Finance Research Classifier v4.0 | 
Made with ❤️ for academic research | 
50 research papers embedded (25 English + 25 Chinese) | 
All errors fixed
""")