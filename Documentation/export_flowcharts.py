import base64
import json
import urllib.request
import re
import os

markdown_file = os.path.join(os.path.dirname(__file__), 'project_flowcharts.md')

def generate_pngs():
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all mermaid code blocks
    mermaid_blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    filenames = ['architecture_flow.png', 'user_flow.png', 'data_pipeline.png']

    for i, block in enumerate(mermaid_blocks):
        if i >= len(filenames):
            break
        
        state = {
            "code": block.strip(),
            "mermaid": {"theme": "default"}
        }
        
        json_bytes = json.dumps(state).encode('utf-8')
        # mermaid.ink requires standard base64 string
        b64_string = base64.b64encode(json_bytes).decode('utf-8')
        
        url = "https://mermaid.ink/img/" + b64_string
        
        out_file = os.path.join(os.path.dirname(__file__), filenames[i])
        print(f"Downloading {filenames[i]} from mermaid.ink...")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                with open(out_file, 'wb') as out:
                    out.write(response.read())
            print(f"Successfully saved {filenames[i]}")
        except Exception as e:
            print(f"Failed to download {filenames[i]}. Error: {e}")

if __name__ == "__main__":
    print("Starting generation of PNG files from Mermaid definitions...")
    generate_pngs()
    print("Done!")
