# 📄 DocVision AI Pro

> 🚀 High-Precision AI Document Processing Tool Powered by Mistral OCR

---

# 🌟 Overview

**DocVision AI Pro** is a high-precision, Streamlit-based document processing system powered by the `mistral-ocr-latest` model.

It intelligently:
- Analyzes document layouts
- Extracts tables with correct orientation
- Reconstructs full documents
- Fixes flipped image issues
- Prevents row/column transpose errors

---

# 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![OCR](https://img.shields.io/badge/OCR-Mistral-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

# 🚀 Key Features

## 🚀 Powered by Mistral OCR
- Uses `mistral-ocr-latest`
- High accuracy text extraction
- Native table understanding

## 🛡️ Orientation Fix System
- Auto skew detection
- Auto rotation correction
- Prevents flipped images
- Maintains correct table alignment

## 📊 Advanced Structure Detection

### 🔲 Structure Analysis Mode
- Detects grid geometry
- Counts exact rows
- Counts exact columns
- No text extraction (layout only)

### 📊 Table Extraction Mode
- Extracts tables in Markdown
- Extracts tables in HTML
- CSV download support
- Solves transpose issue

### 📄 Full Page Reconstruction
- Preserves:
  - Headers
  - Paragraphs
  - Tables
- Outputs valid structured HTML

---

# 📂 Supported Formats

- JPG
- PNG
- PDF (Multi-page supported)
- DOCX

---

# 📥 Export Options

- CSV (Table Data)
- HTML (Full Document)

---

# 📱 UI Features

- Modern milky theme
- Responsive layout
- Desktop support
- Mobile support
- Clean interface

---

# 🛠️ Installation Guide

## 1️⃣ Prerequisites

- Python 3.9+
- Mistral API Key

---

## 2️⃣ Clone Repository

```bash
git clone https://github.com/Abhishek-DS-ML-Gupta/Table-image-OCR.git
cd Table-image-OCR
```

---

## 3️⃣ Create requirements.txt

```text
streamlit
mistralai
opencv-python
numpy
pillow
beautifulsoup4
lxml
pandas
pymupdf
python-docx
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Run Application

```bash
streamlit run app.py
```

---

# 🎯 Application Modes

## 🔲 1. Structure Analysis (AI Mode)

Input:
- Image
- PDF

Output:
- Clean grid
- Row count
- Column count

Use Case:
- Validate table structure before data entry

---

## 📊 2. Table Extraction Only

Input:
- Image containing table
- PDF containing table

Output:
- Markdown table
- HTML table
- CSV file

Special Fix:
- Ensures horizontal rows remain horizontal
- No automatic transpose error

---

## 📄 3. Full Page Reconstruction

Input:
- Mixed content document

Output:
- Structured HTML
- Preserves layout hierarchy

---

# 📈 OCR Processing Pipeline

## 🔄 Step 1: Pre-Processing (OpenCV)
- Auto rotate
- Skew correction
- Image cleaning
- Noise reduction

## 🤖 Step 2: Mistral OCR Engine
- Sends processed image to `mistral-ocr-latest`
- Extracts structured content
- Understands layout natively

## 🔧 Step 3: Post-Processing
- BeautifulSoup parsing
- Pandas table processing
- Orientation validation
- Grid cleaning (Structure Mode)

---

# 📦 Dependencies Overview

| Library        | Purpose |
|---------------|----------|
| Streamlit     | Web Interface |
| Mistral AI    | OCR Engine |
| OpenCV        | Image Processing |
| PyMuPDF       | PDF Rendering |
| Pandas        | CSV & Table Parsing |
| BeautifulSoup | HTML Parsing |
| NumPy         | Image Array Processing |
| Pillow        | Image Handling |
| python-docx   | DOCX Reading |

---

# 📁 Project Structure

```
DocVision-AI-Pro/
│
├── app.py
├── requirements.txt
├── utils/
│   ├── preprocessing.py
│   ├── ocr_engine.py
│   ├── postprocessing.py
│
├── assets/
│   └── ui_styles.css
│
└── README.md
```

---

# 🔗 Documentation Links

- Mistral AI Docs: https://docs.mistral.ai/
- Streamlit Docs: https://docs.streamlit.io/

---

# ⭐ Why Choose DocVision AI Pro?

✔ Fixes OCR transpose errors  
✔ Prevents flipped tables  
✔ Accurate structure detection  
✔ Multi-format support  
✔ Intelligent full-page reconstruction  
✔ Clean modern UI  

---


# 👨‍💻 Author

Abhishek Gupta  
AI / ML Developer  
