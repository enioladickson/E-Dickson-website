import pathlib, re
p = pathlib.Path("public/index.html")
t = p.read_text()

# Remove old fix if e dey
t = re.sub(r"/\* FIX ADMIN.*?max-width: 80px !important;\n\}", "", t, flags=re.S)

fix = """
<style id="chat-fix-final">
#chatForm.chat-form{display:flex!important;flex-direction:row!important;gap:10px!important;align-items:center!important;width:100%!important}
#chatForm #chatInput{flex:1 1 auto!important;flex-grow:1!important;min-width:0!important;width:auto!important;max-width:none!important}
#chatForm .btn.btn-primary{flex:0 0 80px!important;flex-grow:0!important;flex-shrink:0!important;width:80px!important;min-width:80px!important;max-width:80px!important}
</style>
"""

if "chat-fix-final" in t:
    print("Already fixed with final version")
else:
    t = t.replace("</body>", fix + "\n</body>", 1)
    p.write_text(t)
    print("FIXED FINAL - before </body>")
