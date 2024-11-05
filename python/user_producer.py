#!/usr/bin/env python

# based on https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/avro_producer.py
import os
from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

topic = 'users'

class User(object):
    def __init__(self, name, lastName):
        self.name = name
        self.lastName = lastName

def user_to_dict(user, ctx):
    """
    Returns a dict representation of a User instance for serialization.

    Args:
        user (User): User instance.

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.

    Returns:
        dict: Dict populated with user attributes to be serialized.
    """

    # User._address must not be serialized; omit from dict
    return dict(name=user.name,
                lastName=user.lastName)

path = os.path.realpath(os.path.dirname(__file__))
with open(f"{path}/avro/user.avsc") as f:
    schema_str = f.read()

schema_registry_client = SchemaRegistryClient({'url': 'http://localhost:8081'})
avro_serializer = AvroSerializer(schema_registry_client,
                                 schema_str,
                                 user_to_dict)
string_serializer = StringSerializer('utf_8')


producer = Producer({'bootstrap.servers': 'localhost:19092',
                     'client.id': 'client-python'})

print("Producing user records to topic {}. ^C to exit.".format(topic))
user = User(name='python 1',
            lastName='Doe')
producer.produce(topic=topic,
                key=string_serializer(str(uuid4())),
                value=avro_serializer(user, SerializationContext(topic, MessageField.VALUE)))

print("User name {}, lastName {}".format(user.name, user.lastName)) 

user = User(name='python 2',
            lastName='Doe')
producer.produce(topic=topic,
                key=string_serializer(str(uuid4())),
                value=avro_serializer(user, SerializationContext(topic, MessageField.VALUE)))

print("User name {}, lastName {}".format(user.name, user.lastName)) 
print("\nFlushing records...")
producer.flush()
