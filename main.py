import discord
import yaml

# 源服务器ID、频道ID和目标服务器ID、频道ID
source_guild_id = 0
source_channel_id = 0
target_guild_id = 0
target_channel_id = 0

intents = discord.Intents.default()
intents.members = False
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # 如果消息来自源服务器和频道
    if message.guild.id == source_guild_id and message.channel.id == source_channel_id:
        print(message)
        # 获取目标服务器和频道对象
        target_guild = client.get_guild(target_guild_id)
        target_channel = target_guild.get_channel(target_channel_id)
        # 提取消息内容
        content = message.content

        # 检查消息是否有附件
        attachments = message.attachments

        # 检查消息是否有嵌入内容
        embeds = message.embeds

        # 检查消息内容是否为空
        if content.strip() or attachments or embeds:
            # 将消息发送到目标频道
            await target_channel.send(f"{message.author.name}#{message.author.discriminator}: {message.content}",
                                      files=[await att.to_file() for att in message.attachments], embeds=message.embeds)
        else:
            print("Empty message, not sending.")


def main():
    with open("config.yaml", 'r') as config_file:
        config = yaml.safe_load(config_file)

    global source_guild_id, source_channel_id, target_guild_id, target_channel_id
    source_guild_id = config['source_guild_id']
    source_channel_id = config['source_channel_id']
    target_guild_id = config['target_guild_id']
    target_channel_id = config['target_channel_id']

    client.run(config['token'])


if __name__ == '__main__':
    main()
