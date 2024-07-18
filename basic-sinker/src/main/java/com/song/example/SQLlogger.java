package com.song.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SQLlogger {
    private final static Logger log = LoggerFactory.getLogger(SQLlogger.class);

    static {
        try {
            Class.forName("org.postgresql.Driver");
        } catch (ClassNotFoundException e) {
            log.error(e.getMessage());
        }
    }

    private String url;
    private String username;
    private String password;

    public SQLlogger(String url, String username, String password) {
        this.url = url;
        this.username = username;
        this.password = password;
    }

    public void log(String message) {

        String sql = "call public.log_event(?);";

        try (Connection conn = DriverManager.getConnection(this.url, this.username, this.password)) {

            try (PreparedStatement preparedStatement = conn.prepareStatement(sql)) {
                preparedStatement.setString(1, message);
                preparedStatement.execute();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
