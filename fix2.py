import shutil, os
for f in ["public/admin.html","public/index.html"]:
    if os.path.exists(f): shutil.copy(f,f+".backup")
a=open("public/admin.html").read()
a=a.replace("const socket = io();","const socket = io();\nsocket.emit('adminJoin');",1)
open("public/admin.html","w").write(a)
print("admin DONE ✅")
i=open("public/index.html").read()
if "myGuestId" not in i:
    i=i.replace("</body>","<script>let myGuestId=localStorage.getItem('myGuestId'); if(!myGuestId){myGuestId='guest_'+Date.now(); localStorage.setItem('myGuestId',myGuestId);}</script></body>",1)
    i=i.replace("const socket = io();","const socket = io();\nsocket.on('connect',()=>socket.emit('join',myGuestId));",1)
    # add guestId to message - find your userMessage line
    i=i.replace("socket.emit(\"userMessage\"","socket.emit(\"userMessage\", {guestId: myGuestId, name: ",1)
    open("public/index.html","w").write(i)
print("index DONE ✅ - check your send function")
