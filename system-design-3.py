from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Redshift, DocumentDB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.ml import Sagemaker
from diagrams.aws.analytics import Glue
from diagrams.aws.security import Cognito
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.general import User

# Create the diagram
with Diagram("Music Streaming Platform Architecture", show=False, direction="LR"):

    user = User("User")

    with Cluster("Frontend"):
        cloudfront = CloudFront("CloudFront CDN")
        s3_bucket = S3("S3 Bucket")
        api_gateway = APIGateway("API Gateway")

    with Cluster("Backend Services"):
        with Cluster("Auth Service"):
            cognito = Cognito("Amazon Cognito")
        
        with Cluster("Music Search Service"):
            search_lambda = Lambda("Music Search Lambda")
            db = DocumentDB("DocumentDB (MongoDB-compatible)")
        
        with Cluster("Music Streaming Service"):
            streaming_lambda = Lambda("Music Streaming Lambda")

        with Cluster("Recommendation Service"):
            recommendation_lambda = Lambda("Recommendation Lambda")
            sagemaker = Sagemaker("SageMaker")

    with Cluster("Data Pipeline"):
        kinesis = KinesisDataStreams("Kinesis Data Streams")
        glue = Glue("Glue ETL Jobs")
        redshift = Redshift("Redshift Data Warehouse")

    # User interaction flow
    user >> Edge(label="Login/Signup") >> cognito
    user >> Edge(label="Search Music") >> api_gateway >> search_lambda >> db
    user >> Edge(label="Stream Music") >> api_gateway >> streaming_lambda >> s3_bucket >> cloudfront
    user >> Edge(label="Recommendations") >> api_gateway >> recommendation_lambda >> sagemaker

    # Real-time data processing
    user >> Edge(label="User Activity") >> kinesis
    kinesis >> glue >> redshift
    redshift >> recommendation_lambda
    kinesis >> Edge(label="Real-time processing") >> recommendation_lambda

    # Data sources
    s3_bucket << Edge(label="Music Files") << streaming_lambda

