
# Architecture of MLOps- pipeline for the book_data_extractor
## All the structure are divided in total 3 part :
***


```mermaid
graph TD
    %% Source Node
    subgraph Layer 1: Ingestion & In-Memory Preprocessing
        A[🌐 Live Web Infrastructure] -->|Synchronous HTTP GET| B[📄 pipeline.py Extraction Core]
        B -->|Regular Expression Parsing| C{🛡️ Clean Data Quality Gates}
        C -->|Serialize Pure JSON payload| D(💾 retrieve_data.json Warehouse)
    end

    %% Training Node
    subgraph Layer 2: Automated Pipeline Training
        D -->|Dataframe Serialization Stream| E[📄 train_model.py Ensemble Compiler]
        E -->|One-Hot Matrix Engineering| F[📐 Multi-Dimensional Feature Arrays]
        F -->|Matrix Segmentation K=5| G[🔬 5-Fold Cross Validation Loop]
        G -->|Diagnostic Metrics Output| H[📊 MAE / R² Diagnostics Panel]
        F -->|Full Dataset Optimization| I[🧠 Random Forest Engine]
        I -->|joblib Serialization Protocol| J(📁 models/ Frozen Binary Artifacts)
    end

    %% Inference Node
    subgraph Layer 3: Dynamic Runtime Server Interface
        K[💻 Console Interface Terminal] -->|User Parameter Query Loop| L[📄 predict.py Interactive Dashboard]
        J -->|Hydrate Binary Coefficients| L
        L -->|Vector Alignment Mapping| M[🔮 Live Regressor Forecast Matrix]
        M -->|Standard Output Yield Stream| K
    end

    style D fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
