Message Application Helm Charts for Kubernetes


helm install -n message --create-namespace message messageapp/ --set message.image="{account-id}.dkr.ecr.{region-name}.amazonaws.com/message-service" --set message.tag="latest"

Update account-id and region-name in the above installation command.
