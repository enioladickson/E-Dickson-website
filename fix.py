import glob
css_fix = open('fix.css').read() if False else """
/* FIX CHAT BAR PHONE */
.chat-input-area, .chat-input-container, .chat-form {
  display: flex;
  gap: 8px;
  padding: 10px;
  align-items: center;
}
.chat-input-area input, .chat-input-container input, .chat-form input {
  flex: 1;
  min-width: 0;
  width: auto;
  padding: 12px 14px;
  border-radius: 20px;
}
.chat-input-area button, .chat-input-container button, .chat-form button {
  flex-shrink: 0;
  width: 70px;
  min-width: 70px;
  padding: 12px 8px;
  white-space: nowrap;
}
"""
for f in glob.glob('public/*.css') + glob.glob('*.css') + glob.glob('public/*.html'):
    print("Checking:", f)
    txt = open(f).read()
    if "FIX CHAT BAR PHONE" not in txt:
        open(f, 'a').write("\n<style>" + css_fix + "</style>\n" if f.endswith('.html') else "\n" + css_fix)
        print("Fixed:", f)
