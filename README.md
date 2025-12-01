# Agno Multi-Agent Customer Intelligence System

A **multi-agent architecture** built using **Agno**, designed to analyze customer datasets, extract insights, and generate business strategies and reports.

This project demonstrates how specialized agents can collaborate to form a complete analytical intelligence pipeline — from raw statistics to actionable recommendations.

---

## 1. Project Overview

This project is a **full-scale multi-agent system** powered by **Agno**, capable of:

- Running statistical queries on tabular customer datasets  
- Converting raw numbers into meaningful insights  
- Generating targeted marketing/business strategies  
- Producing structured Markdown reports  
- Handling end-to-end orchestration through a single user query  

## 2. System Architecture

```
User Query
│
▼
Orchestrator Agent
│
├──► Data Agent → Fetches statistics via tools
├──► Insight Agent → Turns numbers into insights
├──► Strategy Agent → Converts insights → business actions
└──► Report Agent → Creates Markdown report
```

### Key Features
- Fully modular agents with clear roles  
- Tool-based statistical execution  
- Clean orchestrator that manages all four agents    

---

## 3. Dataset Description

### **File:** [`marketing_campaign.csv`](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis/data)  
*(Tab-separated file; delimiter = `\t`)*

This dataset contains detailed customer characteristics and purchasing behavior.

### **Rows & Columns**

### People
| S.no | Column | Description |
| -- |--------|-------------|
| 1. | ID | Unique customer ID |
| 2. | Year_Birth | Birth year |
| 3. | Education | Level of education |
| 4. | Marital_Status | Single/Married/Other labels |
| 5. | Income | Household yearly income |
| 6. | Kidhome | Number of children |
| 7. | Teenhome | Number of teenagers |
| 8. | Dt_Customer | Enrollment date |
| 9. | Recency | Days since last purchase |
| 10. | Complain | Whether customer complained |

### Products
| Column | Description |
|--------|-------------|
| 11. | MntWines | Spending on wine in last 2 years |
| 12. | MntFruits | Spending on fruits in last 2 years  |
| 13. | MntMeatProducts | Spending on meat in last 2 years |
| 14. | MntFishProducts | Spending on fish in last 2 years |
| 15. | MntSweetProducts | Spending on sweets in last 2 years |
| 16. | MntGoldProds | Spending on gold in last 2 years |


### Promotions
| Column | Description |
|--------|-------------|
| 17. | NumDealsPurchases | Purchases using discounts |
| 18. | AcceptedCmp1 | 1 - Accept offer in 1st campaign else 0 |
| 19. | AcceptedCmp2 | 1 - Accept offer in 2nd campaign else 0 |
| 20. | AcceptedCmp3 | 1 - Accept offer in 3rd campaign else 0 |
| 21. | AcceptedCmp4 | 1 - Accept offer in 4th campaign else 0s |
| 22. | AcceptedCmp5 | 1 - Accept offer in 5th campaign else 0 |
| 23. | Response | 1 - Accept offer in last campaign else 0s |

### Places
| Column | Description |
|--------|-------------|
| 24. | NumWebPurchases | Online purchases |
| 25. | NumCatalogPurchases | Catalog purchases |
| 26. | NumStorePurchases | In-store purchases |
| 27. | NumWebVisitsMonth | Monthly website visits |

### Other
| Column | Description |
|--------|-------------|
| 28. | Z_CostContact |  |
| 29. | Z_Revenue |  |

### 3.1 Derived Metrics (Computed Inside Tools)

To operate on raw data without full cleaning, the **Data Tools** compute helpful derived features:

| Derived Metric | Formula |
|----------------|---------|
| `Children` | Kidhome + Teenhome |
| `TotalSpend` | Sum of all Mnt* columns |
| `CustomerTenureDays` | Today – Dt_Customer |
| `IsHighValue` | Income/top 20% OR TotalSpend/top 20% |

These allow meaningful insights even with raw data.

---

## 4. Business Objectives

This system is built to answer business questions like:

- Who are my high-value customers?  
- What patterns do married customers with kids show?  
- What segments purchase the most wine/meat/sweet products?  
- Which channels (web/store/catalog) perform better?  
- Recommend strategies to increase retention or conversions.  
- Generate an automated marketing report.  

### **KPIs**
- High-value customer distribution  
- Monetary/recency/channel-based behavior  
- Segment-level spend patterns  
- Recommended business actions  
- Executive summary generation  

---

## 5. Agent Responsibilities

| Agent | Purpose | Input | Output | Tools |
|--------|---------|--------|---------|--------|
| **Data Agent** | Runs statistical queries | User question | JSON stats | `global_stats`, `segment_stats`, `top_customers`, `derived_features` |
| **Insight Agent** | Converts stats → insights | JSON stats | Business insights | — |
| **Strategy Agent** | Converts insights → actions | Insights | Strategy list | — |
| **Report Agent** | Generates Markdown report | Stats + insights + strategies | Executive report | — |
| **Orchestrator** | Manages full pipeline | User query | Final report | All agents |

---

## 6. Folder Structure

```
Agno_Customer_Personality_Analysis_Agent/
│
├── data/
│ └── marketing_campaign.csv # Original Kaggle dataset
│
├── agno_app/
│ ├── config.py # Environment & settings
│ ├── data_loader.py # Load raw CSV (tab-delimited)
│ ├── data_interface.py # Derived metrics, schema helpers
│
│ ├── tools/
│ │ └── data_tools.py # Stats & segmentation tools
│
│ ├── agents/
│ │ ├── data_agent.py # Fetches stats
│ │ ├── insight_agent.py # Converts stats → insights
│ │ ├── strategy_agent.py # Converts insights → actions
│ │ └── report_agent.py # Builds Markdown report
│
│ └── orchestrator.py # Orchestration logic
│
├── main.py # CLI entry point
├── requirements.txt
└── README.md
```
---
## 7. Tech Stack

### **Language**
- Python 3.10+

### **Frameworks**
- **Agno** – Multi-agent orchestration  
- **OpenRouter** – LLM provider (free credits)

### **Models**
- Free models or models with free credits  

### **Core Libraries**
- `agno`  
- `pandas`  
- `numpy`  
- `python-dotenv`  
- `requests`  

### **Recommended**
- `pydantic`  
- `loguru`  
- `matplotlib`  

---

## 8. Setup & Installation

### a. Clone Repository

    git clone https://github.com/AnirudhJayant06/Agno_Customer_Personality_Analysis_Agent.git

    cd agno-tabular-agents

### b. Create Virtual Environment & activate it

- Open the terminal in vscode
- Create a virtual environment folder inside the project folder
    ```
    py -3.10 -m venv <VIRTUAL-ENV-NAME>
    ```
- Activate the virtual environment. After that, it 'll look like this "(VIRTUAL-ENV-NAME) C:\Users\Anirudh\..."
    ```
    <VIRTUAL-ENV-NAME>\Scripts\activate
    ```

- Update pip
    ```
    python -m pip install --upgrade pip
    ```
### c. Install Dependencies
```      
pip install -r requirements.txt
```
- To check if everything got installed properly or not
    ```
    pip list
    ```

### d. Setup Environment Variables
> `Need to update this later`
- Create a .env file and add all the keys and important variables:

    ```
    OPENROUTER_API_KEY=your_key_here
    OPENROUTER_MODEL_ID=gpt-4o-mini
    DATA_PATH=data/marketing_campaign.csv
    ```

### e. Run Application
```
python main.py
```
## 9. Usage Example
>  `Update this later`

- Input

- Output

### 10. Roadmap

#### Project & Data Setup
1. Set up project structure and environment  
2. Download original Kaggle dataset  
3. Implement data loading with minimal preprocessing  

#### Data Tools (Light Cleaning + Derived Metrics)
4. Add utility functions for basic statistics  
5. Compute derived metrics (TotalSpend, Children, Tenure, HighValue tags)  
6. Handle minimal issues (missing values, category cleanup)  

#### Multi-Agent System (Core of the Project)
7. Create Agent 1 — Data Agent
   - Runs statistical queries  
   - Uses tools to fetch numeric values  
   - Always returns JSON outputs  

8. Create Agent 2 — Insight Agent
   - Interprets numbers from Data Agent  
   - Generates insights and patterns  

9. Create Agent 3 — Strategy Agent
    - Converts insights → actionable business recommendations  

10. Create Agent 4 — Report Agent
    - Produces structured Markdown reports  

11. Orchestrator
- Connects all agents into an end-to-end pipeline  
- Takes a user query → returns full report  

## Hardening & Enhancements
12. Add strict JSON schemas  
13. Improve logging and error handling  
14. Add Markdown → PDF export  
15. Include optional charts in reports  

## Deployment 
> `NEED TO PLAN`

### 11. License

This project is released under the **MIT License**.

You are free to use, modify, distribute, and build upon this project in both personal and commercial settings, as long as the original copyright and license notice are retained.

## Author
**Anirudh Jayant**  
Machine Learning & GenAI Engineer