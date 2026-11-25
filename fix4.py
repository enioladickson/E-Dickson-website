import shutil
shutil.copy("public/index.html","public/index.html.backup3")
c=open("public/index.html").read()
if "private" not in c.lower() or "only you" not in c:
    note='<div style="font-size:12px;opacity:.7;text-align:center;padding:6px;">🔒 Your messages are private — only you and Admin can see them.</div>'
    if 'id="chatMessages"' in c:
        c=c.replace('id="chatMessages"', 'id="chatMessages"',1)
        # put note just before chatMessages div - find its line
        c=c.replace('<div id="chatMessages"', note+'<div id="chatMessages"',1)
        print("note added before chatMessages")
    elif 'id="messages"' in c:
        c=c.replace('<div id="messages"', note+'<div id="messages"',1)
        print("note added before messages")
    else:
        print("no chat div found - send me chat div line")
    open("public/index.html","w").write(c)
    print("DONE ✅")
else:
    print("already get note")
