import requests

jpegs = []
gifs = []
pngs = []
others = []
fails = []
with open('roster.ini', 'r') as f:
    for url in f:
        try:
            r = requests.head(url[:-1])
        except:
            fails.append(url)
            continue
        if r.status_code != 200:
            fails.append(url)
            continue
        #url works
        ctype = r.headers.get('content-type')
        if not ctype:
            fails.append(url)
            continue
        if ctype == 'image/jpeg':
            jpegs.append(url)
        if ctype == 'image/png':
            pngs.append(url)
        if ctype == 'image/gif':
            gifs.append(url)
        else:
            others.append(url)

with open('jpegs.ini', 'w') as f:
    for url in jpegs:
        f.write(url)

with open('gifs.ini', 'w') as f:
    for url in gifs:
        f.write(url)

with open('pngs.ini', 'w') as f:
    for url in pngs:
        f.write(url)

with open('others.ini', 'w') as f:
    for url in others:
        f.write(url)

with open('fails.ini', 'w') as f:
    for url in fails:
        f.write(url)

print('good: {} bad: {} fail: {}'.format(len(jpegs)+len(pngs), len(gifs)+len(others), len(fails)))