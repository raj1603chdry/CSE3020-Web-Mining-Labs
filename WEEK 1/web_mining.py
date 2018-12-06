import requests
r = requests.get("http://www.vit.ac.in")
#print(r.text)
import re
result = re.findall('<a .*? href="(.*?)" .*?>', r.text)
#print(result)
#result = result.split(',')
for i in result:
	print(i)
fp = open('web_mining_links.txt', 'w')
for i in result:
	fp.write(i)
	fp.write('\n')
fp.close()
