import sys
import time
import os
from playwright.sync_api import sync_playwright

doc_dir = r"c:\Users\vello\OneDrive\Desktop\imp\SACAIM\SACAIM25_Project\Documentation"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # the color_scheme='dark' forces playwright to prefer dark mode if applicable
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, color_scheme='dark')
    
    try:
        print("Capturing SARIMA Forecast in Dark Mode...")
        page.goto('http://localhost:8501', wait_until='networkidle', timeout=30000)
        time.sleep(6) # Wait for Streamlit to initialize models and UI
        
        # Click "Generate Forecast"
        page.locator("button:has-text('Generate Forecast')").click()
        
        # Wait for success message or a small delay
        time.sleep(10) # Wait for forecast computation and chart rendering
        
        page.screenshot(path=os.path.join(doc_dir, 'sarima_dark_forecast.png'), full_page=True)
        print("SARIMA screenshot saved.")
        
        print("Capturing SVM Prediction in Dark Mode...")
        # Click the SVM radio button. Streamlit handles radio buttons in a label div
        page.locator("label", has_text="SVM (Next Month Prediction)").click()
        time.sleep(3)
        
        # Click "Predict Next Month's Price"
        page.locator("button", has_text="Predict Next Month's Price").click()
        time.sleep(5) # Wait for prediction and metric card visualization
        
        page.screenshot(path=os.path.join(doc_dir, 'svm_dark_predict.png'), full_page=True)
        print("SVM screenshot saved.")
        
    except Exception as e:
        print(f"Error during playwright interactions: {e}")
        page.screenshot(path=os.path.join(doc_dir, 'error_state.png'), full_page=True)

    finally:
        browser.close()

print("Dark mode interactive screenshots captured.")
