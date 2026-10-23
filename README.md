# AI Fraud Risk Intelligence

An end-to-end machine learning application that estimates the likelihood of fraudulent financial transactions using XGBoost. The project combines predictive modeling, an interactive Streamlit interface, and transaction history management to demonstrate a practical fraud risk analysis workflow.

## Project Overview

Financial fraud detection is a challenging classification problem because fraudulent transactions represent a small proportion of overall transaction activity. This project uses the IEEE-CIS Fraud Detection dataset to develop a machine learning model that identifies potentially suspicious transactions and presents risk estimates through a web dashboard.

The application is designed as an educational demonstration of machine learning integration, model evaluation, and interactive data analysis.

## Key Features

- **Fraud Risk Prediction:** Estimates transaction fraud probability using an XGBoost classifier.
- **Risk Classification:** Categorizes predictions into Low, Medium, and High risk levels.
- **Interactive Dashboard:** Provides a Streamlit interface for entering transaction details and reviewing prediction results.
- **Transaction Management:** Stores analyzed transactions in an SQLite database.
- **Risk Analytics:** Displays transaction summaries and risk distribution visualizations.
- **Historical Analysis:** Presents previously analyzed transactions in a structured table.
- **Data Export:** Allows users to download transaction history as a CSV file.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Machine Learning | XGBoost, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Web Application | Streamlit |
| Database | SQLite |
| Model Persistence | Joblib |
| Data Visualization | Streamlit charts |

## Dataset

The project uses the IEEE-CIS Fraud Detection dataset from Kaggle.

The dataset contains transaction records with a highly imbalanced target variable, making fraud detection a challenging binary classification task.

**Target variable:** `isFraud`

- `0` — Legitimate transaction
- `1` — Fraudulent transaction

Dataset source: IEEE-CIS Fraud Detection, Kaggle.

## Model Development

The training pipeline performs the following operations:

1. Loads the transaction dataset.
2. Separates input features from the fraud target.
3. Encodes categorical variables using one-hot encoding.
4. Handles missing values.
5. Splits the data into training and testing sets using stratified sampling.
6. Trains an XGBoost classifier using balanced sample weights.
7. Evaluates model discrimination using ROC-AUC.
8. Saves the trained model and its feature list for application use.

### Model Evaluation

The current training pipeline reported the following ROC-AUC score:

| Metric | Result |
|---|---:|
| ROC-AUC | 0.9280 |

ROC-AUC measures how well a model distinguishes between positive and negative classes across different classification thresholds. It does not, by itself, establish the accuracy of individual predictions or the suitability of a threshold for real-world use.

## Project Structure

```text
AI-Fraud-Risk-Intelligence/
├── app.py
├── train_model.py
├── database.py
├── fraud_xgboost_model.pkl
├── fraud_threshold.pkl
├── model_features.pkl
├── fraud_history.db
├── requirements.txt
├── README.md
└── data/
    └── raw/
        ├── train_transaction.csv
        └── train_identity.csv
```

The dataset files and generated database may be excluded from version control when appropriate.

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- pip
- Git (optional)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AI-Fraud-Risk-Intelligence
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell blocks activation, use the virtual environment's Python executable directly.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

### Retrain the Model

If the dataset is available at the expected path, train the model with:

```bash
python train_model.py
```

**Note:** Training overwrites the saved model and feature-list files. Keep backups if you need to preserve a previous model version.

## Limitations

- Predictions depend on the quality of the training data and the information provided to the model.
- The current application collects only a limited set of transaction details, while the model uses a larger feature set.
- Some model features are initialized with default values when corresponding inputs are unavailable. This may affect prediction reliability.
- The displayed risk category depends on the configured threshold.
- The reported ROC-AUC score does not guarantee performance on unseen real-world transactions.

## Future Improvements

- Improve feature alignment between the training pipeline and application inputs.
- Evaluate false positives, false negatives, precision, and recall across multiple thresholds.
- Add explainability using SHAP or other feature-attribution techniques.
- Expand transaction input fields and validate input values.
- Add automated tests and structured logging.
- Improve deployment configuration and model version management.

## Disclaimer

This project is intended for educational and demonstration purposes. It has not been validated for production financial fraud detection and should not be used as the sole basis for financial decisions.