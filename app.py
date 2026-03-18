import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(
    page_title="Gold Price Predictor",
    page_icon="🪙",
    layout="wide"
)

# --- Load Models Cache ---
@st.cache_resource
def load_models():
    sarima = None
    svm = None
    try:
        sarima = joblib.load('sarima_model.pkl')
    except Exception as e:
        st.error(f"Error loading SARIMA model: {e}")
        
    try:
        svm = joblib.load('svm_linear_model.pkl')
    except Exception as e:
        st.error(f"Error loading SVM model: {e}")
        
    return sarima, svm

sarima_model, svm_model = load_models()

# --- Custom CSS ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #1f2937;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    .metric-card {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Main App ---
st.title("Gold Price Forecasting & Prediction Dashboard")
st.markdown("Leverage advanced AI models to analyze trends and forecast future gold prices.")
st.divider()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2933/2933116.png", width=100)
    st.header("Dashboard Controls")
    model_choice = st.radio(
        "Select AI Model:",
        ("SARIMA (Long-term Forecast)", "SVM (Next Month Prediction)")
    )
    st.divider()
    st.info("**SARIMA** is optimal for forecasting multi-period future trends based on historical sequences.\n\nℹ️ **SVM** leverages recent market data to pinpoint the next month's immediate price.")

if model_choice == "SARIMA (Long-term Forecast)":
    st.header("Time Series Forecasting with SARIMA")
    st.markdown("Project gold prices into the future using Statistical Autoregressive Integrated Moving Averages.")
    
    if sarima_model is not None:
        n_periods = st.slider("Number of months to forecast:", min_value=1, max_value=60, value=12)
        
        if st.button("Generate Forecast", type="primary"):
            with st.spinner("Forecasting..."):
                try:
                    forecast = sarima_model.predict(n_periods=n_periods)
                    
                    if isinstance(forecast, pd.Series):
                        forecast_values = forecast.tolist()
                    else:
                        forecast_values = forecast.tolist()
                        
                    st.success(f"Forecast for the next {n_periods} months generated successfully!")
                    
                    # Layout: 2 columns for chart and table
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                    # Create a styled plot
                        fig, ax = plt.subplots(figsize=(12, 6))
                        
                        # Plot styling
                        ax.set_facecolor('#f8fafc')
                        fig.patch.set_facecolor('white')
                        
                        # Data plotting
                        ax.plot(range(1, n_periods + 1), forecast_values, 
                                marker='o', markersize=6, linewidth=2.5, 
                                color='#2563eb', label='AI Forecast')
                                
                        # Fill area under curve
                        ax.fill_between(range(1, n_periods + 1), forecast_values, 
                                      alpha=0.1, color='#2563eb')
                        
                        # Labels and title
                        ax.set_title(f"Gold Price Trajectory: Next {n_periods} Months", 
                                   fontsize=16, fontweight='bold', pad=20, color='#1f2937')
                        ax.set_xlabel("Months Ahead", fontsize=12, fontweight='500', labelpad=10)
                        ax.set_ylabel("Predicted Price (USD/oz)", fontsize=12, fontweight='500', labelpad=10)
                        
                        # Grid and Spines
                        ax.grid(True, linestyle='--', alpha=0.7, color='#cbd5e1')
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.spines['left'].set_color('#94a3b8')
                        ax.spines['bottom'].set_color('#94a3b8')
                        
                        ax.legend(loc='upper right', frameon=True, shadow=True)
                        st.pyplot(fig)
                    
                    with col2:
                        # Display as dataframe
                        df_forecast = pd.DataFrame({
                            "Month": range(1, n_periods + 1), 
                            "Forecast (USD)": forecast_values
                        })
                        st.dataframe(df_forecast, use_container_width=True, hide_index=True)
                    
                except Exception as e:
                    st.error(f"Prediction failed: {e}")
    else:
        st.warning("SARIMA model is not loaded properly. Please ensure 'sarima_model.pkl' is in the project directory.")

else:
    st.header("🎯 Immediate Price Prediction with SVM")
    st.markdown("Utilize Support Vector Machines to predict the immediate upcoming month's gold price based on recent market conditions.")
    
    if svm_model is not None:
        st.subheader("Enter the average gold price for the past 6 months:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            m1 = st.number_input("Month t-6 Price", value=2000.0, step=10.0)
            m4 = st.number_input("Month t-3 Price", value=2030.0, step=10.0)
        with col2:
            m2 = st.number_input("Month t-5 Price", value=2010.0, step=10.0)
            m5 = st.number_input("Month t-2 Price", value=2040.0, step=10.0)
        with col3:
            m3 = st.number_input("Month t-4 Price", value=2020.0, step=10.0)
            m6 = st.number_input("Month t-1 Price", value=2050.0, step=10.0)
            
        features = [m1, m2, m3, m4, m5, m6]
        
        if st.button("Predict Next Month's Price", type="primary"):
            with st.spinner("Predicting..."):
                try:
                    features_array = np.array([features])
                    prediction = svm_model.predict(features_array)[0]
                    
                    # Display large metric card
                    st.markdown(f"""
                        <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0;">
                            <h2 style="color: #166534; margin: 0;">Predicted Next Month Price</h2>
                            <h1 style="color: #15803d; font-size: 3rem; margin: 10px 0;">${prediction:,.2f}</h1>
                            <p style="color: #166534; margin: 0;">Based on SVM Linear Kernel Analysis</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("Price Trend Analysis")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    
                    # Plot styling
                    ax.set_facecolor('#f8fafc')
                    fig.patch.set_facecolor('white')
                    
                    # Data plotting
                    ax.plot(range(-6, 0), features, marker='o', markersize=8, 
                            linewidth=2.5, color='#64748b', label='Historical Data (6 Months)')
                    ax.plot([0], [prediction], marker='*', color='#eab308', 
                            markersize=20, markeredgecolor='black', markeredgewidth=1, 
                            label='AI Prediction')
                            
                    # Add dashed line connecting last point to prediction
                    ax.plot([-1, 0], [features[-1], prediction], linestyle='--', color='#94a3b8')
                    ax.set_xticks(range(-6, 1))
                    ax.set_xticklabels(['t-6', 't-5', 't-4', 't-3', 't-2', 't-1', 'Target Month'], 
                                     fontweight='bold')
                    ax.set_ylabel("Price (USD/oz)", fontsize=12, fontweight='500', labelpad=10)
                    
                    # Grid and Spines
                    ax.grid(True, linestyle='--', alpha=0.7, color='#cbd5e1')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_color('#94a3b8')
                    ax.spines['bottom'].set_color('#94a3b8')
                    
                    ax.legend(loc='best', frameon=True, shadow=True, fontsize=11)
                    st.pyplot(fig)
                    
                except Exception as e:
                    st.error(f"Prediction failed: {e}")
    else:
        st.warning("SVM model is not loaded properly. Please ensure 'svm_linear_model.pkl' is in the project directory.")
