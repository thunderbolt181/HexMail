from gmail.gmail_cmnds import service
from database_functions import fetch_users_from_email,update_history_id
import json

async def get_history_list(data,bot):
    user = await fetch_users_from_email(bot,data['emailAddress'])
    try:
        if user['history_id'] is not None:
            await update_history_id(bot,data)
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            messages_list = history_list_parse(service_obj.history_list(user['history_id']))
            try:
                if len(messages_list)>0: 
                    await get_and_send_mail(messages_list,bot,service_obj,user)
            except Exception as e:
                pass
        else:await update_history_id(bot,data)
    except Exception as e:
        print("in get_history_list",e)

async def get_and_send_mail(messages_list,bot,service_obj,user):
    category = bot.get_channel(int(user['category_id']))
    for id,label in messages_list.items():
        mail_content = service_obj.get_message(id)
        message=''
        for i in mail_content.keys():
            message+=f"\n[{i}]: {mail_content[i]}"
        for text_channel in category.channels:
            if text_channel.name.upper() in label:
                await text_channel.send(f"```ini\n{message}```")

def history_list_parse(history_list):
    try:
        if len(history_list.keys())>0:
            if 'history' in history_list.keys():
                history = history_list['history']
                messages = {}
                for i in history:
                    try:
                        a=i['messagesAdded']
                        messages[a[0]["message"]['id']]=a[0]['message']['labelIds']
                    except Exception as e:
                        pass
                        # print("PushNotification Error:",e)
                return messages
    except:
        pass
    return None

async def main(data,bot):
    await get_history_list(data,bot)