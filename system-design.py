from graphviz import Digraph

def create_music_streaming_diagram():
    dot = Digraph(comment='Music Streaming System Architecture')
    dot.attr(rankdir='TB', size='15,15')

    # Define node styles
    dot.attr('node', shape='box', style='filled', color='lightblue')

    # Client Layer
    with dot.subgraph(name='cluster_client') as c:
        c.attr(label='Client Layer')
        c.node('web_app', 'Web Application')
        c.node('mobile_app', 'Mobile Applications')

    # CDN Layer
    dot.node('cloudfront', 'Amazon CloudFront')

    # Load Balancer
    dot.node('alb', 'Application Load Balancer')

    # API Layer
    dot.node('api_gateway', 'Amazon API Gateway')

    # Authentication
    dot.node('cognito', 'Amazon Cognito')

    # Application Logic Layer
    with dot.subgraph(name='cluster_app_logic') as c:
        c.attr(label='Application Logic Layer (Lambda)')
        c.node('user_service', 'User Profile Service')
        c.node('search_service', 'Search Service')
        c.node('recommend_service', 'Recommendation Service')
        c.node('playlist_service', 'Playlist Management Service')
        c.node('stream_service', 'Streaming Service')

    # Database Layer
    with dot.subgraph(name='cluster_db') as c:
        c.attr(label='Database Layer')
        c.node('rds', 'Amazon RDS\n(User data, Playlists)')
        c.node('dynamodb', 'Amazon DynamoDB\n(User history, Play counts)')
        c.node('elasticache', 'Amazon ElastiCache\n(Caching layer)')
        c.node('neptune', 'Amazon Neptune\n(Recommendation graphs)')

    # Storage Layer
    dot.node('s3', 'Amazon S3\n(Audio files, Static assets)')

    # Search Layer
    dot.node('elasticsearch', 'Amazon Elasticsearch\n(Song search index)')

    # Data Processing
    dot.node('glue', 'AWS Glue\n(ETL jobs)')
    dot.node('redshift', 'Amazon Redshift\n(Data Warehouse)')
    dot.node('athena', 'Amazon Athena\n(Ad-hoc queries)')
    dot.node('msk', 'Amazon MSK (Kafka)\n(Event streaming)')

    # Define edges
    dot.edge('web_app', 'cloudfront')
    dot.edge('mobile_app', 'cloudfront')
    dot.edge('cloudfront', 'alb')
    dot.edge('alb', 'api_gateway')
    dot.edge('api_gateway', 'cognito')
    dot.edge('api_gateway', 'user_service')
    dot.edge('api_gateway', 'search_service')
    dot.edge('api_gateway', 'recommend_service')
    dot.edge('api_gateway', 'playlist_service')
    dot.edge('api_gateway', 'stream_service')
    dot.edge('user_service', 'rds')
    dot.edge('search_service', 'elasticsearch')
    dot.edge('recommend_service', 'neptune')
    dot.edge('recommend_service', 'dynamodb')
    dot.edge('playlist_service', 'rds')
    dot.edge('stream_service', 'cloudfront', label='signed URL')
    dot.edge('cloudfront', 's3')
    dot.edge('rds', 'elasticache')
    dot.edge('dynamodb', 'elasticache')
    dot.edge('user_service', 'msk', label='user events')
    dot.edge('stream_service', 'msk', label='play events')
    dot.edge('msk', 'glue')
    dot.edge('glue', 'redshift')
    dot.edge('redshift', 'athena')
    dot.edge('s3', 'athena')

    # Render the diagram
    dot.render('music_streaming_architecture_v3', format='png', cleanup=True)
    print("Diagram created: music_streaming_architecture_v3.png")

if __name__ == "__main__":
    create_music_streaming_diagram()