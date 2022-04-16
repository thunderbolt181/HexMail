import json
import os
from typing import Optional
import discord
from discord import ui
from gmail.gmail_cmnds import service
from extra_functions import create_message

class ComposeEmailModel(ui.Modal):
    From = ui.TextInput(label="From")
    To = ui.TextInput(label='To')
    Subject = ui.TextInput(label='Subject', style=discord.TextStyle.short)
    Body = ui.TextInput(label='Body', style=discord.TextStyle.paragraph)

    def __init__(self, user, title: str = "Compose Email", timeout: Optional[float] = None, custom_id: str = os.urandom(16).hex()) -> None:
        self.user = user
        super().__init__(title=title, timeout = timeout, custom_id = custom_id)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        raw_message = create_message(self.From._value,self.To._value,self.Subject._value,self.Body._value)
        token = json.loads(self.user['token'].replace("'",'"'))
        service_obj = service(token)
        service_obj.send_message(raw_message)
        await interaction.response.send_message(f'An email is sent:\nFrom :{self.From}\nTo:{self.To}', ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f'There is something wrong with the form Please try again!')
        print("Error in Compose Email Model: ",error)
        return await super().on_error(error, interaction)