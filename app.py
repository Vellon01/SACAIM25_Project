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

# --- Main App ---
st.title("🪙 Gold Price Forecasting & Prediction")
st.markdown("Use machine learning models to forecast future gold prices or predict the price based on recent historic data.")

with st.sidebar:
    st.header("Settings")
    model_choice = st.radio(
        "Choose a Model:",
        ("SARIMA (Time Series Forecast)", "SVM (Price Prediction)")
    )
    st.info("ℹ️ **SARIMA** is best for forecasting future trends based on historical sequences.\n\nℹ️ **SVM** is used here to predict the next month's price given the previous 6 months' prices.")

if model_choice == "SARIMA (Time Series Forecast)":
    st.header("📈 SARIMA Forecasting")
    st.markdown("Forecast gold prices into the future based on historical trends.")
    
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
                        # Create a quick plot
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.plot(range(1, n_periods + 1), forecast_values, marker='o', linestyle='-', color='b', label='Forecasted Price')
                        ax.set_title(f"Gold Price Forecast for Next {n_periods} Months")
                        ax.set_xlabel("Months into the Future")
                        ax.set_ylabel("Predicted Price (USD)")
                        ax.grid(True)
                        ax.legend()
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
    st.header("🎯 SVM Price Prediction")
    st.markdown("Predict the next month's gold price based on the prices of the last 6 months.")
    
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
                    
                    st.success(f"The predicted gold price for the next month is: **${prediction:,.2f}**")
                    
                    st.subheader("Trend Visualization")
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(range(-6, 0), features, marker='o', color='gray', label='Past 6 Months')
                    ax.plot([0], [prediction], marker='*', color='gold', markersize=15, label='Next Month Prediction')
                    ax.set_xticks(range(-6, 1))
                    ax.set_xticklabels(['t-6', 't-5', 't-4', 't-3', 't-2', 't-1', 'Prediction'])
                    ax.set_ylabel("Price (USD)")
                    ax.grid(True, linestyle='--', alpha=0.6)
                    ax.legend()
                    st.pyplot(fig)
                    
                except Exception as e:
                    st.error(f"Prediction failed: {e}")
    else:
        st.warning("SVM model is not loaded properly. Please ensure 'svm_linear_model.pkl' is in the project directory.")
