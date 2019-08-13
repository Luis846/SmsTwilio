from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC74597789a998d190319007e4bd2a36ad'
auth_token = '8102a60f2115a7a6cbf6ef740357a58c'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12053154250',
                     to='var'
                 )

print(message.sid)