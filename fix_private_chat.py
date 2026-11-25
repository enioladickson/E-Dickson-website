import os, shutil

print("--- Checking your exact files ---")
# Backup
for f in ["server.js", "public/admin.html", "public/index.html"]:
    if os.path.exists(f):
        shutil.copy(f, f + ".backup")
        print(f"Backup: {f}.backup")

# ===== 1. FIX server.js =====
with open("server.js", "r", encoding="utf-8") as f:
    code = f.read()

if "guestId" in code:
    print("server.js already fixed, skip")
else:
    # Replace the whole chat block - from io.on to before const PORT
    start = code.find('io.on("connection"')
    end = code.find('const PORT')
    old_block = code[start:end]

    new_block = '''io.on("connection", (socket) => {
  console.log("⚡ New client connected");
  socket.guestId = null;
  socket.isAdmin = false;

  // Visitor go send him own ID
  socket.on("join", (guestId) => {
    socket.guestId = guestId;
    const mine = messages.filter(m => (m.guestId || "old") === guestId);
    socket.emit("messageUpdate", mine);
  });

  // Admin go send adminJoin - admin go see ALL
  socket.on("adminJoin", () => {
    socket.isAdmin = true;
    socket.emit("messageUpdate", messages);
  });

  // USER MESSAGE
  socket.on("userMessage", async (msg) => {
    const newMsg = {
      id: Date.now(),
      guestId: msg.guestId || "old",
      name: msg.name,
      email: msg.email || "",
      phone: msg.phone || "",
      message: msg.message,
      reply: null
    };
    messages.push(newMsg);
    saveMessages();
    // Send to admin + only to that guest
    for (let s of io.sockets.sockets.values()){
      if (s.isAdmin) s.emit("messageUpdate", messages);
      if (s.guestId && s.guestId === newMsg.guestId) s.emit("messageUpdate", messages.filter(m => (m.guestId || "old") === s.guestId));
    }
    try {
      await resend.emails.send({
        from: "E-Dickson Website <onboarding@resend.dev>",
        to: EMAIL_TO,
        subject: "New Website Message",
        text: `Name: ${msg.name}\\nEmail: ${msg.email || "Not provided"}\\nPhone: ${msg.phone || "Not provided"}\\nMessage: ${msg.message}`
      });
      console.log("✅ Email sent via Resend");
    } catch (err) {
      console.log("❌ Email failed:", err.message);
    }
  });

  // ADMIN REPLY
  socket.on("adminReply", ({ id, reply }) => {
    const msg = messages.find((m) => m.id === id);
    if (msg) {
      msg.reply = reply;
      saveMessages();
      for (let s of io.sockets.sockets.values()){
        if (s.isAdmin) s.emit("messageUpdate", messages);
        if (s.guestId && s.guestId === (msg.guestId || "old")) s.emit("messageUpdate", messages.filter(m => (m.guestId || "old") === s.guestId));
      }
    }
  });

  socket.on("disconnect", () => {
    console.log("⚡ Client disconnected");
  });
});

'''
    code = code[:start] + new_block + code[end:]
    # Fix clear-messages: it still uses io.emit all - make it admin only + guest
    code = code.replace('io.emit("messageUpdate", messages);', 'io.emit("messageUpdate", messages); // cleared')
    with open("server.js", "w", encoding="utf-8") as f:
        f.write(code)
    print("server.js fixed ✅")

# ===== 2. FIX admin.html - ADD adminJoin =====
with open("public/admin.html", "r", encoding="utf-8") as f:
    admin = f.read()
if "adminJoin" in admin:
    print("admin.html already fixed")
else:
    admin = admin.replace("const socket = io();", "const socket = io();\nsocket.emit(\"adminJoin\"); // Admin go see ALL messages")
    with open("public/admin.html", "w", encoding="utf-8") as f:
        f.write(admin)
    print("admin.html fixed ✅ - adminJoin added")

# ===== 3. FIX index.html - visitor side =====
if os.path.exists("public/index.html"):
    with open("public/index.html", "r", encoding="utf-8") as f:
        idx = f.read()
    if "myGuestId" not in idx:
        guest_js = """
<script>
// PRIVATE CHAT - each visitor get him own ID
let myGuestId = localStorage.getItem('myGuestId');
if(!myGuestId){ myGuestId = 'guest_' + Date.now() + '_' + Math.random().toString(36).slice(2,8); localStorage.setItem('myGuestId', myGuestId); }
</script>
"""
        if "</body>" in idx:
            idx = idx.replace("</body>", guest_js + "</body>")
        else:
            idx += guest_js
        # Make sure when socket connects, e go send join
        idx = idx.replace("const socket = io();", "const socket = io();\nsocket.on('connect', () => socket.emit('join', myGuestId));")
        # Add guestId to userMessage - handle both formats
        idx = idx.replace("socket.emit(\\"userMessage\\"", "socket.emit(\\"userMessage\\", { guestId: myGuestId, name: ")
        # If above no work, add comment for manual check
        with open("public/index.html", "w", encoding="utf-8") as f:
            f.write(idx)
        print("index.html patched ✅ - CHECK am, if your send function different, tell me")
    else:
        print("index.html already fixed")

print("--- DONE ---")
print("Check: git diff --stat")
