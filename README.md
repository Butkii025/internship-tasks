# 📚 book-data-extractor

An end-to-end Python data pipeline designed to programmatically extract, normalize, cache, and analyze structured bibliographical data from live web sources. 

Instead of relying on pre-packaged static datasets, this project showcases a professional **6-Stage Data Science Lifecycle** moving from raw web scraping and live API integration to deep Exploratory Data Analysis (EDA) and data visualization.

---

### 🏗️ The 6-Stage Data Science Framework

#### 1. Define the Problem
* **Objective:** Analyze Stephen King’s 50-year career trajectory (1974–2024), tracking book lengths, publication velocity, and publisher ecosystem dynamics.

#### 2. Data Acquisition & Ingestion
* **Pipelines:** Extracted semi-structured records from a live REST API (`requests`) and parsed unstructured web layouts via `BeautifulSoup` (`lxml`).
* **Lineage:** Implemented local raw file caching (`raw_data/`) to protect source servers and ensure reproducibility.

#### 3. Data Cleaning & Preprocessing
* **Normalisation:** Flattened nested JSON structures using `pd.json_normalize()`.
* **Integrity:** Cast text objects (`Pages`, `Year`) into integers (`int64`), imputed missing fields, and removed duplicate records.

#### 4. Exploratory Data Analysis (EDA)
* **Profiling:** Used descriptive statistics (`.describe()`) to extract mathematical spreads and identify extreme volume outliers.
* **Feature Engineering:** Programmatically binned publication years into distinct historical career decades (e.g., `1970s`, `1980s`).

#### 5. Data Visualization & Storytelling
* **Visuals:** Built publication-ready charts using `matplotlib` and `seaborn`.
* **Plots:** Plotted publication frequency via line charts, tracked novel length evolution using regression scatter plots, and mapped publisher market share with horizontal bar charts.

#### 6. Interpretation & Insights
* **Conclusions:** Quantified a prolific consistency averaging over 1.2 books per year, visually verified style evolutions toward larger page counts, and exposed dominant corporate publisher alignment.
---
## 🛠️ Tech Stack & Dependencies

* **Core Language & Runtime:** `Python 3.10+`
* **Data Engineering & Analysis:** `pandas` (DataFrames, vectorization), `numpy` (numerical operations)
* **Web Scraping & Connectivity:** `requests` (HTTP client), `beautifulsoup4` (HTML parsing), `lxml` (high-performance XML/HTML tree processing)
* **Data Visualization & Analytics:** `matplotlib` (base plotting engine), `seaborn` (statistical visualizations)
* **Data Quality & Validation (Optional):** `pydantic` or `great_expectations` (schema validation)
* **Storage & Serialization:** `csv`, `json` (native serialization file formats)
* **Environment & Package Management:** `pip` / `virtualenv` (or `conda`)
* **Development Interface:** `Jupyter Notebook` / `VS Code`
---

## 📂 Repository Architecture

```text
📁 book-data-extractor/
│
├── 📁 raw_data/            # Local data staging (Raw cached .json and .html payloads)
├── 📁 cleaned_data/        # Pipeline destination (Final clean analytical data.csv)
│
├── 📄 requests_data.ipynb  # Comprehensive Jupyter Notebook housing code execution
└── 📄 README.md            # Project architecture and analytical summary

```
Extracted Dataset Schema
The final engineered dataset outputs a structured matrix containing 63 unique book records with the following technical metadata:

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

### 1. Evolution of Book Length Over Time
This chart tracks individual works as distributed points to visually illustrate long-term narrative structural growth across decades.

(Tip: Save your scatter plot image from your notebook and link it here!)

### 2. Publisher Dominance Distribution
A ranked distribution illustrating which corporate stakeholders hold the dominant market share of the author's lifelong literary portfolio.

(Tip: Save your horizontal bar chart image from your notebook and link it here!)

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
* **Data Visualization:** `matplotlib`, `seaborn`

---

## 🚀 Step-by-Step Local Installation

Follow these terminal commands to set up the environment on your machine:

### Step 1: Clone the Repository
Clone the project directory from GitHub to your local storage:
```bash
git clone [https://github.com/YOUR_USERNAME/book-data-extractor.git](https://github.com/YOUR_USERNAME/book-data-extractor.git)
cd book-data-extractor
```

### Step 2: Set Up a Isolated Virtual Environment 
Creating a virtual environment ensures that the project dependencies do not conflict with your global Python system packages.
➡️ On Windows:
```python -m venv venv
.\venv\Scripts\activate
```
➡️ On macOS/Linux:
```python3 -m venv venv
source venv/bin/activate
````
### Step 3: Install Dependencies
```
pip install requests beautifulsoup4 lxml pandas numpy matplotlib seaborn notebook
```
### 🏃‍♂️ How to Run the Project
1.Ensure your virtual environment is activated.
```
jupyter notebook
```

Open `requests_data.ipynb` from the dashboard and run the cells sequentially (`Shift + Enter`) to fetch live data and generate the analytical charts.



## ⚫ Authors & Credits

* **Priyanshu Vijay** - *Data Engineer & Analyst* - [Your GitHub Profile](https://github.com/Butkii025)

### 📄 License & Attribution
The data pipeline code is licensed under the MIT License. If you use the cleaned dataset (`data.csv`) generated by this repository for further machine learning or statistical analysis, please attribute it as follows:
> *P.Vijay, (2026). Book Data Extractor Dataset (Version 1.0) [Data set]. GitHub.*
