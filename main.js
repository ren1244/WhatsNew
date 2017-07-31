var TB=[];
function deHtmlConv(s)
{
	return s.replace(/&nbsp;/g,' ')
	        .replace(/&gt;/g,'>')
	        .replace(/&lt;/g,'<')
	        .replace(/&quot;/g,'"')
	        .replace(/&amp;/g,'&');
}
function init()
{
	//alert('2017-07-24 15:23'.search(/\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}/))
	var p=document .getElementById("main");
	var i,N;
	data_bs=JSON.parse(data_bs);
	data_ba=JSON.parse(data_ba);
	data_ey=JSON.parse(data_ey);
	data_bs.forEach(function (val,idx){
		val.data.forEach(function (data,id){
			TB.push({
				title:deHtmlConv(data.title),
				href:data.href,
				date:data.date,
				top:data.top,
				from:'BS_'+val.title
			});
		});
	});
	data_ba.forEach(function (val,idx){
		TB.push({
			title:val.title,
			href:val.href,
			date:val.date,
			top:false,
			from:'BA_巴哈程式設計'
		});
	});
	data_ey.forEach(function (val,idx){
		val.data.forEach(function (data,id){
			TB.push({
				title:deHtmlConv(data.title),
				href:data.href,
				date:data.date,
				top:false,
				from:'EY_'+val.title
			});
		});
	});
	var p=document .getElementById("main");
	createDomTree(p,['table',null,'id','mainTB',[
		['tr',null,
			['th',null,'onclick','refresh(0)',['Text',null,'來源']],
			['th',null,'onclick','refresh(1)',['Text',null,'標題']],
			['th',null,'onclick','refresh(2)',['Text',null,'時間']]
		]
	]]);
	refresh();
	//appendBS(p);
	//appendBA(p);
}
function refresh(key)
{
	var p=document .getElementById("mainTB");
	if(key==0)
	{
		TB.sort(function (a,b){
			return a.from==b.from?
			           (a.date==b.date?0:(a.date<b.date?1:-1)):
			           (a.from<b.from?-1:1)
		});
	}
	else if(key==2)
	{
		TB.sort(function (a,b){
			return a.date==b.date?
			           (a.from==b.from?0:(a.from<b.from?-1:1)):
			           (a.date<b.date?1:-1)
		});
	}
	while(p.children.length>1)
		p .removeChild(p.children[p.children.length-1]);
	for(i=0;i<TB.length;++i)
	{
		if(!TB[i].top)
			createDomTree(p,['tr',null,[
				['td',null,'class','cen',['Text',null,TB[i].from]],
				['td',null,'class','lin',['a',null,'href',TB[i].href,['Text',null,TB[i].title]]],
				['td',null,'class','cen',['Text',null,conv2(TB[i].date)]]
			]]);
	}
	function conv2(t) //轉時間戳為文字
	{
		if(t==0)
			return ""
		var d=new Date
		d.setTime(t*1000)
		return pad(d.getFullYear(),4)+'-'+pad(d.getMonth()+1,2)+'-'+pad(d.getDate(),2)
			   +' '+pad(d.getHours(),2)+':'+pad(d.getMinutes(),2)
		function pad(x,n)
		{
			return ("0000"+x).slice(-n);
		}
	}
}
function createDomTree(p,DataArr)
{
/*根據陣列資料，建立整個DOM
	參數：
		p:掛載目的地，DOM Ref。
		DataArr:陣列，內容規定如下。
			
			[tagNmae,namespace,Attr1,Val1,Attr2,Val2,...,[ChildrenElement]]
			
			tagNmae:標籤名稱 如div p 等
			namespace:如果是一般html元素，填null，否則為xml namespace
			Attr:屬性名稱
			Val:屬性數值
			ChildrenElement:陣列，此tagDOM的代表子物件
*/
	var t,ty,i;
	if(typeof(DataArr[0])!='string')
	{
		for(i=0;i<DataArr.length;++i)
			if(typeof(DataArr[i])!='string')
				createDomTree(p,DataArr[i]);
		return;
	}
	if(DataArr[1])
	{
		p.appendChild(t=document.createElementNS(DataArr[1],DataArr[0]));
		for(i=2;i<DataArr.length;++i)
			if(typeof(DataArr[i])=='string')
			{
				t.setAttributeNS(null,DataArr[i],DataArr[i+1]);
				++i;
			}
			else
				createDomTree(t,DataArr[i]);
	}
	else
	{
		if(DataArr[0]=='Text')
			p.appendChild(t=document.createTextNode(DataArr.slice(2).toString()));
		else
		{
			p.appendChild(t=document.createElement(DataArr[0]));
			for(i=2;i<DataArr.length;++i)
				if(typeof(DataArr[i])=='string')
				{
					if(DataArr[i]=='innerHTML')
						t.innerHTML=DataArr[i+1];
					else
						t.setAttribute(DataArr[i],DataArr[i+1]);
					++i;
				}
				else
					createDomTree(t,DataArr[i]);
		}
	}
}
