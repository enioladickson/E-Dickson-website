import re, shutil, os
if os.path.exists("index.html.backup"):
    shutil.copy("index.html.backup", "index.html")
    print("Backup don restore - card don comot ✅")
else:
    c = open("index.html", encoding="utf-8").read()
    new_c, n = re.subn(r'<!-- INTERNATIONAL RENTAL CARD START -->.*?<!-- INTERNATIONAL RENTAL CARD END -->', '', c, flags=re.DOTALL)
    open("index.html", "w", encoding="utf-8").write(new_c)
    print(f"Card don comot - {n} block removed ✅")
for f in ["rental-card.html", "make_rental_card.py"]:
    if os.path.exists(f):
        os.remove(f)
print("DONE ✅ - Rental app don clean")
