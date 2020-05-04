# Este script se invoca de forma remota para crear los recursos compartidos
# La invocación se debe realizar de la siguiente forma:
# ./cli.sh -f /home/jcla/Projects/xld-scripts/shared-configuration/createXLDSharedConfigurationResources.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-9.0.5-cli/conf/deployit.conf con el siguiente contenido
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

#  / ___|___  _ __  / _(_) __ _ _   _ _ __ __ _| |_(_) ___  _ __  
# | |   / _ \| '_ \| |_| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \ 
# | |__| (_) | | | |  _| | (_| | |_| | | | (_| | |_| | (_) | | | |
#  \____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|

# Creamos el servidor SMTP
smtpServerProperties = {
    'host': 'localhost',
    'port': '1025',
    'fromAddress': 'xldeploy@xebialabs.com',
    'testAddress': 'josecarlos.lopezayala@gmail.com'
    }
createResource("Configuration/smtp-server", "mail.SmtpServer", smtpServerProperties)

# Creamos estructura de directorios para notificaciones
createResource("Configuration/Environments", "core.Directory", None)
createResource("Configuration/Environments/Development", "core.Directory", None)
createResource("Configuration/Environments/Development/EmailNotifications", "core.Directory", None)
createResource("Configuration/Environments/Development/Triggers", "core.Directory", None)
createResource("Configuration/Environments/Preproduction", "core.Directory", None)
createResource("Configuration/Environments/Preproduction/EmailNotifications", "core.Directory", None)
createResource("Configuration/Environments/Preproduction/Triggers", "core.Directory", None)
createResource("Configuration/Environments/Production", "core.Directory", None)
createResource("Configuration/Environments/Production/EmailNotifications", "core.Directory", None)
createResource("Configuration/Environments/Production/Triggers", "core.Directory", None)

# Configuramos las notificaciones por Email
def createEmailNotifications(env):
    environmentName = ""
    if env == "dev":
        environmentName = "Development"
    elif env == "pre":
        environmentName = "Preproduction"
    else:
        environmentName = "Production"
    emailFailedNotificationsProps = {
        'toAddresses': ['{0}team@xebialabs.com'.format(env)],
        'subject': 'FAILED! - Application ${deployedApplication.version.application.name} deployment to ${deployedApplication.environment.name} failed',
        'sendContentAsHtml': 'true',
        'bodyTemplatePath': '/opt/xebialabs/mail-templates/emailFailedDeployment{0}.html'.format(env.capitalize()),
        'mailServer': 'Configuration/smtp-server'
    }
    emailSuccessNotificationsProps = {
        'toAddresses': ['{0}team@xebialabs.com'.format(env)],
        'subject': 'SUCCESSFUL! - Application ${deployedApplication.version.application.name} deployment to ${deployedApplication.environment.name} successful',
        'sendContentAsHtml': 'true',
        'bodyTemplatePath': '/opt/xebialabs/mail-templates/emailSuccessfulDeployment{0}.html'.format(env.capitalize()),
        'mailServer': 'Configuration/smtp-server'
    }
    createResource("Configuration/Environments/{0}/EmailNotifications/EmailFailedDeployment".format(environmentName), "trigger.EmailNotification", emailFailedNotificationsProps)
    createResource("Configuration/Environments/{0}/EmailNotifications/EmailSuccessfulDeployment".format(environmentName), "trigger.EmailNotification", emailSuccessNotificationsProps)

createEmailNotifications('dev')
createEmailNotifications('pre')
createEmailNotifications('pro')

# Configuramos los triggers
def createTriggers(env):
    environmentName = ""
    if env == "dev":
        environmentName = "Development"
    elif env == "pre":
        environmentName = "Preproduction"
    else:
        environmentName = "Production"
    triggerFailedDeploymentProps = {
        'actions': ["Configuration/Environments/{0}/EmailNotifications/EmailFailedDeployment".format(environmentName)],
        'fromState': 'ANY',
        'toState': 'FAILED'
    }
    triggerSuccessfulDeploymentProps = {
        'actions': ["Configuration/Environments/{0}/EmailNotifications/EmailSuccessfulDeployment".format(environmentName)],
        'fromState': 'ANY',
        'toState': 'EXECUTED'
    }
    createResource("Configuration/Environments/{0}/Triggers/FailedDeploymentTrigger".format(environmentName), "trigger.TaskTrigger", triggerFailedDeploymentProps)
    createResource("Configuration/Environments/{0}/Triggers/SuccessfulDeploymentTrigger".format(environmentName), "trigger.TaskTrigger", triggerSuccessfulDeploymentProps)

createTriggers('dev')
createTriggers('pre')
createTriggers('pro')

# Creamos el registry privado en Nexus3 para Docker
dockerRegistryProperties = {
    'url': 'http://lyhsoft-registry:8084',
    'username': 'admin',
    'password': 'admin123'
    }
createResource("Configuration/DockerRegistries", "core.Directory", None)
createResource("Configuration/DockerRegistries/lyhsoft-registry", "docker.Registry", dockerRegistryProperties)

# Creamos directorio para Docker Engines
createResource("Infrastructure/DockerEngines", "core.Directory", None)

# Para crear los DockerEngines utilizamos los ficheros yaml del directorio docker-engines
# Nos damos cuenta que en esos DockerEngines hemos asociado el registro docker que hemos creado

# Creamos una entrada para LocalHost bajo UnixHosts
createResource("Infrastructure/UnixHosts", "core.Directory", None)
createResource("Infrastructure/UnixHosts/localhost", "overthere.LocalHost", {'os': 'UNIX'})
