from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import pytz
import urllib.request
import mimetypes

c1 = '#00BFFF'
c2 = '#FF69B4'
c3 = '#9370DB'
c4 = '#CD853F'
c5 = '#32CD32'


alpha = {'a': c1,'b': c2,'c': c3,'d': c4,'e': c1,'f': c2,'g': c3,'h': c4,'i': c1,'j': c2,'k': c3,'l': c4,'m': c1,'n': c2,'o': c3,'p': c4,'q': c1,'r': c2,'s': c3,'t': c4,'u': c1,'v': c2,'w': c3,'x': c4,'y': c1,'z': c2}

month = {	'01':'January',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'		}

def guess_type_of(link, strict=True):
    link_type, _ = mimetypes.guess_type(link)
    if link_type is None and strict:
        u = urllib.request.urlopen(link)
        link_type = u.headers.gettype() # or using: u.info().gettype()
    return link_type

def home(request):
    try:

        IST = pytz.timezone('Asia/Kolkata')

        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        ip_lst = []
        new_ip = True
        with open('/home/jotaro/mysite/chat/ip_addr.txt','r') as f:
            for line in f:
                ip_lst.append(line.rstrip('\n'))
        if ip_lst != []:
            for l in ip_lst:
                if str(ip) in l:
                    new_ip = False
        if new_ip:
            ipf = open('/home/jotaro/mysite/chat/ip_addr.txt','a')
            ipf.write(str(ip)+":unknown"+"\n")
            ipf.close()

        if request.method == "POST":
            name = request.POST.get('name')
            if name.strip(' ') == '':
                ip_lst = []
                with open('/home/jotaro/mysite/chat/ip_addr.txt','r') as f:
                    for line in f:
                        ip_lst.append(line.rstrip('\n'))
                name_lst = []
                for h1 in ip_lst:
                    name_lst.append(h1.split(":"))
                for h2 in name_lst:
                    if str(ip) == h2[0]:
                        name = h2[1]
            else:
                ip_lst = []
                with open('/home/jotaro/mysite/chat/ip_addr.txt','r') as f:
                    for line in f:
                        ip_lst.append(line.rstrip('\n'))
                file = open('/home/jotaro/mysite/chat/ip_addr.txt','w')
                for h3 in ip_lst:
                    if str(ip) in h3:
                        ind = h3.find(":")
                        h3 = h3[:ind]+":"+name+"\n"
                        file.write(h3)
                    else:
                        file.write(h3+"\n")
                file.close()



            message = request.POST.get('message')
            message = message.strip('\n')
            if message.strip() != '':
                date = str(datetime.now(IST))[:10]
                with open('/home/jotaro/mysite/chat/date.txt','r') as fd:
                    rd1 = fd.readlines()
                rd2 = []
                for d in rd1:
                    rd2.append(d.strip('\n'))
                if date not in rd2:
                    with open('/home/jotaro/mysite/chat/date.txt','a') as fd:
                        fd.write(date+"\n")

                    with open('/home/jotaro/mysite/chat/message.txt','a') as fd:
                        fd.write('<br><fieldset style="padding-top:0; padding-bottom:0; border: 0;"><p style="text-align:center;">'+'<span style="color:#B0B0B0;">'+ month.get(str(date[5:7])) + ' ' + str(date[    8:]) + ', ' + str(date[:4])+'</span></p></fieldset><br>\n')

                f = open("/home/jotaro/mysite/chat/message.txt",'a')
                now = str(datetime.now(IST))[11:16]

                if name == 'unknown':
                    color = c5
                elif name[0].isalpha():
                    color = alpha.get(name[0].lower())
                else:
                    color = c5

                try:
                    file_type = guess_type_of(message)
                except:
                    file_type = ''

                if 'image' in file_type:
                    f.write('<fieldset style="padding-top:0; padding-bottom:0; padding-right:20px; background-color:#DCDCDC; border: 0; display: inline-block; border-radius: 10px;"><legend align="right" style="color:gray;">'+now+'</legend><p>'+'<span style="font-family:Sans-serif;color: '+color+';">'+name+': '+'</span>'+'<br><span style="font-family:Sans-serif;color: black;"><img src= "'+message+'" width="500" height="500"/></span>'+'</p></fieldset><br>\n')
                else:
                    f.write('<fieldset style="padding-top:0; padding-bottom:0; padding-right:20px; background-color:#DCDCDC; border: 0; display: inline-block; border-radius: 10px;"><legend align="right" style="color:gray;">'+now+'</legend><p>'+'<span style="font-family:Sans-serif;color: '+color+';">'+name+': '+'</span>'+'<span style="font-family:Sans-serif;color: black;">'+message+'</span>'+'</p></fieldset><br>\n')

                f.close()

            f = open("/home/jotaro/mysite/chat/message.txt",'r')
            r = f.readlines()
            f.close()


            text1 = '''
            <!DOCTYPE html>
            <html>

            <head>

                {% load static %}
                <link rel="shortcut icon" href="{%  static 'chat/favicon.ico' %}">
                <title>Jotaro Chat Room</title>

                <style>
                    div.sticky1 {
                        position: -webkit-sticky;
                        position: sticky;
                        top: 0;
                        background-color: #24ae78;
                        padding: 10px;
                    }

                    div.sticky2 {
                        position: -webkit-sticky;
                        position: sticky;
                        bottom: 0;
                        background-color: #f6f3ea;
                        padding: 2px;
                    }
                </style>

            </head>
            {% load static %}
            <body style="background-color:#FFFAF0;" onload="window.scrollTo(0,document.body.scrollHeight);">

            <div class="sticky1">
            {% load static %}

            <p style="text-align:left;"><img src="{% static 'chat/logo(2).png' %}" width="100" height="100"/></p>
            <form name = "form1" action = '.'method = 'POST'>{% csrf_token %}
                <p style="text-align:right;"><input style="background-color:#383838; color:white; border-radius: 50px; height: 15px; width: 10%;" type = 'text' name = 'name' placeholder = "Name"/></p>

            </div>
            '''



            text2 = '''
            <div class="sticky2">

                    <p style="text-align:center;"><input style="background-color:#383838; color:white; border-radius: 50px; height: 50px; width: 90%;" type = 'text' name = 'message' placeholder = "Message"/>
                    <input style="background-color:#33475b; color:white; border-radius: 50px; height: 50px; width: 8%;" type = 'submit' value = 'Send'/></p>

            </div>

            {% load static %}<script src="{% static 'chat/non-empty.js' %}"></script>

            </body>
            </html>
            '''

            h = open("/home/jotaro/mysite/chat/templates/chat/home.html",'w')
            h.write(text1)
            for i in r:
                h.write(i)
            h.write(text2)
            h.close()

        return render(request, 'chat/home.html')
    except:
        pass
