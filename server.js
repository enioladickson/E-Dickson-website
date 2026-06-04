require("dotenv").config();
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");
const fs = require("fs");
const session = require("express-session");
const bcrypt = require("bcryptjs");
const nodemailer = require("nodemailer");
const app = express();
const server = http.createServer(app);
const io = new Server(server);
const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.EMAIL_USER || "enioladickson63@gmail.com",
    pass: process.env.EMAIL_PASS
  }
});
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

// STORE ADMIN ACCOUNT HERE
const adminUser = {
  username: "enioladickson63",
  passwordHash: bcrypt.hashSync("kayode1978")
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
app.get("/logout", (req, res) => {
  req.session.destroy(() => {
    res.redirect("/login.html");
  });
});

// PROTECTED ADMIN ROUTE
app.get("/admin", requireLogin, (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin.html"));
});

// ============ CHAT SYSTEM (UNCHANGED) ============
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
  socket.on("userMessage", (msg) => {
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

    // EMAIL NOTIFICATION
    const mailOptions = {
      from: "enioladickson63@gmail.com",
      to: "enioladickson63@gmail.com",
      subject: "New Website Message",
      text: `
Name: ${msg.name}
Email: ${msg.email}
Phone: ${msg.phone}
Message: ${msg.message}
      `
    };

    transporter.sendMail(mailOptions, (err, info) => {
      if (err) {
        console.log("Email failed:", err);
      } else {
        console.log("Email sent successfully");
      }
    });
  }); // ✅ CLOSE userMessage properly

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
}); // ✅ CLOSE io.on properly

server.listen(3000, "0.0.0.0", () => {
  console.log("🚀 Server running at http://127.0.0.1:3000");
});
