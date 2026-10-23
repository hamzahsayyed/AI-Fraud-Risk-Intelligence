import os
import struct
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st

from database import create_table, save_transaction, load_transactions


# PAGE CONFIGURATION
st.set_page_config(
    page_title="NEON | Fraud Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Futuristic dark background */
.stApp {
    background: linear-gradient(135deg, #080b18 0%, #10172d 50%, #080b18 100%);
    color: #e6f1ff;
}

/* Colourful headings */
h1 {
    color: #00f5ff !important;
    text-shadow: 0 0 15px #00f5ff66;
    font-weight: 800 !important;
}

h2, h3 {
    color: #a78bfa !important;
    font-weight: 700 !important;
}

/* Neon metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #151d35, #202747);
    border: 1px solid #00f5ff66;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0 0 14px #00f5ff18;
}

[data-testid="stMetricLabel"] {
    color: #a5b4fc !important;
}

[data-testid="stMetricValue"] {
    color: #00f5ff !important;
}

/* Glowing buttons */
.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    box-shadow: 0 0 20px #00f5ff88;
    transform: translateY(-2px);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #11182d, #090d1b);
    border-right: 1px solid #7c3aed66;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox [data-baseweb="select"] {
    background-color: #151d35;
    color: #00f5ff;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid #7c3aed66;
    border-radius: 12px;
}

/* Coloured dividers */
hr {
    border-color: #7c3aed88 !important;
}
/* Animated 3D cyber background */
.stApp {
    background:
        radial-gradient(ellipse at 20% 20%, #182653 0%, transparent 45%),
        radial-gradient(ellipse at 80% 80%, #301653 0%, transparent 40%),
        #080b18;
    background-attachment: fixed;
}

/* Moving perspective grid */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        linear-gradient(#00f5ff12 1px, transparent 1px),
        linear-gradient(90deg, #00f5ff12 1px, transparent 1px);
    background-size: 45px 45px;
    transform: perspective(500px) rotateX(58deg) scale(1.8);
    transform-origin: center bottom;
    animation: cyberGrid 12s linear infinite;
    mask-image: linear-gradient(to bottom, transparent, black 70%);
    -webkit-mask-image: linear-gradient(to bottom, transparent, black 70%);
}

/* Floating neon light */
.stApp::after {
    content: "";
    position: fixed;
    width: 350px;
    height: 350px;
    top: 15%;
    right: 8%;
    border-radius: 50%;
    background: #7c3aed22;
    filter: blur(90px);
    pointer-events: none;
    z-index: 0;
    animation: neonFloat 8s ease-in-out infinite alternate;
}

@keyframes cyberGrid {
    from { background-position: 0 0; }
    to { background-position: 0 90px; }
}

@keyframes neonFloat {
    from { transform: translate3d(-40px, -20px, 0); }
    to { transform: translate3d(40px, 30px, 0); }
}

/* Keep dashboard content above the background */
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stMain"] {
    position: relative;
    z-index: 1;
}

@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after {
        animation: none;
    }
}
/* =====================================
   NEON CYBERSPACE — ANIMATED BACKGROUND
   ===================================== */

.stApp {
    background:
        radial-gradient(ellipse at 15% 15%, #102b50 0%, transparent 40%),
        radial-gradient(ellipse at 85% 70%, #35105c 0%, transparent 40%),
        linear-gradient(135deg, #050816, #0b1025, #080713);
    background-attachment: fixed;
}

/* Animated 3D perspective grid */
.stApp::before {
    content: "";
    position: fixed;
    inset: -45%;
    z-index: 0;
    pointer-events: none;

    background-image:
        linear-gradient(#00f5ff20 1px, transparent 1px),
        linear-gradient(90deg, #00f5ff20 1px, transparent 1px);

    background-size: 55px 55px;
    transform: perspective(500px) rotateX(58deg) scale(1.3);
    transform-origin: center center;

    animation: neonTunnel 9s linear infinite;

    mask-image: radial-gradient(ellipse, black 15%, transparent 72%);
    -webkit-mask-image: radial-gradient(ellipse, black 15%, transparent 72%);
}

/* Floating 3D neon orb */
.stApp::after {
    content: "";
    position: fixed;
    width: 340px;
    height: 340px;
    top: 12%;
    right: 8%;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;

    background: radial-gradient(
        circle at 30% 30%,
        #00f5ff70,
        #7c3aed45 35%,
        #ec489915 65%,
        transparent 75%
    );

    filter: blur(35px);
    animation: orbFloat 8s ease-in-out infinite alternate;
}

/* Continuous tunnel motion */
@keyframes neonTunnel {
    0% {
        background-position: 0 0, 0 0;
        transform: perspective(500px) rotateX(58deg) scale(1.3);
    }
    100% {
        background-position: 0 110px, 110px 0;
        transform: perspective(500px) rotateX(58deg) scale(1.45);
    }
}

/* Floating orb movement */
@keyframes orbFloat {
    0% {
        transform: translate3d(-40px, -25px, 0) scale(0.85);
    }
    50% {
        transform: translate3d(20px, 25px, 0) scale(1.1);
    }
    100% {
        transform: translate3d(60px, -10px, 0) scale(0.95);
    }
}

/* =====================================
   FUTURISTIC SIDEBAR
   ===================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0b1025 0%,
        #11112c 48%,
        #160b27 100%
    ) !important;

    border-right: 1px solid #00f5ff55;
    box-shadow: 5px 0 30px #00f5ff12;
}

/* Sidebar content spacing */
[data-testid="stSidebar"] > div:first-child {
    background: transparent;
    padding-top: 1.5rem;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #00f5ff !important;
    text-shadow: 0 0 12px #00f5ff35;
}

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #c4d4f5 !important;
}

/* Sidebar input fields */
[data-testid="stSidebar"] input {
    background: #101a32 !important;
    color: #00f5ff !important;
    border: 1px solid #7c3aed80 !important;
    border-radius: 9px !important;
}

/* Sidebar select boxes */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #101a32 !important;
    border-color: #7c3aed80 !important;
    border-radius: 9px !important;
    color: #e6f1ff !important;
}

/* Sidebar sliders */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    box-shadow: 0 0 12px #00f5ff80;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(110deg, #5422a5, #075e80) !important;
    border: 1px solid #00f5ff80 !important;
    border-radius: 10px !important;
    color: white !important;
    padding: 0.65rem 1rem;
    box-shadow: 0 0 12px #00f5ff18;
    transition: all 0.25s ease;
}

[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 22px #00f5ff55;
    border-color: #00f5ff !important;
}

/* Sidebar separators */
[data-testid="stSidebar"] hr {
    border-color: #7c3aed70 !important;
}

/* =====================================
   GLOWING DASHBOARD PANELS
   ===================================== */

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #101a32dd, #21133bdd);
    border: 1px solid #00f5ff55;
    border-radius: 15px;
    box-shadow: 0 0 18px #00f5ff10;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 28px #00f5ff25;
}

/* Keep main content above decorative background */
[data-testid="stMain"] {
    position: relative;
    z-index: 1;
}

/* Respect reduced-motion preferences */
@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after {
        animation: none !important;
    }

    [data-testid="stMetric"],
    [data-testid="stSidebar"] .stButton > button {
        transition: none !important;
    }
}
/* FUTURISTIC HOLOGRAPHIC HEADER */

.cyber-header {
    display: flex;
    align-items: center;
    gap: 25px;
    padding: 25px;
    margin-bottom: 15px;
    background: linear-gradient(
        110deg,
        #101a32dd,
        #17102bdd,
        #081827dd
    );
    border: 1px solid #00f5ff55;
    border-radius: 20px;
    box-shadow: 0 0 30px #00f5ff12;
    overflow: hidden;
}

/* Animated holographic shield */
.holo-shield {
    font-size: 95px;
    color: #00f5ff;
    text-shadow:
        0 0 10px #00f5ff,
        0 0 30px #00f5ff,
        0 0 60px #7c3aed;

    animation: shieldHologram 4s ease-in-out infinite;
    transform-style: preserve-3d;
}

/* Title */
.cyber-title h1 {
    margin: 8px 0 !important;
    font-size: clamp(28px, 4vw, 46px) !important;
    letter-spacing: 3px;
    color: #ffffff !important;
    text-shadow: 0 0 20px #00f5ff65;
}

.cyber-title h1 span {
    background: linear-gradient(90deg, #00f5ff, #a78bfa, #ff4ecd);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.system-label {
    color: #a78bfa;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: bold;
}

.cyber-title p {
    color: #9bb6d9;
    font-size: 12px;
    letter-spacing: 2px;
    margin-bottom: 0;
}

/* Live status indicator */
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    margin: 0 7px;
    border-radius: 50%;
    background: #00ff9d;
    box-shadow: 0 0 12px #00ff9d;
    animation: statusPulse 1.5s infinite;
}

/* Header separator */
.cyber-line {
    height: 2px;
    margin: 20px 0;
    background: linear-gradient(
        90deg,
        transparent,
        #00f5ff,
        #7c3aed,
        #ff4ecd,
        transparent
    );
    background-size: 200% 100%;
    animation: lineFlow 4s linear infinite;
}

/* Animation effects */
@keyframes shieldHologram {
    0%, 100% {
        transform: perspective(400px) rotateY(-12deg) translateY(0);
        filter: hue-rotate(0deg);
    }
    50% {
        transform: perspective(400px) rotateY(12deg) translateY(-8px);
        filter: hue-rotate(35deg);
    }
}

@keyframes statusPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

@keyframes lineFlow {
    from { background-position: 100% 0; }
    to { background-position: -100% 0; }
}

@media (prefers-reduced-motion: reduce) {
    .holo-shield,
    .status-dot,
    .cyber-line {
        animation: none !important;
    }
}

@media (max-width: 600px) {
    .cyber-header {
        gap: 12px;
        padding: 15px;
    }

    .holo-shield {
        font-size: 55px;
    }

    .system-label {
        letter-spacing: 1px;
    }

    .cyber-title p {
        font-size: 9px;
        letter-spacing: 1px;
    }
}
</style>
""", unsafe_allow_html=True)

# MODEL FILES
MODEL_FILE = "fraud_xgboost_model.pkl"
THRESHOLD_FILE = "fraud_threshold.pkl"
FEATURES_FILE = "model_features.pkl"

for filename in (MODEL_FILE, THRESHOLD_FILE, FEATURES_FILE):
    if not os.path.exists(filename):
        st.error(f"Required model file not found: {filename}")
        st.stop()


# LOAD MODEL
try:
    model = joblib.load(MODEL_FILE)
    threshold_data = joblib.load(THRESHOLD_FILE)
    features_data = joblib.load(FEATURES_FILE)

    if isinstance(threshold_data, dict):
        threshold_data = next(iter(threshold_data.values()))

    threshold = float(np.asarray(threshold_data).reshape(-1)[0])

    if isinstance(features_data, pd.DataFrame):
        features = features_data.columns.tolist()
    else:
        features = list(features_data)

    features = [str(feature) for feature in features]

except Exception as error:
    st.error(f"Unable to load the model files: {error}")
    st.stop()


# DATABASE
try:
    create_table()
except Exception as error:
    st.error(f"Database initialization failed: {error}")
    st.stop()


# HELPER FUNCTIONS
def set_feature(input_data, feature_name, value):
    for column in input_data.columns:
        if str(column).lower() == feature_name.lower():
            input_data.loc[0, column] = value
            return


def clean_database_value(value, column_name):
    """Convert legacy byte values into safe values for display."""
    if not isinstance(value, bytes):
        return value

    # Some old rows may contain a 4-byte float in this column.
    if column_name == "Fraud Risk (%)" and len(value) == 4:
        try:
            return float(struct.unpack("<f", value)[0])
        except (struct.error, ValueError):
            return None

    return value.decode("utf-8", errors="replace")


def get_transaction_history():
    history = load_transactions()

    if history is None:
        return pd.DataFrame()

    history = history.copy()

    for column in history.columns:
        history[column] = history[column].apply(
            lambda value: clean_database_value(value, column)
        )

    for column in ("Amount", "Hour", "Fraud Risk (%)"):
        if column in history.columns:
            history[column] = pd.to_numeric(history[column], errors="coerce")

    return history


# PAGE HEADER
st.markdown("""
<div class="cyber-header">
    <div class="holo-shield">⬡</div>
    <div class="cyber-title">
        <div class="system-label">
            ◈ FRAUD INTELLIGENCE SYSTEM // V2.0
        </div>
        <h1>NEON <span>FRAUD AI</span></h1>
        <p>
            ADVANCED TRANSACTION MONITORING
            <span class="status-dot"></span>
            SYSTEM ONLINE
        </p>
    </div>
</div>
<div class="cyber-line"></div>
""", unsafe_allow_html=True)
# TRANSACTION INPUTS
st.sidebar.header("Transaction Details")

amount = st.sidebar.number_input(
    "Transaction Amount (₹)",
    min_value=0.0,
    value=1000.0,
    step=100.0,
)

hour = st.sidebar.selectbox("Transaction Hour", list(range(24)), index=12)

day = st.sidebar.slider(
    "Transaction Day",
    min_value=1,
    max_value=31,
    value=15,
)

card_type = st.sidebar.selectbox(
    "Card Type",
    ["Visa", "Mastercard", "American Express", "Discover"],
)

payment_type = st.sidebar.selectbox(
    "Payment Type",
    ["Credit Card", "Debit Card", "UPI", "Net Banking", "Wallet"],
)

device = st.sidebar.selectbox("Device Type", ["Desktop", "Mobile"])


# ANALYZE TRANSACTION
if st.button("🔍 Analyze Transaction", use_container_width=True):
    try:
        # Build a row with exactly the features expected by the saved model.
        # These columns are set only if they exist in the model feature list.
        input_data = pd.DataFrame(
            np.zeros((1, len(features))),
            columns=features,
        )

        set_feature(input_data, "TransactionAmt", amount)
        set_feature(input_data, "TransactionDT", day * 86400 + hour * 3600)
        set_feature(input_data, "D1", day)

        # These columns are set only if they exist in the model feature list.
        card_feature = "card4_" + card_type.lower()
        set_feature(input_data, card_feature, 1)

    

        probability = float(model.predict_proba(input_data)[0][1])
        fraud_risk = probability * 100

        if probability >= threshold:
            risk_level = "High"
        elif probability >= threshold * 0.5:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        st.subheader("Transaction Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Transaction Amount", f"₹{amount:,.2f}")
        col2.metric("Estimated Fraud Risk", f"{fraud_risk:.2f}%")
        col3.metric("Risk Level", risk_level)

        st.markdown("### ⚡ FRAUD RISK ANALYSIS")
        st.progress(
            min(max(int(fraud_risk), 0), 100),
            text=f"Estimated Fraud Risk: {fraud_risk:.2f}%"
        )

        if risk_level == "High":
            st.error("🚨 HIGH RISK — Further review is required.")
            st.info("Recommendation: Flag for manual verification.")
        elif risk_level == "Medium":
            st.warning("⚠️ MEDIUM RISK — Additional verification is recommended.")
            st.info("Recommendation: Verify before approval.")
        else:
            st.success("🟢 LOW RISK — The model estimates a lower fraud probability.")
            st.info("Recommendation: Continue normal monitoring.")

        st.caption(
            "This is an experimental model estimate, not a confirmed fraud decision."
        )
        transaction = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Amount": float(amount),
            "Hour": int(hour),
            "Card Type": card_type,
            "Payment Type": payment_type,
            "Device": device,
            "Fraud Risk (%)": round(fraud_risk, 2),
            "Risk Level": risk_level,
         }

        save_transaction(transaction)
        st.success("Transaction saved successfully.")

    except Exception as error:
        st.error(f"Transaction analysis failed: {error}")


# TRANSACTION DASHBOARD
st.divider()
st.header("📊 Transaction Dashboard")

try:
    history_df = get_transaction_history()
except Exception as error:
    st.error(f"Unable to load transaction history: {error}")
    history_df = pd.DataFrame()


# DISPLAY HISTORY
if not history_df.empty:
    total_transactions = len(history_df)

    if "Risk Level" in history_df.columns:
        high_risk_count = int(history_df["Risk Level"].eq("High").sum())
    else:
        high_risk_count = 0

    if "Amount" in history_df.columns:
             # VISUAL FRAUD RISK METER
      average_amount = history_df["Amount"].mean()
    else:
        average_amount = 0.0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", total_transactions)
    col2.metric("High-Risk Transactions", high_risk_count)
    col3.metric("Average Transaction Amount", f"₹{average_amount:,.2f}")

    if "Risk Level" in history_df.columns:
        st.subheader("Risk Distribution")
        st.bar_chart(history_df["Risk Level"].value_counts())

    st.subheader("Transaction History")
    st.dataframe(history_df, use_container_width=True)

    csv_data = history_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Transaction History",
        data=csv_data,
        file_name="transaction_history.csv",
        mime="text/csv",
    )
else:
    st.info("No saved transactions yet. Analyze a transaction to get started.")


# FOOTER
st.divider()
st.caption("AI Fraud Risk Intelligence | Educational Project")
st.caption(
    "Predictions are experimental and should not be used alone "
    "to make real financial decisions."
)
