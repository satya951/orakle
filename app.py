from aws_cdk import (
    Stack,
    App,
    Environment,
)
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs_patterns as ecs_patterns
from constructs import Construct  # Needed in CDK v2

class FastapiEcsStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC (Virtual Private Cloud)
        vpc = ec2.Vpc(self, "FastapiVpc", max_azs=2)  # Max 2 availability zones

        # Create an ECS Cluster within the VPC
        cluster = ecs.Cluster(self, "FastapiCluster", vpc=vpc)

        # Reference the ECR repository
        ecr_repo = ecr.Repository.from_repository_arn(
            self,
            "EcrRepository",
            "arn:aws:ecr:eu-central-1:364119026921:repository/devops"
        )

        # Create Fargate Service with Load Balancer
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "FastapiService",
            cluster=cluster,
            task_image_options={
                "image": ecs.ContainerImage.from_ecr_repository(ecr_repo),
                "container_port": 8000  # Port exposed by the FastAPI app
            }
        )

# Entry point for AWS CDK
app = App()
FastapiEcsStack(app, "FastapiEcsStack", env=Environment(account="364119026921", region="eu-central-1"))
app.synth()
