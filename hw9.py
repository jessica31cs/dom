# CS288 Homework 9
# Read the skeleton code carefully and try to follow the structure
# You may modify the code but try to stay within the framework.

import libxml2
import sys
import os
import subprocess
import re
import sys

import MySQLdb

from xml.dom.minidom import parse, parseString

# for converting dict to xml 
from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag):#,atr,val):
   lst=[]
   elms = dom.getElementsByTagName(tag)   #tr
   lst = filter(lambda tr: len(tr.childNodes) == 6, elms)
   lst.remove(lst[0]) #removing the first row; not needed
   # ............

   return lst #list of all trs objects

# get all text recursively to the bottom
def get_text(e): #e is a tr
   lst=[]
   if e.nodeType in [3,4]: #3 or 4 are data
      lst.append(e.data)
   else:
      for i in e.childNodes: # [num, name-symbol,shares, price, chg, %chg]
         lst = lst + get_text(i)
   # ............
   return lst

def get_dict(tr): # returns a dictionary #tr is a list of the cols
   d={}
   s=tr[2].split(' (') # [name, symbol)]
   d['name']=str(s[0])
   d['symbol']=str(s[1].replace(')\n',''))
   d['volume']=int(tr[4].replace(',',''))
   d['price']=float(tr[5].replace('$',''))
   d['chng']=float(tr[6])
   d['pchng']=float(tr[7])
   return d

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

# convert to xhtml
# use: java -jar tagsoup-1.2.jar --files html_file
def html_to_xml(fn):
   # ............
   #t='java -jar tagsoup-1.2.jar --files' + fn  #???
   #/usr/share/java/tagsoup.jar
   subprocess.call('java -jar /usr/share/java/tagsoup.jar --files ' + fn, shell=True)
   xhtml_file = fn.replace('.html','.xhtml')
   return xhtml_file

def extract_values(dm):
   lst = []
   l = get_elms_for_atr_val('tr')#'table','class','most_actives')
   # ............ l has a list of all the trs; should be 100
   #    get_text(e)
   lst=map(lambda tr: get_text(tr) , l) #list of lists
   lst2=map(lambda x: get_dict(x), lst)
   # ............
   return lst2

# mysql> describe most_act"> ive;
def insert_to_db(l,tbl):
   # ............
   conn = MySQLdb.connect(host='localhost', user='cs288', password='CS288.pass', db='stockmarket')
   cursor = conn.cursor()
   prefix = "INSERT INTO " + tbl + " (name, symbol, volume, price, chng, pchng) "
   for d in l: #lst= is a list of dicitonaries
      vals = 'VALUES ("%s", "%s", "%d", "%f", "%f", "%f");' % (d['name'], d['symbol'], d['volume'], d['price'], d['chng'], d['pchng'])
      s = prefix + vals
      #print(s)
      cursor.execute (s)
   conn.commit()
   conn.close()
   return cursor

# show databases;
# show tables;
def main():
   html_fn = sys.argv[1] #ex) 2017_11_30_12_47_38.html
   fn = html_fn.replace('.html','') #2017_11_30_12_47_38
   xhtml_fn = html_to_xml(html_fn) #ex: 2017_11_30_12_47_38.xhtml

   global dom
   dom = parse(xhtml_fn) #we are using the xhtml version
   lst = extract_values(dom) #list of dictionaries

   # make sure your mysql server is up and running
   conn = MySQLdb.connect(host='localhost', user='cs288', password='CS288.pass', db='stockmarket')
   cursor = conn.cursor()
   s='DROP TABLE IF EXISTS ' + fn + ";";
   cursor.execute(s)
   
   s = "CREATE TABLE " + fn + " (name varchar(80), symbol varchar(10), volume integer, price float, chng float, pchng float);"
   cursor.execute (s)
   conn.commit()
   conn.close()
   
   cursor = insert_to_db(lst,fn) # fn = table name for mysql
   #we have a database with table and values in it.^^^
   #done so far...
   #-------------------------------------------------------------------------

   #l = select_from_db(cursor,fn) # display the table on the screen

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser
   #cpy file to html folder: cp /home/jcoyotl39/cs288-p9/hello.php /var/www/html

   #return xml
# end of main()

if __name__ == "__main__":
    main()

# end of hw7.py
