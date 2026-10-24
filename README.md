# 🛡️ AI Fraud Risk Intelligence

An AI/ML-powered application that analyzes financial transaction data and estimates the probability of fraudulent activity using an XGBoost machine learning model.

🚀 **Live Demo:** https://ai-fraud-risk-intelligence-hamzahs.streamlit.app/

## ✨ Features

- **Fraud Risk Prediction:** Estimates the probability of a transaction being fraudulent.
- **Risk Classification:** Categorizes transactions as Low, Medium, or High risk.
- **Interactive Dashboard:** Displays transaction statistics and risk distribution.
- **Transaction History:** Stores analyzed transactions in an SQLite database.
- **CSV Export:** Download transaction history for further analysis.

## 🧠 Technologies Used

- Python
- XGBoost
- Pandas & NumPy
- Scikit-learn
- Streamlit
- SQLite
- Git & GitHub

## 📊 Model Evaluation

The model was developed using the IEEE-CIS Fraud Detection dataset from Kaggle.

Evaluation metrics include:
- ROC-AUC
- Precision
- Recall
- F1-score
- Confusion matrix

Model performance depends on the dataset, input features, and prediction threshold. The application's predictions are experimental and should not be used as the sole basis for real financial decisions.

## ⚙️ Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/hamzahsayyed/AI-Fraud-Risk-Intelligence.git
   ```

2. Open the project folder:

   ```bash
   cd AI-Fraud-Risk-Intelligence
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   streamlit run app.py
   ```

## 📁 Main Project Files

- `app.py` — Streamlit application and fraud risk predictions.
- `train_model.py` — Model training script.
- `database.py` — SQLite database operations.
- `fraud_xgboost_model.pkl` — Trained XGBoost model.
- `fraud_threshold.pkl` — Saved classification threshold.
- `model_features.pkl` — Model feature list.
- `notebooks/` — Exploratory data analysis notebook.

## 📌 Dataset

The project uses the **IEEE-CIS Fraud Detection** dataset from Kaggle. The raw dataset is not included in this repository because of its size.

## ⚠️ Disclaimer

This is an educational AI/ML project. Predictions are estimates and have not been validated for real-world financial deployment.

## 👨‍💻 Author

**Hamza Sayyed**

GitHub: https://github.com/hamzahsayyed
