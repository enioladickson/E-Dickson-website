import shutil
shutil.copy("server.js","server.js.backup2")
c=open("server.js").read()
if "adminDelete" not in c:
    c=c.replace('socket.on("disconnect"', '''socket.on("adminDelete", (id) => {
    if(!socket.isAdmin) return;
    messages = messages.filter(m => m.id !== id);
    saveMessages();
    for(let s of io.sockets.sockets.values()){ if(s.isAdmin) s.emit("messageUpdate", messages); else if(s.guestId) s.emit("messageUpdate", messages.filter(m=>(m.guestId||"old")===s.guestId)); }
  });
  socket.on("disconnect"''',1)
    open("server.js","w").write(c)
    print("server delete DONE ✅")
else:
    print("already get delete")
