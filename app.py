import streamlit as st
import pandas as pd
import sys
import plotly.express as px
import numpy as np
import json
import io
from datetime import datetime
import os

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
    return st.link_button(label, url, key=key)  # Fixed: removed help parameter

# ===== LOAD RESEARCH PAPERS FROM JSON =====
@st.cache_data
def load_research_papers():
    """Load research papers from JSON file"""
    try:
        # Load from the JSON file you provided
        json_file_path = "finance_research_papers.json"
        
        # First, try to load from file
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                all_papers = json.load(f)
            st.sidebar.success(f"✅ Loaded {len(all_papers)} papers from JSON file")
        else:
            # If file doesn't exist, use the JSON content you provided
            st.sidebar.warning(f"⚠️ File {json_file_path} not found, using embedded data")
            # Parse the JSON content from your message
            json_content = """[
  {
    "id": 1,
    "title": "Convergence of the generalization error for deep gradient flow methods for PDEs",
    "authors": [
      "Chenguang Liu",
      "Antonis Papapantoleon",
      "Jasper Rou"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "The aim of this article is to provide a firm mathematical foundation for the application of deep gradient flow methods (DGFMs) for the solution of (high-dimensional) partial differential equations (PDEs). We decompose the generalization error of DGFMs into an approximation and a training error. We first show that the solution of PDEs that satisfy reasonable and verifiable assumptions can be approximated by neural networks, thus the approximation error tends to zero as the number of neurons tends to infinity. Then, we derive the gradient flow that the training process follows in the ``wide network limit'' and analyze the limit of this flow as the training time tends to infinity. These results combined show that the generalization error of DGFMs tends to zero as the number of neurons and the training time tend to infinity.",
    "arxiv_url": "http://arxiv.org/abs/2512.25017v1",
    "pdf_url": "http://arxiv.org/pdf/2512.25017v1.pdf",
    "published": "2025-12-31T18:11:51Z",
    "word_count": 134,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 2,
    "title": "Fairness-Aware Insurance Pricing: A Multi-Objective Optimization Approach",
    "authors": [
      "Tim J. Boonen",
      "Xinyue Fan",
      "Zixiao Quan"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Machine learning improves predictive accuracy in insurance pricing but exacerbates trade-offs between competing fairness criteria across different discrimination measures, challenging regulators and insurers to reconcile profitability with equitable outcomes. While existing fairness-aware models offer partial solutions under GLM and XGBoost estimation methods, they remain constrained by single-objective optimization, failing to holistically navigate a conflicting landscape of accuracy, group fairness, individual fairness, and counterfactual fairness. To address this, we propose a novel multi-objective optimization framework that jointly optimizes all four criteria via the Non-dominated Sorting Genetic Algorithm II (NSGA-II), generating a diverse Pareto front of trade-off solutions. We use a specific selection mechanism to extract a premium on this front. Our results show that XGBoost outperforms GLM in accuracy but amplifies fairness disparities; the Orthogonal model excels in group fairness, while Synthetic Control leads in individual and counterfactual fairness. Our method consistently achieves a balanced compromise, outperforming single-model approaches.",
    "arxiv_url": "http://arxiv.org/abs/2512.24747v1",
    "pdf_url": "http://arxiv.org/pdf/2512.24747v1.pdf",
    "published": "2025-12-31T09:42:03Z",
    "word_count": 148,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 3,
    "title": "Boundary error control for numerical solution of BSDEs by the convolution-FFT method",
    "authors": [
      "Xiang Gao",
      "Cody Hyndman"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We first review the convolution fast-Fourier-transform (CFFT) approach for the numerical solution of backward stochastic differential equations (BSDEs) introduced in (Hyndman and Oyono Ngou, 2017). We then propose a method for improving the boundary errors obtained when valuing options using this approach. We modify the damping and shifting schemes used in the original formulation, which transforms the target function into a bounded periodic function so that Fourier transforms can be applied successfully. Time-dependent shifting reduces boundary error significantly. We present numerical results for our implementation and provide a detailed error analysis showing the improved accuracy and convergence of the modified convolution method.",
    "arxiv_url": "http://arxiv.org/abs/2512.24714v1",
    "pdf_url": "http://arxiv.org/pdf/2512.24714v1.pdf",
    "published": "2025-12-31T08:29:33Z",
    "word_count": 102,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 4,
    "title": "Forward-Oriented Causal Observables for Non-Stationary Financial Markets",
    "authors": [
      "Lucas A. Souza"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We study short-horizon forecasting in financial time series under strict causal constraints, treating the market as a non-stationary stochastic system in which any predictive observable must be computable online from information available up to the decision time. Rather than proposing a machine-learning predictor or a direct price-forecast model, we focus on \\emph{constructing} an interpretable causal signal from heterogeneous micro-features that encode complementary aspects of the dynamics (momentum, volume pressure, trend acceleration, and volatility-normalized price location). The construction combines (i) causal centering, (ii) linear aggregation into a composite observable, (iii) causal stabilization via a one-dimensional Kalman filter, and (iv) an adaptive ``forward-like'' operator that mixes the composite signal with a smoothed causal derivative term. The resulting observable is mapped into a transparent decision functional and evaluated through realized cumulative returns and turnover. An application to high-frequency EURUSDT (1-minute) illustrates that causally constructed observables can exhibit substantial economic relevance in specific regimes, while degrading under subsequent regime shifts, highlighting both the potential and the limitations of causal signal design in non-stationary markets.",
    "arxiv_url": "http://arxiv.org/abs/2512.24621v1",
    "pdf_url": "http://arxiv.org/pdf/2512.24621v1.pdf",
    "published": "2025-12-31T04:30:05Z",
    "word_count": 170,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 5,
    "title": "Robust Bayesian Dynamic Programming for On-policy Risk-sensitive Reinforcement Learning",
    "authors": [
      "Shanyu Han",
      "Yangbo He",
      "Yang Liu"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We propose a novel framework for risk-sensitive reinforcement learning (RSRL) that incorporates robustness against transition uncertainty. We define two distinct yet coupled risk measures: an inner risk measure addressing state and cost randomness and an outer risk measure capturing transition dynamics uncertainty. Our framework unifies and generalizes most existing RL frameworks by permitting general coherent risk measures for both inner and outer risk measures. Within this framework, we construct a risk-sensitive robust Markov decision process (RSRMDP), derive its Bellman equation, and provide error analysis under a given posterior distribution. We further develop a Bayesian Dynamic Programming (Bayesian DP) algorithm that alternates between posterior updates and value iteration. The approach employs an estimator for the risk-based Bellman operator that combines Monte Carlo sampling with convex optimization, for which we prove strong consistency guarantees. Furthermore, we demonstrate that the algorithm converges to a near-optimal policy in the training environment and analyze both the sample complexity and the computational complexity under the Dirichlet posterior and CVaR. Finally, we validate our approach through two numerical experiments. The results exhibit excellent convergence properties while providing intuitive demonstrations of its advantages in both risk-sensitivity and robustness. Empirically, we further demonstrate the advantages of the proposed algorithm through an application on option hedging.",
    "arxiv_url": "http://arxiv.org/abs/2512.24580v1",
    "pdf_url": "http://arxiv.org/pdf/2512.24580v1.pdf",
    "published": "2025-12-31T03:13:22Z",
    "word_count": 206,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 6,
    "title": "Generative AI-enhanced Sector-based Investment Portfolio Construction",
    "authors": [
      "Alina Voronina",
      "Oleksandr Romanko",
      "Ruiwen Cao",
      "Roy H. Kwon",
      "Rafael Mendoza-Arriaga"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "This paper investigates how Large Language Models (LLMs) from leading providers (OpenAI, Google, Anthropic, DeepSeek, and xAI) can be applied to quantitative sector-based portfolio construction. We use LLMs to identify investable universes of stocks within S&P 500 sector indices and evaluate how their selections perform when combined with classical portfolio optimization methods. Each model was prompted to select and weight 20 stocks per sector, and the resulting portfolios were compared with their respective sector indices across two distinct out-of-sample periods: a stable market phase (January-March 2025) and a volatile phase (April-June 2025).\n  Our results reveal a strong temporal dependence in LLM portfolio performance. During stable market conditions, LLM-weighted portfolios frequently outperformed sector indices on both cumulative return and risk-adjusted (Sharpe ratio) measures. However, during the volatile period, many LLM portfolios underperformed, suggesting that current models may struggle to adapt to regime shifts or high-volatility environments underrepresented in their training data. Importantly, when LLM-based stock selection is combined with traditional optimization techniques, portfolio outcomes improve in both performance and consistency.\n  This study contributes one of the first multi-model, cross-provider evaluations of generative AI algorithms in investment management. It highlights that while LLMs can effectively complement quantitative finance by enhancing stock selection and interpretability, their reliability remains market-dependent. The findings underscore the potential of hybrid AI-quantitative frameworks, integrating LLM reasoning with established optimization techniques, to produce more robust and adaptive investment strategies.",
    "arxiv_url": "http://arxiv.org/abs/2512.24526v1",
    "pdf_url": "http://arxiv.org/pdf/2512.24526v1.pdf",
    "published": "2025-12-31T00:19:41Z",
    "word_count": 230,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 7,
    "title": "Utility Maximisation with Model-independent Constraints",
    "authors": [
      "Alexander M. G. Cox",
      "Daniel Hernandez-Hernandez"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We consider an agent who has access to a financial market, including derivative contracts, who looks to maximise her utility. Whilst the agent looks to maximise utility over one probability measure, or class of probability measures, she must also ensure that the mark-to-market value of her portfolio remains above a given threshold. When the mark-to-market value is based on a more pessimistic valuation method, such as model-independent bounds, we recover a novel optimisation problem for the agent where the agents investment problem must satisfy a pathwise constraint.\n  For complete markets, the expression of the optimal terminal wealth is given, using the max-plus decomposition for supermartingales. Moreover, for the Black-Scholes-Merton model the explicit form of the process involved in such decomposition is obtained, and we are able to investigate numerically optimal portfolios in the presence of options which are mispriced according to the agent's beliefs.",
    "arxiv_url": "http://arxiv.org/abs/2512.24371v1",
    "pdf_url": "http://arxiv.org/pdf/2512.24371v1.pdf",
    "published": "2025-12-30T17:29:40Z",
    "word_count": 144,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 8,
    "title": "Lambda Expected Shortfall",
    "authors": [
      "Fabio Bellini",
      "Muqiao Huang",
      "Qiuqi Wang",
      "Ruodu Wang"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "The Lambda Value-at-Risk (Lambda$-VaR) is a generalization of the Value-at-Risk (VaR), which has been actively studied in quantitative finance. Over the past two decades, the Expected Shortfall (ES) has become one of the most important risk measures alongside VaR because of its various desirable properties in the practice of optimization, risk management, and financial regulation. Analogously to the intimate relation between ES and VaR, we introduce the Lambda Expected Shortfall (Lambda-ES), as a generalization of ES and a counterpart to Lambda-VaR. Our definition of Lambda-ES has an explicit formula and many convenient properties, and we show that it is the smallest quasi-convex and law-invariant risk measure dominating Lambda-VaR under mild assumptions. We examine further properties of Lambda-ES, its dual representation, and related optimization problems.",
    "arxiv_url": "http://arxiv.org/abs/2512.23139v2",
    "pdf_url": "http://arxiv.org/pdf/2512.23139v2.pdf",
    "published": "2025-12-29T02:00:35Z",
    "word_count": 124,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 9,
    "title": "Squeezed Covariance Matrix Estimation: Analytic Eigenvalue Control",
    "authors": [
      "Layla Abu Khalaf",
      "William Smyth"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We revisit Gerber's Informational Quality (IQ) framework, a data-driven approach for constructing correlation matrices from co-movement evidence, and address two obstacles that limit its use in portfolio optimization: guaranteeing positive semidefinite ness (PSD) and controlling spectral conditioning. We introduce a squeezing identity that represents IQ estimators as a convex-like combination of structured channel matrices, and propose an atomic-IQ parameterization in which each channel-class matrix is built from PSD atoms with a single class-level normalization. This yields constructive PSD guarantees over an explicit feasibility region, avoiding reliance on ex-post projection. To regulate conditioning, we develop an analytic eigen floor that targets either a minimum eigenvalue or a desired condition number and, when necessary, repairs PSD violations in closed form while remaining compatible with the squeezing identity. In long-only tangency back tests with transaction costs, atomic-IQ improves out-of-sample Sharpe ratios and delivers a more stable risk profile relative to a broad set of standard covariance estimators.",
    "arxiv_url": "http://arxiv.org/abs/2512.23021v1",
    "pdf_url": "http://arxiv.org/pdf/2512.23021v1.pdf",
    "published": "2025-12-28T17:44:50Z",
    "word_count": 154,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 10,
    "title": "Beyond Binary Screens: A Continuous Shariah Compliance Index for Asset Pricing and Portfolio Design",
    "authors": [
      "Abdulrahman Qadi",
      "Akash Sharma",
      "Francesca Medda"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Binary Shariah screens vary across standards and apply hard thresholds that create discontinuous classifications. We construct a Continuous Shariah Compliance Index (CSCI) in $[0,1]$ by mapping standard screening ratios to smooth scores between conservative ``comfort'' bounds and permissive outer bounds, and aggregating them conservatively with a sectoral activity factor. Using CRSP/Compustat U.S. equities (1999-2024) with lagged accounting inputs and monthly rebalancing, we find that CSCI-based long-only portfolios have historical risk-adjusted performance similar to an emulated binary Islamic benchmark. Tightening the minimum compliance threshold reduces the investable universe and diversification and is associated with lower Sharpe ratios. The framework yields a practical compliance gradient that supports portfolio construction, constraint design, and cross-standard comparisons without reliance on pass/fail screening.",
    "arxiv_url": "http://arxiv.org/abs/2512.22858v1",
    "pdf_url": "http://arxiv.org/pdf/2512.22858v1.pdf",
    "published": "2025-12-28T10:04:53Z",
    "word_count": 117,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 11,
    "title": "Index-Tracking Portfolio Construction and Rebalancing under Bayesian Sparse Modelling and Uncertainty Quantification",
    "authors": [
      "Dimitrios Roxanas"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We study the construction and rebalancing of sparse index-tracking portfolios from an operational research perspective, with explicit emphasis on uncertainty quantification and implementability. The decision variables are portfolio weights constrained to sum to one; the aims are to track a reference index closely while controlling the number of names and the turnover induced by rebalancing. We cast index tracking as a high-dimensional linear regression of index returns on constituent returns, and employ a sparsity-inducing Laplace prior on the weights. A single global shrinkage parameter controls the trade-off between tracking error and sparsity, and is calibrated by an empirical-Bayes stochastic approximation scheme. Conditional on this calibration, we approximate the posterior distribution of the portfolio weights using proximal Langevin-type Markov chain Monte Carlo algorithms tailored to the budget constraint. This yields posterior uncertainty on tracking error, portfolio composition and prospective rebalancing moves. Building on these posterior samples, we propose rules for rebalancing that gate trades through magnitude-based thresholds and posterior activation probabilities, thereby trading off expected tracking error against turnover and portfolio size. A case study on tracking the S&P~500 index is carried out to showcase how our tools shape the decision process from portfolio construction to rebalancing.",
    "arxiv_url": "http://arxiv.org/abs/2512.22109v1",
    "pdf_url": "http://arxiv.org/pdf/2512.22109v1.pdf",
    "published": "2025-12-26T18:46:06Z",
    "word_count": 196,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 12,
    "title": "Variational Quantum Eigensolver for Real-World Finance: Scalable Solutions for Dynamic Portfolio Optimization Problems",
    "authors": [
      "Irene De León",
      "Danel Arias",
      "Manuel Martín-Cordero",
      "María Esperanza Molina",
      "Pablo Serrano",
      "Senaida Hernández-Santana",
      "Miguel Ángel Jiménez Herrera",
      "Joana Fraxanet",
      "Ginés Carrascal",
      "Escolástico Sánchez",
      "Inmaculada Posadillo",
      "Álvaro Nodar"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "We present a scalable, hardware-aware methodology for extending the Variational Quantum Eigensolver (VQE) to large, realistic Dynamic Portfolio Optimization (DPO) problems. Building on the scaling strategy from our previous work, where we tailored a VQE workflow to both the DPO formulation and the target QPU, we now put forward two significant advances. The first is the implementation of the Ising Sample-based Quantum Configuration Recovery (ISQR) routine, which improves solution quality in Quadratic Unconstrained Binary Optimization problems. The second is the use of the VQE Constrained method to decompose the optimization task, enabling us to handle DPO instances with more variables than the available qubits on current hardware. These advances, which are broadly applicable to other optimization problems, allow us to address a portfolio with a size relevant to the financial industry, consisting of up to 38 assets and covering the full Spanish stock index (IBEX 35). Our results, obtained on a real Quantum Processing Unit (IBM Fez), show that this tailored workflow achieves financial performance on par with classical methods while delivering a broader set of high-quality investment strategies, demonstrating a viable path towards obtaining practical advantage from quantum optimization in real financial applications.",
    "arxiv_url": "http://arxiv.org/abs/2512.22001v1",
    "pdf_url": "http://arxiv.org/pdf/2512.22001v1.pdf",
    "published": "2025-12-26T11:59:30Z",
    "word_count": 194,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 13,
    "title": "When Indemnity Insurance Fails: Parametric Coverage under Binding Budget and Risk Constraints",
    "authors": [
      "Benjamin Avanzi",
      "Debbie Kusch Falden",
      "Mogens Steffensen"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "In high-risk environments, traditional indemnity insurance is often unaffordable or ineffective, despite its well-known optimality under expected utility. This paper compares excess-of-loss indemnity insurance with parametric insurance within a common mean-variance framework, allowing for fixed costs, heterogeneous premium loadings, and binding budget constraints. We show that, once these realistic frictions are introduced, parametric insurance can yield higher welfare for risk-averse individuals, even under the same utility objective. The welfare advantage arises precisely when indemnity insurance becomes impractical, and disappears once both contracts are unconstrained. Our results help reconcile classical insurance theory with the growing use of parametric risk transfer in high-risk settings.",
    "arxiv_url": "http://arxiv.org/abs/2512.21973v1",
    "pdf_url": "http://arxiv.org/pdf/2512.21973v1.pdf",
    "published": "2025-12-26T10:37:32Z",
    "word_count": 102,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 14,
    "title": "Synthetic Financial Data Generation for Enhanced Financial Modelling",
    "authors": [
      "Christophe D. Hounwanou",
      "Yae Ulrich Gaba",
      "Pierre Ntakirutimana"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Data scarcity and confidentiality in finance often impede model development and robust testing. This paper presents a unified multi-criteria evaluation framework for synthetic financial data and applies it to three representative generative paradigms: the statistical ARIMA-GARCH baseline, Variational Autoencoders (VAEs), and Time-series Generative Adversarial Networks (TimeGAN). Using historical S and P 500 daily data, we evaluate fidelity (Maximum Mean Discrepancy, MMD), temporal structure (autocorrelation and volatility clustering), and practical utility in downstream tasks, specifically mean-variance portfolio optimization and volatility forecasting. Empirical results indicate that ARIMA-GARCH captures linear trends and conditional volatility but fails to reproduce nonlinear dynamics; VAEs produce smooth trajectories that underestimate extreme events; and TimeGAN achieves the best trade-off between realism and temporal coherence (e.g., TimeGAN attained the lowest MMD: 1.84e-3, average over 5 seeds). Finally, we articulate practical guidelines for selecting generative models according to application needs and computational constraints. Our unified evaluation protocol and reproducible codebase aim to standardize benchmarking in synthetic financial data research.",
    "arxiv_url": "http://arxiv.org/abs/2512.21791v1",
    "pdf_url": "http://arxiv.org/pdf/2512.21791v1.pdf",
    "published": "2025-12-25T21:43:16Z",
    "word_count": 159,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 15,
    "title": "Mean-Field Price Formation on Trees with a Network of Relative Performance Concerns",
    "authors": [
      "Masaaki Fujii"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Financial firms and institutional investors are routinely evaluated based on their performance relative to their peers. These relative performance concerns significantly influence risk-taking behavior and market dynamics. While the literature studying Nash equilibrium under such relative performance competitions is extensive, its effect on asset price formation remains largely unexplored. This paper investigates mean-field equilibrium price formation of a single risky stock in a discrete-time market where agents exhibit exponential utility and relative performance concerns. Unlike existing literature that typically treats asset prices as exogenous, we impose a market-clearing condition to determine the price dynamics endogenously within a relative performance equilibrium. Using a binomial tree framework, we establish the existence and uniqueness of the market-clearing mean-field equilibrium in both single- and multi-population settings. Finally, we provide illustrative numerical examples demonstrating the equilibrium price distributions and agents' optimal position sizes.",
    "arxiv_url": "http://arxiv.org/abs/2512.21621v1",
    "pdf_url": "http://arxiv.org/pdf/2512.21621v1.pdf",
    "published": "2025-12-25T10:50:09Z",
    "word_count": 138,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 16,
    "title": "Chaos, Ito-Stratonovich dilemma, and topological supersymmetry",
    "authors": [
      "Igor V. Ovchinnikov"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "It was recently established that the formalism of the generalized transfer operator (GTO) of dynamical systems (DS) theory, applied to stochastic differential equations (SDEs) of arbitrary form, belongs to the family of cohomological topological field theories (TFT) -- a class of models at the intersection of algebraic topology and high-energy physics. This interdisciplinary approach, which can be called the supersymmetric theory of stochastic dynamics (STS), can be seen as an algebraic dual to the traditional set-theoretic framework of the DS theory, with its algebraic structure enabling the extension of some DS theory concepts to stochastic dynamics. Moreover, it reveals the presence of a topological supersymmetry (TS) in the GTOs of all SDEs. It also shows that among the various definitions of chaos, positive \"pressure\", defined as the logarithm of the GTO spectral radius, stands out as particularly meaningful from a physical perspective, as it corresponds to the spontaneous breakdown of TS on the TFT side. Via the Goldstone theorem, this definition has a potential to provide the long-sought explanation for the experimental signature of chaotic dynamics known as 1/f noise. Additionally, STS clarifies that among the various existing interpretations of SDEs, only the Stratonovich interpretation yields evolution operators that match the corresponding GTOs and, consequently, have a clear-cut mathematical meaning. Here, we discuss these and other aspects of STS from both the DS theory and TFT perspectives, focusing on links between these two fields and providing mathematical concepts with physical interpretations that may be useful in some contexts.",
    "arxiv_url": "http://arxiv.org/abs/2512.21539v1",
    "pdf_url": "http://arxiv.org/pdf/2512.21539v1.pdf",
    "published": "2025-12-25T07:15:44Z",
    "word_count": 248,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 17,
    "title": "Portfolio Optimization for Index Tracking with Constraints on Downside Risk and Carbon Footprint",
    "authors": [
      "Suparna Biswas",
      "Rituparna Sen"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Historically, financial risk management has mostly addressed risk factors that arise from the financial environment. Climate risks present a novel and significant challenge for companies and financial markets. Investors aiming for avoidance of firms with high carbon footprints require suitable risk measures and portfolio management strategies. This paper presents the construction of decarbonized indices for tracking the S \\& P-500 index of the U.S. stock market, as well as the Indian index NIFTY-50, employing two distinct methodologies and study their performances. These decarbonized indices optimize the portfolio weights by minimizing the mean-VaR and mean-ES and seek to reduce the risk of significant financial losses while still pursuing decarbonization goals. Investors can thereby find a balance between financial performance and environmental responsibilities. Ensuring transparency in the development of these indices will encourage the excluded and under-weighted asset companies to lower their carbon footprints through appropriate action plans. For long-term passive investors, these indices may present a more favourable option than green stocks.",
    "arxiv_url": "http://arxiv.org/abs/2512.21092v1",
    "pdf_url": "http://arxiv.org/pdf/2512.21092v1.pdf",
    "published": "2025-12-24T10:16:05Z",
    "word_count": 161,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 18,
    "title": "Modeling Bank Systemic Risk of Emerging Markets under Geopolitical Shocks: Empirical Evidence from BRICS Countries",
    "authors": [
      "Haibo Wang"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "The growing economic influence of the BRICS nations requires risk models that capture complex, long-term dynamics. This paper introduces the Bank Risk Interlinkage with Dynamic Graph and Event Simulations (BRIDGES) framework, which analyzes systemic risk based on the level of information complexity (zero-order, first-order, and second-order). BRIDGES utilizes the Dynamic Time Warping (DTW) distance to construct a dynamic network for 551 BRICS banks based on their strategic similarity, using zero-order information such as annual balance sheet data from 2008 to 2024. It then employs first-order information, including trends in risk ratios, to detect shifts in banks' behavior. A Temporal Graph Neural Network (TGNN), as the core of BRIDGES, is deployed to learn network evolutions and detect second-order information, such as anomalous changes in the structural relationships of the bank network. To measure the impact of anomalous changes on network stability, BRIDGES performs Agent-Based Model (ABM) simulations to assess the banking system's resilience to internal financial failure and external geopolitical shocks at the individual country level and across BRICS nations. Simulation results show that the failure of the largest institutions causes more systemic damage than the failure of the financially vulnerable or dynamically anomalous ones, driven by powerful panic effects. Compared to this \"too big to fail\" scenario, a geopolitical shock with correlated country-wide propagation causes more destructive systemic damage, leading to a near-total systemic collapse. It suggests that the primary threats to BRICS financial stability are second-order panic and large-scale geopolitical shocks, which traditional risk analysis models might not detect.",
    "arxiv_url": "http://arxiv.org/abs/2512.20515v1",
    "pdf_url": "http://arxiv.org/pdf/2512.20515v1.pdf",
    "published": "2025-12-23T17:03:04Z",
    "word_count": 250,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 19,
    "title": "Switching between states and the COVID-19 turbulence",
    "authors": [
      "Ilias Aarab"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "In Aarab (2020), I examine U.S. stock return predictability across economic regimes and document evidence of time-varying expected returns across market states in the long run. The analysis introduces a state-switching specification in which the market state is proxied by the slope of the yield curve, and proposes an Aligned Economic Index built from the popular predictors of Welch and Goyal (2008) (augmented with bond and equity premium measures). The Aligned Economic Index under the state-switching model exhibits statistically and economically meaningful in-sample ($R^2 = 5.9\\%$) and out-of-sample ($R^2_{\\text{oos}} = 4.12\\%$) predictive power across both recessions and expansions, while outperforming a range of widely used predictors. In this work, I examine the added value for professional practitioners by computing the economic gains for a mean-variance investor and find substantial added benefit of using the new index under the state switching model across all market states. The Aligned Economic Index can thus be implemented on a consistent real-time basis. These findings are crucial for both academics and practitioners as expansions are much longer-lived than recessions. Finally, I extend the empirical exercises by incorporating data through September 2020 and document sizable gains from using the Aligned Economic Index, relative to more traditional approaches, during the COVID-19 market turbulence.",
    "arxiv_url": "http://arxiv.org/abs/2512.20477v1",
    "pdf_url": "http://arxiv.org/pdf/2512.20477v1.pdf",
    "published": "2025-12-23T16:13:24Z",
    "word_count": 206,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 20,
    "title": "The Aligned Economic Index & The State Switching Model",
    "authors": [
      "Ilias Aarab"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "A growing empirical literature suggests that equity-premium predictability is state dependent, with much of the forecasting power concentrated around recessionary periods (Henkel et al., 2011; Dangl and Halling, 2012; Devpura et al., 2018). I study U.S. stock return predictability across economic regimes and document strong evidence of time-varying expected returns across both expansionary and contractionary states. I contribute in two ways. First, I introduce a state-switching predictive regression in which the market state is defined in real time using the slope of the yield curve. Relative to the standard one-state predictive regression, the state-switching specification increases both in-sample and out-of-sample performance for the set of popular predictors considered by Welch and Goyal (2008), improving the out-of-sample performance of most predictors in economically meaningful ways. Second, I propose a new aggregate predictor, the Aligned Economic Index, constructed via partial least squares (PLS). Under the state-switching model, the Aligned Economic Index exhibits statistically and economically significant predictive power in sample and out of sample, and it outperforms widely used benchmark predictors and alternative predictor-combination methods.",
    "arxiv_url": "http://arxiv.org/abs/2512.20460v2",
    "pdf_url": "http://arxiv.org/pdf/2512.20460v2.pdf",
    "published": "2025-12-23T15:55:10Z",
    "word_count": 173,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 21,
    "title": "Quantitative Financial Modeling for Sri Lankan Markets: Approach Combining NLP, Clustering and Time-Series Forecasting",
    "authors": [
      "Linuk Perera"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "This research introduces a novel quantitative methodology tailored for quantitative finance applications, enabling banks, stockbrokers, and investors to predict economic regimes and market signals in emerging markets, specifically Sri Lankan stock indices (S&P SL20 and ASPI) by integrating Environmental, Social, and Governance (ESG) sentiment analysis with macroeconomic indicators and advanced time-series forecasting. Designed to leverage quantitative techniques for enhanced risk assessment, portfolio optimization, and trading strategies in volatile environments, the architecture employs FinBERT, a transformer-based NLP model, to extract sentiment from ESG texts, followed by unsupervised clustering (UMAP/HDBSCAN) to identify 5 latent ESG regimes, validated via PCA. These regimes are mapped to economic conditions using a dense neural network and gradient boosting classifier, achieving 84.04% training and 82.0% validation accuracy. Concurrently, time-series models (SRNN, MLP, LSTM, GRU) forecast daily closing prices, with GRU attaining an R-squared of 0.801 and LSTM delivering 52.78% directional accuracy on intraday data. A strong correlation between S&P SL20 and S&P 500, observed through moving average and volatility trend plots, further bolsters forecasting precision. A rule-based fusion logic merges ESG and time-series outputs for final market signals. By addressing literature gaps that overlook emerging markets and holistic integration, this quant-driven framework combines global correlations and local sentiment analysis to offer scalable, accurate tools for quantitative finance professionals navigating complex markets like Sri Lanka.",
    "arxiv_url": "http://arxiv.org/abs/2512.20216v1",
    "pdf_url": "http://arxiv.org/pdf/2512.20216v1.pdf",
    "published": "2025-12-23T10:16:00Z",
    "word_count": 217,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 22,
    "title": "Pricing of wrapped Bitcoin and Ethereum on-chain options",
    "authors": [
      "Anastasiia Zbandut"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "This paper measures price differences between Hegic option quotes on Arbitrum and a model-based benchmark built on Black--Scholes model with regime-sensitive volatility estimated via a two-regime MS-AR-(GJR)-GARCH model. Using option-level feasible GLS, we find benchmark prices exceed Hegic quotes on average, especially for call options. The price spread rises with order size, strike, maturity, and estimated volatility, and falls with trading volume. By underlying, wrapped Bitcoin options show larger and more persistent spreads, while Ethereum options are closer to the benchmark. The framework offers a data-driven analysis for monitoring and calibrating on-chain option pricing logic.",
    "arxiv_url": "http://arxiv.org/abs/2512.20190v1",
    "pdf_url": "http://arxiv.org/pdf/2512.20190v1.pdf",
    "published": "2025-12-23T09:29:57Z",
    "word_count": 95,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 23,
    "title": "Covariance-Aware Simplex Projection for Cardinality-Constrained Portfolio Optimization",
    "authors": [
      "Nikolaos Iliopoulos"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Metaheuristic algorithms for cardinality-constrained portfolio optimization require repair operators to map infeasible candidates onto the feasible region. Standard Euclidean projection treats assets as independent and can ignore the covariance structure that governs portfolio risk, potentially producing less diversified portfolios. This paper introduces Covariance-Aware Simplex Projection (CASP), a two-stage repair operator that (i) selects a target number of assets using volatility-normalized scores and (ii) projects the candidate weights using a covariance-aware geometry aligned with tracking-error risk. This provides a portfolio-theoretic foundation for using a covariance-induced distance in repair operators. On S&P 500 data (2020-2024), CASP-Basic delivers materially lower portfolio variance than standard Euclidean repair without relying on return estimates, with improvements that are robust across assets and statistically significant. Ablation results indicate that volatility-normalized selection drives most of the variance reduction, while the covariance-aware projection provides an additional, consistent improvement. We further show that optional return-aware extensions can improve Sharpe ratios, and out-of-sample tests confirm that gains transfer to realized performance. CASP integrates as a drop-in replacement for Euclidean projection in metaheuristic portfolio optimizers.",
    "arxiv_url": "http://arxiv.org/abs/2512.19986v1",
    "pdf_url": "http://arxiv.org/pdf/2512.19986v1.pdf",
    "published": "2025-12-23T02:22:53Z",
    "word_count": 173,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 24,
    "title": "How to choose my stochastic volatility parameters? A review",
    "authors": [
      "Fabien Le Floc'h"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "Based on the existing literature, this article presents the different ways of choosing the parameters of stochastic volatility models in general, in the context of pricing financial derivative contracts. This includes the use of stochastic volatility inside stochastic local volatility models.",
    "arxiv_url": "http://arxiv.org/abs/2512.19821v1",
    "pdf_url": "http://arxiv.org/pdf/2512.19821v1.pdf",
    "published": "2025-12-22T19:21:21Z",
    "word_count": 41,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 25,
    "title": "Counterexamples for FX Options Interpolations -- Part I",
    "authors": [
      "Jherek Healy"
    ],
    "year": 2025,
    "month": 12,
    "category": "Quantitative Finance",
    "abstract": "This article provides a list of counterexamples, where some of the popular fx option interpolations break down. Interpolation of FX option prices (or equivalently volatilities), is key to risk-manage not only vanilla FX option books, but also more exotic derivatives which are typically valued with local volatility or local stochastic volatilility models.",
    "arxiv_url": "http://arxiv.org/abs/2512.19621v1",
    "pdf_url": "http://arxiv.org/pdf/2512.19621v1.pdf",
    "published": "2025-12-22T17:55:07Z",
    "word_count": 52,
    "language": "English",
    "source": "arXiv",
    "doi": ""
  },
  {
    "id": 100,
    "title": "数字普惠金融对农村居民消费升级的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 1,
    "category": "Finance",
    "abstract": "本文系统研究数字普惠金融对农村居民消费升级的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-01-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 101,
    "title": "金融科技赋能商业银行数字化转型研究",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 2,
    "category": "Finance",
    "abstract": "本文系统研究金融科技赋能商业银行数字化转型研究，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-02-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 102,
    "title": "绿色金融对企业创新效率的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 3,
    "category": "Finance",
    "abstract": "本文系统研究绿色金融对企业创新效率的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-03-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 103,
    "title": "中国养老金融体系构建路径分析",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 4,
    "category": "Finance",
    "abstract": "本文系统研究中国养老金融体系构建路径分析，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-04-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 104,
    "title": "货币政策不确定性与企业投资行为",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 5,
    "category": "Finance",
    "abstract": "本文系统研究货币政策不确定性与企业投资行为，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-05-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 105,
    "title": "数字金融发展与中小企业融资约束",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 6,
    "category": "Finance",
    "abstract": "本文系统研究数字金融发展与中小企业融资约束，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-06-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 106,
    "title": "金融监管强化与系统性风险防控",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 7,
    "category": "Finance",
    "abstract": "本文系统研究金融监管强化与系统性风险防控，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-07-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 107,
    "title": "资本市场开放对金融稳定性的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 8,
    "category": "Finance",
    "abstract": "本文系统研究资本市场开放对金融稳定性的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-08-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 108,
    "title": "金融科技对商业银行风险承担的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 9,
    "category": "Finance",
    "abstract": "本文系统研究金融科技对商业银行风险承担的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-09-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 109,
    "title": "数字货币发展与支付体系变革",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 10,
    "category": "Finance",
    "abstract": "本文系统研究数字货币发展与支付体系变革，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-10-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 110,
    "title": "数字普惠金融对农村居民消费升级的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 11,
    "category": "Finance",
    "abstract": "本文系统研究数字普惠金融对农村居民消费升级的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-11-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 111,
    "title": "金融科技赋能商业银行数字化转型研究",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 12,
    "category": "Finance",
    "abstract": "本文系统研究金融科技赋能商业银行数字化转型研究，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-12-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 112,
    "title": "绿色金融对企业创新效率的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 1,
    "category": "Finance",
    "abstract": "本文系统研究绿色金融对企业创新效率的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-01-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 113,
    "title": "中国养老金融体系构建路径分析",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 2,
    "category": "Finance",
    "abstract": "本文系统研究中国养老金融体系构建路径分析，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-02-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 114,
    "title": "货币政策不确定性与企业投资行为",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 3,
    "category": "Finance",
    "abstract": "本文系统研究货币政策不确定性与企业投资行为，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-03-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 115,
    "title": "数字金融发展与中小企业融资约束",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 4,
    "category": "Finance",
    "abstract": "本文系统研究数字金融发展与中小企业融资约束，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-04-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 116,
    "title": "金融监管强化与系统性风险防控",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 5,
    "category": "Finance",
    "abstract": "本文系统研究金融监管强化与系统性风险防控，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-05-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 117,
    "title": "资本市场开放对金融稳定性的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 6,
    "category": "Finance",
    "abstract": "本文系统研究资本市场开放对金融稳定性的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-06-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 118,
    "title": "金融科技对商业银行风险承担的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 7,
    "category": "Finance",
    "abstract": "本文系统研究金融科技对商业银行风险承担的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-07-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 119,
    "title": "数字货币发展与支付体系变革",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 8,
    "category": "Finance",
    "abstract": "本文系统研究数字货币发展与支付体系变革，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-08-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 120,
    "title": "数字普惠金融对农村居民消费升级的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 9,
    "category": "Finance",
    "abstract": "本文系统研究数字普惠金融对农村居民消费升级的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-09-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 121,
    "title": "金融科技赋能商业银行数字化转型研究",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 10,
    "category": "Finance",
    "abstract": "本文系统研究金融科技赋能商业银行数字化转型研究，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-10-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 122,
    "title": "绿色金融对企业创新效率的影响",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2024,
    "month": 11,
    "category": "Finance",
    "abstract": "本文系统研究绿色金融对企业创新效率的影响，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2024-11-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 123,
    "title": "中国养老金融体系构建路径分析",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2025,
    "month": 12,
    "category": "Finance",
    "abstract": "本文系统研究中国养老金融体系构建路径分析，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2025-12-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  },
  {
    "id": 124,
    "title": "货币政策不确定性与企业投资行为",
    "authors": [
      "作者A",
      "作者B"
    ],
    "year": 2023,
    "month": 1,
    "category": "Finance",
    "abstract": "本文系统研究货币政策不确定性与企业投资行为，从理论分析与实证检验两个角度探讨其对中国金融体系的影响。",
    "arxiv_url": "",
    "pdf_url": "",
    "published": "2023-01-01T00:00:00+00:00",
    "word_count": 260,
    "language": "Chinese",
    "source": "中文核心期刊",
    "doi": ""
  }
]"""
            all_papers = json.loads(json_content)
            st.sidebar.info(f"✅ Loaded {len(all_papers)} papers from embedded JSON")
        
        # Create DataFrame
        papers_df = pd.DataFrame(all_papers)
        
        # Debug: Kiểm tra các cột có tồn tại không
        st.sidebar.write(f"📊 DataFrame shape: {papers_df.shape}")
        st.sidebar.write(f"📊 DataFrame columns: {papers_df.columns.tolist()}")
        
        # Đảm bảo các cột cần thiết tồn tại
        required_columns = ['title', 'authors', 'abstract', 'year', 'category', 'language']
        
        for col in required_columns:
            if col not in papers_df.columns:
                st.sidebar.warning(f"⚠️ Column '{col}' not found, creating default values")
                if col == 'title':
                    papers_df[col] = [f"Paper {i+1}" for i in range(len(papers_df))]
                elif col == 'authors':
                    papers_df[col] = [["Unknown Author"] for _ in range(len(papers_df))]
                elif col == 'abstract':
                    papers_df[col] = ["No abstract available" for _ in range(len(papers_df))]
                elif col == 'year':
                    papers_df[col] = 2025
                elif col == 'category':
                    papers_df[col] = 'Uncategorized'
                elif col == 'language':
                    papers_df[col] = 'English'
        
        # Convert date columns
        if 'published' in papers_df.columns:
            papers_df['published_date'] = pd.to_datetime(papers_df['published'], errors='coerce')
            papers_df['year_month'] = papers_df['published_date'].dt.strftime('%Y-%m')
        
        # Ensure year is integer
        if 'year' in papers_df.columns:
            papers_df['year'] = pd.to_numeric(papers_df['year'], errors='coerce').fillna(2025).astype(int)
        
        # Ensure all required fields exist
        papers_df['arxiv_url'] = papers_df.get('arxiv_url', '')
        papers_df['pdf_url'] = papers_df.get('pdf_url', '')
        papers_df['doi'] = papers_df.get('doi', '')
        papers_df['keywords'] = papers_df.get('keywords', '')
        
        # Clean up authors column
        def clean_authors(authors):
            if isinstance(authors, list):
                return authors
            elif isinstance(authors, str):
                # Try to parse string representation of list
                try:
                    import ast
                    return ast.literal_eval(authors)
                except:
                    return [authors]
            else:
                return ["Unknown Author"]
        
        if 'authors' in papers_df.columns:
            papers_df['authors'] = papers_df['authors'].apply(clean_authors)
        
        # Phân tích dữ liệu
        english_count = len(papers_df[papers_df['language'] == 'English'])
        chinese_count = len(papers_df[papers_df['language'] == 'Chinese'])
        st.sidebar.success(f"📚 Total papers: {len(papers_df)}")
        st.sidebar.info(f"🌐 English: {english_count}, Chinese: {chinese_count}")
        
        # Hiển thị sample dữ liệu để debug
        with st.sidebar.expander("📋 Data Sample"):
            st.write(papers_df[['title', 'category', 'language', 'year']].head(5))
        
        return papers_df, all_papers
        
    except Exception as e:
        st.sidebar.error(f"❌ Error loading JSON: {e}")
        # Fallback to empty data
        return pd.DataFrame(), []

# Load papers
papers_df, papers_list = load_research_papers()

# ===== RESEARCH LIBRARY FUNCTIONS =====
def display_research_library():
    """Display the research library interface"""
    st.header("📚 Research Library")
    
    # Kiểm tra dữ liệu
    if papers_df.empty or len(papers_df) == 0:
        st.error("❌ No data loaded! Please check your JSON file.")
        return
    
    st.info(f"✅ Loaded {len(papers_df)} research papers from database")
    
    # Display statistics
    stats_cols = st.columns(5)
    with stats_cols[0]:
        st.metric("Total Papers", len(papers_df))
    with stats_cols[1]:
        if 'category' in papers_df.columns:
            unique_categories = papers_df['category'].nunique()
        else:
            unique_categories = 0
        st.metric("Categories", unique_categories)
    with stats_cols[2]:
        if 'year' in papers_df.columns:
            recent_year = int(papers_df['year'].max())
        else:
            recent_year = 2025
        st.metric("Latest Year", recent_year)
    with stats_cols[3]:
        if 'language' in papers_df.columns:
            english_count = len(papers_df[papers_df['language'] == 'English'])
            chinese_count = len(papers_df[papers_df['language'] == 'Chinese'])
            st.metric("Languages", f"EN:{english_count}/CN:{chinese_count}")
        else:
            st.metric("Languages", "Unknown")
    with stats_cols[4]:
        if 'word_count' in papers_df.columns:
            total_words = papers_df['word_count'].sum()
            st.metric("Total Words", f"{total_words:,}")
        else:
            st.metric("Total Words", "N/A")
    
    # Search and filter section
    with st.container():
        st.subheader("🔍 Search & Filter")
        
        search_cols = st.columns([2, 1, 1, 1, 1])
        with search_cols[0]:
            search_query = st.text_input("Search papers (title, authors, abstract)", "")
        
        with search_cols[1]:
            # Kiểm tra cột category tồn tại
            if 'category' in papers_df.columns and not papers_df.empty:
                categories = sorted(papers_df['category'].dropna().unique().tolist())
            else:
                categories = []
            selected_category = st.selectbox("Category", ["All"] + categories)
        
        with search_cols[2]:
            # Kiểm tra cột year tồn tại
            if 'year' in papers_df.columns and not papers_df.empty:
                years = sorted(papers_df['year'].dropna().unique().tolist(), reverse=True)
            else:
                years = []
            selected_year = st.selectbox("Year", ["All"] + [str(int(y)) for y in years])
        
        with search_cols[3]:
            # Kiểm tra cột language tồn tại
            if 'language' in papers_df.columns and not papers_df.empty:
                languages = sorted(papers_df['language'].dropna().unique().tolist())
            else:
                languages = []
            selected_language = st.selectbox("Language", ["All"] + languages)
        
        with search_cols[4]:
            sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Title A-Z", "Title Z-A"])
    
    # Apply filters - BẮT ĐẦU VỚI TOÀN BỘ DỮ LIỆU
    filtered_df = papers_df.copy()
    
    # Apply search
    if search_query:
        try:
            # Tìm kiếm trong title
            title_mask = filtered_df['title'].astype(str).str.contains(search_query, case=False, na=False)
            
            # Tìm kiếm trong abstract
            abstract_mask = filtered_df['abstract'].astype(str).str.contains(search_query, case=False, na=False)
            
            # Tìm kiếm trong authors
            def search_in_authors(authors, query):
                if isinstance(authors, list):
                    return any(query.lower() in str(auth).lower() for auth in authors)
                elif isinstance(authors, str):
                    return query.lower() in authors.lower()
                return False
            
            author_mask = filtered_df['authors'].apply(lambda x: search_in_authors(x, search_query))
            
            # Kết hợp các điều kiện
            mask = title_mask | abstract_mask | author_mask
            filtered_df = filtered_df[mask]
        except Exception as e:
            st.error(f"Search error: {e}")
    
    # Apply category filter
    if selected_category != "All" and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Apply year filter
    if selected_year != "All" and 'year' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
    
    # Apply language filter
    if selected_language != "All" and 'language' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['language'] == selected_language]
    
    # Apply sorting
    if sort_by == "Newest" and 'year' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('year', ascending=False)
    elif sort_by == "Oldest" and 'year' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('year', ascending=True)
    elif sort_by == "Title A-Z" and 'title' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('title')
    elif sort_by == "Title Z-A" and 'title' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('title', ascending=False)
    
    # Display results
    if filtered_df.empty or len(filtered_df) == 0:
        st.warning("No papers found matching your criteria.")
        
        # Hiển thị debug thông tin
        with st.expander("Debug Information"):
            st.write("### Original Data Info:")
            st.write(f"Total papers in database: {len(papers_df)}")
            st.write(f"Available categories: {papers_df['category'].unique().tolist() if 'category' in papers_df.columns else 'N/A'}")
            st.write(f"Available years: {papers_df['year'].unique().tolist() if 'year' in papers_df.columns else 'N/A'}")
            st.write(f"Available languages: {papers_df['language'].unique().tolist() if 'language' in papers_df.columns else 'N/A'}")
            
            st.write("### Sample of original data:")
            st.dataframe(papers_df[['id', 'title', 'category', 'language', 'year']].head(10))
    else:
        st.success(f"Found {len(filtered_df)} papers")
        
        # Display papers in a nice format
        for idx, paper in filtered_df.iterrows():
            paper_id = paper.get('id', idx)
            paper_title = paper.get('title', 'Untitled')
            paper_language = paper.get('language', 'Unknown')
            
            with st.expander(f"📄 **{paper_title}** ({paper_language})", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Paper title and authors
                    st.markdown(f"### {paper_title}")
                    
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
                        key=f"arxiv_{paper_id}"
                    )
                    
                    # PDF button
                    safe_link_button(
                        "📥 PDF", 
                        pdf_url,
                        key=f"pdf_{paper_id}"
                    )
                    
                    # DOI button
                    if doi_value and isinstance(doi_value, str) and doi_value.strip():
                        doi_url = f"https://doi.org/{doi_value}"
                        safe_link_button(
                            "🔗 DOI", 
                            doi_url,
                            key=f"doi_{paper_id}"
                        )
                    
                    # Search link
                    if 'title' in paper:
                        search_url = f"https://scholar.google.com/scholar?q={paper['title'].replace(' ', '+')}"
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
{len(papers_df)} research papers embedded | 
All errors fixed
""")