import neocities
import requests
def send_score(name, score):
	s = requests.get('https://gunpointgame.neocities.org/').text
	news = s[s.find("<ol>") + len("<ol>"):s.find("</ol>")].replace('  ', '')[1:-1]
	listoftop = {}
	for p in news.split('\n'):
		try:
			x = p[4:-5].split(" | ")
			listoftop[x[0]] = int(x[1])
		except: pass
	listoftop[name] = (score if listoftop[name] < score else listoftop[name]) if name in listoftop.keys() else score
	listoftop = dict(sorted(listoftop.items(), key=lambda item: item[1], reverse = True))
	out = ""
	for i in listoftop:
		out += f"<li>{i} | {listoftop[i]}</li>\n"

	nc = neocities.NeoCities("gunpointgame", "cronus")
	html = s[:(s.find("<ol>") + len("<ol>"))] + out + s[s.find("</ol>"):]
	with open('hs.html', 'w') as f:
		f.write(html)
		f.close()
	nc.upload(("hs.html", "index.html"))
