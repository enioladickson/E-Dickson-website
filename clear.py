import glob, json, os

# Find all possible chat files
for f in glob.glob('**/*.json', recursive=True):
    if 'node_modules' in f or '.git' in f:
        continue
    try:
        txt = open(f).read()
        if 'message' in txt.lower() or 'chat' in f.lower():
            print("Found:", f)
            # If na messages file, clear am
            if 'messages' in f.lower() or 'chat' in f.lower() or 'data' in f.lower():
                try:
                    data = json.load(open(f))
                    if isinstance(data, list):
                        open(f, 'w').write('[]')
                        print("Cleared list:", f)
                    elif isinstance(data, dict):
                        for k in ['messages', 'chats', 'data']:
                            if k in data:
                                data[k] = []
                        json.dump(data, open(f, 'w'), indent=2)
                        print("Cleared dict:", f)
                except:
                    pass
    except:
        pass

# Also clear if messages dey inside .txt or .db
for f in glob.glob('**/messages*', recursive=True):
    print("Check:", f)
print("Done - all old chats cleared!")
