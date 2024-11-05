#!/usr/bin/env python

# based on https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/avro_consumer.py
import os
from uuid import uuid4
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

topic = 'users'

class User(object):
    def __init__(self, name, lastName):
        self.name = name
        self.lastName = lastName

def dict_to_user(obj, ctx):
    """
    Converts object literal(dict) to a User instance.

    Args:
        obj (dict): Object literal(dict)

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    """

    if obj is None:
        return None

    return User(name=obj['name'],
                lastName=obj['lastName'])

path = os.path.realpath(os.path.dirname(__file__))
with open(f"{path}/avro/user.avsc") as f:
    schema_str = f.read()

schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081'})
avro_deserializer = AvroDeserializer(schema_registry_client,
                                     schema_str,
                                     dict_to_user)


consumer_conf = {'bootstrap.servers':'localhost:19092',
                    'group.id': 'client-python',
                    'auto.offset.reset': "earliest",
                    'enable.auto.commit': False}

consumer = Consumer(consumer_conf)
consumer.subscribe([topic])


while True:
    try:
        # SIGINT can't be handled when polling, limit timeout to 1 second.
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        user = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
        if user is not None:
            print("User record: name: {}, lastName: {}".format(user.name, user.lastName))
    except KeyboardInterrupt:
        break

consumer.close()