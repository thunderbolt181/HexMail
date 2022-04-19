async def fetch_users_from_discord_id(bot,user):
    user_info = await bot.db.fetchrow("""
        SELECT * FROM users 
        LEFT OUTER JOIN user_token ON (users.discord_id = user_token.fk_user) 
        WHERE users.discord_id = $1;
    """,str(user.id))
    if user_info is None:
        return False
    return user_info

async def fetch_users_from_email(bot,email):
    user_info = await bot.db.fetchrow("""
        SELECT * FROM user_token 
        RIGHT OUTER JOIN users ON (user_token.fk_user = users.discord_id)
        WHERE user_token.email = $1;
    """,str(email))
    if user_info is None:
        return False
    return user_info

async def update_history_id(bot,data):
    await bot.db.execute("""
        UPDATE user_token
        SET history_id = $1
        WHERE email = $2;
        """,int(data['historyId']),data['emailAddress'])

async def fetch_from_user_token(bot,email):
    user_info = await bot.db.execute("""
        SELECT * FROM user_token
        WHERE email=$1;
        """,email)
    if user_info is None:
        return False
    return user_info

async def delete_user_token(bot,email):
    user_info = await bot.db.execute("""
            DELETE FROM user_token
            WHERE email=$1;
            """,email)
    if user_info is None:return False
    else:return True