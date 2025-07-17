# consumer/gps_consumer.py
import json
from kafka import KafkaConsumer

# ✅ Store the latest GPS positions for each car
latest_positions = {}

def start_consumer():
    consumer = KafkaConsumer(
        "gps-coordinates",                   # topic name
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",        # read from beginning
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("✅ Kafka Consumer started... listening for GPS data...")

    for message in consumer:
        gps_data = message.value
        car_id = gps_data["car_id"]
        latest_positions[car_id] = gps_data

        # ✅ Print log for debugging
        print(f"📡 Received → {car_id}: {gps_data['lat']:.6f}, {gps_data['lon']:.6f} at {gps_data['timestamp']}")

