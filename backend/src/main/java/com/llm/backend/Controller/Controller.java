package com.llm.backend.Controller;


import java.util.HashMap;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import com.llm.backend.Model.ConnectSQL;
import com.llm.backend.Model.EnvData;
import com.llm.backend.Model.SendMail;
import com.llm.backend.Model.OTPGenerator;
import com.llm.backend.Model.UserData;





@CrossOrigin("*")
@RestController
public class Controller {

    static Map<String, String> data;
    static HashMap<Integer, String> ids ;
    static int reqId;
    static HashMap<Integer, UserData> users;

    static{
        EnvData envData = new EnvData();
        envData.loadDataFromEnvFile();
        data = envData.getData();
        ids = new HashMap<>();
        reqId = 0;
        users = new HashMap<>();
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
        reqId++;
        OTPGenerator otpGenerator = new OTPGenerator();
        String otp = otpGenerator.generateOTP();
        ids.put(reqId, otp);
        users.put(reqId, userData);
        String mailBody = "Dear "+name+",\n\n Thank you for using our service. Here is your One Time Password (OTP): \n\n OTP: "+otp+"\n\n  Please do not share this OTP with anyone. Our team will never ask for your OTP.\n\n If you didn't request this OTP, please ignore this email.\n\n Best regards,\n\n Your Team";
        SendMail sendMail = new SendMail(
            data.get("MAIL"),
            data.get("APP_PASSWORD")
        );
        sendMail.send(email, "One Time Password (OTP)", mailBody);
        return ResponseEntity.ok().body(Map.of("message", "OTP sent successfully", "request_id", reqId));

    }

    @PostMapping("/otp")
    public ResponseEntity<?> otp(@RequestBody Map<String, String> body) {
        int requestId = Integer.parseInt(body.get("requestId"));
        if (!ids.containsKey(requestId)) {
            return ResponseEntity.badRequest().body("RequestId is invalid");
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
        else if(!ids.get(requestId).equals(otp)){
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
            state.executeUpdate("Insert into users (email, password, name, auth) values ('"+users.get(requestId).email+"', '"+users.get(requestId).password+"', '"+users.get(requestId).name+"' , '"+auth+"')");
            connectSQL.closeStatement(state);
            connectSQL.closeConnection();
        } catch (SQLException e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body("An error occurred while updating User Details.");
        }
        ids.remove(requestId);
        users.remove(requestId);
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

}



