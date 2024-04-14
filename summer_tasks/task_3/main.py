s = [("a", "b"),("a", "e"),("a", "f"),("b", "c"),("b", "d"), ("d", "e"), ("e", "f"), ("f", "g"), ("g", "h"), ("h", "d"), ("h", "f")]
b = []
k = 0
while len(s) > 1:
    for i in s[k]:
        for j in s[k + 1]:
            b.append(i + " " + j)
    s.pop(k)
    s.pop(k)
    s.insert(k, b)
    b = []
s = s[0]
print(s)
o = []

for p in s:
    if set(p.split()) not in o:
        o.append(set(p.split()))
print(o)
print(min(o, key=lambda x: len(x)))
print(max(o, key=lambda x: len(x)))
