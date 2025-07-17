import json, time, random
from kafka import KafkaProducer
from fetch_route import route_points  # ✅ we reuse the fetched points

KAFKA_BROKER = "localhost:9092"
TOPIC = "gps-coordinates"

# ✅ Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# ✅ Simulate 50 cars
cars = [f"car_{i}" for i in range(1, 51)]

print(f"🚗 Streaming {len(route_points)} GPS points for {len(cars)} cars...")

# ✅ Loop through route and send GPS updates
for idx, (lat, lon) in enumerate(route_points):
    for car in cars:
        gps_data = {
            "car_id": car,
            "lat": lat + random.uniform(-0.0001, 0.0001),  # small deviation
            "lon": lon + random.uniform(-0.0001, 0.0001),
            "timestamp": int(time.time())
        }
        producer.send(TOPIC, value=gps_data)

    print(f"[{idx+1}/{len(route_points)}] Sent GPS batch for all cars → {lat},{lon}")
    time.sleep(0.5)  # simulate delay for realism

producer.flush()
print("✅ Finished streaming GPS data!")
