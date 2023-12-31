import discord
from discord.ext import commands
from discord import app_commands
import sys
import dataHandler
import configs

loggingID = configs.loggingChannelID

sys.dont_write_bytecode = True

class userDeposit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="teller-user-deposit", description="Check the balance of your personal account")
    @app_commands.checks.has_role(configs.bankTellerID)
    async def userDeposit(self, interaction:discord.Interaction, user:discord.Member, diamondblocks:int, diamonds:int, iron:int):
        amount = 0
        db = await dataHandler.mongoCore.pullData()
        marketInfo = await db.market.find_one({"_id": "marketInfo"})
        amount += diamondblocks*9*marketInfo["convRate"]
        amount += diamonds*marketInfo["convRate"]
        amount += iron
        await dataHandler.balance.user.change(user.id, amount)
        await interaction.response.send_message(f"Successfully deposited i${amount} into user {user.name}'s account.", ephemeral=True)
        await user.send(f"i${amount} was deposited into your personal account")
        loggingChannel = self.client.get_channel(loggingID)
        loggingEmbed = discord.Embed(title="Deposited Into User Account", description=f"Bank Teller {interaction.user.name}({interaction.user.id}) deposited i${amount} into user {user.name}({user.id})'s accpunt.")
        await loggingChannel.send(embed = loggingEmbed)


async def setup(client):
    await client.add_cog(userDeposit(client))