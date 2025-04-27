#!/usr/bin/env python3
import os

import aws_cdk as cdk

from weather_project.weather_project_stack import WeatherDataStack


app = cdk.App()

WeatherDataStack(app, "WeatherDataStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()
