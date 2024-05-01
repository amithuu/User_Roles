import mailtrap

from django.http.response import HttpResponse


def simple(request, data):
    mail = mailtrap.Mail(
        sender = mailtrap.Address(email = 'django@mailtrap.club', name = 'MailTrap test'),
        to = [mailtrap.Address(email = 'amithkulkarni99@gmail.com')],
        subject = 'Login Credentials',
        text = data,
    )
    
    client = mailtrap.MailTrapCLient(token = 'c5426bf29fdebf2d744c8520d9d2a724')
    client.send(mail)
    return HttpResponse('Message Sent!')