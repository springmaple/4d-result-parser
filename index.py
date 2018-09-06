import urllib.request


def getRealContent(s):
    start = s.index('<ul class="qzt-page-list">')
    end = s.index('</ul>', start)
    return s[start:end].split('</li>')


def getInfo(s):
    a, _, c = s.partition('<span class="content title">')
    title, _, c = c.partition('</span>')
    a, _, c = c.partition('src="')
    image, _, c = c.partition('"')
    a, _, c = c.partition('<span class="content">')
    ch, _, c = c.partition('</span>')
    a, _, c = c.partition('<span class="content">')
    en, _, c = c.partition('</span>')
    return title, image, ch, en


def buildReq(url):
    return urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })


# URL = 'http://www.4dmanager.com/qzt/tpk/'
# URL = 'http://www.4dmanager.com/qzt/gym/'
URL = 'http://www.4dmanager.com/qzt/wzt/'
PAGE_START = 1
PAGE_END = 200

import sqlite3
conn = sqlite3.connect('data.db')
conn.execute("""
CREATE TABLE data (
    id INTEGER PRIMARY KEY,
    title TEXT,
    ch TEXT,
    en TEXT,
    img_url TEXT,
    img BLOB
)
""")

for page_num in range(PAGE_START, PAGE_END + 1):
    req = buildReq(URL + str(page_num))
    f = urllib.request.urlopen(req)
    content = f.read()

    real_contents = (x for x in getRealContent(content.decode('utf-8')) if x)

    for data_str in real_contents:
        title, image, ch, en = getInfo(data_str)

        if not (title or image or ch or en):
            continue

        img_req = buildReq(image)
        f = urllib.request.urlopen(img_req)
        img = f.read()
        with open('img/' + title + '.png', mode='wb') as img_file:
            img_file.write(img)

        conn.execute('INSERT INTO data (title, ch, en, img_url, img) VALUES (?, ?, ?, ?, ?)',
                     (title, ch, en, image, img))

conn.commit()


