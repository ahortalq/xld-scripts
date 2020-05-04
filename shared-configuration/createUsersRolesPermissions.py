# Este script se invoca de forma remota para crear los roles y los usuarios
# La invocación se debe realizar de la siguiente forma:
# cd /opt/xebialabs/xl-deploy-9.5.1-cli/bin/
# ./cli.sh -f /home/jcla/Projects/xld-scripts/shared-configuration/createUsersRolesPermissions.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-9.0.5-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

# Create users
def createUsers():
    security.createUser('ahortal', 'ahortal')
    security.createUser('csantamaria', 'csantamaria')
    security.createUser('jclopez', 'jclopez')
    security.createUser('antonio', 'antonio')
    security.createUser('vsalguero', 'vsalguero')
    security.createUser('amateos', 'amateos')
    security.createUser('cvalero', 'cvalero')
    security.createUser('jccobo', 'jccobo')
    security.createUser('ahartman', 'ahartman')
    security.createUser('jmurcia', 'jmurcia')
    security.createUser('mvega', 'mvega')
    security.createUser('ycobo', 'ycobo')
    security.createUser('jsalguero', 'jsalguero')
    security.createUser('isanchez', 'isanchez')
    security.createUser('agiraldo', 'agiraldo')

# Agrupación de usuarios en listas para facilitar la asignación de roles
calculatorDev = ['ahortal', 'jmurcia']
calculatorPre = ['csantamaria', 'mvega']
calculatorPro = ['jclopez', 'ycobo']
tutorialDev = ['antonio', 'jsalguero']
tutorialPre = ['vsalguero', 'isanchez']
tutorialPro = ['amateos', 'agiraldo']
votingAppDev = ['cvalero']
votingAppPre = ['jccobo']
votingAppPro = ['ahartman']
votingAppK8sDev = ['csantamaria']
votingAppK8sPre = ['ahortal']
votingAppK8sPro = ['jclopez']

# Establecemos los permisos
def grantPermissionsApplication(application, applicationUsersDEV, applicationUsersPRE, applicationUsersPRO):
    # Asignación de roles a usuarios. Es necesario definir 3 roles. Para dev, uat y pro.
    security.assignRole(application + "Dev", applicationUsersDEV)
    security.assignRole(application + "Pre", applicationUsersPRE)
    security.assignRole(application + "Pro", applicationUsersPRO)

    # Concedemos permiso de login, reports y read a los nuevos roles
    for env in ['Dev', 'Pre', 'Pro']:
        rol = application + env
        # Asignamos permiso de login para todos los roles
        security.grant('login', rol)
        # Permitimos que los roles tengan acceso a los reports y logs de despliegue
        security.grant('report#view', rol)
        # Todos los roles tendrán permiso de lectura a la carpeta Applications
        security.grant("read", rol, ["Applications/Applications"])
        # Todos los roles tendrán permiso de lectura a la nueva aplicacion
        security.grant("read", rol, ["Applications/Applications/application-{0}".format(application)])
        # Los usuarios con role Dev, deben poder crear nuevas versiones en XL Deploy
        if env == "Dev":
            security.grant('import#initial', rol, ["Applications/Applications/application-{0}".format(application)])
            security.grant('import#remove', rol, ["Applications/Applications/application-{0}".format(application)])
            security.grant('import#upgrade', rol, ["Applications/Applications/application-{0}".format(application)])
            # Las versiones deberían ser inmutables, por lo tanto debería evitarse conceder el permiso repo#edit
            # En cualquier caso, si se desea conceder, descomentar la siguiente línea
            # security.grant("repo#edit", rol, ["Applications/Applications/application-{0}".format(application)])
        # Asociamos permisos de lectura a los environments
        security.grant("read", rol, ["Environments/application-{0}".format(application)])
        security.grant("read", rol, ["Environments/application-{0}/application-{0}-{1}".format(application, env.lower())])
        # Autorizamos a realizar los tres tipos de despliegues (deploy inicial, upgrade y undeploy)
        security.grant("deploy#initial", rol, ["Environments/application-{0}/application-{0}-{1}".format(application, env.lower())])
        security.grant("deploy#upgrade", rol, ["Environments/application-{0}/application-{0}-{1}".format(application, env.lower())])
        security.grant("deploy#undeploy", rol, ["Environments/application-{0}/application-{0}-{1}".format(application, env.lower())])
        # Asociamos los permisos a la carpeta dictionaries-application a todos los roles
        security.grant("read", rol, ["Environments/dictionaries-{0}".format(application)])
        security.grant("repo#edit", rol, ["Environments/dictionaries-{0}".format(application)])

# Como conceder los permisos
# grantPermissionsApplication("calculator", calculatorDev, calculatorPre, calculatorPro)
# grantPermissionsApplication("tutorial", tutorialDev, tutorialPre, tutorialPro)
# grantPermissionsApplication("voting-app", votingAppDev, votingAppPre, votingAppPro)
# grantPermissionsApplication("moby-counter", [], [], [])
# grantPermissionsApplication("petportal", [], [], [])
# grantPermissionsApplication("remedy-stub-docker", [], [], [])
# grantPermissionsApplication("moby-counter", [], [], [])
# grantPermissionsApplication("voting-app-docker", [], [], [])
# grantPermissionsApplication("calculator-app-k8s", [], [], [])
# grantPermissionsApplication("istio-k8s", [], [], [])
# grantPermissionsApplication("tutorial-app-k8s", [], [], [])
# grantPermissionsApplication("voting-app-k8s", [], [], [])
# grantPermissionsApplication("istio-k8s", [], [], [])
grantPermissionsApplication("ms-backend", [], [], [])
