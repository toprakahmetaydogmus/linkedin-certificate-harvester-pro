<div align="center">

# 🏆 LinkedIn Certificate Harvester & Repo Portfolio Architect Pro v22.0

**Universal, Multi-Language, High-DPI Desktop Suite & Portfolio Generator**

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-CustomTkinter-00E5FF.style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Automation](https://img.shields.io/badge/Automation-Playwright-00E676.svg?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![OCR Engine](https://img.shields.io/badge/OCR-Tesseract-8A2BE2.svg?style=for-the-badge)](https://github.com/tesseract-ocr/tesseract)
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)

[TR 🇹🇷](#-türkçe-açıklama) | [EN 🇬🇧](#-english-guide)

---

</div>

## 📌 Overview / Genel Bakış

**LinkedIn Certificate Harvester & Portfolio Architect Pro** is a comprehensive desktop application designed to automatically extract, document, enhance, and showcase 100% of your LinkedIn certifications, credentials, and licenses.

It transforms scraped or imported certifications into a **responsive interactive HTML portfolio (`index.html`)** and an **ultra-stylish GitHub Profile `README.md`**, before automatically publishing them straight to your GitHub repository with zero configuration hassle.

---

## ✨ Key Features / Temel Özellikler

- 🌐 **LinkedIn AI Harvester (Zero-Drop Engine)**
  - Automated Playwright browser context that scrolls and triggers GraphQL pagination batches safely.
  - Guarantees 100% credential recovery across all paginated certification items without missing data.
  - Automatically detects the profile owner's name and headline from the live page.

- 📸 **Ultra HD Document Preservation Engine**
  - Converts low-res LinkedIn thumbnail CDN URLs to high-res `1280x1280` document images.
  - Automatically generates clean vector-style badge cards for courses without uploaded media assets (avoiding full-page screenshot artifacts).

- 🎨 **Luxury Interactive HTML Portfolio Architect**
  - Generates a single-file, zero-dependency, ultra-modern HTML portfolio (`index.html`).
  - Supports dark/light themes, instant search, dynamic issuer filtering chips, list/grid layout toggle, and interactive image lightbox modal.

- 📜 **GitHub Profile README Architect**
  - Generates markdown tables with high-res asset previews, credential badges, issuer tags, and direct online verification links.
  - Includes custom themes (*Tokyo Night Cyberpunk*, *Modern Minimal Glass*, *Matrix Hacker Green*, *Executive Sapphire*).

- 🐙 **GitHub Auto-Pusher**
  - Seamlessly initializes git repositories, commits assets (`README.md`, `index.html`, and images), and pushes directly to GitHub via Git CLI or pure Python REST API fallback (PAT token).

- 🌍 **Multi-Language Engine**
  - Instant 1-click toggle between **Türkçe (TR 🇹🇷)** and **English (EN 🇬🇧)**.

- 🔒 **Zero-Leak Privacy Guarantee**
  - No cookies, login credentials, or sensitive data are stored in your export repository.

- 🚀 **Executable Ready (.exe)**
  - Fully packaged desktop app using CustomTkinter and PyInstaller (`build_exe.py`).

---

## 🏗️ System Architecture & Workflow / Sistem Mimarısı

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      LINKEDIN CERTIFICATE HARVESTER                     │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
      ┌──────────────────────────────┼──────────────────────────────┐
      ▼                              ▼                              ▼
 [Playwright Web Harvester]   [Local HTML Import / OCR]    [Manual Entry / PDF]
      │                              │                              │
      └──────────────────────────────┼──────────────────────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    HD Image Engine & OCR    │
                      │  - 1280px CDN Upscaling     │
                      │  - Vector Badge Generator   │
                      │  - Tesseract OCR Extraction │
                      └─────────────────────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    Certificate Store JSON   │
                      └─────────────────────────────┘
                                     │
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
┌───────────────────────┐                         ┌───────────────────────┐
│ Dynamic README.md     │                         │ Interactive index.html│
│ (Markdown Portfolio)  │                         │ (HTML Web Portfolio)  │
└───────────────────────┘                         └───────────────────────┘
            │                                                 │
            └────────────────────────┬────────────────────────┘
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │     GitHub Auto-Pusher      │
                      │  (Git CLI / REST API Fallback)│
                      └─────────────────────────────┘
```

---

## ⚙️ Installation & Requirements / Kurulum ve Gereksinimler

### Prerequisites / Ön Gereksinimler

1. **Python 3.9+** installed on your system.
2. *(Optional, for OCR)* **Tesseract OCR**:
   - Windows: Install via `tesseract-ocr-w64-setup.exe` or let `app.py` auto-detect default paths (`C:\Program Files\Tesseract-OCR\tesseract.exe`).
3. *(Optional, for automated pushing)* **Git CLI** or a **GitHub Personal Access Token (PAT)**.

### Quick Setup / Hızlı Kurulum

```bash
# 1. Clone the repository
git clone https://github.com/toprakahmetaydogmus/linkedin-certificate-harvester-pro.git
cd linkedin-certificate-harvester-pro

# 2. Install required Python dependencies
pip install -r requirements.txt

# 3. Install Playwright browser binaries
playwright install chromium
```

---

## 🚀 Usage Guide / Kullanım Rehberi

### 1. Launching the Desktop Application
Run the main script:
```bash
python app.py
```

### 2. Harvester Workflow / Sertifika Toplama
1. Open the **LinkedIn AI Harvester** tab.
2. Enter your LinkedIn Certifications URL (e.g. `https://www.linkedin.com/in/username/details/certifications/`).
3. Click **🚀 Launch Browser**. Log into LinkedIn if prompted.
4. Click **⚡ HARVEST ALL CERTIFICATES**. The automated engine will perform paced deep scrolls, triggering GraphQL requests and extracting 100% of certificates, issuers, dates, credential IDs, verification links, and HD images.
5. Alternatively, import from a saved LinkedIn HTML file or local PDF/image files.

### 3. Managing Certificates / Sertifika Yönetimi
1. Navigate to the **📜 Certificates** tab to view all harvested credentials.
2. Inspect metadata, verify links, copy markdown snippets, or manually delete/add missing certifications.

### 4. Generating Portfolios / Portfolyo Oluşturma
1. Go to the **🎨 README & HTML Portfolio** tab.
2. Select your visual theme (e.g., *Tokyo Night Cyberpunk*).
3. Click **💾 Save as index.html** to export the standalone web portfolio.
4. Click **💾 Save as README.md** to export the GitHub Markdown portfolio.
5. Click **🌐 Open Live HTML Portfolio** to preview the interactive web page directly in your default browser.

### 5. Publishing to GitHub / GitHub'a Aktarım
1. Go to the **🐙 GitHub Auto-Pusher** tab.
2. Set your **Export Directory**, **GitHub Username**, **Repository Name** (e.g. `profile-readme-certificates`), and **Commit Message**.
3. (Optional) Provide a GitHub PAT Token if Git CLI is not installed.
4. Click **🚀 Push README, index.html & Assets to GitHub**.

---

## 🛠️ Building Standalone Executable (.exe) / Executable Derleme

You can package the entire application into a portable, single-file Windows executable (`.exe`) without needing Python on target machines:

```bash
python build_exe.py
```

The compiled binary will be saved in the `dist/` directory as `LinkedInCertArchitectPro.exe`.

---

## 📁 Project Structure / Proje Yapısı

```
.
├── app.py                  # Main CustomTkinter Application & Logic Engine
├── build_exe.py            # PyInstaller build automation script
├── requirements.txt        # Python package dependencies
├── index.html              # Generated sample interactive HTML portfolio
├── assets/
│   ├── logo.ico            # Windows Application Icon
│   ├── logo.png            # Visual Logo Branding
│   └── template.html       # Portfolio HTML Template
└── README.md               # Documentation
```

---

## 🔒 Security & Privacy / Güvenlik ve Gizlilik

- **Local Storage:** Saved certificate metadata and downloaded high-res assets reside locally in `~/.linkedin_cert_architect`.
- **Zero Session Persistence in Repositories:** Browser cookies and session state are kept strictly in your local user directory (`chrome_user_session`) and are never uploaded or committed to GitHub repositories.

---

## 🇹🇷 Türkçe Açıklama

**LinkedIn Certificate Harvester & Repo Portfolio Architect Pro**, LinkedIn üzerindeki tüm lisans, sertifika ve başarı belgelerinizi %100 eksiksiz biçimde otomatik toplayan, görsellerini yüksek çözünürlüğe (HD) dönüştüren ve bunları hem **canlı etkileşimli HTML portfolyoya (`index.html`)** hem de **GitHub Profile `README.md`** sayfasına dönüştüren masaüstü yazılımıdır.

### Öne Çıkan Özellikler:
- **Derin Tarama Motoru:** Sayfayı kademeli kaydırarak GraphQL verilerinin tamamını yakalar.
- **HD Belge Dönüştürme:** Küçük resim bağlantılarını `1280px` HD kalitesine yükseltir; belgesi olmayan kurslar için özel nitelikli kartlar üretir.
- **Canlı Etkileşimli Portfolyo:** Arama, filtreleme, tema değiştirme ve tam ekran belge inceleme modallı `index.html` üretir.
- **Tek Tıkla GitHub Push:** Hazırlanan tüm belgeleri, görselleri ve Markdown/HTML dosyalarını doğrudan GitHub reponuza yükler.
- **Çift Dil Desteği:** Türkçe ve İngilizce arayüz seçeneği.

---

## 👤 Author & Credits / Yazar ve Teşekkürler

- **Platform Architect & Developer:** [Toprak Ahmet Aydoğmuş](https://github.com/toprakahmetaydogmus)
- **Target Showcase Profile:** Yusuf Dalbudak

---

<div align="center">
  <sub>Built with ❤️ using Python, CustomTkinter, Playwright, and BeautifulSoup4.</sub>
</div>
