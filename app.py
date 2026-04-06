import os
import redis
from flask import Flask

app = Flask(__name__)

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)

def get_hit_count():
    try:
        return cache.incr("hits")
    except redis.exceptions.ConnectionError:
        return "Redis not ready yet"

@app.route("/")
def hello():
    count = get_hit_count()
    return f"Hello from Docker! This page has been viewed {count} times.\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
