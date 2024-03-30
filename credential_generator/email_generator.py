import random
validchars='abcdefghijklmnopqrstuvwxyz1234567890'
loginlen=random.randint(4,15)
login=''
for i in range(loginlen):
    pos=random.randint(0,len(validchars)-1)
    login=login+validchars[pos]
if login[0].isnumeric():
    pos=random.randint(0,len(validchars)-10)
    login=validchars[pos]+login

servers=['@gmail','@yahoo','@redmail','@hotmail','@bing']
servpos=random.randint(0,len(servers)-1)
email=login+servers[servpos]
tlds=['.com','.in','.gov','.ac.in','.net','.org']
tldpos=random.randint(0,len(tlds)-1)
email=email+tlds[tldpos]
print(email)