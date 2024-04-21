package com.llm.backend.Controller;


import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import com.llm.backend.Model.User;
import com.llm.backend.Model.EnvData;
import java.util.*;
import com.llm.backend.Model.ConnectSQL;
import java.sql.Statement;


@RestController
public class Controller {
    /*@PostMapping("/register")
    public String (@RequestBody  entit y) {
        TODO: process POST request
        
        return entity;
    }*/

    public static void main(String[] args){
        EnvData envData = new EnvData();
        envData.loadDataFromEnvFile();
        Map<String, String> data = envData.getData();
        ConnectSQL connectSQl = new ConnectSQL(
            data.get("SQL_HOST"),
            data.get("SQL_USERNAME"),
            data.get("SQL_PASSWORD"),
            data.get("SQL_PORT")
        );
        connectSQl.initiateConnection();
        connectSQl.closeConnection();

    }

    

}
