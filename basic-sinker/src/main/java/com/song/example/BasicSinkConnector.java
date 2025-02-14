package com.song.example;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.Task;
import org.apache.kafka.connect.sink.SinkConnector;
import org.slf4j.Logger;

public class BasicSinkConnector extends SinkConnector {
    private final static Logger log = ConsoleLogger.log;
    private Map<String, String> configProperties;

    @Override
    public String version() {
        log.info("BasicSinkConnector - Calling version()");

        return "1.0";
    }

    @Override
    public void start(Map<String, String> props) {
        log.info("BasicSinkConnector - Calling start()");

        configProperties = props;
    }

    @Override
    public Class<? extends Task> taskClass() {
        log.info("BasicSinkConnector - Calling taskClass()");

        return BasicSinkTask.class;
    }

    @Override
    public List<Map<String, String>> taskConfigs(int maxTasks) {
        log.info("BasicSinkConnector - Calling taskConfigs()");

        List<Map<String, String>> taskConfigs = new ArrayList<>();
        for (int i = 0; i < maxTasks; i++) {
            Map<String, String> taskProps = new HashMap<>();
            taskProps.putAll(configProperties);
            taskProps.put("task.id", Integer.toString(i));
            taskConfigs.add(taskProps);
        }

        return taskConfigs;
    }

    @Override
    public void stop() {
        log.info("BasicSinkConnector - Calling stop()");
    }

    @Override
    public ConfigDef config() {
        log.info("BasicSinkConnector - Calling config()");

        ConfigDef defs = new ConfigDef();
        return defs;
    }

}
