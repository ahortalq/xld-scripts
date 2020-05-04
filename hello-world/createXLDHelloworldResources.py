# Este script se invoca de forma remota para crear la infraestructura de la aplicación de Tutorial
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/helloworld/createXLDHelloworldResources.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-9.0.3-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

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

def createOrUpdateEnvironment(env):
    environmentName = "Environments/application-helloworld/application-helloworld-{0}/application-helloworld-{0}".format(env)
    requiresOkTestManager = False
    requiresOkReleaseManager = False
    if env == "pre":
        requiresOkTestManager = True
    if env == "pro":
        requiresOkTestManager = True
        requiresOkReleaseManager = True
    myContainers = [
        "Infrastructure/K8s/cluster-k8s-local/ns-helloworld-{0}".format(env)
    ]
    # Calculamos los triggers
    if env == "dev":
        triggerEnvironmentName = "Development"
    elif env == "pre":
        triggerEnvironmentName = "Preproduction"
    else:
        triggerEnvironmentName = "Production"
    triggerFailed = "Configuration/Environments/{0}/Triggers/FailedDeploymentTrigger".format(triggerEnvironmentName)
    triggerSuccessful = "Configuration/Environments/{0}/Triggers/SuccessfulDeploymentTrigger".format(triggerEnvironmentName)
    triggers = [triggerFailed, triggerSuccessful]
    if not repository.exists(environmentName):
        myEnvironment = factory.configurationItem(environmentName, 'udm.Environment', {'members': myContainers, 'requiresOkTestManager': requiresOkTestManager, 'requiresOkReleaseManager': requiresOkReleaseManager, 'triggers': triggers})
        repository.create(myEnvironment)
        print("Environment {0} created".format(environmentName))
    else:
        myEnvironment = repository.read(environmentName)
        myEnvironment.members = myContainers
        myEnvironment.requiresOkTestManager = requiresOkTestManager
        myEnvironment.requiresOkReleaseManager = requiresOkReleaseManager
        myEnvironment.triggers = triggers
        repository.update(myEnvironment)
        print("Environment {0} updated".format(environmentName))

#        / ___|___  _ __ | |_ __ _(_)_ __   ___ _ __ ___ 
#        | |   / _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
#        | |__| (_) | | | | || (_| | | | | |  __/ |  \__ \
#         \____\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/

createResource("Infrastructure/K8s", "core.Directory", None)
caCert = '''
-----BEGIN CERTIFICATE-----
MIICyDCCAbCgAwIBAgIBADANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwprdWJl
cm5ldGVzMB4XDTE5MDgwNjE0MzI1OFoXDTI5MDgwMzE0MzI1OFowFTETMBEGA1UE
AxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMUx
sCAFuq6XwS1j/mVxD60Waehr4Lb4Eg3OqSsxH6Ev+vNn7daOYleqQkqRdvF9NEKQ
47YBxA+2hDbf5ZpvKYsHWIy3Eq23fehs3rr3XRmrJcNM8PbwBEY93nyunZQTYZQI
EuFQ8OeHNYTJ2qR07kCAWdzqyjcCPzNVrE5+8zZlDrOLPl7ubVnEykDTYyFSp2ly
vjHAQ+wQlnUvsuChvfXXydnAQy6AuuTgLrdMEdHWD7JC4+qV6YSk6j6EB2mhuJKF
nJJ/E1BkQgeYS5hFrbDq15427YBe+hipoOM2ePmbxCjoHH9iXcGfVMhjAidtpQrv
dYBkUb4TgnZsPQ8xuxkCAwEAAaMjMCEwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB
/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAILAFTT6dUu7ZvgxAXkm9s2q7BDo
LbgrtfIAt9Ir5PjkCLJG0VE5j22U7SaySKeQiseTo3OrvojFASwlIHzCg6kQPkCq
24sr0OxfXxDDiV1AmZPFsihLcLGcb/dpJqJV1c0eWr++YwryyU90KJBRVpOVvAY8
uC6mioeNMWrxYk0sZBszgsfZxqJ2b5i9e63s+suQFvofRDkh0O/j5Gj+u6moKpb8
CKEAax7d1s/yaSrok4qzvig4DltQMAD2fw9iFqPX3A5cQ5aJWb9a4dGJ8e9oUIFO
Zbv7nI/ilFbCpe+ThouhPTb9LKv+UKpZy/1Y/1ZheiFMlzwr5Stl/wlYdiI=
-----END CERTIFICATE-----
'''
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWhsZmY2Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI4ZmMyNDFkNy04MDc1LTRmMzUtYTczZC01MDJmMzA2ODY2ODMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.XOa3IU-nxJqklvu6v8nF3su0maX2R9zeybwUfAi5c0nCcDlEt7vavOI3LGk5Fu_5l_P5WAbD2_zIqfiT5911FKtzeqfy4ScSHB-e78mNgq0RXV8Q4oXWs9dgh8Wb90v-4Q57JbukKVWILTaf3r_E8j3M_7cF3jbXo3ubewqW09DEycrYwDl2bJOiPhYXUmuJFWKHAvVeRwQPOsM7y9HDMoI2OFSvHo-5ecCI4rAfsPHEQRRamAb2VnM2e-XSGB7fKnniR-Acyxch0bVelpT69QVPpvuv-h60ZZlPYvzqj8rF-jdCipm1-IeOugRRwQ7AH-N-a5Vdii1zFHLrCLYhHQ'
createResource("Infrastructure/K8s/cluster-k8s-local", "k8s.Master", {'apiServerURL': 'https://172.42.42.100:6443', 'caCert': caCert, 'token': token})
createResource("Infrastructure/K8s/cluster-k8s-local/ns-helloworld-dev", "k8s.Namespace", {'namespaceName': 'ns-helloworld-dev'})
createResource("Infrastructure/K8s/cluster-k8s-local/ns-helloworld-pre", "k8s.Namespace", {'namespaceName': 'ns-helloworld-pre'})
createResource("Infrastructure/K8s/cluster-k8s-local/ns-helloworld-pro", "k8s.Namespace", {'namespaceName': 'ns-helloworld-pro'})

# | ____|_ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_ ___ 
# |  _| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
# | |___| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_\__ \
# |_____|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|___/

# Necesitamos crear un entorno que agrupe los distintos elementos que hemos creado antes
# Primero creamos la estructura de directorios
createResource("Environments/application-helloworld", "core.Directory", None)
createResource("Environments/application-helloworld/application-helloworld-dev", "core.Directory", None)
createResource("Environments/application-helloworld/application-helloworld-pre", "core.Directory", None)
createResource("Environments/application-helloworld/application-helloworld-pro", "core.Directory", None)
createOrUpdateEnvironment('dev')
createOrUpdateEnvironment('pre')
createOrUpdateEnvironment('pro')

#    / \   _ __  _ __ | (_) ___ __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \/ __|
#  / ___ \| |_) | |_) | | | (_| (_| | |_| | (_) | | | \__ \
# /_/   \_\ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|___/

createResource("Applications/Applications", "core.Directory", None)
createResource("Applications/Applications/application-helloworld", "core.Directory", None)
createResource("Applications/Applications/application-helloworld/helloworld", "udm.Application", None)

#  / ___|___  _ __  / _(_) __ _ _   _ _ __ __ _| |_(_) ___  _ __  
# | |   / _ \| '_ \| |_| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \ 
# | |__| (_) | | | |  _| | (_| | |_| | | | (_| | |_| | (_) | | | |
#  \____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|

def getEnvironments(application):
    environments = []
    for env in ['dev', 'pre', 'pro']:
        environmentName = "Environments/application-{0}/application-{0}-{1}/application-{0}-{1}".format(application, env)
        environments = environments + [environmentName]
    return environments

# Creamos el pipeline
createResource("Configuration/pipeline-helloworld", "release.DeploymentPipeline", {'pipeline': getEnvironments('helloworld')})

# Y lo asociamos
helloworld = repository.read("Applications/Applications/application-helloworld/helloworld")
helloworld.pipeline = "Configuration/pipeline-helloworld"
repository.update(helloworld)
