from datetime import datetime, timedelta
import googlemaps
from email.message import EmailMessage
import ssl
import smtplib
def get_commute_duration(home_address, work_address, google_maps_api_key):
    #Set Google api key in Google Maps
    gmaps = googlemaps.Client(key = google_maps_api_key)

    #Set direction
    directions = gmaps.directions(home_address, work_address)#Create directions object
    first_leg = directions[0]["legs"][0]#Create the starting point
    durationstring = first_leg["duration"]["text"]#Get the time to get to the worklocation
    duration = int("".join(filter(str.isdigit, durationstring)))#change the time to integer for easier calculation
    return durationstring, duration

def send_text_message(message, email_account, email_password, receiver_number):
    #Set emails for both sender and receiver
    sender = email_account
    receiver = receiver_number
    
    #Create email object
    em = EmailMessage()
    em["From"] = sender#the email sender
    em["To"] = receiver#the email receiver
    em.set_content(message)#Add the email content to send
    
    #Create secure socket layer
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:#Access to gmail email server (Can change to other email provider's server)
        smtp.login(email_account, email_password)#Login to gmail email account
        smtp.sendmail(sender, receiver, em.as_string())#send the email

def main():
    #Set email account and password
    email_account = "Enter email account"
    email_password = "Enter email google app password"#This has to be Google App Password
    #Set email address of the phone number
    receiver_number = "Enter email address of the phone number"#This will text message to the phone number
    #Set home and work address
    home_address = "Enter home address"
    work_address = "Enter work address"
    #Get Google Maps api key
    google_maps_api_key = "Enter Google Maps api key"

    #Find duration
    durationstring, duration = get_commute_duration(home_address, work_address, google_maps_api_key)
    #Define time delta representing the minutes
    duration = timedelta(minutes=duration)
    
    #Find current time
    now = datetime.now()
    #Find arrive time
    arrival_time = (now + duration).strftime("%I:%M %p")

    #Set text message
    message = (
    f"Good Morning.\n\n"   
    f"Estimate commute time from home to work at 9am: {durationstring}.\n\n"
    f"Leave now for work at 9am to arrive at approximately {arrival_time}.\n"   
    )

    #Send text message
    send_text_message(message, email_account, email_password, receiver_number)

if __name__ == "__main__":
    main()