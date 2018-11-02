import requests

fail = 0
bad = 0
good = 0
with open('roster.ini', 'r') as f:
    for url in f:
        try:
            r = requests.head(url[:-1])
        except:
            fail += 1
            continue
        if r.status_code != 200:
            fail += 1
            continue
        #url works
        ctype = r.headers.get('content-type')
        if not ctype:
            fail += 1
            continue
        if ctype == 'image/gif':
            bad += 1
            with open('gifs.ini', 'a') as g:
                g.write(url)
        elif ctype == 'image/jpeg':
            good += 1
            with open('jpegs.ini', 'a') as g:
                g.write(url)
        else:
            bad += 1
            with open('others.ini', 'a') as g:
                g.write(url)

print('good: {} bad: {} fail: {}'.format(good, bad, fail))