package com.llm.backend.Controller;


import java.util.HashMap;
import java.util.Map;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import com.llm.backend.Model.ConnectSQL;
import com.llm.backend.Model.EnvData;
import com.llm.backend.Model.SendMail;
import com.llm.backend.Model.OTPGenerator;
import com.llm.backend.Model.UserData;





@Configuration
@RestController
public class Controller {

    static Map<String, String> data;
    static HashMap<String, String> ids ;
    static HashMap<String, UserData> users;

    static{
        EnvData envData = new EnvData();
        envData.loadDataFromEnvFile();
        data = envData.getData();
        ids = new HashMap<>();
        users = new HashMap<>();
    }


    @Bean
    public WebMvcConfigurer configure() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry){
                registry.addMapping("/**").allowedOrigins("http://localhost:3000", "https://localhost:3000", "http://127.0.0.1:3000", "http://127.0.0.1:3000")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*");
            }
        };
    }


    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody Map<String, String> body){
        String email = body.get("email");
        String password = body.get("password");
        String name = body.get("name");
        UserData userData = new UserData(email, password, name);
        if (email == null || name == null || password == null) {
            return ResponseEntity.badRequest().body("Email, name, and password are required.");
        }
        ConnectSQL connectSQL = new ConnectSQL(
            data.get("SQL_HOST"),
            data.get("SQL_USERNAME"),
            data.get("SQL_PASSWORD"),
            data.get("SQL_PORT")
        );
        connectSQL.initiateConnection();
        try{
            Statement state = connectSQL.getStatement();
            ResultSet rs = state.executeQuery("select * from users where email = '" + email+"'");
            if (rs.next()) {
                connectSQL.closeStatement(state);
                connectSQL.closeConnection();
                return ResponseEntity.badRequest().body("Email already exists.");
            }
        } catch (SQLException e) {
            // Handle the SQLException
            e.printStackTrace();
            return ResponseEntity.badRequest().body("An error occurred while checking for existing email.");
        }
        connectSQL.closeConnection();
        OTPGenerator otpGenerator = new OTPGenerator();
        String otp = otpGenerator.generateOTP();
        ids.put(email, otp);
        users.put(email, userData);
        String mailBody = "Dear "+name+",\n\n Thank you for using our service. Here is your One Time Password (OTP): \n\n OTP: "+otp+"\n\n  Please do not share this OTP with anyone. Our team will never ask for your OTP.\n\n If you didn't request this OTP, please ignore this email.\n\n Best regards,\n\n Your Team";
        SendMail sendMail = new SendMail(
            data.get("MAIL"),
            data.get("APP_PASSWORD")
        );
        sendMail.send(email, "One Time Password (OTP)", mailBody);
        return ResponseEntity.ok().body(Map.of("message", "OTP sent successfully", "request_id", email));

    }

    @PostMapping("/otp")
    public ResponseEntity<?> otp(@RequestBody Map<String, String> body) {
        String email = body.get("requestId");
        if (!ids.containsKey(email)) {
            return ResponseEntity.badRequest().body("email is invalid");
        }
        String otp = body.get("otp");
        if (otp == null) {
            return ResponseEntity.badRequest().body("OTP is required.");
        }
        else if(otp.length() != 6){
            return ResponseEntity.badRequest().body("OTP should be 6 characters long.");
        }
        else if(!otp.matches("[0-9]+")){
            return ResponseEntity.badRequest().body("OTP should contain only numbers.");
        }
        else if(!ids.get(email).equals(otp)){
            return ResponseEntity.badRequest().body("Invalid OTP.");
        }
        OTPGenerator otpGenerator = new OTPGenerator();
        String auth = otpGenerator.generateAlphanumeric();


        ConnectSQL connectSQL = new ConnectSQL(
            data.get("SQL_HOST"),
            data.get("SQL_USERNAME"),
            data.get("SQL_PASSWORD"),
            data.get("SQL_PORT")
        );
        connectSQL.initiateConnection();
        try{
            Statement state = connectSQL.getStatement();
            state.executeUpdate("Insert into users (email, password, name, auth) values ('"+users.get(email).email+"', '"+users.get(email).password+"', '"+users.get(email).name+"' , '"+auth+"')");
            connectSQL.closeStatement(state);
            connectSQL.closeConnection();
        } catch (SQLException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body("An error occurred while updating User Details.");
        }
        ids.remove(email);
        users.remove(email);
        return ResponseEntity.ok().body(Map.of("message", auth));

    }
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> body) {
        String email = body.get("email");
        String password = body.get("password");
        if (email == null || password == null) {
            return ResponseEntity.badRequest().body("Email and password are required.");
        }
        ConnectSQL connectSQL = new ConnectSQL(
            data.get("SQL_HOST"),
            data.get("SQL_USERNAME"),
            data.get("SQL_PASSWORD"),
            data.get("SQL_PORT")
        );
        connectSQL.initiateConnection();
        try{
            Statement state = connectSQL.getStatement();
            ResultSet rs = state.executeQuery("select * from users where email = '" + email+"'");
            if (!rs.next()) {
                connectSQL.closeStatement(state);
                connectSQL.closeConnection();
                return ResponseEntity.badRequest().body("Email does not exist.");
            }
            if (!rs.getString("password").equals(password)) {
                connectSQL.closeStatement(state);
                connectSQL.closeConnection();
                return ResponseEntity.badRequest().body("Invalid password.");
            }
            String auth = rs.getString("auth");
            connectSQL.closeStatement(state);
            connectSQL.closeConnection();
            return ResponseEntity.ok().body(Map.of("message", "Login successful", "auth", auth));
        } catch (SQLException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body("An error occurred while checking for existing email.");
        }
    }

    @PostMapping("/auth")
    public ResponseEntity<?> auth(@RequestBody Map<String, String> body) {
        String auth = body.get("auth");
        String email = body.get("email");
        if (auth == null || email == null) {
            return ResponseEntity.badRequest().body("Email and Auth is required.");
        }
        ConnectSQL connectSQL = new ConnectSQL(
            data.get("SQL_HOST"),
            data.get("SQL_USERNAME"),
            data.get("SQL_PASSWORD"),
            data.get("SQL_PORT")
        );
        connectSQL.initiateConnection();
        try{
            Statement state = connectSQL.getStatement();
            ResultSet rs = state.executeQuery("select * from users where email = '" + email+"'");
            if (!rs.next()) {
                connectSQL.closeStatement(state);
                connectSQL.closeConnection();
                return ResponseEntity.badRequest().body("Email does not exist.");
            }
            if (!rs.getString("auth").equals(auth)) {
                connectSQL.closeStatement(state);
                connectSQL.closeConnection();
                return ResponseEntity.badRequest().body("Invalid Auth.");
            }
            connectSQL.closeStatement(state);
            connectSQL.closeConnection();
            return ResponseEntity.ok().body(Map.of("message", "Auth successful"));
        } catch (SQLException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body("An error occurred while checking for existing email.");
        }
    }

}



