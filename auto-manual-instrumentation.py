# This is a simple Flask application that will be used to demonstrate the OpenTelemetry Python library combined with
# automatic instrumentation.

# We set the following envvars:
# OTEL_TRACES_EXPORTER='console'
# OTEL_METRICS_EXPORTER='none'
# OTEL_SERVICE_NAME='auto-manual-instrumentation-flask'
# FLASK_APP=auto-manual-instrument.py

# OpenTelemetry tracging API: https://opentelemetry.io/docs/reference/specification/trace/api
from opentelemetry import trace

# A provider is our entrypoint for the OpenTelemetry Tracing API.
from opentelemetry.sdk.trace import TracerProvider

from random import randint
from flask import Flask, request

# Create a TracerProvider and register it as 'provider'.
provider = TracerProvider()
# Set our provider as the global trace provider.
trace.set_tracer_provider(provider)
# Create a tracer object.
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


@app.route("/roll")
def roll():
    sides = int(request.args.get('sides'))
    rolls = int(request.args.get('rolls'))
    return roll_sum(sides, rolls)


def roll_sum(sides, rolls):
    # We are now applying manual instrumentation to the roll_sum function as previously.
    # That will create two spans: a parent representing the /roll route (and is auto-implemented), one child
    # representing the roll_sum function, and an event per roll attached. We have removed any reference to a processor
    # from the setup code.
    with tracer.start_as_current_span("roll_sum"):
        span = trace.get_current_span()
        sum = 0
        for r in range(0, rolls):
            result = randint(1, sides)
            span.add_event("log", {
                "roll.sides": sides,
                "roll.result": result,
            })
            sum += result
        return str(sum)

# The result is that our roll_sum span lists our route span as its parent!
# Additionally, with auto-instrumentation, we get free information about exceptions.
# By changing the number of rolls in the curl command to a non-numeric value and hitting our auto-instrumented Flask
# server again, we will see a trace that contains an error event that describes the issue, including a traceback
