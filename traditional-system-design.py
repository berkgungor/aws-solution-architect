from diagrams import Diagram
from diagrams.aws.compute import EC2, ALB, API
from diagrams.aws.database import RDS, DynamoDB, Redshift
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Athena
from diagrams.aws.bigdata import Glue
from diagrams.aws.integration import Kafka
from diagrams.aws.security import IAM, KMS
from diagrams.aws.ai import SageMaker
from diagrams.aws.management import CloudWatch, CloudTrail
from diagram.aws.cdn import CloudFront as CDN

with Diagram("Music Streaming System Architecture", show=False):
    # Client-side components
    client_app = API("Client App")

    # Load Balancer
    alb = ALB("Application Load Balancer")

    # Authentication
    cognito = API("AWS Cognito")

    # Microservices
    user_service = EC2("User Service")
    search_service = EC2("Search Service")
    recommendation_service = EC2("Recommendation Service")
    streaming_service = EC2("Streaming Service")
    data_processing_service = EC2("Data Processing Service")

    # Databases
    rds = RDS("Amazon RDS")
    dynamodb = DynamoDB("Amazon DynamoDB")
    s3 = S3("Amazon S3")
    redshift = Redshift("Amazon Redshift")

    # Caching and CDN
    redis_cache = EC2("Redis Cache")
    cloudfront = CloudFront("Amazon CloudFront")

    # Data Streaming and Processing
    kafka = Kafka("Apache Kafka")
    glue = Glue("AWS Glue")
    athena = Athena("Amazon Athena")

    # Analytics and Machine Learning
    sagemaker = SageMaker("Amazon SageMaker")

    # Monitoring and Logging
    cloudwatch = CloudWatch("Amazon CloudWatch")
    cloudtrail = CloudTrail("AWS CloudTrail")

    # Security and Compliance
    iam = IAM("AWS IAM")
    kms = KMS("AWS KMS")

    # Draw the diagram
    client_app >> alb >> [user_service, search_service, recommendation_service, streaming_service]
    user_service >> rds
    search_service >> dynamodb
    streaming_service >> s3
    s3 >> cloudfront
    cloudfront >> client_app
    data_processing_service >> kafka
    kafka >> glue
    glue >> redshift
    redshift >> athena
    athena >> client_app
    redis_cache << user_service
    redis_cache << search_service
    redis_cache << recommendation_service
    redis_cache << streaming_service
    client_app >> cognito
    iam >> [user_service, search_service, recommendation_service, streaming_service, data_processing_service]
    kms >> [s3, rds, dynamodb, redshift]
    cloudwatch << [user_service, search_service, recommendation_service, streaming_service, data_processing_service]
    cloudtrail << [user_service, search_service, recommendation_service, streaming_service, data_processing_service]
    sagemaker >> recommendation_service

