import requests
import re
r = requests.get("http://www.vit.ac.in")
img_src = re.findall('img.*?src="(.*?)".*?', r.text)
for i in img_src:
	print(i)
fp = open('web_mining_images.txt', 'w')
for i in img_src:
	fp.write(i)
	fp.write('\n')
fp.close()
