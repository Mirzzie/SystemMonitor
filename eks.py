from kubernetes import client, config
#load the config from kubeconfig

config.load_kube_config()

#Api client
api = client.ApiClient()


# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-app-container",
                        image="539393095924.dkr.ecr.us-east-1.amazonaws.com/my_app_image:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)


# create deployment
api_instance = client.AppsV1Api(api)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-app-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)

