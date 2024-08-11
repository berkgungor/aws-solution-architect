from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb, Aurora, Redshift
from diagrams.aws.network import APIGateway, CloudFront, Route53
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.aws.analytics import KinesisDataStreams, Glue, Athena
from diagrams.aws.ml import Sagemaker
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS
from diagrams.aws.network import ELB
from diagrams.aws.compute import EC2
from diagrams.aws.general import Client
from diagrams.aws.database import Elasticache

with Diagram("Serverless Music Streaming Architecture", show=True, direction="TB"):

    clients = Client("Web/Mobile Clients")

    with Cluster("API Layer"):
        api_gw = APIGateway("API Gateway")
        auth = Cognito("Auth")

    clients >> api_gw >> auth

    with Cluster("Microservices"):
        with Cluster("Business Logic (Lambda)"):
            user_mgmt = Lambda("User Management")
            song_search = Lambda("Song Search")
            recommendations = Lambda("Recommendations")
            song_streaming = Lambda("Song Streaming")
        
        api_gw >> user_mgmt
        auth >> user_mgmt
        api_gw >> song_search
        api_gw >> recommendations
        api_gw >> song_streaming

    with Cluster("Database Layer"):
        dynamodb_user_data = Dynamodb("DynamoDB (User Data)")
        dynamodb_metadata = Dynamodb("DynamoDB (Song Metadata)")
        aurora_serverless = Aurora("Aurora Serverless")
        dynamodb_logs = Dynamodb("DynamoDB (User Activity Logs)")

        user_mgmt >> dynamodb_user_data
        song_search >> dynamodb_metadata
        recommendations >> dynamodb_logs

    with Cluster("Storage Layer"):
        s3_media = S3("S3 (Media Files)")
        song_streaming >> s3_media

    with Cluster("Content Delivery"):
        cdn = CloudFront("CloudFront (CDN)")
        s3_media >> cdn
        song_streaming >> cdn

    with Cluster("Caching Layer"):
        cache = Elasticache("ElastiCache (Redis)")
        dynamodb_metadata >> cache

    with Cluster("Data Streaming"):
        kinesis = KinesisDataStreams("Kinesis Data Streams")
        dynamodb_logs >> kinesis

    with Cluster("Data Processing and ETL"):
        glue = Glue("Glue ETL")
        kinesis >> glue
        s3_data_lake = S3("S3 (Data Lake)")
        glue >> s3_data_lake

    with Cluster("Data Warehouse"):
        redshift = Redshift("Redshift Serverless")
        glue >> redshift

    with Cluster("Data Analysis"):
        athena = Athena("Athena")
        s3_data_lake >> athena

    with Cluster("Machine Learning"):
        sagemaker = Sagemaker("SageMaker")
        glue >> sagemaker
        recommendations >> sagemaker

    with Cluster("Monitoring"):
        cloudwatch = Cloudwatch("CloudWatch")
        api_gw >> cloudwatch
        user_mgmt >> cloudwatch
        song_search >> cloudwatch
        recommendations >> cloudwatch
        song_streaming >> cloudwatch
