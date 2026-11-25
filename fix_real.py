import pathlib
p = pathlib.Path("public/index.html")
t = p.read_text()

# Fix the real .chat-form block (line 407-411)
old_form = ".chat-form{display:flex;align-items:center;gap:8px;border-top:1px solid rgba(0,255,200,.2);background:var(--panel);padding:12px}"
new_form = ".chat-form{display:flex;align-items:center;gap:10px;border-top:1px solid rgba(0,255,200,.2);background:var(--panel);padding:14px}"
t = t.replace(old_form, new_form)

old_input = ".chat-form input{flex:1;min-width:0;border-radius:8px;border:1px solid rgba(0,255,200,.2);background:rgba(0,0,0,.5);padding:10px 12px;font-size:12px;color:#fff}"
new_input = ".chat-form input{flex:1;min-width:0;border-radius:12px;border:1px solid rgba(0,255,200,.2);background:rgba(0,0,0,.5);padding:14px 14px;font-size:16px;color:#fff}"
t = t.replace(old_input, new_input)

old_btn = ".chat-form .btn{height:40px;padding:0 16px;font-size:12px}"
new_btn = ".chat-form .btn{height:52px;min-width:76px;padding:0 18px;font-size:15px;flex-shrink:0;white-space:nowrap}"
t = t.replace(old_btn, new_btn)

# Add phone fix for the box itself - before </style> first time
if "CHAT-BOX-PHONE-FIX" not in t:
    phone_css = """
/* CHAT-BOX-PHONE-FIX */
@media (max-width: 600px) {
  .chat-box { left:12px !important; right:12px !important; width:auto !important; bottom:100px !important; height:70vh !important; max-height:70vh !important; }
  .chat-form { padding:14px !important; gap:10px !important; }
  .chat-form input { font-size:16px !important; padding:14px !important; }
  .chat-form .btn { height:52px !important; min-width:76px !important; font-size:15px !important; }
}
"""
    t = t.replace("</style>", phone_css + "</style>", 1)

p.write_text(t)
print("DONE - real chat-form fixed")
