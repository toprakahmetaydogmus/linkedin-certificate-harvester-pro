import os
import sys
import subprocess
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_py = os.path.join(base_dir, "app.py")
    ico_path = os.path.join(base_dir, "assets", "logo.ico")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        "--name=LinkedInCertArchitectPro",
        f"--icon={ico_path}",
        "--collect-all=customtkinter",
        f"--add-data={os.path.join(base_dir, 'assets')};assets",
        "--exclude-module=torch",
        "--exclude-module=matplotlib",
        "--exclude-module=scipy",
        "--exclude-module=pandas",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        "--exclude-module=tensorboard",
        "--exclude-module=cv2",
        app_py
    ]
    
    print("Building lightweight executable...")
    res = subprocess.run(cmd, cwd=base_dir)
    if res.returncode == 0:
        exe_path = os.path.join(base_dir, "dist", "LinkedInCertArchitectPro.exe")
        print(f"[OK] Executable built at: {exe_path}")
        desktop_exe = os.path.join(r"c:\Users\topra_n3vq63d\OneDrive\Desktop", "LinkedInCertArchitectPro.exe")
        try:
            shutil.copy(exe_path, desktop_exe)
            print(f"[OK] Copied to Desktop: {desktop_exe}")
        except Exception as e:
            print(f"Desktop copy warning: {e}")
    else:
        print(f"Build failed with exit code: {res.returncode}")

if __name__ == "__main__":
    build()
