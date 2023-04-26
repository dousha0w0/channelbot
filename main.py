import discord
import yaml
import asyncio


def create_client(config):
    intents = discord.Intents.default()
    intents.members = False
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    @client.event
    async def on_message(message):
        source_guild_id = config['source_guild_id']
        source_channel_id = config['source_channel_id']
        target_guild_id = config['target_guild_id']
        target_channel_id = config['target_channel_id']

        if message.guild.id == source_guild_id and message.channel.id == source_channel_id:
            target_guild = client.get_guild(target_guild_id)
            target_channel = target_guild.get_channel(target_channel_id)
            content = message.content

            attachments = message.attachments
            embeds = message.embeds

            if content.strip() or attachments or embeds:
                await target_channel.send(f"{message.author.name}#{message.author.discriminator}: {message.content}",
                                          files=[await att.to_file() for att in message.attachments],
                                          embeds=message.embeds)
            else:
                print("Empty message, not sending.")

    return client


async def main():
    with open("config.yaml", 'r') as config_file:
        config = yaml.safe_load(config_file)

    clients = [create_client(account_config) for account_config in config['accounts']]

    await asyncio.gather(
        *[client.start(account_config['token']) for client, account_config in zip(clients, config['accounts'])])


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except discord.errors.LoginFailure as e:
        print(f"Error:{e}")
