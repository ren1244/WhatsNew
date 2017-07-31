import openwebpage as op
import re
import json
import time

T=['電腦軟體討論','C & C++ 語言','PHP 語言','電腦程式設計','電腦設計技術交流','網頁設計交流']
#T=['電腦設計技術交流','C & C++ 語言']

def t_convert(t_str): #轉換讀取到的時間為timestemp
	#example:2017-03-20 13:15
	pat1=re.compile('(半|\d+)\s*(分鐘|小時|天)前')
	pat2=re.compile('((\d{4})-(\d{1,2})-(\d{1,2})|今天|昨天|前天) (\d{2}):(\d{2}) (P|A)M')
	mch1=pat1.search(t_str)
	mch2=pat2.search(t_str)
	d=time.time()
	if(mch1):
		n=mch1.group(1)
		if(n=='半'):
			n=0.5
		else:
			n=int(n)
		if(mch1.group(2)=='分鐘'):
			n=n*60
		elif(mch1.group(2)=='小時'):
			n=n*3600
		else: #天
			n=n*86400
		return int(d-n)
	elif(mch2):
		if(mch2.group(1)=='今天'):
			d=d
		elif(mch2.group(1)=='昨天'):
			d=d-86400
		elif(mch2.group(1)=='前天'):
			d=d-86400*2
		else:
			h=int(mch2.group(5))
			h=h%12
			if(mch2.group(7)=='P'):
				h=h+12
			t_time=time.strptime(mch2.group(1)+' '+str(h)+':'+mch2.group(6),'%Y-%m-%d %H:%M')
			return int(time.mktime(t_time))
		h=int(mch2.group(5))
		h=h%12
		if(mch2.group(7)=='P'):
			h=h+12
		d=time.localtime(d)
		t_time=time.strptime(str(d[0])+'-'+str(d[1]).zfill(2)+'-'+str(d[2]).zfill(2)+' '+str(h)+':'+mch2.group(6),'%Y-%m-%d %H:%M')
		return int(time.mktime(t_time))
	else:
		return 0

#依莉電腦
A=[]
data=op.getWebPage('http://www.eyny.com')
pat1=re.compile('lib/static//image/index_t/th_93\.jpg')
pat2=re.compile('</table>')
pat3=re.compile('<a href=')
pat4=re.compile('\s*>\s*')
pat5=re.compile('\s*</a>')
RS=op.patSep(data,pat1,pat2)
data=data[RS[1]:RS[2]]
RS=op.patSep_all(data,pat3,pat4,pat5)
for R in RS:
	if data[R[3]:R[4]] in T:
		A.append([data[R[1]:R[2]][1:-1],data[R[3]:R[4]]])
		print(data[R[1]:R[2]])
		print(data[R[3]:R[4]])

#A=[['eyny_1.txt','eyny_1.txt'],['eyny_2.txt','eyny_2.txt']]
B=[]
pat1=re.compile('<tbody id="normalthread[^>]*><tr[^>]*>')
pat2=re.compile('</tr></tbody>')

pat3=re.compile('<th[^>]*><em>[^<]*<a[^>]*>[^<]*</a>[^<]*</em>\s*<a\s+href="')
pat4=re.compile('"[^>]*>\s*')
pat5=re.compile('\s*</a>(<img[^>]*>|<[/]?span[^>]*>|<[/]?a[^>]*>)*\s*</th>')

pat6=re.compile('<td class="by"><cite><a[^>]*>[^<]*</a></cite><em>')
pat7=re.compile('</em></td>')

pat8=re.compile('<[^>]*>')

for page in A:
	lk='http://www.eyny.com/'+page[0]
	#lk=page[0]
	print(lk)
	data=op.getWebPage(lk)
	RS1=op.patSep_all(data,pat1,pat2)
	tmp={'title':page[1],'data':[]}
	#print(RS1)
	for R1 in RS1:
		data2=data[R1[1]:R1[2]]
		R2=op.patSep(data2,pat3,pat4,pat5,pat6,pat7,pat6,pat7)
		if R2:
			print(data2[R2[1]:R2[2]]) #href
			print(data2[R2[3]:R2[4]]) #title
			print(pat8.sub('',data2[R2[11]:R2[12]]))
			tmp['data'].append({
				'title':pat8.sub('',data2[R2[3]:R2[4]]),
				'href':'http://www.eyny.com/'+data2[R2[1]:R2[2]],
				'date':t_convert(pat8.sub('',data2[R2[11]:R2[12]]).replace('&nbsp;',' '))
			})
	B.append(tmp)
	#tmp=['title':page[1],data:[]]
with open('EY.js','wb') as f:
	f.write(('var data_ey='+json.dumps(json.dumps(B))+';').encode('utf-8'))

#with open(fname,'wb') as f:
#	f.write(data.encode('utf-8'))
#
#data=op.getWebPage('https://www.eyny.com/forum.php?mod=forumdisplay&fid=550')

#with open('eyny_a.txt','wb') as f:
#	f.write(data)
