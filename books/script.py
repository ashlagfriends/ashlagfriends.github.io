import urllib2  # the lib that handles the url stuff
import codecs

data = urllib2.urlopen("http://www.ashlagbaroch.org/Zohar/") # it's a file like object and works just like a file
json = codecs.open('info.json', 'wb', encoding="utf-8")
string = ''
list1 = []
dict1 = {}
loop = 0
for line in data: # files are iterable
    if "(pdf)" in line:
        line = line.replace('&nbsp;', '')
        string =  line[line.find('">',)+2:line.find(' (pdf)</a>')].decode(encoding='UTF-8')
        dict1['bookname'] = string.encode("UTF-8")
        dict1['document'] = line[line.find('href="',)+6:line.find('">')]
        list1.append(dict1)
        dict1 = {}
print(list1)
json.write(str(list1).encode("UTF-8"))
json.close()
