# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
sys.path.append("./")
sys.setrecursionlimit(10000000)
from kafka import KafkaProducer, KafkaConsumer
import json
from app.configs import kafka
from app.configs import admin

if admin.use_kafka is True:
    producer = KafkaProducer(bootstrap_servers=kafka.bootstrap_servers, compression_type='gzip')


def insert_message_to_kafka(key, msg):
    if not admin.use_kafka:
        return False

    if isinstance(key, str):
        key = key.encode()
    try:
        future = producer.send(topic=kafka.kafka_topic, key=key, value=json.dumps(msg).encode())
        # result = future.get(timeout=10)
        return future
    except Exception as e:
        print('发送失败: {}'.format(e))


kafka_offset_reset = 'earliest' #latest,earliest,none 首次拉取kafka订阅的模式

def get_message_from_kafka():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka')
    return consumer

def get_message_from_kafka_independent_listener():
    consumer=KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=admin.independent_listener_kafka_client_group_id,auto_offset_reset=kafka_offset_reset,client_id='get_message_from_kafka_independent_listener')
    return consumer

if __name__ == "__main__":
    future = insert_message_to_kafka(key='123231231', msg={'msg': 'test'})
    if future:
        result = future.get(timeout=10)
        print(result)