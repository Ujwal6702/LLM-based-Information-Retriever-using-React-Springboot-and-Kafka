package com.llm.backend.Model;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class EnvData {
    private HashMap<String, String> data;

    public EnvData() {
        this.data = new HashMap<>();
    }

    public void loadDataFromEnvFile() {
        String currentDirectory = System.getProperty("user.dir");
        Path parentDirectory = Paths.get(currentDirectory);
        Path envFilePath = parentDirectory.resolve(".env");
        if (Files.exists(envFilePath)) {
            try {
                Files.lines(envFilePath)
                        .map(line -> line.split("="))
                        .forEach(pair -> {
                            if (pair.length == 2) {
                                data.put(pair[0], pair[1]);
                            }
                        });
            } catch (IOException e) {
                e.printStackTrace(); 
            }
        } else {
            System.err.println(".env file not found in the parent directory.");
           
        }
    }

    public Map<String, String> getData() {
        return data;
    }

}