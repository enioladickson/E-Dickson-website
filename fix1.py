import shutil
shutil.copy("server.js","server.js.backup")
c=open("server.js").read()
# 1. Add guestId to new message - 1 line
c=c.replace("id: Date.now(),","id: Date.now(),\n      guestId: msg.guestId || 'old',",1)
# 2. Stop sending ALL messages on connect, wait for join
c=c.replace('socket.emit("messageUpdate", messages);','// wait for join / adminJoin',1)
# 3. Add join + adminJoin after connect log
c=c.replace('console.log("⚡ New client connected");','''console.log("⚡ New client connected");
  socket.on("join", (gid) => { socket.guestId=gid; socket.emit("messageUpdate", messages.filter(m=>(m.guestId||"old")===gid)); });
  socket.on("adminJoin", () => { socket.isAdmin=true; socket.emit("messageUpdate", messages); });''',1)
# 4. When new message / reply come, send filtered
c=c.replace('io.emit("messageUpdate", messages);','''for(let s of io.sockets.sockets.values()){ if(s.isAdmin) s.emit("messageUpdate", messages); else if(s.guestId) s.emit("messageUpdate", messages.filter(m=>(m.guestId||"old")===s.guestId)); }''')
open("server.js","w").write(c)
print("server.js DONE ✅")
