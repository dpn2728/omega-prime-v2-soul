import os
import sys
import platform
import subprocess
import socket

# --- Environment Info ---
print("\n--- Environment ---")
print("Python:", platform.python_version())
print("Platform:", platform.platform())

# --- CPU & Memory ---
try:
    import psutil
    print("CPU cores:", psutil.cpu_count())
    print("Memory (MB):", round(psutil.virtual_memory().total/1024/1024))
except ModuleNotFoundError:
    print("psutil not installed. Run: pip3 install --user psutil")

# --- Network Check (SMTP) ---
print("\n--- Network ---")
try:
    socket.create_connection(('smtp.gmail.com', 587), timeout=5)
    print("SMTP reachable ✅")
except:
    print("SMTP not reachable ❌")

# --- Background Processes ---
print("\n--- Background Processes ---")
subprocess.run(['ps','-ef'])

# --- Cloud Project Config ---
print("\n--- Cloud Project ---")
os.system('gcloud config list')

# --- Disk Usage ---
print("\n--- Disk Usage ---")
subprocess.run(['df','-h'])

# --- Installed Python Packages ---
print("\n--- Installed Packages ---")
subprocess.run([sys.executable,'-m','pip','list'])

# --- Test Gmail Login with App Password ---
print("\n--- Gmail SMTP Test ---")
try:
    import smtplib
    email_user = "dpn2728@gmail.com"
    app_password = "xnal ovyf xxzp vhiw".replace(" ", "")  # remove spaces automatically
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    server.starttls()
    server.login(email_user, app_password)
    print("SMTP login success ✅")
    server.quit()
except Exception as e:
    print("SMTP login failed ❌")
    print("Error:", e)
