# in this example, we are using the auto-instrumentation agent to instrument our application
# see: https://opentelemetry.io/docs/instrumentation/python/automatic/

# Firstly, we install opentelemetry-instrumentation-flask and opentelemetry-exporter-otlp
# The latter is not strictly needed due to fact we are using the console exporter, but we get runtime errors if we don't

# We have set the following envvars:
# OTEL_TRACES_EXPORTER=console
# OTEL_METRICS_EXPORTER=console
# OTEL_SERVICE_NAME='auto-instrumentation-flask'
# FLASK_APP=auto-instrument.py

# We then invoke our app with:
# opentelemetry-instrument flask run

# The result is The output is similar to before, with a single trace containing a single span—but now we have a list of
# attributes that describe (from a Flask point of view) what is actually happening. We can see it was a GET request,
# via HTTP, to ‘/random,’ which came from the local 127.0.0.1 IP address. This comes for free—and has been defined in
# the opentelemetry-instrumentation-flask package.

from random import randint
from flask import Flask, request

app = Flask(__name__)


@app.route("/roll")
def roll():
    sides = int(request.args.get('sides'))
    rolls = int(request.args.get('rolls'))
    return roll_sum(sides, rolls)


def roll_sum(sides, rolls):
    sum = 0
    for r in range(0, rolls):
        result = randint(1, sides)
        sum += result
    return str(sum)
