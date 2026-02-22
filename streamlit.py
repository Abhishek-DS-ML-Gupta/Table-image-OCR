# pip install streamlit mistralai opencv-python numpy pillow beautifulsoup4 lxml pandas pymupdf python-docx

import streamlit as st
from mistralai import Mistral
import cv2
import numpy as np
from PIL import Image
import io
import base64
from bs4 import BeautifulSoup
import pandas as pd
import tempfile
import os
import json

# PDF Handling
import fitz  # PyMuPDF

# Word Handling
from docx import Document

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="DocVision AI - Advanced Modes",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# CUSTOM CSS
# =============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: linear-gradient(180deg, #FDFBF7 0%, #F3F0E6 100%); }
    
    .app-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .app-header h1 {
        background: linear-gradient(135deg, #1A202C 0%, #4A5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .app-header p { color: #718096; font-size: 1rem; margin: 0; }

    /* Mode Cards */
    .mode-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .mode-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.25rem;
        border: 2px solid #E2E8F0;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    
    .mode-card.active {
        border-color: #4A90E2;
        background: #EBF8FF;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.15);
    }
    
    .mode-icon { font-size: 1.8rem; margin-bottom: 0.5rem; display: block; }
    .mode-title { font-size: 1rem; font-weight: 700; color: #2D3748; margin-bottom: 0.25rem; display: block; }
    .mode-desc { font-size: 0.8rem; color: #718096; }
    
    /* Layout */
    .result-box {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        height: 100%;
    }
    
    .stat-box {
        background: #F7FAFC;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    
    .stat-value { font-size: 2rem; font-weight: 800; color: #2D3748; }
    .stat-label { font-size: 0.8rem; color: #718096; text-transform: uppercase; }

    .stButton>button {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100%;
    }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #38A169 0%, #2F855A 100%) !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.8rem !important;
        font-weight: 600 !important;
        border: none !important;
        width: auto !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .mode-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    api_key = st.text_input("Mistral API Key", type="password", placeholder="Enter Key...")
    
    if api_key:
        client = Mistral(api_key=api_key)
        st.success("🔑 Connected")
    else:
        st.info("👈 Enter API Key")
    
    st.markdown("---")
    # Language Configuration
    st.markdown("#### 🌐 Language Hint")
    lang_input = st.text_input("Languages (comma separated)", value="English, Hindi", key="lang_input")
    lang_list = [l.strip() for l in lang_input.split(',') if l.strip()]

# =============================
# HELPER FUNCTIONS
# =============================
def image_to_base64(image):
    """Converts PIL Image to Base64 string safely."""
    if image.mode == "RGBA":
        image = image.convert("RGB")
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def parse_json_output(text):
    """Extract JSON from AI response."""
    try:
        # Try finding JSON block
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        return json.loads(text.strip())
    except:
        return None

def parse_html_output(text):
    """Extract HTML from AI response."""
    if "```html" in text:
        return text.split("```html")[1].split("```")[0].strip()
    elif "<table" in text:
        # Try to extract just the table if no code block
        soup = BeautifulSoup(text, "lxml")
        table = soup.find("table")
        return str(table) if table else text
    return text

def get_table_stats(html):
    try:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        if not table: return 0, 0
        rows = len(table.find_all("tr"))
        cols = max([len(r.find_all(["td", "th"])) for r in table.find_all("tr")])
        return rows, cols
    except:
        return 0, 0

def html_to_csv(html):
    try:
        dfs = pd.read_html(str(html))
        if dfs: return dfs[0].to_csv(index=False).encode('utf-8')
    except: pass
    return None

def md_to_csv(md_text):
    try:
        dfs = pd.read_html(md_text)
        if dfs: return dfs[0].to_csv(index=False).encode('utf-8')
    except: pass
    return None

# =============================
# FILE PROCESSORS
# =============================
def process_upload(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    data = {"preview": None, "pages": []}
    
    try:
        if ext in [".jpg", ".jpeg", ".png"]:
            img = Image.open(uploaded_file)
            if img.mode == "RGBA": img = img.convert("RGB")
            data["pages"].append({"image": img, "num": 1})
            data["preview"] = img
            
        elif ext == ".pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            doc = fitz.open(tmp_path)
            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                data["pages"].append({"image": img, "num": i+1})
            doc.close()
            os.unlink(tmp_path)
            if data["pages"]: data["preview"] = data["pages"][0]["image"]
            
        elif ext == ".docx":
            # Simplified DOCX extraction
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            doc = Document(tmp_path)
            # Extract images
            for i, rel in enumerate(doc.part.rels.values()):
                if "image" in rel.target_ref:
                    try:
                        img = Image.open(io.BytesIO(rel.target_part.blob))
                        if img.mode == "RGBA": img = img.convert("RGB")
                        data["pages"].append({"image": img, "num": i+1})
                    except: pass
            os.unlink(tmp_path)
            if data["pages"]: data["preview"] = data["pages"][0]["image"]
            
    except Exception as e:
        st.error(f"File Error: {e}")
        
    return data

# =============================
# MISTRAL PROCESSING
# =============================
def get_prompt(mode, lang_list):
    """Returns specific prompt based on mode."""
    
    langs = ", ".join(lang_list) if lang_list else "Auto Detect"
    
    # Mode 1: Structure Analysis
    if mode == "Structure Analysis (AI)":
        return f"""
        System: You are a precise document layout analysis engine. Your goal is to determine the grid structure of the document.
        Task: Analyze the image and count the exact number of rows and columns in the main data table/grid.
        Languages detected: {langs}.
        
        Constraints:
        - Do not count header rows separately from data rows; count total rows.
        - If there are nested tables, count the outer grid structure.
        - Output MUST be valid JSON.
        
        Output Format:
        {{ "rows": integer, "cols": integer }}
        """

    # Mode 2: Table Extraction
    elif mode == "Table Extraction Only":
        return f"""
        System: You are a highly accurate OCR table extraction engine.
        Task: Extract the table content from the image into a Markdown table.
        Languages detected: {langs}.
        
        Rules:
        1. Do not add any introductory text.
        2. Extract all rows and columns exactly as seen.
        3. Use Markdown table format (| Col1 | Col2 |).
        4. If a cell is empty, leave it blank but keep the column separator.
        """

    # Mode 3: Full Page Reconstruction
    else:
        return f"""
        System: You are an intelligent document reconstruction engine.
        Task: Reconstruct the document content EXACTLY as it appears visually, preserving layout.
        Languages detected: {langs}.
        
        Instructions:
        1. If the content is a table or grid, output it as HTML <table>.
        2. If it is text, preserve headers and paragraphs.
        3. For tables: Wrap the HTML in a code block: ```html ... ```
        4. Ensure all data is captured accurately.
        """

def process_page(image, mode):
    """Sends image to Mistral OCR API."""
    b64 = image_to_base64(image)
    prompt = get_prompt(mode, lang_list)
    
    try:
        # Mistral OCR Call
        response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/png;base64,{b64}"
            }
        )
        
        # Extract raw text from OCR
        raw_text = response.pages[0].markdown if response.pages else ""
        
        # If structure mode, we need to send the raw text to a chat model to get JSON
        # OR we can just parse the markdown for table structure.
        # Since OCR gives markdown, for 'Structure Analysis' we will parse the markdown table.
        
        if mode == "Structure Analysis (AI)":
            # Parse markdown table to count rows/cols
            if "|" in raw_text:
                lines = [l for l in raw_text.split('\n') if l.strip().startswith('|')]
                # Remove separator lines (e.g., |---|---|)
                data_lines = [l for l in lines if not all(c in '|- :' for c in l)]
                
                rows = len(data_lines)
                cols = len(data_lines[0].split('|')) - 2 if data_lines else 0
                
                return {"type": "stats", "rows": rows, "cols": cols, "raw": raw_text}
            else:
                # Fallback if OCR didn't find table, ask LLM to count visually
                # (This requires a vision-chat model call which is slower, using OCR is faster)
                # For now returning 0 if no table detected
                return {"type": "stats", "rows": 0, "cols": 0, "raw": raw_text}
        
        elif mode == "Table Extraction Only":
            return {"type": "markdown", "content": raw_text}
            
        else: # Full Page
            # Check if OCR returned a table, convert to HTML for display
            if "|" in raw_text and raw_text.count('|') > 5:
                # It's likely a markdown table, convert to HTML
                try:
                    dfs = pd.read_html(raw_text)
                    html = dfs[0].to_html(index=False, border=1) if dfs else raw_text
                    return {"type": "html", "content": html}
                except:
                    return {"type": "text", "content": raw_text}
            return {"type": "text", "content": raw_text}

    except Exception as e:
        return {"type": "error", "content": str(e)}

# =============================
# MAIN UI
# =============================
st.markdown("""
<div class="app-header">
    <h1>📄 DocVision AI Pro</h1>
    <p>Structure Analysis • Table Extraction • Full Page Reconstruction</p>
</div>
""", unsafe_allow_html=True)

# --- Mode Selection ---
st.markdown("#### 🎯 Select Processing Mode")

if "mode" not in st.session_state:
    st.session_state.mode = "Table Extraction Only"

modes = [
    ("Structure Analysis (AI)", "🔲", "Counts rows & cols"),
    ("Table Extraction Only", "📊", "Markdown Table"),
    ("Full Page Reconstruction", "📄", "HTML Layout")
]

cols_mode = st.columns(3)
for i, (m, icon, desc) in enumerate(modes):
    with cols_mode[i]:
        is_active = st.session_state.mode == m
        st.markdown(f"""
        <div class="mode-card {'active' if is_active else ''}" onclick="">
            <span class="mode-icon">{icon}</span>
            <span class="mode-title">{m}</span>
            <span class="mode-desc">{desc}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select", key=f"btn_{i}"):
            st.session_state.mode = m

st.markdown("---")

# --- Upload ---
uploaded_file = st.file_uploader("📎 Upload Image, PDF or DOCX", type=["png", "jpg", "jpeg", "pdf", "docx"])

# --- Processing ---
if uploaded_file and api_key:
    doc_data = process_upload(uploaded_file)
    
    if doc_data["pages"]:
        st.success(f"✅ Loaded {len(doc_data['pages'])} page(s)")
        
        # Preview in Expander
        with st.expander("🖼️ Preview Source", expanded=False):
            if len(doc_data["pages"]) > 1:
                c_prev = st.columns(min(4, len(doc_data["pages"])))
                for idx, p in enumerate(doc_data["pages"]):
                    if idx < len(c_prev):
                        c_prev[idx].image(p["image"], caption=f"Page {p['num']}", use_container_width=True)
            else:
                st.image(doc_data["preview"], use_container_width=True)

        # Process Button
        if st.button(f"🚀 Process ({st.session_state.mode})", type="primary"):
            results = []
            prog = st.progress(0)
            
            for i, page in enumerate(doc_data["pages"]):
                prog.progress((i+1)/len(doc_data["pages"]))
                res = process_page(page["image"], st.session_state.mode)
                res["page_num"] = page["num"]
                res["image"] = page["image"]
                results.append(res)
            
            prog.empty()
            st.session_state.results = results

# --- Results Display ---
if "results" in st.session_state:
    results = st.session_state.results
    
    for res in results:
        st.markdown(f"### 📄 Page {res['page_num']}")
        
        # 2 Column Layout: Source | Result
        col_src, col_res = st.columns([1, 2])
        
        with col_src:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.image(res["image"], caption="Source", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_res:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            
            # Handle Different Modes
            if res["type"] == "stats":
                # Structure Mode
                r, c = res["rows"], res["cols"]
                
                s1, s2 = st.columns(2)
                with s1:
                    st.markdown(f'<div class="stat-box"><div class="stat-value">{r}</div><div class="stat-label">Rows</div></div>', unsafe_allow_html=True)
                with s2:
                    st.markdown(f'<div class="stat-box"><div class="stat-value">{c}</div><div class="stat-label">Columns</div></div>', unsafe_allow_html=True)
                
                with st.expander("View Raw OCR Data"):
                    st.code(res["raw"], language="markdown")
                    
            elif res["type"] == "markdown":
                # Table Extraction Mode
                st.markdown("**Extracted Table:**")
                st.markdown(res["content"])
                
                csv = md_to_csv(res["content"])
                if csv:
                    st.download_button("📥 Download CSV", data=csv, file_name=f"page_{res['page_num']}.csv", mime="text/csv")
                    
            elif res["type"] == "html":
                # Full Page (HTML Table detected)
                st.markdown("**Reconstructed Table:**")
                st.components.v1.html(res["content"], height=400, scrolling=True)
                
                csv = html_to_csv(res["content"])
                if csv:
                    st.download_button("📥 Download CSV", data=csv, file_name=f"page_{res['page_num']}.csv", mime="text/csv")
            
            elif res["type"] == "text":
                # Full Page (Text)
                st.markdown("**Extracted Content:**")
                st.markdown(res["content"])
            
            elif res["type"] == "error":
                st.error(f"Error: {res['content']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        