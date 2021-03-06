# Este script se invoca de forma remota para crear la infraestructura de la aplicación de Tutorial para Aws y ECS
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/tutorial/createXLDTutorialAwsEcsResources.py aws_access_key_id aws_secret_access_key
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

# La aplicación la cargamos utilizando xl apply -f app-ecs.yaml

# Las claves para acceder a AWS se reciben por parámetro
import sys
aws_access_key_id = sys.argv[1]
aws_secret_access_key = sys.argv[2]

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
    dictionaryName = "Environments/dictionaries-tutorial-ecs/dictionary-application-tutorial-ecs-{0}".format(env)
    if not repository.exists(dictionaryName):
        myDict = factory.configurationItem(dictionaryName, 'udm.Dictionary', {})
        repository.create(myDict)
        print("Dictionary {0} created".format(dictionaryName))
    else:
        myDict = repository.read(dictionaryName)
        # Por ahora no necesitamos dictEntries
        # myDict.entries = dictEntries
        repository.update(myDict)
        print("Dictionary {0} updated".format(dictionaryName))

def createOrUpdateEnvironment(env):
    environmentName = "Environments/application-tutorial-ecs/application-tutorial-ecs-{0}/application-tutorial-ecs-{0}".format(env)
    dictionaryName = "Environments/dictionaries-tutorial-ecs/dictionary-application-tutorial-ecs-{0}".format(env)
    dictionaries = [dictionaryName]
    requiresOkTestManager = False
    requiresOkReleaseManager = False
    if env == "pre":
        requiresOkTestManager = True
    if env == "pro":
        requiresOkTestManager = True
        requiresOkReleaseManager = True
    myContainers = [
        "Infrastructure/Aws/aws-tutorial-ecs-{0}".format(env)
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

createResource("Infrastructure/Aws", "core.Directory", None)
createResource("Infrastructure/Aws/aws-tutorial-ecs-dev", "aws.Cloud", {'accesskey': aws_access_key_id, 'accessSecret': aws_secret_access_key})
createResource("Infrastructure/Aws/aws-tutorial-ecs-pre", "aws.Cloud", {'accesskey': aws_access_key_id, 'accessSecret': aws_secret_access_key})
createResource("Infrastructure/Aws/aws-tutorial-ecs-pro", "aws.Cloud", {'accesskey': aws_access_key_id, 'accessSecret': aws_secret_access_key})

# |  _ \(_) ___| |_(_) ___  _ __   __ _ _ __(_) ___  ___ 
# | | | | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
# | |_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \
# |____/|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/

createResource("Environments/dictionaries-tutorial-ecs", "core.Directory", None)
createOrUpdateDictionary('dev')
createOrUpdateDictionary('pre')
createOrUpdateDictionary('pro')

# | ____|_ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_ ___ 
# |  _| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __/ __|
# | |___| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_\__ \
# |_____|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|___/

# Necesitamos crear un entorno que agrupe los distintos elementos que hemos creado antes
# Primero creamos la estructura de directorios
createResource("Environments/application-tutorial-ecs", "core.Directory", None)
createResource("Environments/application-tutorial-ecs/application-tutorial-ecs-dev", "core.Directory", None)
createResource("Environments/application-tutorial-ecs/application-tutorial-ecs-pre", "core.Directory", None)
createResource("Environments/application-tutorial-ecs/application-tutorial-ecs-pro", "core.Directory", None)
createOrUpdateEnvironment('dev')
createOrUpdateEnvironment('pre')
createOrUpdateEnvironment('pro')

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
createResource("Configuration/pipeline-tutorial-ecs", "release.DeploymentPipeline", {'pipeline': getEnvironments('tutorial-ecs')})

# Y lo asociamos
tutorial = repository.read("Applications/Infrastructures/Aws/infrastructure-ecs-tutorial")
tutorial.pipeline = "Configuration/pipeline-tutorial-ecs"
repository.update(tutorial)
