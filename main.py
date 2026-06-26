import discord
from discord.ext import tasks
import random, json
from datetime import datetime
from zoneinfo import ZoneInfo

with open("config.json","r",encoding="utf-8") as f:
    cfg=json.load(f)

def load(name):
    with open(f"data/{name}.txt","r",encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]

bpms=load("bpm")
keys=load("keys")
types=load("types")
moods=load("moods")
rules=load("rules")

intents=discord.Intents.default()
client=discord.Client(intents=intents)

sent_date=None

@tasks.loop(minutes=1)
async def scheduler():
    global sent_date
    now=datetime.now(ZoneInfo(cfg["timezone"]))
    today=now.date()
    if now.hour==cfg["post_hour"] and now.minute==cfg["post_minute"] and sent_date!=today:
        ch=client.get_channel(int(cfg["channel_id"]))
        if ch:
            embed=discord.Embed(
                title=cfg["title"],
                color=0x8A2BE2
            )
            embed.add_field(name="🎵 BPM",value=random.choice(bpms),inline=True)
            embed.add_field(name="🎹 Key",value=random.choice(keys),inline=True)
            embed.add_field(name="👤 Type Beat",value=random.choice(types),inline=False)
            embed.add_field(name="🌑 Mood",value=random.choice(moods),inline=True)
            embed.add_field(name="⚡ Challenge",value=random.choice(rules),inline=False)
            embed.set_footer(text=cfg["footer"])
            await ch.send(embed=embed)
            sent_date=today

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    scheduler.start()

client.run(cfg["token"])
