import os
import time
import subprocess
import shutil

cv_file = 'cv.md'
pdf_out = os.path.abspath('assets/pdf/AnnaRobakowskaCV.pdf')
site_pdf_out = os.path.abspath('_site/assets/pdf/AnnaRobakowskaCV.pdf')

template_path = os.path.abspath('assets/templates/template.html')
style_css_path = os.path.abspath('assets/css/style.css')
print_css_path = os.path.abspath('assets/css/print-style.css')

pandoc_dir = r"C:\Users\annam\AppData\Local\Pandoc"
os.environ['PATH'] = f"{pandoc_dir};{os.environ.get('PATH', '')}"

def rebuild():
    print(f"[{time.strftime('%H:%M:%S')}] Change detected in cv.md! Generating updated PDF...")
    cmd = [
        "pandoc",
        cv_file,
        "-o", pdf_out,
        "--template=" + template_path,
        "--css=" + style_css_path,
        "--css=" + print_css_path,
        "--pdf-engine=weasyprint",
        "--metadata", "title=Anna Robakowska CV"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_out):
        os.makedirs(os.path.dirname(site_pdf_out), exist_ok=True)
        shutil.copy(pdf_out, site_pdf_out)
        print(f"[{time.strftime('%H:%M:%S')}] SUCCESS: http://127.0.0.1:4000/assets/pdf/AnnaRobakowskaCV.pdf updated!")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Error: {res.stderr}")

if __name__ == '__main__':
    print("Watching cv.md for changes... (Press Ctrl+C to stop)")
    last_mtime = 0
    try:
        while True:
            if os.path.exists(cv_file):
                mtime = os.path.getmtime(cv_file)
                if mtime != last_mtime:
                    last_mtime = mtime
                    rebuild()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Watcher stopped.")
