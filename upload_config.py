import redis
import argparse
import json

parser = argparse.ArgumentParser(description="Upload config to redis")
parser.add_argument("--file", default="config.json", help="Configuration file")
parser.add_argument("--host", type=str, required=True, help="Redis host")

args = parser.parse_args()
print(args.file)
print(args.host)

configuration = args.file

with open(configuration, "r") as conf:
    configuration_data = json.load(conf)


r = redis.StrictRedis(host=args.host, port=6379, db=0)
r.set("config", json.dumps(configuration_data))

print("Configuration uploaded to redis")
