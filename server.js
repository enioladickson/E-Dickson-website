require("dotenv").config();
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");
const fs = require("fs");
const session = require("express-session");
const bcrypt = require("bcryptjs");
const { Resend } = require("resend");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// === RESEND SETUP ===
const resend = new Resend(process.env.RESEND_API_KEY);
const EMAIL_TO = process.env.EMAIL_TO || "enioladickson63@gmail.com";

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// SESSION CONFIG
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 24 * 60 * 60 * 1000 } // 1 day
  })
);

// STATIC FILES
app.use(express.static(path.join(__dirname, "public")));

// STORE ADMIN ACCOUNT HERE - NOW FROM .env, NOT HARD-CODED
const adminUser = {
  username: "enioladickson63",
  passwordHash: bcrypt.hashSync(process.env.ADMIN_PASSWORD || "change-me")
};

// AUTH MIDDLEWARE
function requireLogin(req, res, next) {
  if (req.session.isAdmin) return next();
  res.redirect("/login.html");
}

// LOGIN API
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  if (username !== adminUser.username) {
    return res.json({ success: false, message: "Invalid username" });
  }

  if (!bcrypt.compareSync(password, adminUser.passwordHash)) {
    return res.json({ success: false, message: "Invalid password" });
  }

  req.session.isAdmin = true;
  res.json({ success: true });
});

// LOGOUT
app.post("/clear-messages", (req, res) => {
  messages = [];
  saveMessages();
  io.emit("messageUpdate", messages);
  res.json({ success: true });
});
app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/login.html");
  });
});

// PROTECTED ADMIN ROUTE
app.get("/admin", requireLogin, (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin.html"));
});

// ============ CHAT SYSTEM ============
let messages = fs.existsSync(path.join(__dirname, "messages.json"))
  ? JSON.parse(fs.readFileSync(path.join(__dirname, "messages.json")))
  : [];

function saveMessages() {
  fs.writeFileSync(
    path.join(__dirname, "messages.json"),
    JSON.stringify(messages, null, 2)
  );
}

io.on("connection", (socket) => {
  console.log("⚡ New client connected");

  socket.emit("messageUpdate", messages);

  // USER MESSAGE
  socket.on("userMessage", async (msg) => {
    const newMsg = {
      id: Date.now(),
      name: msg.name,
      email: msg.email || "",
      phone: msg.phone || "",
      message: msg.message,
      reply: null
    };

    messages.push(newMsg);
    saveMessages();
    io.emit("messageUpdate", messages);

    // EMAIL NOTIFICATION VIA RESEND
    try {
      await resend.emails.send({
        from: "E-Dickson Website <onboarding@resend.dev>",
        to: EMAIL_TO,
        subject: "New Website Message",
        text: `Name: ${msg.name}\nEmail: ${msg.email || "Not provided"}\nPhone: ${msg.phone || "Not provided"}\nMessage: ${msg.message}`
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
      io.emit("messageUpdate", messages);
    }
  });

  socket.on("disconnect", () => {
    console.log("⚡ Client disconnected");
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, "0.0.0.0", () => {
  console.log(`🚀 Server running at http://127.0.0.1:${PORT}`);
});
