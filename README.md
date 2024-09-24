EKS Cluster creation using terraform

1) cd message_application/terraform/
2) Update region_name in variables.tf file
3) Update aws_access_key, aws_secret_key in terraform.tfvars
4) terraform init
5) terraform plan
6) terraform apply
7) terraform destroy(to delete cluster)

Create Docker Image

1) cd message-image/
2) docker build -t message/message_service:latest .

Upload Docker Image to ECR

1) aws ecr get-login-password –region <region-name> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region-name>.amazonaws.com
2) docker tag message/message_service:latest <account-id>.dkr.ecr.<regionname>.amazonaws.com:latest
3) aws ecr create-repository --repository-name message-service --region <region-name>
4) docker push <account-id>.dkr.ecr.<region-name>.amazonaws.com:latest

Install Message Application

1) cd message_application/messageapp
2) helm upgrade --install -n message --create-namespace message messageapp/ --set message.image="<account-id>.dkr.ecr.<region-name>.amazonaws.com/message-service" --set message.tag="latest"

Create Nginx Controller Loadbalancer

1) kubectl apply -f message_application/ingress-controller.yaml
2) Validate the ingress hostname by using below command
   “kubectl get ingress -A | grep message-service-ingress | awk '{print $5}'”
3) Check if you are able to access application URL
   /get/messages: http://<ingress-hostname>/get/messages
   /search: http://<ingress-hostname>/search
   /create: http://<ingress-hostname>/create

Install Prometheus

1) cd message_application/
2) helm upgrade --install prometheus -n prom --create-namespace prometheus/
4) Ingress Hostname “kubectl get ingress -A | grep prometheus-ingress | awk '{print $5}'”
5) For Prometheus URL Check: “http://<ingress-hostname>/prometheus”

Install Alertmanager

1) cd message_application/
2) helm upgrade --install alertmanager -n prom --create-namespace alertmanager/
3) Ingress Hostname “kubectl get ingress -A | grep alertmanager-ingress | awk '{print $5}'”
4) For Alertmanager: “http://<ingress-hostname>/alertmanager”
5) Added the slack and email based alert features
