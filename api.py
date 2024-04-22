from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp
from pydantic import BaseModel
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySqL@123",
    database="NexGenDB"
)


cursor = connection.cursor()

class UserRegistration(BaseModel):
    email: str
    name: str
    password: str


def generateAuthenticationKey():
    return pyotp.random_base32()



def sendMail(mail, subject, body):
    try:
        sender_email = "nexgenhackathon@gmail.com"
        receiver_email = mail
        password = "ivco skca aznw dgvs"  

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except:
        return False

reqid = [0]
ids = {}
verify_data = {}
origins = [
    "http://localhost",
    "http://localhost:8080",  # Add your frontend URL here
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:3001",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



def otpMail(mail, name, password):
    cursor.execute("SELECT * FROM users WHERE email = %s", (mail,))
    result = cursor.fetchone()
    if result:
        raise HTTPException(status_code=400, detail="Email already exists")
    reqid[0] += 1
    totp = pyotp.TOTP(generateAuthenticationKey(), interval=300)
    body = f"""
        Dear {name},

        Thank you for using our service. Here is your One Time Password (OTP):

        OTP: {totp.now()}

        Please do not share this OTP with anyone. Our team will never ask for your OTP.

        If you didn't request this OTP, please ignore this email.

        Best regards,
        Your Team
        """
    ids[reqid[0]] = totp
    if sendMail(mail, "One Time Password (OTP) for NexGen Hackathon", body):
        verify_data[reqid[0]] = [mail, name, password]
        print(ids)
        print(verify_data)
        return {"message": "OTP sent successfully", "request_id": reqid[0]}
    else:
        return {"message": "Failed to send OTP", "request_id": None}


app = FastAPI()





@app.post("/register/")
async def register(user_data: UserRegistration):
    email = user_data.email
    name = user_data.name
    password = user_data.password

    if not (email and name and password):
        raise HTTPException(status_code=400, detail="Email, name, and password are required.")

    return otpMail(email, name, password)


class verify(BaseModel):
    requestId: int
    otp: str


@app.post("/verify/")
async def register(verify_val: verify):
    if verify_val.requestId not in ids:
        raise HTTPException(status_code=400, detail="Invalid request ID")
        
    else:
        if ids[verify_val.requestId].verify(verify_val.otp):
            curr = generateAuthenticationKey()
            cursor.execute('INSERT INTO users (name, email, password, auth) VALUES (%s, %s, %s, %s)', (verify_data[verify_val.requestId][1], verify_data[verify_val.requestId][0], verify_data[verify_val.requestId][2], curr))
            connection.commit()     
            return {"message": curr}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP")
class login(BaseModel):
    email: str
    password: str

@app.post("/login/")
async def login(user_data: login):
    email = user_data.email
    password = user_data.password

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    print(result)
    print(password)
    if not result:
        raise HTTPException(status_code=400, detail="User not found")
    if result[3] != password:
        raise HTTPException(status_code=400, detail="Invalid password")
    return {"message": result[4]}

class access(BaseModel):
    email: str
    auth: str

@app.post("/chathistory/")
async def getChatHistory(user_data: access):
    email = user_data.email
    auth = user_data.auth

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    print(result)
    if not result:
        raise HTTPException(status_code=400, detail="User not found")
    if result[4] != auth:
        raise HTTPException(status_code=400, detail="Invalid auth")
    cursor.execute("SELECT * FROM chat_history WHERE user_id=%s", (result[0],))
    result = cursor.fetchall()
    if result:
        return {"message": result}
    else:
        return {"message": "No chat history found"}


