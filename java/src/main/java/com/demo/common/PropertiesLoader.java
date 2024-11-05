package com.demo.common;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Properties;

public class PropertiesLoader {

    private static final String PATH = "src/main/resources/client.properties";

    public static Properties load() throws IOException {


        if (!Files.exists(Paths.get(PATH))) {
            throw new IOException(PATH + " not found.");
        }
        final Properties cfg = new Properties();
        try (final InputStream inputStream = new FileInputStream(PATH)) {
            cfg.load(inputStream);
        }
        return cfg;
    }
}
