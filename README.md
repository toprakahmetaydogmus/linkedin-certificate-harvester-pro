<div align="center">

# 🏆 LinkedIn Certificate Harvester & GitHub Portfolio Architect Pro

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Automated_Scraper-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![Tesseract OCR](https://img.shields.io/badge/Tesseract-Vision_OCR-5C6BC0?style=for-the-badge&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter_Dark-00E5FF?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![GitHub API](https://img.shields.io/badge/GitHub-Auto_Pusher-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/rest)

**AI-Powered LinkedIn Certificate Extractor, OCR Vision Analyzer, Dynamic Profile README Architect & Universal GitHub Auto-Pusher.**

</div>

---

## 🌟 Key Features

- **🌐 LinkedIn AI Harvester (Playwright & BS4)**:
  - Automates profile navigation, expands certification sections, and extracts certificate titles, issuers, issue dates, credential IDs, and direct verification URLs.
  - Takes pixel-perfect high-resolution screenshots of certificate cards.
- **👁️ OCR Vision Engine (Tesseract + PIL)**:
  - Multi-pass image enhancement (contrast optimization, grayscale thresholding, noise removal) to extract verified text from images & PDFs.
- **📂 Local Certificate PDF/Image Batch Importer**:
  - Ingests local `.pdf`, `.png`, `.jpg` certificates with zero cloud dependency.
- **🎨 Dynamic Portfolio & Profile README Architect**:
  - Live preview with rich cyberpunk and modern dark themes (*Tokyo Night*, *Minimal Glass*, *Matrix Green*, *Sapphire*).
  - Generates SVG banners, shield badges, credential tables, and OCR summaries.
- **🐙 Universal GitHub Auto-Pusher**:
  - Checks if `git` is on system `PATH`; auto-installs via **Winget** if missing.
  - **Pure Python REST API fallback**: pushes commits & creates repos even if Git is not installed!
- **🛡️ Privacy First & Zero-Hardcoding**:
  - No credentials, tokens, or personal info stored in source code. Fully customizable for any user.

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/toprakahmetaydogmus/linkedin-certificate-harvester-pro.git
cd linkedin-certificate-harvester-pro
pip install -r requirements.txt
playwright install chromium
```

### 2. Launch Application
```bash
python app.py
```

---

## 🛠️ Architecture Overview

```
linkedin-certificate-harvester-pro/
├── app.py                     # Main CustomTkinter GUI & Orchestration Engine
├── requirements.txt           # Dependency Manifest
├── .gitignore                 # Privacy & Cache Filter
└── README.md                  # Project Documentation
```

---

## 📜 License
MIT License. Open-source & free for developers and researchers.
