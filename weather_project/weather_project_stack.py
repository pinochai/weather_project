from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_s3 as s3,
    Duration,
    RemovalPolicy
)
from constructs import Construct

class WeatherDataStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB Table
        table = dynamodb.Table(
            self, "WeatherDataTable",
            partition_key=dynamodb.Attribute(name="record_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
         # Create S3 Bucket
        bucket = s3.Bucket(self, "WeatherDataBucket",
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create Fetch Lambda Function
        fetch_lambda = _lambda.Function(
            self, "FetchWeatherData",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="fetch.lambda_handler",
            code=_lambda.Code.from_asset("lambda_package")
        )

        # Create Store Lambda Function
        store_lambda = _lambda.Function(
            self, "StoreWeatherData",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="store.lambda_handler",
            code=_lambda.Code.from_asset("lambda_package"),
            environment={
                "TABLE_NAME": table.table_name,
                "BUCKET_NAME": bucket.bucket_name
            },
        )

       # Grant Store Lambda write permissions to DynamoDB and S3
        table.grant_write_data(store_lambda)
        bucket.grant_write(store_lambda)

        # Step Functions Tasks
        fetch_task = tasks.LambdaInvoke(
            self, "Fetch Weather Data",
            lambda_function=fetch_lambda,
            result_path="$.weather_data"
        )

        store_task = tasks.LambdaInvoke(
            self, "Store Weather Data",
            lambda_function=store_lambda,
            payload_response_only=True
        )

        # Step Function Definition
        definition = fetch_task.next(store_task)

        step_function = sfn.StateMachine(
            self, "WeatherDataStateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(definition)
        )

        # EventBridge Rule to Trigger Step Function
        rule = events.Rule(
            self, "ScheduledRule",
            schedule=events.Schedule.rate(Duration.hours(1))
        )
        rule.add_target(targets.SfnStateMachine(step_function))

        # Create SNS Topics
        topic = sns.Topic(self, "WeatherDataTopic")

        # Subscribe an email address to the SNS Topic
        topic.add_subscription(subs.EmailSubscription("mehdi.sghaier@draexlmaier.com"))

        # Add SNS Topic ARN to Store Lambda environment variables
        store_lambda.add_environment("TOPIC_ARN", topic.topic_arn)

        # Create IAM Policy for SNS Publish
        sns_publish_policy = iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=[topic.topic_arn]
        )

        # Attach the policy to the Lambda function's role
        store_lambda.add_to_role_policy(sns_publish_policy)

        # Create API Gateway
        api = apigw.RestApi(self, "WeatherDataApi",
            rest_api_name="Weather Data Service",
            description="This service serves weather data."
        )

        # Create API Gateway Resources and Methods
        fetch_integration = apigw.LambdaIntegration(fetch_lambda)

        weather = api.root.add_resource("weather")
        weather.add_method("GET", fetch_integration)  # GET /weather