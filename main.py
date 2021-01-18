from requests_html import HTMLSession
from tqdm import tqdm
from json import dump
from os import makedirs

makedirs('img', exist_ok=True)

session = HTMLSession()
r = session.get('https://boardgamegeek.com/browse/boardgame')
table = r.html.find('#collectionitems', first=True)
rows = table.find('tr')[1:]

records = []
for index, row in enumerate(tqdm(rows)):
    url = row.find('a.primary', first=True).absolute_links.pop()
    r = session.get(url)
    r.html.render()

    records.append({
        'name': row.find('a.primary', first=True).text,
        'rank': index + 1,
        'brief': row.find('p.dull', first=True).text,
        'score': float(row.find('td.collection_bggrating', first=True).text),
        'year': int(row.find('span.dull', first=True).text.strip('()')),
        'description': r.html.find('article.game-description-body', first=True).text,
        'categories': [element.text for element in r.html.find('span.rank-title')[1:]],
        'complexity': float(r.html.find('div.gameplay-item-primary')[3].find('span.ng-binding', first=True).text)
    })

    image_url = r.html.find('img.img-responsive', first=True).attrs['ng-src']
    r = session.get(image_url)
    with open(f'img/{index}.jpg', 'wb') as handler:
        handler.write(r.content)

with open('all.json', 'w', encoding='utf8') as f:
    dump(records, f)
