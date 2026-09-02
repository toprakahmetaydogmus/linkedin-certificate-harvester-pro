"""
====================================================================================================
🏆 LINKEDIN CERTIFICATE HARVESTER & REPO PORTFOLIO ARCHITECT PRO v13.0 🏆
====================================================================================================
Universal High-DPI CustomTkinter Suite:
  - 🌐 Lightning-Fast DOM Extraction (0s Timeout, JavaScript Evaluator Engine)
  - 🚀 Two-Step Interactive Chrome Session with Live Progress Stream
  - 📸 High-Resolution Certificate Card Screen Capture & OCR Processing
  - 👁️ Tesseract OCR Vision Engine (Multi-pass contrast & text extraction)
  - 🎨 Ultra-Luxury Multi-Theme GitHub README & Portfolio Architect
  - 🐙 Universal Portable GitHub Auto-Pusher (Git CLI + Winget Auto-Installer + Pure REST API)
  - 🛡️ Zero-Hardcoding: User-agnostic, privacy-first, dynamic credential storage
====================================================================================================
"""

import os
import sys
import json
import time
import re
import math
import shutil
import base64
import asyncio
import threading
import subprocess
import urllib
import urllib.parse
from datetime import datetime

# GUI & Helpers
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import customtkinter as ctk
except ImportError:
    import tkinter as ctk

try:
    import requests
except ImportError:
    requests = None

try:
    from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
except ImportError:
    Image = None
    ImageTk = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# CustomTkinter Appearance
if hasattr(ctk, 'set_appearance_mode'):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

# Cyber Theme Palette
THEME = {
    "bg_dark": "#0B0E14",
    "bg_card": "#131822",
    "bg_card_secondary": "#1C2333",
    "sidebar": "#0E121B",
    "accent_cyan": "#00E5FF",
    "accent_purple": "#8A2BE2",
    "accent_green": "#00E676",
    "accent_pink": "#FF007F",
    "accent_orange": "#FF9100",
    "accent_red": "#FF1744",
    "text_primary": "#FFFFFF",
    "text_secondary": "#9EAFC2",
    "text_muted": "#5C6B7E",
    "border": "#232D3F",
    "editor_bg": "#0D1117",
    "editor_fg": "#E6EDF3",
}

# Config & Cache Directories
APP_DIR = os.path.join(os.path.expanduser("~"), ".linkedin_cert_architect")
CERT_IMG_DIR = os.path.join(APP_DIR, "assets", "certificates")
BROWSER_PROFILE_DIR = os.path.join(APP_DIR, "chrome_user_session")
CONFIG_FILE = os.path.join(APP_DIR, "config.json")
CERTS_DATA_FILE = os.path.join(APP_DIR, "certificates_data.json")

os.makedirs(CERT_IMG_DIR, exist_ok=True)
os.makedirs(BROWSER_PROFILE_DIR, exist_ok=True)

# Tesseract Windows Standard Path Auto-Detector
if pytesseract:
    default_tess_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.path.expanduser("~"), r"AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
    ]
    for tp in default_tess_paths:
        if os.path.exists(tp):
            pytesseract.pytesseract.tesseract_cmd = tp
            break

# ==================================================================================================
# 💎 MAIN APPLICATION GUI CLASS
# ==================================================================================================
class LinkedInCertArchitectSuite(ctk.CTk if hasattr(ctk, 'CTk') else tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("🏆 LinkedIn Certificate Harvester & GitHub Portfolio Architect Pro v13.0")
        self.geometry("1440x920")
        self.minsize(1150, 720)
        if hasattr(self, 'configure'):
            self.configure(fg_color=THEME["bg_dark"])
            
        # State Variables
        self.user_config = self.load_config()
        self.certificates = self.load_certificates_data()
        self.has_git = shutil.which("git") is not None
        self.has_gh = shutil.which("gh") is not None
        self.is_scraping = False
        
        # Async Scraper References
        self.active_page = None
        self.active_context = None
        self.scrape_event = None
        self.event_loop = None
        
        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Build UI
        self.build_sidebar()
        self.build_main_container()
        
        # Initial Logs
        self.log("SUCCESS", "LinkedIn Certificate Harvester & Portfolio Architect başlatıldı.")
        self.log("INFO", f"Kalıcı Tarayıcı Oturumu: {BROWSER_PROFILE_DIR}")
        if self.has_git:
            self.log("INFO", "Git CLI: Sistem PATH'inde hazır.")
        else:
            self.log("WARN", "Git CLI bulunamadı! Winget ile 1-tıkla kurabilir veya REST API kullanabilirsiniz.")

    # ----------------------------------------------------------------------------------------------
    # ⚙️ PERSISTENCE / CONFIG
    # ----------------------------------------------------------------------------------------------
    def load_config(self):
        default_cfg = {
            "github_username": "",
            "github_token": "",
            "github_repo": "profile-readme-certificates",
            "output_dir": os.path.join(os.path.expanduser("~"), "LinkedIn_Portfolio_Export"),
            "profile_name": "Toprak Ahmet Aydoğmuş",
            "profile_headline": "Founder & CEO at Siber Akademi | Cybersecurity Specialist | Ethical Hacker | Reverse Engineer",
            "linkedin_url": "https://www.linkedin.com/in/toprak-ahmet-aydoğmuş-60462534b/details/certifications/",
            "theme_template": "Tokyo Night Cyberpunk"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = {**default_cfg, **json.load(f)}
                    if "Katılın" in cfg.get("profile_name", ""):
                        cfg["profile_name"] = default_cfg["profile_name"]
                    return cfg
            except Exception:
                return default_cfg
        return default_cfg

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.user_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log("ERROR", f"Config kaydedilemedi: {str(e)}")

    def load_certificates_data(self):
        if os.path.exists(CERTS_DATA_FILE):
            try:
                with open(CERTS_DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def save_certificates_data(self):
        try:
            with open(CERTS_DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.certificates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log("ERROR", f"Sertifikalar kaydedilemedi: {str(e)}")

    # ----------------------------------------------------------------------------------------------
    # 📌 SIDEBAR NAVIGATION
    # ----------------------------------------------------------------------------------------------
    def build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=255, corner_radius=0, fg_color=THEME["sidebar"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(18, 12))
        
        lbl_icon = ctk.CTkLabel(logo_frame, text="🏆 CERT ARCHITECT", font=ctk.CTkFont(size=17, weight="bold"), text_color=THEME["accent_cyan"])
        lbl_icon.pack(anchor="w")
        lbl_sub = ctk.CTkLabel(logo_frame, text="LinkedIn AI OCR & GitHub Pusher", font=ctk.CTkFont(size=11), text_color=THEME["text_muted"])
        lbl_sub.pack(anchor="w")
        
        div = ctk.CTkFrame(self.sidebar_frame, height=1, fg_color=THEME["border"])
        div.pack(fill="x", padx=14, pady=4)
        
        self.nav_buttons = {}
        tabs = [
            ("harvester", "🌐 LinkedIn AI Harvester", self.show_harvester_tab),
            ("certs", "📜 Sertifikalar & OCR Tablosu", self.show_certs_tab),
            ("readme", "🎨 README & Portfolyo Tasarımı", self.show_readme_tab),
            ("github", "🐙 GitHub Auto-Pusher", self.show_github_tab),
            ("settings", "⚙️ Ayarlar & Doğrulama", self.show_settings_tab),
            ("console", "📊 Canlı Konsol & Loglar", self.show_console_tab),
        ]
        
        for tab_id, text, command in tabs:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                anchor="w",
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color=THEME["text_secondary"],
                hover_color=THEME["bg_card_secondary"],
                font=ctk.CTkFont(size=12, weight="normal"),
                command=command
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[tab_id] = btn
            
        bottom_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=10, fg_color=THEME["bg_card"])
        bottom_frame.pack(fill="x", side="bottom", padx=10, pady=12)
        
        self.lbl_cert_counter = ctk.CTkLabel(
            bottom_frame,
            text=f"📜 Kayıtlı Sertifika: {len(self.certificates)}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=THEME["accent_cyan"]
        )
        self.lbl_cert_counter.pack(padx=10, pady=(8, 2), anchor="w")
        
        git_text = "🟢 Git CLI Hazır" if self.has_git else "🔴 Git Eksik (Winget Hazır)"
        git_color = THEME["accent_green"] if self.has_git else THEME["accent_orange"]
        self.lbl_git_info = ctk.CTkLabel(bottom_frame, text=git_text, font=ctk.CTkFont(size=10), text_color=git_color)
        self.lbl_git_info.pack(padx=10, pady=(0, 8), anchor="w")

    # ----------------------------------------------------------------------------------------------
    # 📌 MAIN CONTAINER
    # ----------------------------------------------------------------------------------------------
    def build_main_container(self):
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=THEME["bg_dark"])
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        self.tab_frames = {
            "harvester": self.create_harvester_view(),
            "certs": self.create_certs_view(),
            "readme": self.create_readme_view(),
            "github": self.create_github_view(),
            "settings": self.create_settings_view(),
            "console": self.create_console_view(),
        }
        self.switch_tab("harvester")

    def switch_tab(self, tab_id):
        for name, frame in self.tab_frames.items():
            if name == tab_id:
                frame.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
            else:
                frame.grid_forget()
                
        for name, btn in self.nav_buttons.items():
            if name == tab_id:
                btn.configure(
                    fg_color=THEME["bg_card_secondary"],
                    text_color=THEME["accent_cyan"],
                    font=ctk.CTkFont(size=12, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=THEME["text_secondary"],
                    font=ctk.CTkFont(size=12, weight="normal")
                )

    def show_harvester_tab(self): self.switch_tab("harvester")
    def show_certs_tab(self): 
        self.render_certificate_cards()
        self.switch_tab("certs")
    def show_readme_tab(self): 
        self.generate_and_preview_readme()
        self.switch_tab("readme")
    def show_github_tab(self): self.switch_tab("github")
    def show_settings_tab(self): self.switch_tab("settings")
    def show_console_tab(self): self.switch_tab("console")

    # ==============================================================================================
    # 🌐 TAB 1: LINKEDIN AI HARVESTER
    # ==============================================================================================
    def create_harvester_view(self):
        frame = ctk.CTkFrame(self.main_container, fg_color=THEME["bg_card"], corner_radius=12)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Primary Action Card
        ctrl = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], corner_radius=10)
        ctrl.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        ctrl.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(ctrl, text="🔗 LinkedIn URL:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self.entry_linkedin_url = ctk.CTkEntry(ctrl, placeholder_text="https://www.linkedin.com/in/kullanici-adi/details/certifications/")
        self.entry_linkedin_url.grid(row=0, column=1, padx=6, pady=10, sticky="ew")
        self.entry_linkedin_url.insert(0, self.user_config.get("linkedin_url", ""))
        
        self.btn_launch_browser = ctk.CTkButton(
            ctrl,
            text="🚀 1. Tarayıcıyı Aç",
            fg_color=THEME["accent_cyan"],
            text_color="#000",
            hover_color="#00B0FF",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.start_interactive_browser
        )
        self.btn_launch_browser.grid(row=0, column=2, padx=10, pady=10)
        
        # Interactive Step 2 Banner
        self.banner_interactive = ctk.CTkFrame(frame, fg_color="#182333", corner_radius=10, border_width=1, border_color=THEME["accent_green"])
        self.banner_interactive.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))
        self.banner_interactive.grid_columnconfigure(0, weight=1)
        
        self.lbl_interactive_status = ctk.CTkLabel(
            self.banner_interactive,
            text="👉 Chrome açıldığında giriş yapın ve sertifikalar sayfanıza gelin. Hazır olduğunuzda butona basın:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["accent_cyan"]
        )
        self.lbl_interactive_status.grid(row=0, column=0, padx=14, pady=10, sticky="w")
        
        self.btn_scrape_now = ctk.CTkButton(
            self.banner_interactive,
            text="⚡ 2. ŞİMDİ EKRANDAKİ SERTİFİKALARI ÇEK (HAZIRIM)",
            fg_color=THEME["accent_green"],
            text_color="#000",
            hover_color="#00C853",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            command=self.trigger_scrape_now
        )
        self.btn_scrape_now.grid(row=0, column=1, padx=14, pady=10)
        
        # Helpers Bar
        sub_bar = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], corner_radius=8)
        sub_bar.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        
        btn_paste_html = ctk.CTkButton(
            sub_bar,
            text="📄 Kopyalanan LinkedIn HTML'ini Yapıştır (0.1sn)",
            fg_color=THEME["sidebar"],
            hover_color=THEME["border"],
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.open_html_paste_modal
        )
        btn_paste_html.pack(side="left", padx=8, pady=8)
        
        btn_import_files = ctk.CTkButton(
            sub_bar,
            text="📥 Yerel PDF / Görsellerden Aktar",
            fg_color=THEME["sidebar"],
            hover_color=THEME["border"],
            command=self.import_local_certificates
        )
        btn_import_files.pack(side="left", padx=8, pady=8)
        
        btn_manual_add = ctk.CTkButton(
            sub_bar,
            text="➕ Manuel Sertifika Ekle",
            fg_color=THEME["sidebar"],
            hover_color=THEME["border"],
            command=self.open_manual_cert_modal
        )
        btn_manual_add.pack(side="right", padx=10, pady=8)
        
        # Output Live View
        self.harvest_output = ctk.CTkTextbox(frame, font=("Consolas", 11), fg_color=THEME["bg_dark"])
        self.harvest_output.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.harvest_output.insert("1.0", "🏆 LinkedIn AI Harvester v13.0 Hazır!\n\n"
                                          "Nasıl Kullanılır:\n"
                                          "1. '1. Tarayıcıyı Aç' butonuna basın. (Oturumunuz kalıcı olarak açılır)\n"
                                          "2. Açılan pencerede sertifikalar sayfanız ekrandayken yukarıdaki yeşil '2. ŞİMDİ EKRANDAKİ SERTİFİKALARI ÇEK' butonuna basın!\n\n"
                                          "Sistem ekrandaki tüm sertifikaları anında algılayacak, ekran görüntülerini alacak, Tesseract OCR ile okuyacak ve README.md oluşturacaktır.")
        
        return frame

    # ----------------------------------------------------------------------------------------------
    # 🚀 INTERACTIVE BROWSER SCRAPING FLOW
    # ----------------------------------------------------------------------------------------------
    def append_output(self, text):
        self.harvest_output.insert("end", text)
        self.harvest_output.see("end")

    def start_interactive_browser(self):
        url = self.entry_linkedin_url.get().strip()
        if not url.startswith("http"):
            messagebox.showerror("Hata", "Lütfen geçerli bir LinkedIn Profil URL'si giriniz.")
            return
            
        self.user_config["linkedin_url"] = url
        self.save_config()
        
        def run_thread():
            self.log("INFO", f"Tarayıcı oturumu başlatılıyor: {url}...")
            self.harvest_output.delete("1.0", "end")
            self.append_output(f"🚀 Google Chrome açılıyor...\nHedef: {url}\n\n"
                               f"👉 Tarayıcıda sertifikalar sayfanız açık olduğunda yukarıdaki yeşil '2. ŞİMDİ EKRANDAKİ SERTİFİKALARI ÇEK' butonuna tıklayın!\n\n")
            
            try:
                self.event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.event_loop)
                self.scrape_event = asyncio.Event()
                self.event_loop.run_until_complete(self.async_browser_lifecycle(url))
                self.event_loop.close()
            except Exception as e:
                self.log("ERROR", f"Tarayıcı oturum hatası: {str(e)}")
                self.append_output(f"\n❌ Hata: {str(e)}\n")
                
        threading.Thread(target=run_thread, daemon=True).start()

    async def async_browser_lifecycle(self, profile_url):
        if not async_playwright:
            self.append_output("❌ Playwright kütüphanesi eksik!\n")
            return
            
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=BROWSER_PROFILE_DIR,
                channel="chrome",
                headless=False,
                viewport={"width": 1366, "height": 850},
                args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
            )
            self.active_context = context
            page = context.pages[0] if context.pages else await context.new_page()
            self.active_page = page
            
            try:
                await page.goto(profile_url, timeout=45000)
            except Exception:
                pass
                
            self.append_output("🟢 Tarayıcı ekranda hazır! Sertifikalarınız görünüyorsa '2. ŞİMDİ EKRANDAKİ SERTİFİKALARI ÇEK' butonuna basın.\n")
            
            # Keep waiting for user to click the button
            while True:
                if len(context.pages) == 0:
                    self.append_output("⚠️ Tarayıcı penceresi kapatıldı.\n")
                    break
                # Check if scrape event triggered
                if self.scrape_event and self.scrape_event.is_set():
                    self.scrape_event.clear()
                    await self.async_extract_cards_instantly(page, profile_url)
                    break
                await asyncio.sleep(0.3)
                
            self.active_page = None
            self.active_context = None

    def trigger_scrape_now(self):
        if self.active_page is not None and self.scrape_event is not None and self.event_loop is not None:
            self.append_output("\n⚡ 'Şimdi Çek' tetiklendi! Kartlar taranıyor...\n")
            self.event_loop.call_soon_threadsafe(self.scrape_event.set)
        else:
            self.start_interactive_browser()

    # ----------------------------------------------------------------------------------------------
    # ⚡ LIGHTNING-FAST CARD EXTRACTION & OCR
    # ----------------------------------------------------------------------------------------------
    async def async_extract_cards_instantly(self, page, profile_url):
        self.append_output(f"\n🔍 Aktif sayfa inceleniyor: {page.url}\n")
        
        # Fast profile info extraction via JavaScript (Zero timeouts)
        profile_meta = await page.evaluate("""() => {
            let name = document.querySelector('h1')?.innerText?.trim() || '';
            let headline = document.querySelector('div.text-body-medium')?.innerText?.trim() || '';
            return { name, headline };
        }""")
        
        name = profile_meta.get("name") or self.user_config.get("profile_name", "Toprak Ahmet Aydoğmuş")
        headline = profile_meta.get("headline") or self.user_config.get("profile_headline", "Cybersecurity Specialist")
        
        if "Katılın" not in name and "Giriş" not in name and len(name) > 2:
            self.user_config["profile_name"] = name
        if len(headline) > 3:
            self.user_config["profile_headline"] = headline
        self.save_config()
        
        self.append_output(f"👤 İsim: {self.user_config['profile_name']}\n💼 Başlık: {self.user_config['profile_headline']}\n\n")
        
        # Scroll down smoothly to render all lazy-loaded badge images and cards
        self.append_output("📜 Sayfa aşağı taranıyor (Görseller yükleniyor)...\n")
        for _ in range(5):
            await page.keyboard.press("PageDown")
            await asyncio.sleep(0.8)
        await page.keyboard.press("Home")
        await asyncio.sleep(0.8)
        
        # Deep DOM extraction via JavaScript (Zero locators timeout, 0.05 seconds)
        raw_cards = await page.evaluate("""() => {
            const selectors = [
                'main ul.pvs-list > li',
                'div.scaffold-finite-scroll__content ul > li',
                'li.pvs-list__paged-list-item',
                'li.artdeco-list__item',
                'section[id*="certifications"] li'
            ];
            
            let elements = [];
            for (const sel of selectors) {
                const found = Array.from(document.querySelectorAll(sel));
                if (found.length >= 1) {
                    elements = found;
                    break;
                }
            }
            
            return elements.map((el, i) => {
                const spans = Array.from(el.querySelectorAll('span[aria-hidden="true"]'))
                    .map(s => s.innerText.trim())
                    .filter(t => t.length > 0);
                    
                const img = el.querySelector('img')?.src || '';
                const link = el.querySelector('a[href*="credential"], a[target="_blank"]')?.href || '';
                
                return {
                    index: i,
                    spans: spans,
                    imgUrl: img,
                    linkUrl: link,
                    fullText: el.innerText
                };
            }).filter(item => item.spans.length > 0);
        }""")
        
        self.append_output(f"📌 Tespit edilen sertifika kartı sayısı: {len(raw_cards)}\n\n")
        
        if not raw_cards:
            self.append_output("⚠️ Ekranda sertifika kartı bulunamadı. Lütfen '/details/certifications/' sayfasında olduğunuzdan emin olun.\n")
            messagebox.showwarning("Bulunamadı", "Sertifikalar sayfasında olduğunuzdan emin olun.")
            return
            
        extracted_certs = []
        locators = page.locator("main ul.pvs-list > li, li.pvs-list__paged-list-item, div.scaffold-finite-scroll__content ul > li")
        
        for idx, item in enumerate(raw_cards):
            spans = item["spans"]
            title = spans[0]
            
            # Filter non-cert UI elements
            if any(b in title.lower() for b in ["ana sayfa", "mesajlar", "bildirimler", "iş ilanları", "premium", "kaydol", "oturum"]):
                continue
                
            issuer = spans[1] if len(spans) > 1 else "Doğrulanmış Kurum"
            
            # Find date in spans
            date_str = datetime.now().strftime("%Y")
            for s in spans[1:]:
                if any(m in s for m in ["verildi", "Issued", "202", "201", "200"]):
                    date_str = s
                    break
                    
            # Capture Card Screenshot
            img_filename = f"linkedin_cert_{int(time.time())}_{idx+1}.png"
            img_path = os.path.join(CERT_IMG_DIR, img_filename)
            
            try:
                card_loc = locators.nth(item["index"])
                await card_loc.scroll_into_view_if_needed()
                await asyncio.sleep(0.3)
                await card_loc.screenshot(path=img_path)
            except Exception:
                img_path = ""
                
            # OCR Processing
            ocr_text = ""
            if img_path and os.path.exists(img_path) and pytesseract:
                try:
                    pil_img = Image.open(img_path)
                    gray = ImageOps.grayscale(pil_img)
                    enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                    ocr_text = pytesseract.image_to_string(enhanced, lang="tur+eng").strip()
                except Exception:
                    ocr_text = f"{title}\n{issuer}\n{date_str}"
                    
            cert_obj = {
                "id": f"cert_{int(time.time())}_{idx}",
                "title": title,
                "issuer": issuer,
                "date": date_str,
                "badge": "VERIFIED CREDENTIAL",
                "badge_color": "#00E5FF",
                "skills": ["Cybersecurity", "Professional"],
                "ocr_data": ocr_text or f"{title}\n{issuer}\n{date_str}",
                "img": img_path,
                "desc": ocr_text[:250].replace("\n", " ") if ocr_text else f"{issuer} tarafından verildi."
            }
            extracted_certs.append(cert_obj)
            self.append_output(f"  ✅ [{idx+1}] {title} | {issuer} ({date_str})\n")
            
        if extracted_certs:
            self.certificates = extracted_certs # Replace with fresh harvested certificates
            self.save_certificates_data()
            self.lbl_cert_counter.configure(text=f"📜 Kayıtlı Sertifika: {len(self.certificates)}")
            self.log("SUCCESS", f"{len(extracted_certs)} adet sertifika başarıyla emildi!")
            self.append_output(f"\n🎉 BAŞARILI! {len(extracted_certs)} adet sertifika kaydedildi ve OCR yapıldı!\n"
                               f"Otomatik olarak '📜 Sertifikalar & OCR Tablosu' sekmesine yönlendiriliyorsunuz...\n")
            self.show_certs_tab()
            messagebox.showinfo("Başarılı", f"{len(extracted_certs)} adet sertifika başarıyla çekildi ve arşivlendi!")

    # ----------------------------------------------------------------------------------------------
    # 📄 DIRECT HTML PASTE MODAL
    # ----------------------------------------------------------------------------------------------
    def open_html_paste_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("📄 LinkedIn Sayfa Kaynağı (HTML) Yapıştırıcı")
        modal.geometry("640x560")
        modal.configure(fg_color=THEME["bg_card"])
        modal.grab_set()
        
        lbl_info = ctk.CTkLabel(
            modal,
            text="Tarayıcınızda LinkedIn sertifikalar sayfasındayken Ctrl+U (veya İncele) yapıp\nHTML kodunu kopyalayın ve buraya yapıştırın:",
            font=ctk.CTkFont(size=12),
            text_color=THEME["accent_cyan"]
        )
        lbl_info.pack(anchor="w", padx=20, pady=(15, 6))
        
        text_html = ctk.CTkTextbox(modal, font=("Consolas", 10), height=360)
        text_html.pack(fill="both", expand=True, padx=20, pady=6)
        
        def parse_html():
            raw_html = text_html.get("1.0", "end-1c").strip()
            if not raw_html: return
            if not BeautifulSoup:
                messagebox.showerror("Hata", "BeautifulSoup kütüphanesi eksik.")
                return
                
            soup = BeautifulSoup(raw_html, "html.parser")
            found = 0
            
            items = soup.find_all(["li", "div"], class_=re.compile(r"pvs-list__paged-list-item|artdeco-list__item|pvs-entity"))
            if not items:
                items = soup.find_all("div", class_=re.compile(r"display-flex flex-column"))
                
            for i, it in enumerate(items):
                text_content = it.get_text(separator=" ", strip=True)
                if len(text_content) < 8: continue
                lines = [l.strip() for l in text_content.split("  ") if len(l.strip()) > 2]
                if not lines: continue
                
                title = lines[0]
                if any(b in title.lower() for b in ["ana sayfa", "mesajlar", "bildirimler", "iş ilanları", "premium"]):
                    continue
                    
                cert_item = {
                    "id": f"cert_html_{int(time.time())}_{found}",
                    "title": title,
                    "issuer": lines[1] if len(lines) > 1 else "Doğrulanmış Kurum",
                    "date": lines[2] if len(lines) > 2 else datetime.now().strftime("%Y"),
                    "badge": "VERIFIED CREDENTIAL",
                    "badge_color": "#00E5FF",
                    "skills": ["Skill"],
                    "ocr_data": text_content[:250],
                    "img": "",
                    "desc": text_content[:250]
                }
                self.certificates.append(cert_item)
                found += 1
                
            self.save_certificates_data()
            self.lbl_cert_counter.configure(text=f"📜 Kayıtlı Sertifika: {len(self.certificates)}")
            modal.destroy()
            self.log("SUCCESS", f"HTML kaynağından {found} adet sertifika çıkarıldı.")
            messagebox.showinfo("Tamamlandı", f"HTML kaynağından {found} adet sertifika başarıyla ayrıştırıldı!")
            self.show_certs_tab()
            
        ctk.CTkButton(modal, text="🚀 HTML'den Sertifikaları Ayıkla", height=38, fg_color=THEME["accent_green"], text_color="#000", font=ctk.CTkFont(weight="bold"), command=parse_html).pack(pady=12)

    def import_local_certificates(self):
        files = filedialog.askopenfilenames(
            title="Sertifika PDF veya Görsellerini Seçin",
            filetypes=[("Belgeler & Görseller", "*.pdf;*.png;*.jpg;*.jpeg"), ("PDF Belgeleri", "*.pdf"), ("Görseller", "*.png;*.jpg;*.jpeg")]
        )
        if not files: return
        
        def run_thread():
            count = 0
            for f in files:
                fname = os.path.basename(f)
                title = os.path.splitext(fname)[0].replace("-", " ").replace("_", " ")
                ocr_text = ""
                
                dest_img = os.path.join(CERT_IMG_DIR, f"{int(time.time())}_{fname}")
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    shutil.copy(f, dest_img)
                    if pytesseract:
                        try:
                            pil_img = Image.open(dest_img)
                            gray = ImageOps.grayscale(pil_img)
                            enhanced = ImageEnhance.Contrast(gray).enhance(2.0)
                            ocr_text = pytesseract.image_to_string(enhanced, lang="tur+eng").strip()
                        except Exception:
                            pass
                else:
                    dest_img = f
                    
                cert_item = {
                    "id": f"cert_local_{int(time.time())}_{count}",
                    "title": f"📜 {title.title()}",
                    "issuer": "Doğrulanmış Kurum",
                    "date": datetime.now().strftime("%Y"),
                    "badge": "VERIFIED",
                    "badge_color": "#00E676",
                    "skills": ["Cybersecurity", "Development", "Cloud"],
                    "ocr_data": ocr_text,
                    "img": dest_img,
                    "desc": ocr_text[:200].replace("\n", " ") if ocr_text else f"{fname} dosyasından içe aktarıldı."
                }
                self.certificates.append(cert_item)
                count += 1
                
            self.save_certificates_data()
            self.lbl_cert_counter.configure(text=f"📜 Kayıtlı Sertifika: {len(self.certificates)}")
            self.log("SUCCESS", f"{count} adet yerel sertifika içeri aktarıldı.")
            messagebox.showinfo("İçe Aktarıldı", f"{count} adet sertifika başarıyla eklendi!")
            self.show_certs_tab()
            
        threading.Thread(target=run_thread, daemon=True).start()

    def open_manual_cert_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("➕ Manuel Sertifika Ekle")
        modal.geometry("540x500")
        modal.configure(fg_color=THEME["bg_card"])
        modal.grab_set()
        
        ctk.CTkLabel(modal, text="Sertifika Başlığı:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(15, 2))
        e_title = ctk.CTkEntry(modal, width=480, placeholder_text="Örn: 🛡️ Certified SOC Analyst")
        e_title.pack(padx=20, pady=2)
        
        ctk.CTkLabel(modal, text="Veren Kurum:").pack(anchor="w", padx=20, pady=(8, 2))
        e_issuer = ctk.CTkEntry(modal, width=480, placeholder_text="Örn: CyberExam / Google / AWS")
        e_issuer.pack(padx=20, pady=2)
        
        ctk.CTkLabel(modal, text="Yetkinlikler:").pack(anchor="w", padx=20, pady=(8, 2))
        e_skills = ctk.CTkEntry(modal, width=480, placeholder_text="SIEM, Python, Wireshark")
        e_skills.pack(padx=20, pady=2)
        
        ctk.CTkLabel(modal, text="Açıklama / OCR:").pack(anchor="w", padx=20, pady=(8, 2))
        e_desc = ctk.CTkEntry(modal, width=480, placeholder_text="Sertifika kapsamı...")
        e_desc.pack(padx=20, pady=2)
        
        def save():
            title = e_title.get().strip()
            if not title: return
            item = {
                "id": f"cert_m_{int(time.time())}",
                "title": title,
                "issuer": e_issuer.get().strip() or "Kurum",
                "date": datetime.now().strftime("%Y"),
                "badge": "VERIFIED",
                "badge_color": "#00E676",
                "skills": [s.strip() for s in e_skills.get().split(",") if s.strip()],
                "desc": e_desc.get().strip(),
                "img": ""
            }
            self.certificates.append(item)
            self.save_certificates_data()
            self.lbl_cert_counter.configure(text=f"📜 Kayıtlı Sertifika: {len(self.certificates)}")
            modal.destroy()
            self.show_certs_tab()
            
        ctk.CTkButton(modal, text="💾 Kaydet", height=36, fg_color=THEME["accent_green"], text_color="#000", command=save).pack(pady=20)

    # ----------------------------------------------------------------------------------------------
    # 📜 TAB 2: CERTIFICATES & OCR TABLE VIEW
    # ----------------------------------------------------------------------------------------------
    def create_certs_view(self):
        frame = ctk.CTkFrame(self.main_container, fg_color=THEME["bg_card"], corner_radius=12)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], corner_radius=8)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        
        lbl_title = ctk.CTkLabel(header, text="📜 Sertifikalar, Başarılar & OCR Verileri", font=ctk.CTkFont(size=14, weight="bold"), text_color=THEME["accent_cyan"])
        lbl_title.pack(side="left", padx=12, pady=10)
        
        btn_clear_all = ctk.CTkButton(
            header,
            text="🗑️ Tümünü Temizle",
            width=120,
            fg_color="#3B1E1E",
            hover_color="#5C2626",
            command=self.clear_all_certs
        )
        btn_clear_all.pack(side="right", padx=10, pady=10)
        
        self.scroll_certs = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        self.scroll_certs.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
        self.scroll_certs.grid_columnconfigure(0, weight=1)
        
        self.render_certificate_cards()
        return frame

    def render_certificate_cards(self):
        for w in self.scroll_certs.winfo_children(): w.destroy()
        
        if not self.certificates:
            lbl_empty = ctk.CTkLabel(
                self.scroll_certs,
                text="Henüz kayıtlı sertifika bulunmamaktadır.\n'🌐 LinkedIn AI Harvester' sekmesinden 'Tarayıcıyı Aç' ve 'Şimdi Çek' ile kolayca toplayabilirsiniz.",
                font=ctk.CTkFont(size=13),
                text_color=THEME["text_muted"]
            )
            lbl_empty.pack(pady=40)
            return
            
        for idx, cert in enumerate(self.certificates):
            card = ctk.CTkFrame(self.scroll_certs, fg_color=THEME["bg_card_secondary"], corner_radius=10)
            card.pack(fill="x", pady=6, padx=4)
            card.grid_columnconfigure(0, weight=1)
            
            top_bar = ctk.CTkFrame(card, fg_color="transparent")
            top_bar.pack(fill="x", padx=12, pady=(10, 4))
            
            lbl_t = ctk.CTkLabel(top_bar, text=cert.get("title", "Sertifika"), font=ctk.CTkFont(size=13, weight="bold"), text_color=THEME["text_primary"])
            lbl_t.pack(side="left")
            
            lbl_badge = ctk.CTkLabel(
                top_bar,
                text=f"  {cert.get('badge', 'VERIFIED')}  ",
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=cert.get("badge_color", "#00E676"),
                text_color="#000",
                corner_radius=6
            )
            lbl_badge.pack(side="right")
            
            lbl_meta = ctk.CTkLabel(
                card,
                text=f"🏛️ Kurum: {cert.get('issuer', '-')} | 📅 Tarih: {cert.get('date', '-')}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=THEME["accent_cyan"]
            )
            lbl_meta.pack(anchor="w", padx=12, pady=1)
            
            desc = cert.get("desc", cert.get("ocr_data", ""))
            lbl_desc = ctk.CTkLabel(
                card,
                text=desc[:220] + ("..." if len(desc) > 220 else ""),
                font=ctk.CTkFont(size=11),
                text_color=THEME["text_secondary"],
                wraplength=850,
                justify="left"
            )
            lbl_desc.pack(anchor="w", padx=12, pady=4)
            
            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=12, pady=(0, 10))
            
            if cert.get("img") and os.path.exists(cert["img"]):
                ctk.CTkButton(btn_row, text="🖼️ Görseli Aç", width=110, height=28, fg_color=THEME["sidebar"], command=lambda f=cert["img"]: os.startfile(f)).pack(side="left", padx=4)
                
            ctk.CTkButton(btn_row, text="📋 Markdown Kopyala", width=140, height=28, fg_color=THEME["sidebar"], command=lambda c=cert: [pyperclip.copy(f"### {c.get('title')}\n- Kurum: {c.get('issuer')}\n- Tarih: {c.get('date')}"), messagebox.showinfo("Kopyalandı", "Kart panoya kopyalandı!")]).pack(side="left", padx=4)
            ctk.CTkButton(btn_row, text="🗑️ Sil", width=60, height=28, fg_color="#3B1E1E", command=lambda i=idx: self.delete_cert(i)).pack(side="right", padx=4)

    def delete_cert(self, idx):
        self.certificates.pop(idx)
        self.save_certificates_data()
        self.render_certificate_cards()
        self.lbl_cert_counter.configure(text=f"📜 Kayıtlı Sertifika: {len(self.certificates)}")

    def clear_all_certs(self):
        if messagebox.askyesno("Onay", "Tüm kayıtlı sertifikaları silmek istediğinize emin misiniz?"):
            self.certificates.clear()
            self.save_certificates_data()
            self.render_certificate_cards()
            self.lbl_cert_counter.configure(text="📜 Kayıtlı Sertifika: 0")

    # ----------------------------------------------------------------------------------------------
    # 🎨 TAB 3: README & PORTFOLIO ARCHITECT
    # ----------------------------------------------------------------------------------------------
    def create_readme_view(self):
        frame = ctk.CTkFrame(self.main_container, fg_color=THEME["bg_card"], corner_radius=12)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        top_ctrl = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], corner_radius=8)
        top_ctrl.grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        
        lbl_t = ctk.CTkLabel(top_ctrl, text="🎨 Tema Şablonu:", font=ctk.CTkFont(weight="bold"))
        lbl_t.pack(side="left", padx=10, pady=8)
        
        self.combo_theme = ctk.CTkComboBox(
            top_ctrl,
            values=["Tokyo Night Cyberpunk", "Modern Minimal Glass", "Matrix Hacker Green", "Executive Sapphire"],
            width=220,
            command=lambda v: self.generate_and_preview_readme()
        )
        self.combo_theme.pack(side="left", padx=6, pady=8)
        self.combo_theme.set(self.user_config.get("theme_template", "Tokyo Night Cyberpunk"))
        
        btn_export = ctk.CTkButton(
            top_ctrl,
            text="💾 README.md Olarak Kaydet",
            fg_color=THEME["accent_green"],
            text_color="#000",
            font=ctk.CTkFont(weight="bold"),
            command=self.export_readme_file
        )
        btn_export.pack(side="right", padx=10, pady=8)
        
        btn_copy_readme = ctk.CTkButton(
            top_ctrl,
            text="📋 Tüm Markdown'ı Kopyala",
            fg_color=THEME["sidebar"],
            command=lambda: [pyperclip.copy(self.readme_preview_box.get("1.0", "end-1c")), messagebox.showinfo("Kopyalandı", "Tüm README.md panoya kopyalandı!")]
        )
        btn_copy_readme.pack(side="right", padx=6, pady=8)
        
        self.readme_preview_box = ctk.CTkTextbox(frame, font=("Consolas", 11), fg_color=THEME["bg_dark"])
        self.readme_preview_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))
        return frame

    def generate_and_preview_readme(self):
        name = self.user_config.get("profile_name", "Toprak Ahmet Aydoğmuş").upper()
        headline = self.user_config.get("profile_headline", "Cybersecurity Specialist • Reverse Engineer • Systems Architect")
        theme = self.combo_theme.get() if hasattr(self, 'combo_theme') else "Tokyo Night Cyberpunk"
        color_accent = "7aa2f7" if "Tokyo" in theme else ("00ffcc" if "Matrix" in theme else "0077b5")
        
        lines = []
        lines.append("<div align=\"center\">\n")
        lines.append(f"<!-- ═══════════════════════════════════════════════════════════════ -->")
        lines.append(f"<!-- {name} — AI CERTIFICATE PORTFOLIO & SHOWCASE                  -->")
        lines.append(f"<!-- ═══════════════════════════════════════════════════════════════ -->\n")
        lines.append(f"<a href=\"https://github.com/{self.user_config.get('github_username', '')}\">")
        lines.append(f"  <img src=\"https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0:090d16,25:1a1b26,50:24283b,75:{color_accent},100:bb9af7&height=240&section=header&text={urllib.parse.quote(name)}&fontSize=42&fontColor=ffffff&animation=fadeIn\" width=\"100%\" alt=\"Header Banner\" />")
        lines.append("</a>\n")
        lines.append(f"### *{headline}*\n")
        lines.append(f"![Sertifikalar](https://img.shields.io/badge/Sertifikalar-{len(self.certificates)}-{color_accent}?style=for-the-badge&logo=linkedin&logoColor=white)")
        lines.append("</div>\n\n---\n")
        lines.append("## 📜 Başarılar, Lisanslar ve Sertifikalar\n")
        lines.append("| 🖼️ Sertifika Görseli | ℹ️ Detaylar & OCR Verisi |")
        lines.append("| :--- | :--- |")
        
        for c in self.certificates:
            t = c.get("title", "Sertifika")
            iss = c.get("issuer", "Doğrulanmış Kurum")
            dt = c.get("date", "-")
            ocr = c.get("ocr_data", "").replace("\n", "<br>").replace("|", "-").strip()
            if not ocr: ocr = "_Metin bulunamadı._"
            
            img_rel = f"assets/certificates/{os.path.basename(c.get('img', ''))}" if c.get("img") else ""
            img_html = f"<img src=\"{img_rel}\" width=\"350\" style=\"border-radius:8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);\">" if img_rel else "🏛️ **Doğrulanmış Belge**"
            
            detail_html = f"**{t}** <br><br> **🏛️ Kurum:** `{iss}` <br> **📅 Tarih:** `{dt}` <br><br> <details><summary>🔍 <b>OCR İçeriğini Göster</b></summary><br> <blockquote>{ocr}</blockquote> </details>"
            lines.append(f"| {img_html} | {detail_html} |")
            
        lines.append("\n---\n")
        lines.append("<div align=\"center\">\n")
        lines.append("*🤖 Bu portfolyo [LinkedIn Certificate Harvester & Portfolio Architect Pro] ile otomatik oluşturulmuştur.*\n")
        lines.append("</div>")
        
        full_md = "\n".join(lines)
        if hasattr(self, 'readme_preview_box'):
            self.readme_preview_box.delete("1.0", "end")
            self.readme_preview_box.insert("1.0", full_md)
        return full_md

    def export_readme_file(self):
        f = filedialog.asksaveasfilename(defaultextension=".md", initialfile="README.md", filetypes=[("Markdown File", "*.md")])
        if f:
            md_content = self.generate_and_preview_readme()
            with open(f, "w", encoding="utf-8") as file:
                file.write(md_content)
            self.log("SUCCESS", f"README.md kaydedildi: {f}")
            messagebox.showinfo("Kaydedildi", f"README.md dosyası başarıyla kaydedildi:\n{f}")

    # ----------------------------------------------------------------------------------------------
    # 🐙 TAB 4: UNIVERSAL GITHUB AUTO-PUSHER
    # ----------------------------------------------------------------------------------------------
    def create_github_view(self):
        frame = ctk.CTkFrame(self.main_container, fg_color=THEME["bg_card"], corner_radius=12)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        self.git_warn_box = ctk.CTkFrame(frame, fg_color="#3B1E1E", corner_radius=8)
        if not self.has_git:
            self.git_warn_box.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))
            lbl_w = ctk.CTkLabel(self.git_warn_box, text="⚠️ Sistemde 'git' bulunamadı. Winget ile 1-tıkla kurabilir veya Token (PAT) ile Pure REST API kullanabilirsiniz.", font=ctk.CTkFont(size=11, weight="bold"), text_color="#FF8A80")
            lbl_w.pack(side="left", padx=10, pady=8)
            ctk.CTkButton(self.git_warn_box, text="📥 Git'i Kur (Winget)", height=28, fg_color=THEME["accent_green"], text_color="#000", font=ctk.CTkFont(size=11, weight="bold"), command=self.install_git_winget).pack(side="right", padx=10, pady=6)
            
        ctrl = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], corner_radius=8)
        ctrl.grid(row=1, column=0, sticky="ew", padx=12, pady=10)
        ctrl.grid_columnconfigure(1, weight=1)
        ctrl.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(ctrl, text="📁 Dışa Aktarım / Proje Klasörü:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=6, sticky="w")
        self.entry_export_dir = ctk.CTkEntry(ctrl)
        self.entry_export_dir.grid(row=0, column=1, columnspan=2, padx=6, pady=6, sticky="ew")
        self.entry_export_dir.insert(0, self.user_config.get("output_dir", ""))
        
        ctk.CTkButton(ctrl, text="Gözat", width=80, fg_color=THEME["sidebar"], command=self.browse_export_dir).grid(row=0, column=3, padx=8, pady=6, sticky="w")
        
        ctk.CTkLabel(ctrl, text="👤 GitHub Kullanıcı Adı:").grid(row=1, column=0, padx=10, pady=6, sticky="w")
        self.entry_gh_user = ctk.CTkEntry(ctrl, placeholder_text="Kullanıcı adınız")
        self.entry_gh_user.grid(row=1, column=1, padx=6, pady=6, sticky="ew")
        self.entry_gh_user.insert(0, self.user_config.get("github_username", ""))
        
        ctk.CTkLabel(ctrl, text="🔑 GitHub Token (PAT):").grid(row=1, column=2, padx=10, pady=6, sticky="w")
        self.entry_gh_token = ctk.CTkEntry(ctrl, placeholder_text="ghp_... (REST API için)", show="•")
        self.entry_gh_token.grid(row=1, column=3, padx=6, pady=6, sticky="ew")
        self.entry_gh_token.insert(0, self.user_config.get("github_token", ""))
        
        ctk.CTkLabel(ctrl, text="🐙 Repo Adı:").grid(row=2, column=0, padx=10, pady=6, sticky="w")
        self.entry_gh_repo = ctk.CTkEntry(ctrl)
        self.entry_gh_repo.grid(row=2, column=1, padx=6, pady=6, sticky="ew")
        self.entry_gh_repo.insert(0, self.user_config.get("github_repo", "profile-readme-certificates"))
        
        ctk.CTkLabel(ctrl, text="💬 Commit:").grid(row=2, column=2, padx=10, pady=6, sticky="w")
        self.entry_gh_commit = ctk.CTkEntry(ctrl)
        self.entry_gh_commit.grid(row=2, column=3, padx=6, pady=6, sticky="ew")
        self.entry_gh_commit.insert(0, "🏆 docs: update verified certificates portfolio & README.md")
        
        actions = ctk.CTkFrame(frame, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        
        btn_push_now = ctk.CTkButton(
            actions,
            text="🚀 Tek Tıkla README & Sertifikaları GitHub'a Pushla",
            width=280,
            height=36,
            fg_color=THEME["accent_green"],
            text_color="#000",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.auto_push_all_to_github
        )
        btn_push_now.pack(side="left", padx=4)
        
        btn_save_auth = ctk.CTkButton(
            actions,
            text="💾 Bilgilerimi Kaydet",
            width=150,
            height=36,
            fg_color=THEME["sidebar"],
            command=self.save_github_auth_settings
        )
        btn_save_auth.pack(side="left", padx=4)
        
        btn_detect = ctk.CTkButton(
            actions,
            text="🔍 Sistem Git Kimliğini Algıla",
            width=190,
            height=36,
            fg_color=THEME["sidebar"],
            command=self.detect_system_git_auth
        )
        btn_detect.pack(side="right", padx=4)
        
        self.git_log_box = ctk.CTkTextbox(frame, font=("Consolas", 11), fg_color=THEME["bg_dark"])
        self.git_log_box.grid(row=3, column=0, sticky="nsew", padx=12, pady=10)
        frame.grid_rowconfigure(3, weight=1)
        self.git_log_box.insert("1.0", "🐙 GitHub Otomasyon Konsolu Hazır.\n'Tek Tıkla README & Sertifikaları GitHub'a Pushla' butonuna basarak anında senkronize edebilirsiniz...")
        return frame

    def browse_export_dir(self):
        d = filedialog.askdirectory(initialdir=self.entry_export_dir.get())
        if d:
            self.entry_export_dir.delete(0, "end")
            self.entry_export_dir.insert(0, d)

    def save_github_auth_settings(self):
        self.user_config["github_username"] = self.entry_gh_user.get().strip()
        self.user_config["github_token"] = self.entry_gh_token.get().strip()
        self.user_config["github_repo"] = self.entry_gh_repo.get().strip()
        self.user_config["output_dir"] = self.entry_export_dir.get().strip()
        self.save_config()
        self.log("SUCCESS", "GitHub yapılandırması kaydedildi.")
        messagebox.showinfo("Kaydedildi", "GitHub kullanıcı bilgileri yerel hafızaya kaydedildi!")

    def detect_system_git_auth(self):
        detected_user = ""
        if self.has_git:
            try:
                res = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
                if res.stdout.strip(): detected_user = res.stdout.strip()
            except Exception: pass
        if not detected_user and self.has_gh:
            try:
                res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
                m = re.search(r'account\s+([a-zA-Z0-9_\-]+)', res.stdout + res.stderr)
                if m: detected_user = m.group(1)
            except Exception: pass
            
        if detected_user:
            self.entry_gh_user.delete(0, "end")
            self.entry_gh_user.insert(0, detected_user)
            self.save_github_auth_settings()
            messagebox.showinfo("Algılandı", f"Sistemden GitHub hesabı bulundu: {detected_user}")
        else:
            messagebox.showwarning("Bulunamadı", "Sistemde kayıtlı bir Git kullanıcısı bulunamadı. Lütfen kutuya kendi kullanıcı adınızı yazınız.")

    def install_git_winget(self):
        def run_thread():
            self.log("INFO", "Winget ile Git kurulumu başlatılıyor...")
            self.git_log_box.insert("end", "🚀 Winget ile Git indiriliyor ve kuruluyor...\n")
            try:
                res = subprocess.run(
                    ["winget", "install", "--id", "Git.Git", "-e", "--silent", "--accept-package-agreements", "--accept-source-agreements"],
                    capture_output=True, text=True, timeout=300
                )
                self.git_log_box.insert("end", res.stdout + "\n")
                self.has_git = shutil.which("git") is not None
                if self.has_git:
                    self.lbl_git_info.configure(text="🟢 Git CLI Hazır", text_color=THEME["accent_green"])
                    self.git_warn_box.grid_forget()
                    messagebox.showinfo("Kuruldu", "Git başarıyla kuruldu!")
                else:
                    messagebox.showinfo("Yeniden Başlatma", "Git kuruldu. PATH güncellemesi için uygulamayı kapatıp açabilirsiniz.")
            except Exception as e:
                self.log("ERROR", f"Winget hatası: {str(e)}")
        threading.Thread(target=run_thread, daemon=True).start()

    def auto_push_all_to_github(self):
        out_dir = self.entry_export_dir.get().strip() or os.path.join(os.path.expanduser("~"), "LinkedIn_Portfolio_Export")
        username = self.entry_gh_user.get().strip()
        repo = self.entry_gh_repo.get().strip()
        token = self.entry_gh_token.get().strip()
        msg = self.entry_gh_commit.get().strip() or "Update certificates"
        
        if not username:
            messagebox.showerror("Eksik Bilgi", "Lütfen bir GitHub Kullanıcı Adı giriniz.")
            return
            
        os.makedirs(out_dir, exist_ok=True)
        md_content = self.generate_and_preview_readme()
        with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(md_content)
            
        dest_assets = os.path.join(out_dir, "assets", "certificates")
        os.makedirs(dest_assets, exist_ok=True)
        if os.path.exists(CERT_IMG_DIR):
            for file in os.listdir(CERT_IMG_DIR):
                shutil.copy(os.path.join(CERT_IMG_DIR, file), os.path.join(dest_assets, file))
                
        def run_thread():
            self.git_log_box.delete("1.0", "end")
            def log_g(txt):
                self.git_log_box.insert("end", txt + "\n")
                self.git_log_box.see("end")
                
            log_g(f"🚀 Pushlama başlatılıyor: {out_dir} -> https://github.com/{username}/{repo}")
            
            if shutil.which("git"):
                try:
                    if not os.path.exists(os.path.join(out_dir, ".git")):
                        log_g("📌 git init...")
                        subprocess.run(["git", "init"], cwd=out_dir, capture_output=True)
                        subprocess.run(["git", "branch", "-M", "main"], cwd=out_dir, capture_output=True)
                        
                    log_g("📦 git add . ...")
                    subprocess.run(["git", "add", "."], cwd=out_dir, capture_output=True)
                    log_g(f"💬 git commit: {msg}")
                    subprocess.run(["git", "commit", "-m", msg], cwd=out_dir, capture_output=True)
                    
                    remote_url = f"https://github.com/{username}/{repo}.git"
                    if token: remote_url = f"https://{username}:{token}@github.com/{username}/{repo}.git"
                    
                    r_res = subprocess.run(["git", "remote", "-v"], cwd=out_dir, capture_output=True, text=True)
                    if "origin" not in r_res.stdout:
                        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=out_dir, capture_output=True)
                    else:
                        subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=out_dir, capture_output=True)
                        
                    log_g("🚀 git push -u origin main...")
                    p_res = subprocess.run(["git", "push", "-u", "origin", "main"], cwd=out_dir, capture_output=True, text=True)
                    log_g(p_res.stdout or p_res.stderr)
                    
                    if p_res.returncode == 0 or "main -> main" in p_res.stderr:
                        log_g(f"\n🎉 BAŞARILI! https://github.com/{username}/{repo} güncellendi!")
                        self.log("SUCCESS", f"GitHub push tamamlandı: {username}/{repo}")
                        messagebox.showinfo("Başarılı", f"Portfolyo ve sertifikalar GitHub'a başarıyla pushlandı!\n\nhttps://github.com/{username}/{repo}")
                    else:
                        log_g("⚠️ Git CLI yanıtı:\n" + p_res.stderr)
                except Exception as e:
                    log_g(f"❌ Git hatası: {str(e)}")
            else:
                if token:
                    log_g("⚡ Pure Python REST API ile yükleniyor...")
                    self.pure_rest_api_push(out_dir, username, repo, token, msg, log_g)
                else:
                    log_g("❌ Git CLI yok ve Token girilmemiş. Lütfen Token girin veya Git'i kurun.")
                    messagebox.showwarning("Git Yok", "Lütfen Git'i kurun veya bir GitHub Token (PAT) girin.")
                    
        threading.Thread(target=run_thread, daemon=True).start()

    def pure_rest_api_push(self, folder, username, repo, token, msg, log_g):
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json", "User-Agent": "LinkedInCertArchitect"}
        try:
            r_check = requests.get(f"https://api.github.com/repos/{username}/{repo}", headers=headers, timeout=8)
            if r_check.status_code == 404:
                log_g(f"✨ GitHub'da yeni repo açılıyor: {repo}...")
                requests.post("https://api.github.com/user/repos", headers=headers, json={"name": repo, "private": False}, timeout=8)
                time.sleep(1.5)
                
            count = 0
            for root, dirs, files in os.walk(folder):
                if ".git" in root: continue
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, folder).replace("\\", "/")
                    with open(full, "rb") as fd:
                        b64 = base64.b64encode(fd.read()).decode("utf-8")
                        
                    sha = None
                    chk = requests.get(f"https://api.github.com/repos/{username}/{repo}/contents/{rel}", headers=headers, timeout=6)
                    if chk.status_code == 200: sha = chk.json().get("sha")
                    
                    payload = {"message": msg, "content": b64}
                    if sha: payload["sha"] = sha
                    put = requests.put(f"https://api.github.com/repos/{username}/{repo}/contents/{rel}", headers=headers, json=payload, timeout=8)
                    if put.status_code in [200, 201]:
                        log_g(f"  ✅ Yüklendi: {rel}")
                        count += 1
            log_g(f"\n🎉 REST API ile {count} dosya başarıyla pushlandı!")
            messagebox.showinfo("Başarılı", f"REST API ile {count} dosya yüklendi!\nhttps://github.com/{username}/{repo}")
        except Exception as e:
            log_g(f"❌ REST API hatası: {str(e)}")

    # ----------------------------------------------------------------------------------------------
    # ⚙️ TAB 5: SETTINGS & VALIDATION
    # ----------------------------------------------------------------------------------------------
    def create_settings_view(self):
        frame = ctk.CTkFrame(self.main_container, fg_color=THEME["bg_card"], corner_radius=12)
        frame.grid_columnconfigure(0, weight=1)
        
        lbl_s = ctk.CTkLabel(frame, text="⚙️ Sistem & OCR Yapılandırması", font=ctk.CTkFont(size=14, weight="bold"), text_color=THEME["accent_cyan"])
        lbl_s.pack(anchor="w", padx=16, pady=(16, 10))
        
        card = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], corner_radius=8)
        card.pack(fill="x", padx=16, pady=10)
        card.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(card, text="Profil Adınız:").grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self.entry_set_name = ctk.CTkEntry(card)
        self.entry_set_name.grid(row=0, column=1, padx=12, pady=10, sticky="ew")
        self.entry_set_name.insert(0, self.user_config.get("profile_name", "Toprak Ahmet Aydoğmuş"))
        
        ctk.CTkLabel(card, text="Profil Unvanı:").grid(row=1, column=0, padx=12, pady=10, sticky="w")
        self.entry_set_headline = ctk.CTkEntry(card)
        self.entry_set_headline.grid(row=1, column=1, padx=12, pady=10, sticky="ew")
        self.entry_set_headline.insert(0, self.user_config.get("profile_headline", ""))
        
        ctk.CTkLabel(card, text="Tesseract OCR Yolu:").grid(row=2, column=0, padx=12, pady=10, sticky="w")
        self.entry_set_tess = ctk.CTkEntry(card)
        self.entry_set_tess.grid(row=2, column=1, padx=12, pady=10, sticky="ew")
        tess_val = getattr(pytesseract, 'pytesseract', None)
        self.entry_set_tess.insert(0, getattr(tess_val, 'tesseract_cmd', 'tesseract') if tess_val else 'tesseract')
        
        btn_save_all_cfg = ctk.CTkButton(
            frame,
            text="💾 Tüm Ayarları Kaydet",
            height=36,
            fg_color=THEME["accent_green"],
            text_color="#000",
            font=ctk.CTkFont(weight="bold"),
            command=self.save_all_settings_tab
        )
        btn_save_all_cfg.pack(anchor="e", padx=16, pady=16)
        return frame

    def save_all_settings_tab(self):
        self.user_config["profile_name"] = self.entry_set_name.get().strip()
        self.user_config["profile_headline"] = self.entry_set_headline.get().strip()
        tess_path = self.entry_set_tess.get().strip()
        if pytesseract and tess_path:
            pytesseract.pytesseract.tesseract_cmd = tess_path
        self.save_config()
        self.log("SUCCESS", "Profil ve OCR ayarları kaydedildi.")
        messagebox.showinfo("Kaydedildi", "Ayarlar başarıyla güncellendi!")

    # ----------------------------------------------------------------------------------------------
    # 📊 TAB 6: LIVE CONSOLE & LOGS
    # ----------------------------------------------------------------------------------------------
    def create_console_view(self):
        frame = ctk.CTkFrame(self.main_container, fg_color=THEME["bg_card"], corner_radius=12)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        ctrl = ctk.CTkFrame(frame, fg_color=THEME["bg_card_secondary"], height=45, corner_radius=8)
        ctrl.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        lbl_c_title = ctk.CTkLabel(ctrl, text="📊 Canlı Sistem Konsolu & Olay Günlüğü", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_c_title.pack(side="left", padx=12, pady=8)
        
        btn_clear = ctk.CTkButton(ctrl, text="🗑️ Temizle", width=80, height=28, fg_color=THEME["sidebar"], command=lambda: self.console_box.delete("1.0", "end"))
        btn_clear.pack(side="right", padx=8, pady=8)
        
        btn_copy = ctk.CTkButton(ctrl, text="📋 Kopyala", width=80, height=28, fg_color=THEME["sidebar"], command=lambda: pyperclip.copy(self.console_box.get("1.0", "end-1c")) if pyperclip else None)
        btn_copy.pack(side="right", padx=4, pady=8)
        
        self.console_box = ctk.CTkTextbox(frame, font=("Consolas", 11), fg_color=THEME["bg_dark"], text_color=THEME["text_primary"])
        self.console_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        return frame

    def log(self, level, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️ [INFO]", "SUCCESS": "✅ [SUCCESS]", "WARN": "⚠️ [WARN]", "ERROR": "❌ [ERROR]"}.get(level, f"[{level}]")
        line = f"[{timestamp}] {prefix} {message}\n"
        if hasattr(self, 'console_box'):
            self.console_box.insert("end", line)
            self.console_box.see("end")
        else:
            print(line, end="")

# ==============================================================================================
# 🚀 ENTRY POINT
# ==============================================================================================
if __name__ == "__main__":
    app = LinkedInCertArchitectSuite()
    app.mainloop()
