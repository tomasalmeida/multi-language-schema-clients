# Start the docker environment

```shell
    cd env
    docker compose up -d
    cd ..
```

# Register the schema and create the topic

```shell
    cd env
    # Create the test-topics
    docker compose exec kafka kafka-topics --bootstrap-server kafka:9092 --topic users --create --partitions 1 --replication-factor 1

    cd ..
    #create the schema
    jq -n --rawfile schema java/src/main/resources/avro/user.avsc  '{schema: $schema}' | \
    curl --silent http://localhost:8081/subjects/users-value/versions --json @- | jq
```

# Run the java clients

```shell
    cd java
    mvn clean package 

    # run producer
     java -classpath target/multiclient-1.0.0-SNAPSHOT-jar-with-dependencies.jar com.demo.UserProducer

    # run consumer
     java -classpath target/multiclient-1.0.0-SNAPSHOT-jar-with-dependencies.jar com.demo.UserConsumer
     
     cd .. 
```

# Run the python clients

```shell
    cd python
    pip install virtualenv
    virtualenv kafka-env
    source kafka-env/bin/activate
    pip install confluent-kafka
    pip install requests
    pip install fastavro

    # run producer
    python3 user_producer.py

    #run consumer
    python3 user_consumer.py
    cd ..
```

# shutdown

```shell
    cd env
    docker compose down -v
    cd ..
```

# NOTE: 

## auto commit is disabled, so you can re run consumers to get all events

## Control center is available in http://localhost:9021/
