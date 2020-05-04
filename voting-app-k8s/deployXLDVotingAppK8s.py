# Este script se invoca de forma remota para lanzar despliegues de la aplicación de Voting App
# La invocación se debe realizar de la siguiente forma:
# cd /opt/xebialabs/xl-deploy-9.0.5-cli/bin/
# ./cli.sh -f /home/jcla/Projects/xld-scripts/voting-app-k8s/deployXLDVotingAppK8s.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

def deployVotingApp(environment):
    # Load package
    package = repository.read("Applications/Applications/application-voting-app-k8s/deployment-vote/20.4.0-B102")
    # Load environment
    environment = repository.read("Environments/application-voting-app-k8s/application-voting-app-k8s-{0}/application-voting-app-k8s-{0}".format(environment))
    # Start deployment
    deploymentRef = deployment.prepareInitial(package.id, environment.id)
    depl = deployment.prepareAutoDeployeds(deploymentRef)
    task = deployment.createDeployTask(depl)
    print("taskId = {0}".format(task.id))
    deployit.startTaskAndWait(task.id)


for e in ['dev', 'pre', 'pro']:
    deployVotingApp(e)
