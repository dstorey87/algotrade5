# AlgoTradePro5: AI-Driven Trading Application

## Variables, APIs, Keys, Sensitive information

All variables, should be mapped to the .env file in the root of the project, this ensures we alwayss know where to look for values in the event of an issue, and we are able to customize the app simply by editing values within here.

## Rule 1

Commit and push changes to feature branches every milestone, i.e. refactoring, new component, verified core component fix, test successes.

Keep the time between commits short as not to lose context.

## Rule 2

Keep workspace clean! 

Always clear up after your changes, redundant files to be deleted (after a commit only), structure files and code cleanly in folders, ensure integration at all times, any unintegrated files are considered rogue and to be removed.

Github repo: https://github.com/dstorey87/algotrade5

## Rule 3

Testing, should always be built in to the code, or code built with it in mind

No new code should be considered complete without a test to confirm the validity of it. Check further down for clearer instructions on how to do this.

## 1. Overview

AlgoTradePro5 is an AI-driven cryptocurrency trading system built on the FreqTrade framework. Its primary objective is to transform an initial £10 investment into £1000 within one week. This is achieved through continuous AI-powered strategy refinement, machine learning (ML), large language models (LLMs), and rigorous quantum loop backtesting.

**Audience:** GitHub Copilot will act as the sole developer, responsible for creating, maintaining, and updating this system. All processes, changes, and documentation updates are to be automated where possible.

### Commands:
All commands should use Powershell by default, we are running Windows 11 as the host system, be mindful of this

---

## 2. Project Scope & Constraints

- Initial Capital: £10
- Profit Target: £1000 in 7 days
- Win Rate Target: 85%
- GitHub Copilot: Exclusive developer and documenter
- Strict Use of AI Models: Pre-downloaded models in `C:\AlgoTradPro5\models`
- Talib is banned; Pandas is the preferred library for indicators
- Open-source software and free tools only
- Dockerized architecture for portability and consistency

---

## 3. Documentation & Change Management

### Critical Files

- `architecture-analysis.md`: System architecture, design decisions
- `integration-guide.md`: Integration steps and dependencies
- `journal.md`: Append-only log of all changes with reasons and timestamps

### Git & Version Control

- Every change requires immediate commit with clear messages
- Automated journaling for every code modification

---

AlgoTradePro5
├── architecture-analysis.md
├── integration-guide.md
├── config.json
├── freqai_config.json
├── models
│   ├── llm
│   │   ├── deepseek
│   │   ├── mistral
│   │   ├── mixtral
│   │   └── qwen
│   └── ml
│       ├── cibrx
│       ├── deepseek_v2
│       ├── mistral_trading
│       ├── phi-1.5
│       ├── phi-2
│       ├── stablelm-zephyr-3b
│       ├── openchat
│       └── quantum
├── docker-compose.yml
├── trade_logs
├── data (SQL databases)
├── frontend (Claude 3.5/3.7 optimized frontend)
├── README.md
└── journal.md
```

---

## 5. Installation & Setup Guide

### Step 1: Environment Setup

- Install Docker Desktop: [Docker Desktop Download](https://www.docker.com/products/docker-desktop)
- Confirm Docker installation: `docker --version`

### Step 2: FreqTrade Installation

```bash
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
docker-compose up -d
```

### Step 3: FreqAI Installation

```bash
pip install freqai
```

- Ensure models are only loaded from `C:\AlgoTradPro5\models`

---

## 6. Data Management

- **SQL Database Only** for all data types (historical, real-time, and future)
- Avoid any transient or non-persistent data
- Tables to include: `historical_prices`, `pair_metrics`, `quantum_loop_results`, `optimization_history`, `paper_trades`, `expanded_strategies`

### Data Preprocessing & Cleansing

#### Overview

Effective data preprocessing is critical to ensure the quality and reliability of inputs fed into ML/LLM models. The pipeline must be designed to handle missing data, outliers, and data normalization efficiently.

#### Handling Outliers

- Use FreqAI's built-in outlier detection methods:
  - **Dissimilarity Index (DI)**: Monitors prediction uncertainty and flags outliers.
  - **Support Vector Machine (SVM)**: One-class SVM to identify anomalies.
  - **DBSCAN Clustering**: Identifies noise and isolates it from valid data clusters.
- These methods can be configured directly in `freqai` settings to automate outlier management.

#### Handling Missing Data

- Apply imputation techniques:
  - **Mean/Median Imputation**: Fill missing values with statistical averages.
  - **Multiple Imputation (MICE)**: More sophisticated estimation for missing values.
- Integrate scikit-learn's `SimpleImputer` within preprocessing pipelines to automate missing data handling.

#### Data Normalization

- Standardize features to ensure uniform input scales:
  - **Min-Max Scaling**: Normalize features to a [0, 1] range.
  - **Standard Scaling**: Zero mean and unit variance for features.
- Ensures that ML/LLM models process all inputs consistently.

#### Integration with FreqTrade & FreqAI

- Define custom preprocessing transformers in the FreqAI feature pipeline.
- Configure preprocessing to run in real-time for streaming data and historical data sets.
- Ensure full compatibility with SQL data storage and Dockerized deployment.

#### Continuous Monitoring & Feedback

- Implement automated monitoring of data quality metrics.
- Logs for data anomalies, cleaning operations, and preprocessing steps.
- Incorporate feedback loops from ML/LLM models to refine preprocessing strategies continuously.

---

## 7. AI Models and Roles

### Machine Learning (ML)

- Predictive analytics, risk assessments
- Strategy development & backtesting

### Large Language Models (LLMs)

- Human-readable strategy explanations
- Automated journaling
- Error handling & optimization recommendations

---

## 8. Risk Management & Capital Allocation

### Position Sizing Techniques

- **Fixed Fractional**: 1-2% per trade (e.g., £0.10 - £0.20 on £10)
- **Kelly Criterion**:

```
f* = p - (1 - p) / b
```

- Where:
  - `f*` = fraction of capital to risk
  - `p` = probability of win
  - `b` = win/loss ratio

### Stop-Loss Mechanisms

- **Fixed Stop-Loss**
- **Trailing Stop-Loss**
- **Volatility-Based Stop-Loss** (e.g., ATR)

### Drawdown Limits

- Max risk per trade: 1-2%
- Hard Drawdown Cap: 10% of total equity. Auto halt.

### Hard Stop Enforcement

- Constraints coded in AI/ML logic
- AI/ML cannot bypass risk management rules
- Real-time monitoring & alert system
- Manual intervention needed to resume after breaches

---

## 9. Quantum Loop Strategy Execution

- Continuous forward/backward testing of strategies
- Catalogue winning trades; test under different conditions
- Transition validated strategies to paper trading
- Post-paper trading, strategies move to live trading
- Autonomous LLM expands strategies and fetches data as required

---

## 10. Frontend Development

- Build human-readable web interface optimized for Claude 3.5/3.7
- Key Features:
  - Trade execution control
  - Visualization of strategy performance
  - Access to trade logs and dashboards

---

## 11. Code Validation & Continuous Integration

- Automated validation scripts to check for unintegrated or redundant code
- Enforced documentation updates in `architecture-analysis.md` & `integration-guide.md`
- Continuous GitHub commits and changelog maintenance

---

## 12. Monitoring & Validation

- Nightly validation scripts (code, data integrity)
- SQL dashboard monitoring:
  - Pair health metrics
  - Strategy success rates
  - Drawdown levels
  - Quantum loop performance

#### Solution Approach

- **Trade Failures**:

  - Implement error-handling mechanisms within FreqTrade's strategy scripts to log and monitor unsuccessful trades.
  - Utilize FreqTrade's built-in logging system to capture exceptions and anomalies during trade execution.

- **API Connection Issues**:

  - Leverage FreqTrade's REST API and monitor endpoints such as `/api/v1/ping` to verify exchange connectivity.
  - Implement retry mechanisms and raise alerts for persistent connection failures.

- **Unusual Drawdowns**:

  - Configure FreqTrade's MaxDrawdown protection to halt trading when drawdowns exceed predefined thresholds.
  - Regularly monitor account balance and equity curve through SQL dashboards.

#### Push Notification Methods

- **Slack Notifications**:

  - Integrate FreqTrade webhook configuration to send real-time alerts to Slack channels when critical events occur.
  - Use Claude 3.5/3.7 for generating Slack integration code optimized for the Windows environment.

- **Email Notifications**:

  - Integrate Apprise notification library to send email alerts on predefined critical events.
  - Ensure the system works seamlessly on Windows and within Docker containers.

#### Implementation Considerations

- Ensure all monitoring scripts and integrations are compatible with the Windows OS.
- Utilize Claude 3.5/3.7 to generate error-handling routines, API monitoring scripts, and integration code.
- Simulate trade failures, API disruptions, and drawdowns during testing phases to verify alert accuracy and timeliness.
  - Pair health metrics
  - Strategy success rates
  - Drawdown levels
  - Quantum loop performance

---

## 13. Outstanding Tasks

###

### LLM Feedback Reinforcement Learning

- Incorporate reinforcement learning from human feedback (RLHF) or scoring to improve LLM decision-making over time.

### Scalability Considerations

- Add potential for scaling across multiple exchanges, accounts, or with increased capital after initial success.

-

---

## 14. Reference

- This README.md is the master reference
- All architectural, strategic, and implementation details are managed here
