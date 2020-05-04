# Este script se invoca de forma remota para crear la infraestructura de la aplicación de Voting App
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/voting-app-k8s/createXLDVotingAppK8sResources.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

# La aplicación la cargamos utilizando xl apply -f app.yaml

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

def createOrUpdateDictionary(env):
    dictEntries = {
        'environment': env
    }
    dictionaryName = "Environments/dictionaries-voting-app-k8s/dictionary-application-voting-app-k8s-{0}".format(env)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {'entries': dictEntries})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))

def createOrUpdateEnvironment(env):
    environmentName = "Environments/application-voting-app-k8s/application-voting-app-k8s-{0}/application-voting-app-k8s-{0}".format(env)
    dictionaryName = "Environments/dictionaries-voting-app-k8s/dictionary-application-voting-app-k8s-{0}".format(env)
    dictionaries = [dictionaryName]
    requiresOkTestManager = False
    requiresOkReleaseManager = False
    if env == "pre":
        requiresOkTestManager = True
    if env == "pro":
        requiresOkTestManager = True
        requiresOkReleaseManager = True
    myContainers = [
        "Infrastructure/KubernetesClusters/on-premise-cluster/ns-voting-app-{0}".format(env)
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
        myEnvironment = factory.configurationItem(environmentName, 'udm.Environment', {'members': myContainers, 'dictionaries': dictionaries, 'requiresOkTestManager': requiresOkTestManager, 'requiresOkReleaseManager': requiresOkReleaseManager, 'triggers': triggers})
        repository.create(myEnvironment)
        print("Environment {0} created".format(environmentName))
    else:
        myEnvironment = repository.read(environmentName)
        myEnvironment.members = myContainers
        myEnvironment.dictionaries = dictionaries
        myEnvironment.requiresOkTestManager = requiresOkTestManager
        myEnvironment.requiresOkReleaseManager = requiresOkReleaseManager
        myEnvironment.triggers = triggers
        repository.update(myEnvironment)
        print("Environment {0} updated".format(environmentName))

#        / ___|___  _ __ | |_ __ _(_)_ __   ___ _ __ ___ 
#        | |   / _ \| '_ \| __/ _` | | '_ \ / _ \ '__/ __|
#        | |__| (_) | | | | || (_| | | | | |  __/ |  \__ \
#         \____\___/|_| |_|\__\__,_|_|_| |_|\___|_|  |___/

createResource("Infrastructure/KubernetesClusters", "core.Directory", None)
caCertOnPremise = '''
-----BEGIN CERTIFICATE-----
MIICyDCCAbCgAwIBAgIBADANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwprdWJl
cm5ldGVzMB4XDTE5MDkyNDE2NTEwN1oXDTI5MDkyMTE2NTEwN1owFTETMBEGA1UE
AxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJpc
e6EOgIjCyPIzGu85KQMNGrshoXelpW+kQ1Vh3KOg4YUTfE7JI8Yk1c0IUuZ4XBEo
kiDIEW7LkmXM7biTcWoFrnp+yn8YjWsZ4x1ZpcmptyxTZqiwZKRN8Hz7WrWiVKhE
s+0/+u/onQAr1gs0+it0YG1nrrxK9PW5opeMtyl3pU8ol5RaKU99xVxGdeJtxt5o
C6K/jP4HY3C4c5GmBIRa2UOSSyz2g3//AfHymrZjPTzfA8lBoPtC2zp6ImZI9ehp
z4rptkEOtOjhnyk55+Q5nhnMHKmOw8u/6FNovdotZaprcQn/cQQHyzCp15kyaWwv
NKBcXOWPfHqJ/Y34S+UCAwEAAaMjMCEwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB
/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAFanPd/OwmZ0EcE4y2RFhByguAMw
yYrdr90Hf10NKdg+logU0NFFbeGECDcINwgdLQzT4K/rb9sASAlEiCZHRnfSWLzS
hBj+ikWM4ipBPVAnP/jkDW32I3+GchatHriA6madlpL8B2Jbk0gwsqIEYtNFhFR1
Gg7nrEIvLMKtQ//9Bt+gI6+hykMASK1wlWmBIcaee5aMvFyTz7Z4BQPDC3uA7wsG
t/Gus1LOSq+ZXsbTUoB5Lnh4oyqxXdrwWPHdL3jQ3NBcxVxlROVnz5p831UEEKPd
Y7UzIOvpvWh4xUbiscw4CuCCY0h7F7Fn6xUnO6fDO1LyqLWEQhJCjv0lFGA=
-----END CERTIFICATE-----
'''
tokenOnPremise = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlFWMTFVNWM4UnYxTnZpT3VPOERraUJ6S2dIX182NUZnT2VtSWRvYWpLVTAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLWZ0OGJ0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIxZGU3NTQ0Ny1lN2I0LTRjOWQtYjRkYi0wMjM5ZjY5ODBkZDAiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.miLhUMyVBSfSpUS4tcDzR4tmmArKVHOsBNapDSTFiramNUg0aPoAhvoLIgMtXDesQlkPh9s-hnFR0LlM1FfVvAwCCP1UHip_jDAt2oLrdbMaB-TgBLlUO5VmW0aQVDRhqztg6mADfl14_O5lnI-cjU5Pq37rdHv_7H8nEk7CA1XhgwH77jROs19JUwmmmZM3CrG8M00jQHx6E1pC5zVxN_joG1F3Hm9q5Ngk0ZrGh7l9sS9NZrhY4riX5ZjLsC29SkJIA0Hc59Uhjiv8yShUnBsOC4PKAiCltFWTlvE38g6cvIOf4j7YJ5KgVhiXeLyOYFQs8f8UJYE-xmdUu2WPrg'
createResource("Infrastructure/KubernetesClusters/on-premise-cluster", "k8s.Master", {'apiServerURL': 'https://172.42.42.100:6443', 'skipTLS': True, 'caCert': caCertOnPremise, 'token': tokenOnPremise})
createResource("Infrastructure/KubernetesClusters/on-premise-cluster/ns-voting-app-dev", "k8s.Namespace", {'namespaceName': 'ns-voting-app-dev'})
createResource("Infrastructure/KubernetesClusters/on-premise-cluster/ns-voting-app-pre", "k8s.Namespace", {'namespaceName': 'ns-voting-app-pre'})
createResource("Infrastructure/KubernetesClusters/on-premise-cluster/ns-voting-app-pro", "k8s.Namespace", {'namespaceName': 'ns-voting-app-pro'})

# |  _ \(_) ___| |_(_) ___  _ __   __ _ _ __(_) ___  ___ 
# | | | | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
# | |_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \
# |____/|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/

createResource("Environments/dictionaries-voting-app-k8s", "core.Directory", None)
createOrUpdateDictionary('dev')
createOrUpdateDictionary('pre')
createOrUpdateDictionary('pro')

# | ____|_ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_ ___ 
# |  _| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
# | |___| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_\__ \
# |_____|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|___/

# Necesitamos crear un entorno que agrupe los distintos elementos que hemos creado antes
# Primero creamos la estructura de directorios
createResource("Environments/application-voting-app-k8s", "core.Directory", None)
createResource("Environments/application-voting-app-k8s/application-voting-app-k8s-dev", "core.Directory", None)
createResource("Environments/application-voting-app-k8s/application-voting-app-k8s-pre", "core.Directory", None)
createResource("Environments/application-voting-app-k8s/application-voting-app-k8s-pro", "core.Directory", None)
createOrUpdateEnvironment('dev')
createOrUpdateEnvironment('pre')
createOrUpdateEnvironment('pro')

#    / \   _ __  _ __ | (_) ___ __ _| |_(_) ___  _ __  ___ 
#   / _ \ | '_ \| '_ \| | |/ __/ _` | __| |/ _ \| '_ \/ __|
#  / ___ \| |_) | |_) | | | (_| (_| | |_| | (_) | | | \__ \
# /_/   \_\ .__/| .__/|_|_|\___\__,_|\__|_|\___/|_| |_|___/

# La aplicacion se crea con el fichero app.yaml y los blueprints

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
createResource("Configuration/pipeline-voting-app-k8s", "release.DeploymentPipeline", {'pipeline': getEnvironments('voting-app-k8s')})

# Y lo asociamos
deployment_db = repository.read("Applications/Applications/application-voting-app-k8s/deployment-db")
deployment_redis = repository.read("Applications/Applications/application-voting-app-k8s/deployment-redis")
deployment_result = repository.read("Applications/Applications/application-voting-app-k8s/deployment-result")
deployment_worker = repository.read("Applications/Applications/application-voting-app-k8s/deployment-worker")
service_db = repository.read("Applications/Applications/application-voting-app-k8s/service-db")
service_redis = repository.read("Applications/Applications/application-voting-app-k8s/service-redis")
service_result = repository.read("Applications/Applications/application-voting-app-k8s/service-result")
virtual_service_result = repository.read("Applications/Applications/application-voting-app-k8s/virtual-service-result")

deployment_db.pipeline = "Configuration/pipeline-voting-app-k8s"
deployment_redis.pipeline = "Configuration/pipeline-voting-app-k8s"
deployment_result.pipeline = "Configuration/pipeline-voting-app-k8s"
deployment_worker.pipeline = "Configuration/pipeline-voting-app-k8s"
service_db.pipeline = "Configuration/pipeline-voting-app-k8s"
service_redis.pipeline = "Configuration/pipeline-voting-app-k8s"
service_result.pipeline = "Configuration/pipeline-voting-app-k8s"
virtual_service_result.pipeline = "Configuration/pipeline-voting-app-k8s"

repository.update(deployment_db)
repository.update(deployment_redis)
repository.update(deployment_result)
repository.update(deployment_worker)
repository.update(service_db)
repository.update(service_redis)
repository.update(service_result)
repository.update(virtual_service_result)