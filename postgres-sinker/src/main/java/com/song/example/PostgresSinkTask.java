package com.song.example;

import java.util.Collection;
import java.util.Map;

import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.sink.SinkRecord;
import org.apache.kafka.connect.sink.SinkTask;
import org.slf4j.Logger;

@SuppressWarnings("unused")
public class PostgresSinkTask extends SinkTask {
    private final static Logger log = ConsoleLogger.log;
    private Map<String, String> props;

    @Override
    public String version() {
        log.info("PostgresSinkTask - Calling version()");
        return "1.0";
    }

    @Override
    public void put(Collection<SinkRecord> records) {
        log.info("PostgresSinkTask - Calling put()");
        for (SinkRecord record : records) {
            log.info("------------------ new record ------------------");

            log.info(record.toString());

            var fields = record.valueSchema().fields();
            log.info(fields.toString());

            var values = (Struct)record.value();
            log.info(values.toString());
            log.info("");
        }

        // log.info("Throwing exception in put");
        // Even with an exception in the put(), the flush() is still called. The document does not say if the offset will be committed
        // For safety, we need to make sure the flush() will throw error if put() fails, so the offset is not committed
        // throw new org.apache.kafka.connect.errors.DataException("Artificial Exception in put");
    }

    @Override
    public void flush(Map<TopicPartition, OffsetAndMetadata> currentOffsets) {
        log.info("PostgresSinkTask - Calling flush()");

        // log.info("Throwing exception in flush");
        // throw new org.apache.kafka.connect.errors.DataException("Artificial Exception in flush");
    }

    @Override
    public void start(Map<String, String> props) {
        log.info("PostgresSinkTask - Calling start()");

        this.props = props;
        for (var e : props.entrySet()) {
            log.info(e.getKey() + " - " + e.getValue());
        }
    }

    @Override
    public void stop() {
        log.info("PostgresSinkTask - Calling stop()");
    }

}
