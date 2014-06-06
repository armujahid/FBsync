import fbconsole as fb
import shutil # for moving files
fb.APP_ID = '741896972509458'  #if you face error then reinstall fbconsole or logout
fb.AUTH_SCOPE = ['publish_stream','publish_actions','manage_pages','photo_upload','user_photos']
fb.logout() #helps to update token by deleting it. 
fb.authenticate() 




#tokens = []
pnames = []
for i in range(len(fb.get('/me/accounts')['data'])):
    #tokens.append(fb.get('/me/accounts')['data'][i]['access_token'])
    pnames.append(fb.get('/me/accounts')['data'][i]['name'])

for i in range(len(pnames)):
    print i,': ',pnames[i]

pageno = input('Enter page no.')





print 'Accessing ',pnames[pageno]
fb.ACCESS_TOKEN = fb.get('/me/accounts')['data'][pageno]['access_token']
#ACCESS_TOKEN = get('/me/accounts')['data'][0]['access_token']
#print fb.ACCESS_TOKEN
#print fb.get('/me')







#aid = []
anames = []
for i in range(len(fb.get('/me/albums')['data'])):
    #aid.append(fb.get('/me/albums')['data'][i]['id'])
    anames.append(fb.get('/me/albums')['data'][i]['name'])

for i in range(len(anames)):
    print i,': ',anames[i]

ano = input('Enter album no.')
#albumid = '604917512927398'
albumid = fb.get('/me/albums')['data'][ano]['id']
print 'Accessing',anames[ano]


#photo uploading test via fbconsole (works in linux, not in windows) 
#status = fb.post('/me/feed', {'message':'windows'})
#print status
#status = fb.post("/%s/photos"%albumid, {"source":open("temp.PNG")})
#status = fb.post("/me/photos", {"source":open("temp.PNG")})

from facepy import GraphAPI # I have used facepy because photo uploading from fbconsole was not working in windows although it works under linux.

# Initialize the Graph API with a valid access token (optional,
# but will allow you to do all sorts of fun stuff).
graph = GraphAPI(fb.ACCESS_TOKEN)


from os import walk

mypath = 'pics'
paths = ['pics']
destinationpath = 'uploaded/'
nooffiles = 0



import sys
from PyQt4 import QtCore
#noofnewfiles = 0
def directory_changed(path):
    #global noofnewfiles
    print('Directory Changed: %s' % path)
    newf = []    
    for (dirpath, dirnames, filenames) in walk(mypath):
        newf.extend(filenames)
        break
    if len(newf) > nooffiles:
        upload()
    else:
        print 'sync complete waiting for new files'
	

app = QtCore.QCoreApplication(sys.argv)
fs_watcher = QtCore.QFileSystemWatcher(paths)
fs_watcher.directoryChanged.connect(directory_changed)


def upload():
    print 'uploading.......'
    global nooffiles
    global fs_watcher
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    nooffiles = len(f)


    print f
    for i in f:
        status = graph.post(
            path = '%s/photos'%albumid,
            source = open(mypath+'/'+i, 'rb')
        )
        print 'Uploaded',i
        #print status
        fs_watcher.removePath(mypath)
        shutil.move(mypath+'/'+i, destinationpath)
        fs_watcher.addPath(mypath)
        nooffiles = nooffiles - 1
        
    #nooffiles = 0
    #f.remove(i)
    print 'queue uploaded waiting for new files'

upload()




        







sys.exit(app.exec_())


