#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd
BASE_URL ="http://www.cec.org.al/Portals/0/Documents/CEC%202013/zgjedhje-per-kuvend/2017/zaz_qv/170324_-_DTI_-_QV_zgjedhes/report1+(2)/90.htm"
page = requests.get(BASE_URL)
doc = lh.fromstring(page.content)
row=[]
rowlist=[]
admnistrative=[]
admnistrativelist=[]
tr_elements = (doc.xpath('//td[@align= "CENTER"]'))
for i in range(0, len(doc.xpath('//td[@align= "CENTER"]'))-1):
    admnistrative=[tr_elements[i].text_content()];
    admnistrativelist.append(admnistrative)
    if not "rowspan" in tr_elements[i].attrib:
        row=("1")
    else:
        row=tr_elements[i].attrib["rowspan"]
    rowlist.append(row)
rowlistint= [int(x) for x in rowlist]
admulti= [a*b for a,b in zip (admnistrativelist,rowlistint)]
def iterFlatten(root):
    if isinstance(root, (list, tuple)):
        for element in root:
            for e in iterFlatten(element):
                yield e
    else:
        yield root
flatten=list(iterFlatten(admulti))
admultidata= pd.DataFrame(flatten)
admultidata.columns=["Administrative"]
second_table=[]
second_tablelist=[]
tr_elements2=doc.xpath('//*[not((@align= "CENTER") or(self::b))]/font[@size= "2"]')
for j in range (0, len(doc.xpath('//*[not((@align= "CENTER") or(self::b))]/font[@size= "2"]')),4):
    second_table={
        "QV":tr_elements2[j].text_content(),
        "Zgjedhës":tr_elements2[j+1].text_content(),
        "Vendnodhja e QV":tr_elements2[j+2].text_content(),
        "Ambjenti":tr_elements2[j+3].text_content(),
      #  "zaz": tr_elements4[j].text_content()
    }
    second_tablelist.append(second_table)
list2=pd.DataFrame.from_dict(second_tablelist)
all=admultidata.join(list2)
multi=[]
multilist=[]
first_tablelist=[]
seco_tablelist=[]
thir_tablelist=[]
tr_elements6 = doc.xpath('//td[@align= "RIGHT"]/b/font[@size="2"]')
for i in range(1, len(doc.xpath('//td[@align= "RIGHT"]/b/font[@size="2"]')),3):
    multi=tr_elements6[i].text_content()
    multilist.append(multi)
multilistint= [int(x) for x in multilist]    
tr_elements1=doc.xpath('//b')
for j in range (2, len (doc.xpath('//b'))-13, 13):
    first_table =tr_elements1[j].text_content(),
    seco_table = tr_elements1[j+1].text_content(),
    third_table = tr_elements1[j+2].text_content(),
    first_tablelist.append(first_table),
    seco_tablelist.append(seco_table )
    thir_tablelist.append(third_table )
list1multi= [a*b for a,b in zip (first_tablelist,multilistint)]
list1multi2= [a*b for a,b in zip (seco_tablelist,multilistint)]
list1multi3= [a*b for a,b in zip (thir_tablelist,multilistint)]
flatten1=list(iterFlatten(list1multi))
flatten2=list(iterFlatten(list1multi2))
flatten3=list(iterFlatten(list1multi3))
zaz = pd.DataFrame.from_dict(flatten1)
Qarku = pd.DataFrame.from_dict(flatten2)
Bashkia = pd.DataFrame.from_dict(flatten3)
zaz.columns=["Zaz"]
Qarku.columns=["Qarku"]
Bashkia.columns=["Bashkia"]
all1=Bashkia.join(all)
all2=Qarku.join(all1)
all3 =zaz.join(all2)

#put your path here between ("")
all3.to_csv("test2.csv")


# In[ ]:




