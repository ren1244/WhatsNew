import openwebpage as op
import re
import json
import time

def t_convert(t_str): #轉換讀取到的時間為timestemp
	#example:2017-03-20 13:15
	pat=re.compile('((\d{2})/(\d{2})|(今|昨)日) (\d{2}):(\d{2})')
	mch=pat.search(t_str)
	if(mch==None):
		return 0
	if(mch.group(4)): # 今 or 昨
		d=time.time()
		if(mch.group(4)=='昨'):
			d=d-86400
		d=time.localtime(d)
		t_time=time.strptime(str(d[0])+'-'+str(d[1])+'-'+str(d[2])+' '+mch.group(5)+':'+mch.group(6),'%Y-%m-%d %H:%M')
		return int(time.mktime(t_time))
	d=time.localtime()
	t_time=time.strptime(str(d[0])+'/'+t_str,'%Y/%m/%d %H:%M')
	return int(time.mktime(t_time))



#巴哈程式版
data=op.getWebPage('https://forum.gamer.com.tw/B.php?bsn=60292')

pat1=re.compile('<tr class="FM-sticky">')
pat2=re.compile('</tr>')
RS=op.patSep_all(data,pat1,pat2)
data=data[RS[len(RS)-1][3]:]
"""
pat1=re.compile('<td class="FM-blist3"')
pat2=re.compile('href="')
pat3=re.compile('"\s*>')
pat4=re.compile('</a>')
pat5=re.compile('<td class="FM-blist6"><a[^>]*>\s*')
pat6=re.compile('\s*</a>')
RS=op.patSep_all(data,pat1,pat2,pat3,pat4,pat5,pat6)
"""

pat1=re.compile('<td class="FM-blist3"[^>]*>\s*(?:<a.*(?!href|>).href="([^"]*)"|<cite)[^>]*>([^<]*)</[^>]*>\s*</td>')
pat2=re.compile('<td class="FM-blist6"><a[^>]*>([^<]*)</a>')

B=[]
ss=0
mch1=pat1.search(data,ss)
if(mch1!=None):
	ss=mch1.end()
	mch2=pat2.search(data,ss)
	ss=mch2.end()
else:
	mch2=None
while(mch1!=None and mch2!=None):
	print(mch1.group(1))
	print(mch1.group(2))
	print(mch2.group(1))
	if(mch1.group(1)):
		B.append({
			'href':'https:'+mch1.group(1),
			'title':mch1.group(2),
			'date':t_convert(mch2.group(1))
		})
	mch1=pat1.search(data,ss)
	if(mch1!=None):
		ss=mch1.end()
		mch2=pat2.search(data,ss)
		ss=mch2.end()
	else:
		mch2=None
"""


for R in RS:
	B.append({
		'href':'https:'+data[R[3]:R[4]],
		'title':data[R[5]:R[6]],
		'date':t_convert(data[R[9]:R[10]])
	})
	#print(data[R[3]:R[4]])
	#print(data[R[5]:R[6]])
	#print(data[R[9]:R[10]])
"""
with open('BA.js','wb') as f:
	f.write(('var data_ba='+json.dumps(json.dumps(B))+';').encode('utf-8'))


