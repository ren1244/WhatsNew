import re
import requests

def getWebPage(url):
	if(url[:4]=='http'):
		r=requests.get(url)
		if(r.status_code==200):
			byte_data=r.content
		else:
			return ''
	else:
		f=open(url,'rb')
		if(f):
			byte_data=f.read()
			f.close() 
		else:
			return ''
	data=byte_data.decode('ISO-8859-1')
	mch1=re.search('charset\b*=\b*[0-9A-Za-z\-_]+\b*',data)
	mch2=re.compile('=\b*[0-9A-Za-z\-_]+').search(data,mch1.start(),mch1.end())
	enc=data[mch2.start()+1:mch2.end()].strip()
	L={'gb2312':'gb18030','big5':'cp950'}
	if enc in L:
		enc=L[enc]
	data=data[:mch1.start()]+'charset=utf-8'+data[mch1.end():]
	data=data.encode('ISO-8859-1').decode(enc)
	return data

def patSep(str_,*pats,**sss):
	A=[]
	pos=0
	if 'ss' in sss:
		pos=sss['ss']
	for p in pats:
		mch=p.search(str_,pos)
		if(mch==None):
			break
		pos=mch.end()
		A.append(mch.start())
		A.append(mch.end())
	return A if len(pats)*2==len(A) else None

def patSep_all(str_,*pats,**sss):
	A=[]
	pos=0
	n=len(pats)*2-1
	if 'ss' in sss:
		pos=sss['ss']
	mch=patSep(str_,*pats,ss=pos)
	while(mch!=None):
		A.append(mch)
		mch=patSep(str_,*pats,ss=mch[n])
	return A
