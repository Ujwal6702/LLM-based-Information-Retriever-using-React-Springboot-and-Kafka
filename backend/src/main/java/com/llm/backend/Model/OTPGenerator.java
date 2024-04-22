package com.llm.backend.Model;
import java.util.Random;
import java.security.SecureRandom;


public class OTPGenerator {
    private String CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    private int OTP_LENGTH = 6;
    private int ALPHANUMERIC_LENGTH = 32;
    private Random random = new SecureRandom();

    public String generateOTP() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < OTP_LENGTH; i++) {
            sb.append(random.nextInt(10));
        }
        return sb.toString();
    }

    public String generateAlphanumeric() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ALPHANUMERIC_LENGTH; i++) {
            int randomIndex = random.nextInt(CHARS.length());
            sb.append(CHARS.charAt(randomIndex));
        }
        return sb.toString();
    }
}
