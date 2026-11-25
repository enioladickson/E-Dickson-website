import pathlib
p = pathlib.Path("public/index.html")
t = p.read_text()

fix = """
/* FIX ADMIN + FLOATING CHAT - INPUT SQUEEZED */
#chatForm, .chat-form, #messageForm, #adminForm {
  display: flex !important;
  flex-direction: row !important;
  gap: 10px !important;
  align-items: center !important;
  width: 100% !important;
}
#chatForm input, .chat-form input, #chatInput, #message-input {
  flex: 1 1 auto !important;
  flex-grow: 1 !important;
  min-width: 0 !important;
  width: auto !important;
  max-width: none !important;
}
#chatForm button, .chat-form button, .chat-form .btn, #chatForm .btn {
  flex: 0 0 80px !important;
  flex-grow: 0 !important;
  flex-shrink: 0 !important;
  width: 80px !important;
  min-width: 80px !important;
  max-width: 80px !important;
}
"""

if "INPUT SQUEEZED" in t:
    print("Already fixed before - no duplicate")
else:
    t = t.replace("</style>", fix + "\n</style>", 1)
    p.write_text(t)
    print("FIXED - saved")
