import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import string
import nltk
from nltk.stem.porter import PorterStemmer

index = {}

def visible_text(element):
  if element.parent.name in ['style', 'title', 'script', 'head', '[document]', 'class', 'a', 'li']:
    return False
  elif isinstance(element, Comment):
    return False
  elif re.match(r"[\s\r\n]+",str(element)): 
    return False
  return True

def read_url(url, url_number):

  ps = PorterStemmer()

  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  text = soup.findAll(text = True)
  result = list(filter(visible_text, text))
  counter = 0;
  words = []
  for i in result:
    temp = i.split(' ')
    for word in temp:
      k = []
      temp_word = word.lower()
      for c in temp_word:
        if c not in list(string.punctuation):
          k.append(c)
      temp_word = ''.join(k)
      words.append(temp_word)
  for i in words:
    if(i.isalpha()):
      i = ps.stem(i)
      if not i in index.keys():
        index[i] = [(url_number, counter)]
        counter = counter + len(i) + 1
      else:
        index[i].append((url_number, counter))
        counter = counter + len(i) + 1

  return None
  
read_url('https://en.wikipedia.org/wiki/Apple', 1)
read_url('https://en.wikipedia.org/wiki/Banana', 2)

sorted_keys = sorted(index.keys())

f = open("output2.txt", "w")
output_line = "Word".ljust(15) + "Frequency".ljust(15) + "Posting List".ljust(15) + "\n"
f.writelines(output_line)
f.writelines('-------------------------------------------------------------------------\n\n')
for i in sorted_keys:
  print(i, len(index[i]), index[i])
  output_string = str(i).ljust(15) + str(len(index[i])).ljust(15) + str(index[i]).ljust(15) + "\n"
  f.writelines(output_string)
  f.writelines('\n')
  
f.close()
  


