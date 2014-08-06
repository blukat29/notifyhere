import imaplib
import re

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login("you@example.com","Pa55w0rd")

ret, res = m.list()
boxes = []
for line in res:
    attr, root, name = re.search(r'\((.+)\) "(.+)" "(.+)"', line).groups()
    if "Noselect" in attr:
        continue
    boxes.append((name, name.replace("&","+").decode("utf-7")))

for box in boxes:
    raw, decoded = box
    ret, res = m.select(raw)
    total = int(res[0])
    ret, res = m.search(None, "(UNSEEN)")
    unseen = len(res[0].split())
    print raw, decoded, total, unseen

