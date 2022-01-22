import json
from discord.errors import Forbidden

def save_or_check_user_info(user):
    file = open('user_info.json','r+')
    try:
        user_id = json.loads(file.read())
    except:
        user_id={}
    file.close()
    if str(user.id) in user_id.keys():
        file.close()
        return user_id[str(user.id)]
    try:
        user_info = {}
        user_info['guild'] = user.guild.name
        user_info['name'] = user._user.name
        user_info['avatar'] = user._user.avatar
        user_info['bot'] = user._user.bot
        user_info['system'] = user._user.system
        user_id[str(user.id)]=user_info
        file = open('user_info.json','w')
        file.seek(0)
        json.dump(user_id,file)
        file.close()
        return user_id[user.id]
    except:return False

def save_user(user,id):
    try:
        file = open('user_info.json','r+')
        user_id = json.loads(file.read())
        user_id[str(id)]=user
        file.seek(0)
        file.write(json.dumps(user_id))
        file.close()
        return True
    except Exception as error:
        print("save_user_error=>",error)
        return False

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