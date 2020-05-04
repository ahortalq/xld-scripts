# Este script se invoca de forma remota para crear Usuarios y Roles en XLR
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/shared-configuration/createUsersRolesPermissionsXLR.py user password
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli
#
# En el fichero cna.yaml se encuentra la template de XLR que genera lo necesario

import sys
user = sys.argv[1]      # Para conectar con XLR
password = sys.argv[2]  # Para conectar con XLR

import urllib2
import json
import base64

def callXLR(url, data):
    req = urllib2.Request(url)
    base64string = base64.b64encode("{0}:{1}".format(user, password))
    req.add_header("Authorization", "Basic %s" % base64string)
    req.add_header('Content-Type','application/json')
    if data is not None:
        data = json.dumps(data)
        return urllib2.urlopen(req, data)
    else:
        return urllib2.urlopen(req)

users = [
    {
        "login": "agiraldo",
        "data": {
            "fullName": "Alfredo Giraldo",
            "password": "agiraldo",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "ahartman",
        "data": {
            "fullName": "Alberto Hartman",
            "password": "ahartman",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "ahortalq",
        "data": {
            "fullName": "Azucena Hortal Quirante",
            "password": "ahortalq",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "amateos",
        "data": {
            "fullName": "Alberto Mateos",
            "password": "amateos",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "antonio",
        "data": {
            "fullName": "Antonio Psicólogo",
            "password": "antonio",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "charo",
        "data": {
            "fullName": "Rosario Santamaría Cervantes",
            "password": "charo",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "cvalero",
        "data": {
            "fullName": "Carmen Valero",
            "password": "cvalero",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "isanchez",
        "data": {
            "fullName": "Inmaculada Sáncez",
            "password": "isanchez",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jccobo",
        "data": {
            "fullName": "Juan Carlos Cobo",
            "password": "jccobo",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jcla",
        "data": {
            "fullName": "José Carlos",
            "password": "jcla",
            "email": "jclopez@xebialabs.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jmurcia",
        "data": {
            "fullName": "Juan Murcia",
            "password": "jmurcia",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "jsalguero",
        "data": {
            "fullName": "Juan Salguero",
            "password": "jsalguero",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "mvega",
        "data": {
            "fullName": "Maria Vega",
            "password": "mvega",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "vsalguero",
        "data": {
            "fullName": "Vanesa Salguero",
            "password": "vsalguero",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },
    {
        "login": "ycobo",
        "data": {
            "fullName": "Yolanda Cobo",
            "password": "ycobo",
            "email": "lyhsoftcompany@gmail.com",
            "loginAllowed": True,
            "firstDayOfWeek": 1
        }
    },

]
roles = ['desarrollo', 'automatizacion', 'cloud', 'provisioning', 'seguridad']

def loadUsers():
    for u in users:
        url = "http://localhost:5516/api/v1/users/{0}".format(u["login"])
        try:
            response = callXLR(url, None)
            print("Ya existe el usuario {0}".format(u["login"]))
        except urllib2.HTTPError as err:
            if err.code == 404:
                print("Creamos el usuario {0}".format(u["login"]))
                data = u["data"]
                response = callXLR(url, data)

def loadRoles():
    for r in roles:
        print("Evaluando rol {0}".format(r))
        url = "http://localhost:5516/api/v1/roles/{0}".format(r)
        try:
            response = callXLR(url, None)
            print("Ya existe el rol {0}".format(r))
        except urllib2.HTTPError as err:
            print("Codigo de error = {0}".format(err.code))
            if err.code == 404:
                print("Creamos el rol {0}".format(r))
                data = {
                    "name" : r
                }
                response = callXLR(url, data)

# loadRoles() No cargamos los roles porque éstos se cargan a nivel general y no los necesitamos por ahora
# Lo que sí vamos a cargar son los teams por cada carpeta empezando por la de Terraform.
loadUsers()
