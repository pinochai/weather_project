import aws_cdk as core
import aws_cdk.assertions as assertions

from weather_project.weather_project_stack import WeatherProjectStack

# example tests. To run these tests, uncomment this file along with the example
# resource in weather_project/weather_project_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WeatherProjectStack(app, "weather-project")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
