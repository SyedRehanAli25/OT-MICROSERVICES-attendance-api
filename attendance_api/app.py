"""
Module for calling the main flask application.
The application will be only supported with Flask and Gunicorn.
"""
from flask import Flask, json
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics

# Updated imports for the package structure
from attendance_api.router.attendance import route as create_record
from attendance_api.router.cache import cache
from attendance_api.utils.json_encoder import DataclassJSONEncoder
from attendance_api.client.redis.redis_conn import get_caching_data

app = Flask(__name__)

swagger = Swagger(app)

metrics = PrometheusMetrics(app)
metrics.info("attendance_api", "Attendance API opentelemetry metrics", version="0.1.0")

cache.init_app(app, get_caching_data())

app.config['JSON_SORT_KEYS'] = False
json.provider.DefaultJSONProvider.sort_keys = False
app.json_encoder = DataclassJSONEncoder

app.register_blueprint(create_record, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
