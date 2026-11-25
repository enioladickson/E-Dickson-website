import shutil
shutil.copy("public/index.html","public/index.html.backup2")
c=open("public/index.html").read()

# 1. Create guestId BEFORE socket
if "myGuestId" not in c:
    c=c.replace("var socket = null;", "var myGuestId=localStorage.getItem('myGuestId'); if(!myGuestId){myGuestId='guest_'+Date.now()+'_'+Math.random().toString(36).slice(2,8); localStorage.setItem('myGuestId',myGuestId);}\n  var socket = null;",1)
    print("guestId added")

# 2. After socket connect, send join
if "emit('join'" not in c:
    c=c.replace("socket = io();", "socket = io(); socket.on('connect', function(){ socket.emit('join', myGuestId); });",1)
    print("join added")

# 3. Add guestId to BOTH userMessage emits
c=c.replace("socket.emit('userMessage', { name:", "socket.emit('userMessage', { guestId: myGuestId, name:",)
print("userMessage fixed:", c.count("guestId: myGuestId"), "places")

open("public/index.html","w").write(c)
print("index.html DONE ✅")
