package com.song.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

// This class is not thread safe,
// because a Kafka connect task is running in a single thread
public class SQLSinker {
    private String url;
    private String username;
    private String password;
    List<String> sql_batch;

    public SQLSinker(String url, String username, String password) {
        this.sql_batch = new ArrayList<>();

        this.url = url;
        this.username = username;
        this.password = password;
    }

    public List<String> unloadBatch() {
        var batch = this.sql_batch;
        this.sql_batch = new ArrayList<>();

        return batch;
    }

    public int size() {
        return this.sql_batch.size();
    }

    public void put(String sql, Object[] data) {
        for (int i = 0; i < data.length; i++) {
            var v = data[i];
            data[i] = (v == null) ? "null" : (!(v instanceof String) ? v : "'" + ((String) v).replace("'", "''") + "'");
        }

        var cmd = String.format(sql, data);
        this.sql_batch.add(cmd);
    }

    public void flush() throws SQLException {
        var batch = this.unloadBatch();
        
        if (batch.isEmpty()) {
            return;
        }

        try (Connection conn = DriverManager.getConnection(this.url, this.username, this.password)) {
            // Make sure the statement is executed with a transaction
            conn.setAutoCommit(false);

            var sql = String.join(";\n", batch);
            try (PreparedStatement preparedStatement = conn.prepareStatement(sql)) {
                preparedStatement.execute();
                conn.commit();
            }
        }
    }
}
