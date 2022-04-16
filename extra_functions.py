import base64
from email.mime.text import MIMEText
import json
from discord.errors import Forbidden
import re
import html2text

def parse_mail(payld):
    if 'parts' in payld.keys():
        mssg_parts = payld['parts'] # fetching the message parts
        part_one  = mssg_parts[0] # fetching first element of the part
        part_body = part_one['body'] # fetching body of the message
    else:
        part_body = payld['body']
    part_data = part_body['data'] # fetching data from the body
    clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
    clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
    mail = clean_one.encode('utf-8')
    mail = base64.b64decode(mail)
    mail = mail.decode('utf-8')
    h = html2text.HTML2Text()
    h.ignore_links=False
    h.ignore_images=True
    h.ignore_tables=False
    mail = h.handle(mail)
    mail = re.sub('\n\n\n+',"\n",str(mail))
    mail = re.sub('   +',' ',mail)
    return mail

async def check_user(ctx,user,new_auth=False):
    if user:
        if user['token']!=None or new_auth:
            return True
        else:await ctx.channel.send("You are not authorized. Please send '.new_auth' to start the process of authorization")
    else:await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authorization.")
    return False

async def longer_msg(ctx,msg):
    j=0
    i=2000
    while True:
        while msg[i]!=" ":
            i-=1
        else:
            await ctx.channel.send(msg[j:i])
        j=i
        if i+2000<len(msg):i+=2000
        else:
            await ctx.channel.send(msg[j:])
            break

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['From'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information about missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)