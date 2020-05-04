# Este script se invoca de forma remota para crear la infraestructura de la aplicación de Calculadora
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/petclinic/createXLDPetclinicResources.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-9.0.5-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

# En este caso se puede crear todo desde el fichero app.yaml

def createResource(name, type, props):
    if not repository.exists(name):
        if props:
            myCI = factory.configurationItem(name, type, props)
        else:
            myCI = factory.configurationItem(name, type)
        repository.create(myCI)
        print("CI {0} created".format(name))
    else:
        print("CI {0} existed".format(name))

#    / \   _ __  _ __ | (_) ___ __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \/ __|
#  / ___ \| |_) | |_) | | | (_| (_| | |_| | (_) | | | \__ \
# /_/   \_\ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|___/

createResource("Applications/Applications", "core.Directory", None)
createResource("Applications/Applications/application-petclinic", "core.Directory", None)
createResource("Applications/Applications/application-petclinic/petclinic-war", "udm.Application", None)
createResource("Applications/Applications/application-petclinic/petclinic-ear", "udm.Application", None)
