import openwebpage as op
import re
import json
import time

T=['C/C++','PHP','MySQL','Java Script/ Node.js','AJAX / JSON / jQuery','CSS/HTML5/Bootstarp']
#T=['C/C++','PHP']
#取得討論區
data=op.getWebPage('http://www.blueshop.com.tw/board/default.asp')
pat1=re.compile('<ul\s+class\s*=\s*"menu"\s+id\s*=\s*"BRDarea\d+')
pat2=re.compile('</ul>')
pat3=re.compile('<a\s+title="')
pat4=re.compile('"\s+href="')
pat5=re.compile('">\s*')
pat6=re.compile('\s*</a>')

A=[]
RS=op.patSep_all(data,pat1,pat2)
for R in RS:
	s=data[R[1]:R[2]]
	r=op.patSep_all(s,pat3,pat4,pat5,pat6)
	for q in r:
		if s[q[5]:q[6]] in T:
			A.append([s[q[3]:q[4]],s[q[5]:q[6]]])
		#print(s[q[3]:q[4]])
		#print(s[q[5]:q[6]])
#data=op.getWebPage('BS_PHP.txt')


def t_convert(t_str): #轉換讀取到的時間為timestemp
	#example:2017-03-20 13:15
	pat=re.compile('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})')
	mch=pat.search(t_str)
	if(mch==None):
		return 0
	t_time=time.strptime(t_str,'%Y-%m-%d %H:%M')
	return int(time.mktime(t_time))

#討論區內容
B=[]
pat1=re.compile('SRC="/images/itea_talk\w*\.gif')
pat2=re.compile('<a href="')
pat3=re.compile('">\s*')
pat4=re.compile('\s*</a>')
pat5=re.compile('<TD nowrap valign="top">\s*')
pat6=re.compile('\s*</TD>')
for webpage in A:
	data=op.getWebPage('http://www.blueshop.com.tw'+webpage[0])
	if(data==''):
		continue
	tmp={'title':webpage[1],'data':[]}
	RS=op.patSep_all(data,pat1,pat2,pat3,pat4,pat5,pat6)
	for R in RS:
		top=True if R[1]-R[0]>28 else False
		tmp['data'].append({
			'href':'https://www.blueshop.com.tw'+data[R[3]:R[4]],
			'title':data[R[5]:R[6]],
			'date':t_convert(data[R[9]:R[10]]),
			'top':top
		})
	N=len(tmp['data'])
	i=N-1
	last=None
#	while(i>=0):
#		obj=tmp['data'][i]
#		if(i==N-1 or obj['top']!=tmp['data'][i+1]['top']):
#			last=None
#		if(obj['date']==0):
#			if(last):
#				obj['date']=last+1
#		last=obj['date']
#		i=i-1
	B.append(tmp)

with open('BS.js','wb') as f:
	f.write(('var data_bs='+json.dumps(json.dumps(B))+';').encode('utf-8'))
