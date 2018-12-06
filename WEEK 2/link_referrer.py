import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.vit.ac.in")
soup = BeautifulSoup(page.content, 'html.parser')

l = list(soup.find_all('a'))
c = 0
d = {}
l3 = []
l4 = []
d1 = {}

for i in l:
    if c > 100:
        break
    else:
        c+=1
        try:  
            l2 = []
            a1 = i["href"]
            page1 = requests.get(i["href"])
            soup1 = BeautifulSoup(page1.content, 'html.parser')

            l1 = list(soup1.find_all('a'))
            #print ("C", c)
            for j in range(len(l1)):
                l2.append(l1[j]["href"])
            if len(l2) > 1:
                d[a1] = l2

        except:
            pass

for i in d.values():
    l3.append(i)

l4 = list(set([val for sublist in l3 for val in sublist]))

for i in l4:
    l5 = []
    for j in d.keys():
        if i in d[j]:
            l5.append(j)
    d1[i] = l5

for i in d1.keys():
    print (i, ":")
    for j in d1[i]:
        print ("            ", j)

