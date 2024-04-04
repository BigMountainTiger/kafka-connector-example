package com.song.example;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;

import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.sink.SinkRecord;
import org.apache.kafka.connect.sink.SinkTask;
import org.slf4j.Logger;

public class PostgresSinkTask extends SinkTask {
    private final static Logger log = ConsoleLogger.log;
    private SQLSinker sinker;
    private Map<String, String> props;

    @Override
    public String version() {
        log.info("PostgresSinkTask - Calling version()");
        return "1.0";
    }

    @Override
    public void put(Collection<SinkRecord> records) {
        log.info("PostgresSinkTask - Calling put()");

        this.sinker.unloadBatch();
        var upsert_sql = props.get("upsert_sql");
        var upsert_fields = props.get("upsert_fields").split("\\|");
        var delete_sql = props.get("delete_sql");
        var delete_fields = props.get("delete_fields").split("\\|");

        for (SinkRecord record : records) {
            var values = (Struct) record.value();
            var operation = values.getString("operation");

            String sql;
            var entries = new ArrayList<>();
            if ("DELETE".equals(operation)) {
                sql = delete_sql;
                for (var e : delete_fields) {
                    entries.add(values.getString(e));
                }
            } else {
                sql = upsert_sql;
                for (var e : upsert_fields) {
                    entries.add(values.getString(e));
                }
            }

            this.sinker.put(sql, entries.toArray());
        }

        try {
            this.sinker.flush();
        } catch (SQLException e) {
            log.info("PostgresSinkTask - put(), failed to flush");
            throw new org.apache.kafka.connect.errors.DataException(e.getMessage());
        }
    }

    @Override
    public void flush(Map<TopicPartition, OffsetAndMetadata> currentOffsets) {
        log.info("PostgresSinkTask - Calling flush()");
    }

    @Override
    public void start(Map<String, String> props) {
        log.info("PostgresSinkTask - Calling start()");

        this.props = props;
        for (var e : props.entrySet()) {
            log.info(e.getKey() + " - " + e.getValue());
        }

        var url = "jdbc:postgresql://host.docker.internal:5432/postgres";
        this.sinker = new SQLSinker(url, "postgres", "docker");
    }

    @Override
    public void stop() {
        log.info("PostgresSinkTask - Calling stop()");
    }

}
