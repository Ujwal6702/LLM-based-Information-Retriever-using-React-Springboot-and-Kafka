package com.llm.backend.Controller;


import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import com.llm.backend.Model.User;
import com.llm.backend.Model.EnvData;
import java.util.*;
import com.llm.backend.Model.ConnectSQL;
import java.sql.Statement;
import com.llm.backend.Model.SendMail;


@RestController
public class Controller {

    static Map<String, String> data;

    static{
        EnvData envData = new EnvData();
        envData.loadDataFromEnvFile();
        data = envData.getData();
    }

    /*@PostMapping("/register")
    public String (@RequestBody  entit y) {
        TODO: process POST request
        
        return entity;
    }*/

    public static void main(String[] args){
        
        /*ConnectSQL connectSQl = new ConnectSQL(
            data.get("SQL_HOST"),
            data.get("SQL_USERNAME"),
            data.get("SQL_PASSWORD"),
            data.get("SQL_PORT")
        );
        connectSQl.initiateConnection();
        connectSQl.closeConnection();*/
        SendMail sendMail = new SendMail(
            data.get("MAIL"),
            data.get("APP_PASSWORD")
        );
        sendMail.send("ujwalujwalc@gmail.com", "Test", "Test mail from LLM");


    }



    

}
