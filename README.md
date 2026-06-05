# 📚 book-data-extractor

An end-to-end Python data pipeline designed to programmatically extract, normalize, cache, and analyze structured bibliographical data from live web sources. 

Instead of relying on pre-packaged static datasets, this project showcases a professional **End-to-End Data Lifecycle** moving from raw web scraping and live API integration to Predictive Machine Learning modeling and data visualization.

---

### 🏗️ The Enhanced Data Science Framework

#### 1. Define the Problem
* **Objective:** Analyze Stephen King’s 50-year career trajectory (1974–2024), tracking book lengths, publication velocity, and publisher ecosystem dynamics to predict future publication lengths.

#### 2. Data Acquisition & Ingestion
* **Pipelines:** Extracted semi-structured records from a live REST API (`requests`) and parsed unstructured web layouts via `BeautifulSoup` (`lxml`).
* **Lineage:** Implemented local raw file caching (`raw_data/`) to protect source servers and ensure reproducibility.

#### 3. Data Cleaning & Preprocessing
* **Normalization:** Unpacked and flattened deeply nested JSON dictionary structures using `pd.json_normalize()`.
* **Integrity:** Cast text objects (`Pages`, `Year`) into integers (`int64`), imputed missing fields, and removed duplicate records based on unique key constraints.

#### 4. Exploratory Data Analysis (EDA) & Feature Engineering
* **Profiling:** Used descriptive statistics (`.describe()`) to extract mathematical spreads and identify extreme volume outliers.
* **Transformations:** Binned publication years into historical career decades and engineered text-based categorical vectors using One-Hot Encoding (`drop_first=True`) to prepare data matrices for machine learning algorithms.

#### 5. Predictive Modeling Engine (Machine Learning Stage)
* **Model Selection:** Deployed an ensemble **Random Forest Regressor** configured with 100 decision tree estimators to forecast book lengths based on publishing house patterns and historical timelines. *(Note: System architecture is modularly designed to easily swap or benchmark against **Gradient Boosting / XGBoost** models for tabular optimization).*
* **Evaluation:** Split data matrix into a rigorous 80/20 train/test split with a fixed seed (`random_state=42`) to guarantee experiment reproducibility. Performance was quantified on blind validation targets utilizing Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

#### 6. Data Visualization & Storytelling
* **Visuals:** Built publication-ready charts using `matplotlib` and `seaborn`.
* **Plots:** Plotted publication frequency via line charts, tracked novel length evolution using regression scatter plots, and mapped publisher market share with horizontal bar charts.

#### 7. Interpretation & Insights
* **Conclusions:** Quantified a prolific consistency averaging over 1.2 books per year, visually verified style evolutions toward larger page counts, and exposed dominant corporate publisher alignment.

---

## 🛠️ Tech Stack & Dependencies

* **Core Language & Runtime:** `Python 3.10+`
* **Machine Learning & Modeling:** `scikit-learn` (Random Forest, Regressors, Model Selection Metrics)
* **Data Engineering & Analysis:** `pandas` (DataFrames, JSON normalization, vectorization), `numpy` (numerical operations)
* **Web Scraping & Connectivity:** `requests` (HTTP client), `beautifulsoup4` (HTML parsing), `lxml` (high-performance XML/HTML tree processing)
* **Data Visualization & Analytics:** `matplotlib` (base plotting engine), `seaborn` (statistical visualizations)
* **Storage & Serialization:** `csv`, `json` (native serialization file formats)
* **Environment Management:** `pip` / `virtualenv` (or `conda`)

---

## 📂 Repository Architecture

```text
📁 book-data-extractor/
│
├── 📁 raw_data/            # Local data staging (Raw cached .json and .html payloads)
├── 📁 cleaned_data/        # Pipeline destination (Final clean analytical data.csv)
│
├── 📄 pipeline.py          # Production Script: The automated end-to-end ETL & Data Ingestion engine
├── 📄 train_model.py       # Production Script: Machine learning training and evaluation execution
├── 📄 requests_data.ipynb  # Interactive workspace housing exploratory analysis and visual rendering
└── 📄 README.md            # Project architecture and analytical summary─ 📄 README.md            # Project architecture and analytical summary

```
## 📊 Extracted Dataset Schema

The final cleaned dataset contains 63 unique book records structured according to the following relational schema:

| Column Name | Data Type | Key Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`id`** | `Integer` | Primary Key | No | Unique identifier assigned to each book to enforce database row integrity. |
| **`Title`** | `String` | - | No | The official published title of the literary work. |
| **`Year`** | `Integer` | - | No | The original calendar year of publication (ranges from 1974 to 2024). |
| **`Publisher`** | `String` | - | No | The distributing corporate publishing house name. |
| **`ISBN`** | `String` | Unique Key | Yes | Universal International Standard Book Number used for retail tracking. |
| **`Pages`** | `Integer` | - | No | Total physical page count of the book's standard print edition. |

***

## Visual Insights Gallery

These chart tracks individual annual book release counts to illustrate continuous narrative output and publishing frequency shifts across a 50-year timeline.

<p align="center"> More extracted graphs ➡️
  <img src="Extracted-graphs" alt="graphs" width="850"/>
</p>
<br><br>
  <img width="2000" height="1000" alt="book_length_evolution" src="https://github.com/user-attachments/assets/0c4e6503-8514-42ed-b532-1b026d95b473" />

***
## ⚙️ Prerequisites & Local Setup

To run this project locally, your environment needs to have Python installed along with the required web scraping, data engineering, and data visualization dependencies.

### 1. System Requirements
* **Python Runtime:** `Python 3.10` or higher is recommended.
* **Package Manager:** `pip` (comes bundled with Python installations).

### 2. Required Python Libraries
The core dependencies are split into three modules:
* **Networking & Parsing:** `requests`, `beautifulsoup4`, `lxml`
* **Data Processing:** `pandas`, `numpy`
* **Data Visualization:** `matplotlib`, `seaborn`, `scikit-learn notebook`

---

## 🚀 Running the Production Pipeline

Follow these terminal commands to set up the environment on your machine:

### Step 1: Run the ETL Pipeline Script
```
python pipeline.py
```
### Step 2: Execute the Machine Learning Layer 
Train your Random Forest Regressor and evaluate predictive metrics on your clean dataset:
```
python train_model.py
````
### Step 3: Interactive Workspace
To view the full visual data discovery process and plot historical graphs step-by-step:
```
jupyter notebook
```
Open requests_data.ipynb from the browser dashboard and run cells sequentially.

***

## ⚫ Authors & Credits

* **Priyanshu Vijay** - *Data Engineer & ML Analyst* - [Butkii025](https://github.com/Butkii025)

### 📄 License & Attribution
The data pipeline code is licensed under the MIT License. If you use the cleaned dataset (`data.csv`) generated by this repository for further machine learning or statistical analysis, please attribute it as follows:
> *P.Vijay, (2026). Book Data Extractor Dataset (Version 1.0) [Data set]. GitHub.*
