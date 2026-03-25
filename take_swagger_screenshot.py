import sys
import os
import time
from playwright.sync_api import sync_playwright

doc_dir = r"c:\Users\vello\OneDrive\Desktop\imp\SACAIM\SACAIM25_Project\Documentation"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080}, color_scheme='dark')
    
    try:
        print("Waiting for FastAPI server to stabilize...")
        time.sleep(4) 
        print("Capturing FastAPI Swagger UI in Dark Mode...")
        page.goto('http://127.0.0.1:8000/docs', wait_until='networkidle', timeout=30000)
        time.sleep(2) # Give swagger JS time to render all components
        
        # Inject standard invert CSS to force Dark Mode onto Swagger UI
        css = """
        html { filter: invert(90%) hue-rotate(180deg); background: #121212; }
        body { background: #121212; }
        img, video { filter: invert(100%) hue-rotate(180deg); }
        """
        page.add_style_tag(content=css)
        time.sleep(1)
        
        page.screenshot(path=os.path.join(doc_dir, 'fastapi_swagger.png'), full_page=True)
        print("Swagger UI screenshot successfully saved.")
        
    except Exception as e:
        print(f"Error capturing Swagger UI: {e}")
    finally:
        browser.close()
