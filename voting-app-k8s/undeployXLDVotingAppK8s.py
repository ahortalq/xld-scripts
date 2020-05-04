# Este script se invoca de forma remota para lanzar despliegues de la aplicación de Voting App
# La invocación se debe realizar de la siguiente forma:
# cd /opt/xebialabs/xl-deploy-9.0.5-cli/bin/
# ./cli.sh -f /home/jcla/Projects/xld-scripts/voting-app-k8s/undeployXLDVotingAppK8s.py
# El usuario y la password están en el fichero /opt/xebialabs/xl-deploy-X-cli/conf/deployit.conf con el siguiente contenido
# cli.username=admin
# cli.password=password      <- la password se modifica la primera vez que ejecutemos el cli

def undeployVotingApp(environment):
    taskID = deployment.createUndeployTask("Environments/application-voting-app-k8s/application-voting-app-k8s-{0}/application-voting-app-k8s-{0}/deployment-vote".format(environment)).id
    print("taskId = {0}".format(taskID))
    deployit.startTaskAndWait(taskID)

for e in ['dev', 'pre', 'pro']:
    undeployVotingApp(e)

