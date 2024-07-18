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
public class BasicSinkTask extends SinkTask {
    private final static Logger log = ConsoleLogger.log;
    private Map<String, String> props;

    @Override
    public String version() {
        log.info("BasicSinkTask - Calling version()");
        return "1.0";
    }

    @Override
    public void put(Collection<SinkRecord> records) {
        log.info("BasicSinkTask - Calling put()");
        log.info("No. of records in a single put() call: " + records.size());
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
        // For safety, we need to make sure the flush() will throw error if put() fails, so the offset is not committed (for absolute certainty?)

        // After testing, it is found that if Non-RetriableException thrown the offsets will not be committed, even though the flush method is still called.
        // throw new org.apache.kafka.connect.errors.DataException("Artificial Exception in put");

        // If RetriableException, put will keep retrying without committing the offset
        // throw new org.apache.kafka.connect.errors.RetriableException("Artificial Exception in put");
    }

    @Override
    public void flush(Map<TopicPartition, OffsetAndMetadata> currentOffsets) {
        log.info("BasicSinkTask - Calling flush()");

        // log.info("Throwing exception in flush");
        // throw new org.apache.kafka.connect.errors.DataException("Artificial Exception in flush");
    }

    @Override
    public void start(Map<String, String> props) {
        log.info("BasicSinkTask - Calling start()");

        this.props = props;
        for (var e : props.entrySet()) {
            log.info(e.getKey() + " - " + e.getValue());
        }
    }

    @Override
    public void stop() {
        log.info("BasicSinkTask - Calling stop()");
    }

}
