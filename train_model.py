import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.utils.class_weight import compute_sample_weight

print("Loading dataset...")

transactions = pd.read_csv("data/raw/train_transaction.csv")

print("Preparing data...")

X = transactions.drop(columns=["isFraud", "TransactionID"])
y = transactions["isFraud"]

X = pd.get_dummies(X, dummy_na=True)
X = X.fillna(-999)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

weights = compute_sample_weight("balanced", y_train)

print("Training model...")

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="auc",
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train, sample_weight=weights)

predictions = model.predict_proba(X_test)[:, 1]
from sklearn.metrics import confusion_matrix

y_pred = (predictions >= 0.826997).astype(int)

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

print("True Negatives:", tn)
print("False Positives:", fp)
print("False Negatives:", fn)
print("True Positives:", tp)
auc = roc_auc_score(y_test, predictions)

print(f"ROC-AUC: {auc:.4f}")

joblib.dump(model, "fraud_xgboost_model.pkl")
joblib.dump(list(X.columns), "model_features.pkl")

print("Model and features saved successfully!")
print("Evaluation completed successfully.")