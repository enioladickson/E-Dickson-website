import pathlib

# 1. FIX CHAT BAR IN public/index.html
p = pathlib.Path("public/index.html")
txt = p.read_text()
if "CHAT-BAR-FIX-V2" not in txt:
    css = """
<style>
/* CHAT-BAR-FIX-V2 */
.chat-input-area, .chat-input-container, .chat-form { display:flex !important; gap:8px !important; padding:10px !important; align-items:center !important; }
.chat-input-area input, .chat-input-container input, .chat-form input { flex:1 !important; min-width:0 !important; width:auto !important; padding:12px 14px !important; border-radius:20px !important; }
.chat-input-area button, .chat-input-container button, .chat-form button { flex-shrink:0 !important; width:70px !important; min-width:70px !important; padding:12px 8px !important; }
</style>
"""
    txt = txt.replace("</body>", css + "</body>") if "</body>" in txt else txt + css
    p.write_text(txt)
    print("Fixed chat bar in public/index.html")

# 2. ADD CLEAR ROUTE TO server.js
s = pathlib.Path("server.js")
st = s.read_text()
if "/clear-messages" not in st:
    st = st.replace(
        'app.get("/logout"',
        '''app.post("/clear-messages", (req, res) => {
  messages = [];
  saveMessages();
  io.emit("messageUpdate", messages);
  res.json({ success: true });
});
app.get("/logout"'''
    )
    s.write_text(st)
    print("Added /clear-messages to server.js")
else:
    print("Clear route already dey")
