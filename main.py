import URLMining

text = ''

with open("file.txt", "r") as t:
    text = [line[:len(line)-1:] for line in t]
text = ' '.join(text)
print(text)
u = URLMining.URLMining()
u.parse_verify(text, "file3")
u.get_table()