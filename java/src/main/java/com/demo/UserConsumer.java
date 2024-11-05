package com.demo;

import com.demo.common.PropertiesLoader;
import com.demo.model.User;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

import static com.demo.UserProducer.TOPIC_USERS;

public class UserConsumer  {

    public static final Logger LOGGER = LoggerFactory.getLogger(UserConsumer.class);

    public static void main(String[] args) throws Exception {


        Properties properties = PropertiesLoader.load();
        KafkaConsumer<String, User> consumer = new KafkaConsumer<>(properties);

        LOGGER.info("Starting consumer...");
        try (consumer) {
            consumer.subscribe(Collections.singletonList(TOPIC_USERS));
            while (true) {
                ConsumerRecords<String, User> records = consumer.poll(Duration.ofMillis(1000));
                for (ConsumerRecord<String, User> record : records) {
                    LOGGER.info("User: {}", record.value());
                }
            }
        }
    }
}
