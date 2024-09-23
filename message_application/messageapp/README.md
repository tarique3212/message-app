Message Application Helm Charts for Kubernetes


helm install -n message --create-namespace message messageapp/ --set message.image="021891604918.dkr.ecr.us-west-2.amazonaws.com/message-service" --set message.tag="latest"

