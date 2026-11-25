import pathlib, re
p = pathlib.Path("public/index.html")
t = p.read_text()

# 1. Comot ALL my former fixes
t = re.sub(r"/\* FIX ADMIN.*?max-width: 80px !important;\n\}", "", t, flags=re.S)
t = re.sub(r'<style id="chat-fix-final">.*?</style>', "", t, flags=re.S)
t = re.sub(r"/\* FIX.*?INPUT SQUEEZED.*?\n\}", "", t, flags=re.S)

# 2. Put ONE clean original-style, before </body>
fix = """
<style id="chat-restore-original">
#chatForm.chat-form{display:flex!important;flex-direction:row!important;gap:10px!important;align-items:center!important;width:100%!important}
#chatForm #chatInput{flex:1!important;min-width:0!important;width:auto!important}
#chatForm .btn{flex:none!important;width:auto!important;min-width:0!important;white-space:nowrap!important;padding:10px 18px!important}
</style>
"""
if "chat-restore-original" not in t:
    t = t.replace("</body>", fix + "\n</body>", 1)
    p.write_text(t)
    print("RESTORED to BEFORE look")
else:
    print("Already restored")
