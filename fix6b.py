import shutil
shutil.copy("public/admin.html","public/admin.html.backup4")
c=open("public/admin.html").read()
if "adminDelete" not in c:
    old="    box.appendChild(textarea);\n    box.appendChild(button);"
    new="""    box.appendChild(textarea);
    box.appendChild(button);
    const delBtn = document.createElement("button");
    delBtn.innerText = "🗑 Delete";
    delBtn.style = "background:red;color:white;margin-left:8px;padding:8px 12px;border:none;border-radius:8px;cursor:pointer;";
    delBtn.onclick = () => { if(confirm("Delete this message?")) socket.emit("adminDelete", m.id); };
    box.appendChild(delBtn);"""
    c=c.replace(old,new,1)
    open("public/admin.html","w").write(c)
    print("Delete button added ✅")
else:
    print("already get delete")
print("DONE ✅")
