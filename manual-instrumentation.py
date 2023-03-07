# This is a simple Flask application that will be used to demonstrate the OpenTelemetry Python library.

# There are three concepts at play in this opentelemetry demo:
# A provider (in this case TracingProvider) is the API entry point that holds configuration.
# A processor defines the method of sending the created elements (spans) onwards.
# A tracer is an actual object which creates the spans.

# OpenTelemetry tracging API: https://opentelemetry.io/docs/reference/specification/trace/api
from opentelemetry import trace

# A provider is our entrypoint for the OpenTelemetry Tracing API.
# The OpenTelemetry tracing API has three main classes:
# TracerProvider - our entrypoint
# Tracer - the class responsible for creating spans
# Span - the API to trace an operation
from opentelemetry.sdk.trace import TracerProvider

# BatchSpanProcessor is an implementation of SpanProcessor that batches ended spans and pushes them to the configured
# SpanExporter.
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Implementation of SpanExporter that prints spans to the console. In production we would send to an opentelemetry
# collector.
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

from random import randint
from flask import Flask, request

# Create a TracerProvider and register it as 'provider'.
provider = TracerProvider()
# Create a BatchSpanProcessor and register it as 'processor'. Pass BatchSpanProcessor a ConsoleSpanExporter.
processor = BatchSpanProcessor(ConsoleSpanExporter())
# Register the processor with the provider.
provider.add_span_processor(processor)
# Set the provider as the global trace provider.
trace.set_tracer_provider(provider)
# Create a tracer object.
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


@app.route("/roll")
def roll():
    # Create a span with the name 'server_request' and set it as the current span. We also set an attribute on the span
    # start_as_current_span is the context manager for creating a new span, and setting it as the current span in this
    # tracer's context. Exiting the context manager will call the span's end method, as well as return the current span
    # to its previous value by returning to the previous context.
    with tracer.start_as_current_span("server_request",
                                      attributes={"endpoint": "/roll"}):
        sides = int(request.args.get('sides'))
        rolls = int(request.args.get('rolls'))
        return roll_sum(sides, rolls)


def roll_sum(sides, rolls):
    # Retrieve the current span from the tracer's context.
    span = trace.get_current_span()
    sum = 0
    for r in range(0, rolls):
        result = randint(1, sides)
        # Add an event to the current span to provide additional information.
        span.add_event("log", {
            "roll.sides": sides,
            "roll.result": result,
            })
        sum += result
    return str(sum)
