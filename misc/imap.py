import imaplib

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login("you@example.com","Pa55w0rd")

ret, l = m.list()
print ret
for a in l:
    print a

m.select("shopping")
#ret, u = m.search(None, "UnSeen")
ret, u = m.uid('search', None, "UnSeen")
print ret
u = u[0]
i = u[0]
print i
ret, b = m.fetch(i, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
print b

