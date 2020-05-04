# Este script se invoca de forma remota para crear Environments y Applications en XLR
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/environments-application/createEnvironmentsAndApplication.py applicationName user password
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli
#
# En el fichero cna.yaml se encuentra la template de XLR que genera lo necesario

import sys
application = sys.argv[1]
user = sys.argv[2]      # Para conectar con XLR
password = sys.argv[3]  # Para conectar con XLR

import urllib2
import json
import base64

releaseId = "Release12227ed3358840f28d19357e358a5683"
folderId = "Folderda945fcd46854ef7a514fc977f0c49af"
url = "http://localhost:5516/api/v1/templates/Applications/{0}/start".format(releaseId)
data = {
    "releaseTitle" : "Creating environments and application for {0}".format(application),
    "folderId" : "Applications/{0}".format(folderId),
    "releaseVariables" : {"applicationName" : application}
}
req = urllib2.Request(url)
base64string = base64.b64encode("{0}:{1}".format(user, password))
req.add_header("Authorization", "Basic %s" % base64string)
req.add_header('Content-Type','application/json')
data = json.dumps(data)
response = urllib2.urlopen(req, data)


#  ____        _   _                 _____ 
# |  _ \ _   _| |_| |__   ___  _ __ |___ / 
# | |_) | | | | __| '_ \ / _ \| '_ \  |_ \ 
# |  __/| |_| | |_| | | | (_) | | | |___) |
# |_|    \__, |\__|_| |_|\___/|_| |_|____/ 
#        |___/                             
#
# import requests
# data = '{"releaseTitle" : "pruebecita", "folderId" : "Applications/Folderda945fcd46854ef7a514fc977f0c49af", "releaseVariables" : {"applicationName" : "tutorial"}}'
# headers = {"Content-Type" : "application/json"}
# requests.post('http://localhost:5516/api/v1/templates/Applications/Release12227ed3358840f28d19357e358a5683/create', headers=headers, auth=('admin', '2001jcla'), data=data)

#  ____            _     
# | __ )  __ _ ___| |__  
# |  _ \ / _` / __| '_ \ 
# | |_) | (_| \__ \ | | |
# |____/ \__,_|___/_| |_|
#                        
# curl -u 'admin:2001jcla' -v -H "Content-Type: application/json" http://localhost:5516/api/v1/templates/Applications/Release12227ed3358840f28d19357e358a5683/create -i -X POST -d '{"releaseTitle": "My Automated Release Tutorial", "folderId": "Applications/Folderda945fcd46854ef7a514fc977f0c49af", "releaseVariables" : {"applicationName" : "tutorial"}}'
