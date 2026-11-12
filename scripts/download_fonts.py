"""Download Google Fonts (Noto Sans Kannada, Noto Sans Devanagari, Inter) and self-host them."""
import os
import re
import urllib.request

def download_and_self_host():
    font_dir = "frontend/public/fonts"
    os.makedirs(font_dir, exist_ok=True)
    
    url = (
        "https://fonts.googleapis.com/css2?"
        "family=Inter:wght@400;500;600;700&"
        "family=Noto+Sans+Devanagari:wght@400;500;600;700&"
        "family=Noto+Sans+Kannada:wght@400;500;600;700&"
        "display=swap"
    )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    print("Fetching Google Fonts CSS...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        css = resp.read().decode("utf-8")
        
    blocks = re.findall(r"@font-face\s*\{([^}]+)\}", css)
    print(f"Discovered {len(blocks)} @font-face declarations.")
    
    downloaded = {}
    local_rules = []
    
    for idx, block in enumerate(blocks):
        fam_m = re.search(r"font-family:\s*['\"]([^'\"]+)['\"]", block)
        weight_m = re.search(r"font-weight:\s*(\d+)", block)
        src_m = re.search(r"src:\s*url\((https://[^)]+\.woff2)\)", block)
        unicode_m = re.search(r"unicode-range:\s*([^;]+);", block)
        
        if fam_m and weight_m and src_m:
            fam = fam_m.group(1)
            weight = weight_m.group(1)
            src_url = src_m.group(1)
            urange = unicode_m.group(1).strip() if unicode_m else None
            
            clean_fam = fam.lower().replace(" ", "-")
            clean_name = f"{clean_fam}-{weight}-{idx}.woff2"
            local_path = os.path.join(font_dir, clean_name)
            
            if src_url not in downloaded:
                print(f"Downloading {clean_name} for {fam} (weight {weight})...")
                urllib.request.urlretrieve(src_url, local_path)
                downloaded[src_url] = f"/fonts/{clean_name}"
                
            local_src = downloaded[src_url]
            rule = (
                f"@font-face {{\n"
                f"  font-family: '{fam}';\n"
                f"  font-style: normal;\n"
                f"  font-weight: {weight};\n"
                f"  font-display: swap;\n"
                f"  src: url('{local_src}') format('woff2');"
            )
            if urange:
                rule += f"\n  unicode-range: {urange};"
            rule += "\n}"
            local_rules.append(rule)
            
    css_output = (
        "/* Self-hosted fonts: Noto Sans Kannada, Noto Sans Devanagari, Inter */\n"
        "/* 100% offline self-hosted from frontend/public/fonts */\n\n"
        + "\n\n".join(local_rules)
        + "\n"
    )
    
    with open("frontend/src/app/fonts.css", "w", encoding="utf-8") as f:
        f.write(css_output)
        
    print(f"Successfully generated frontend/src/app/fonts.css with {len(local_rules)} rules.")
    print(f"Downloaded {len(downloaded)} distinct woff2 font files to {font_dir}.")

if __name__ == "__main__":
    download_and_self_host()
