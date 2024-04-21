package com.llm.backend.Model;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class ConnectSQL {
    String host;
    String user;
    String password;
    String port;

    Connection connect = null;
    public ConnectSQL(String host, String user, String password, String port) {
        this.host = host;
        this.user = user;
        this.password = password;
        this.port = port;
    }

    public void initiateConnection() {
        try {
            this.connect = DriverManager.getConnection(
                "jdbc:mysql://" + host + ":" + port + "/LLMDB",
                user,
                password
            );
            this.connect.setAutoCommit(true);
            System.out.println("Connection to database established.");
        } catch (SQLException e) {
            System.out.println("Failed to create database: " + e.getMessage());
        }
    }

    public Statement getStatement(){
        try {
            return connect.createStatement();
        } catch (SQLException e) {
            System.out.println("Failed to create statement: " + e.getMessage());
            return null;
        }
    }

    public void closeConnection() {
        try {
            System.out.println("Closing connection to database.");
            connect.close();
        } catch (SQLException e) {
            System.out.println("Failed to close connection: " + e.getMessage());
        }
    }

    public void closeStatement(Statement statement) {
        try {
            statement.close();
        } catch (SQLException e) {
            System.out.println("Failed to close statement: " + e.getMessage());
        }
    }

}
