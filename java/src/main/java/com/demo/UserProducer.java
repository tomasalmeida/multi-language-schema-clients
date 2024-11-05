package com.demo;

import com.demo.common.PropertiesLoader;
import com.demo.model.User;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Properties;

public class UserProducer {

    public static final String TOPIC_USERS = "users";

    public static final Logger LOGGER = LoggerFactory.getLogger(UserProducer.class);

    public static void main(String[] args) throws Exception {
        Properties properties = PropertiesLoader.load();
        KafkaProducer<String, User> producer = new KafkaProducer<>(properties);

        ProducerRecord<String, User> userRecord;

        userRecord = new ProducerRecord<>(TOPIC_USERS, new User("java 1", "Doe 1"));
        producer.send(userRecord);
        LOGGER.info("User sent: {}", userRecord.value());

        userRecord = new ProducerRecord<>(TOPIC_USERS, new User("java 2", "Doe 2"));
        producer.send(userRecord);
        LOGGER.info("User sent: {}", userRecord.value());

        producer.close();
    }
}
 