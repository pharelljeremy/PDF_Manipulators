# build.py
import PyInstaller.__main__
import platform
import os
import shutil

def build_macos():
    """Build macOS application"""
    options = [
        'pdf_gui.py',
        '--name=PDFManipulator',
        '--windowed',
        '--onefile',
        '--clean',
        '--target-arch=universal2',  # Support both Intel and M1 Macs
        '--hidden-import=PyPDF2',
        '--hidden-import=reportlab',
        '--collect-all=reportlab',
        # Add icon if you have one:
        # '--icon=assets/icon.icns',
    ]
    PyInstaller.__main__.run(options)
    
    # Create DMG (optional)
    # You'll need create-dmg installed: brew install create-dmg
    if shutil.which('create-dmg'):
        os.system('create-dmg --volname "PDF Manipulator" --window-pos 200 120 --window-size 600 300 --icon-size 100 --icon "PDFManipulator.app" 175 120 --hide-extension "PDFManipulator.app" --app-drop-link 425 120 "dist/PDFManipulator.dmg" "dist/PDFManipulator.app"')

def build_windows():
    """Build Windows executable"""
    options = [
        'pdf_gui.py',
        '--name=PDFManipulator',
        '--windowed',
        '--onefile',
        '--clean',
        '--hidden-import=PyPDF2',
        '--hidden-import=reportlab',
        '--collect-all=reportlab',
        # Add icon if you have one:
        # '--icon=assets/icon.ico',
    ]
    PyInstaller.__main__.run(options)

def main():
    # Create requirements.txt if it doesn't exist
    with open('requirements.txt', 'w') as f:
        f.write('PyPDF2\nreportlab\nPyInstaller')
    
    # Determine OS and build accordingly
    if platform.system() == 'Darwin':
        build_macos()
    elif platform.system() == 'Windows':
        build_windows()
    else:
        print("Unsupported operating system")

if __name__ == '__main__':
    main()