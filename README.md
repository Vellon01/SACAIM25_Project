# Gold Price Forecasting & Prediction 

This project leverages machine learning to forecast and track gold prices using two distinct modeling approaches: **SARIMA** (Seasonal Autoregressive Integrated Moving Average) and **SVR** (Support Vector Regression, specifically a linear model).

The project is structured with a robust **FastAPI backend** for serving model predictions, paired with an interactive **Streamlit dashboard** for visualizing forecasts and market indicators. Recent updates include comprehensive documentation generation, automated UI/API screenshot capture, and architectural flowcharts.

## 🧠 Models Overview

1. **SARIMA Model** (`sarima_model.pkl`)
   - **Purpose**: Time series forecasting of future gold prices.
   - **Use Case**: Predicting future trends based solely on historical price data over a specific number of periods (days/months).

2. **SVM Linear Model** (`svm_linear_model.pkl`)
   - **Purpose**: Price prediction based on concurrent market features.
   - **Use Case**: Given current market indicators (6 specific numerical features), predict the current or imminent gold price.

## 🚀 API Architecture (FastAPI)

The backend is built with FastAPI to ensure high performance, automatic documentation generation, and straightforward deployment.

### Endpoints
- `GET /` - Health check. Verifies if both models have been successfully loaded into memory.
- `POST /predict/sarima` - Accepts `n_periods` (integer) and returns a list of future forecasted prices.
- `POST /predict/svm` - Accepts exactly 6 `features` (list of floats) and returns the predicted price based on those market conditions.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+ (Python 3.12+ recommended)
- `pip`

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd SACAIM25_Project
```

### 2. Install Dependencies
Install all required libraries, including FastAPI, Scikit-Learn, and statsmodels:
```bash
pip install -r requirements.txt
pip install fastapi uvicorn httpx pmdarima
```

*(Note: If you have conflicting Python versions, use `python -m pip install ...` to ensure it targets your active environment).*

## 🏃‍♂️ Running the API Locally

To start the FastAPI server locally, run the following command from the project root:

```bash
uvicorn api:app --reload
```

The server will start on `http://127.0.0.1:8000`.

### Viewing the Interactive API Docs
FastAPI automatically generates interactive Swagger documentation. Once the server is running, navigate to:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Here, you can visually test both the `/predict/sarima` and `/predict/svm` endpoints right from your browser!

## 📊 Streamlit Interactive Dashboard

A standalone Streamlit application is available to visually interact with the models. It loads the `.pkl` models directly for a simple, monolithic deployment without needing the API running.

🌐 **Live Demo:** [https://goldpriceprediction0.streamlit.app/](https://goldpriceprediction0.streamlit.app/)

To launch the dashboard:
```bash
streamlit run app.py
```
This will open a browser window at `http://localhost:8501`.

## 📚 Documentation & Architecture

The `Documentation/` directory contains in-depth reports, diagrams, and automation scripts to maintain project documentation:
- **Mermaid Flowcharts**: Visualizing system architecture (`architecture_flow.mmd`), data pipelines (`data_pipeline.mmd`), and user flows (`user_flow.mmd`).
- **Word Documents**: Automatically generated, structured `.docx` files detailing domain knowledge and system design.
- **Automation Scripts**: Python automation (`build_docs*.py`, `take_screenshots.py`, `export_flowcharts.py`, etc.) automatically captures UI/API screenshots and compiles the final documentation layout.

## 📂 Project Structure
```text
SACAIM25_Project/
├── api.py                      # FastAPI application script
├── app.py                      # Streamlit dashboard application
├── test_api.py                 # Local testing script for the API
├── sarima_model.pkl            # Trained SARIMA forecasting model
├── svm_linear_model.pkl        # Trained Support Vector prediction model
├── requirements.txt            # Project dependencies
├── research.ipynb              # Model exploration and training notebook
├── Documentation/              # Architecture diagrams, Word docs, and Generation Scripts
│   ├── build_docs_v2.py        # Docx generation pipeline
│   ├── export_flowcharts.py    # Generates PNGs from Mermaid files
│   ├── take_dark_screenshots.py # Automates UI screenshot capture
│   └── ...                     # System diagrams (.mmd, .png) & textual docs
├── take_swagger_screenshot.py  # Script for capturing Swagger UI snapshot
└── README.md                   # This file
```

## 📝 License
This project was developed for the SACAIM 2025 conference
