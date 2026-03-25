import sys
import os
import time
import subprocess

def install_and_import(package, import_name):
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import('playwright', 'playwright')

print("Installing Playwright browsers...")
subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

from playwright.sync_api import sync_playwright

doc_dir = r"c:\Users\vello\OneDrive\Desktop\imp\SACAIM\SACAIM25_Project\Documentation"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    print("Screenshotting Streamlit...")
    try:
        # Streamlit might take a bit to start up, so we use a longer timeout and wait.
        page.goto('http://localhost:8501', wait_until='networkidle', timeout=30000)
        time.sleep(8)  # Give extra time for Streamlit to render custom CSS and text
        page.screenshot(path=os.path.join(doc_dir, 'streamlit_dashboard.png'), full_page=True)
        print("Streamlit screenshot saved.")
    except Exception as e:
        print(f"Error screenshotting Streamlit: {e}")
        
    print("Screenshotting FastAPI Swagger UI...")
    try:
        page.goto('http://localhost:8000/docs', wait_until='networkidle', timeout=30000)
        time.sleep(3)
        page.screenshot(path=os.path.join(doc_dir, 'fastapi_swagger.png'), full_page=True)
        print("FastAPI screenshot saved.")
    except Exception as e:
        print(f"Error screenshotting FastAPI: {e}")
        
    browser.close()

print("All screenshots generated successfully.")
