import random
from typing import List

import discord
from discord.ext import tasks
from babel.dates import format_timedelta
from tortoise import timezone

from utils.cog_class import Cog
from utils.inventory_items import FoieGras
from utils.models import DiscordUser


class DuckBoss(Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.boss_every_n_minutes = 1440
        self.background_loop.start()
        self.iterations_no_spawn = 1
        self.iterations_spawn = 0

    @property
    def luck(self):
        if self.iterations_spawn:
            # If a duck spawned
            return self.boss_every_n_minutes / self.iterations_no_spawn * self.iterations_spawn * 100
        else:
            # No boss spawned, is it "normal" ?
            # This is the probability that no ducks appeared for n iterations given that a duck has a chance to appear
            # every self.boss_every_n_minutes iterations.
            # I ask a math guy for this, I trust him completely, so I'll say that it is right, but don't question me
            # about it. Thanks Cyril.
            # He said the following:
            # "It is one minus the cumulative distribution function of a geometric random variable."
            return (((self.boss_every_n_minutes - 1) / self.boss_every_n_minutes) ** self.iterations_no_spawn) * 100

    def cog_unload(self):
        self.background_loop.cancel()

    async def create_boss_embed(self, bangs=0, boss_message=None):
        boss_life = self.config()['required_bangs']

        new_embed = discord.Embed(
            title=random.choice(["A devil is here...", "A devil appeared...", "Lucifer has spawned...", "KILL THE DEVIL !",
                                 "All hail the Lord of Hatred", "The Lord of Destruction is among us", "The Lord of Terror has arrived", "Hark! The Lord of Pain is here", "The Maiden of Anguish is upon us", "Destroy the Lord of Lies", "Send the Lord of Sin back to Hell", "At last the devil has shown himself", "The Devil has finally revealed itself", "Prove your worth and banish this devil", "The time has come to battle the Devil himself", "Lets see what you are made of...", "The Devil has entered the chat", "...And the Heavens shall tremble marking his arrival...", "Have faith for its time to kill the Devil", "Finally a worthy adversary...", "Have no mercy on this fool", "HE has arrived"]),
            color=discord.Color.green(),
            description="React with 🔫 to kill it.",
        )

        new_embed.add_field(name="Health", value=f"{boss_life - bangs}/{boss_life}")
        if boss_message:
            time_delta = timezone.now() - boss_message.created_at
            old_embed = boss_message.embeds[0]
            new_embed.set_image(url=old_embed.image.url)
            new_embed.set_footer(text=f"The Devil spawned {format_timedelta(time_delta, locale='en_US')} ago")
        else:
            new_embed.set_image(url=random.choice(["https://i.imgur.com/zZLcNhH.jpg",
                                                   "https://i.imgur.com/TtbHsYk.jpg",
                                                   "https://i.imgur.com/IwqsEl3.jpg",
                                                   "https://i.imgur.com/b1Mm3nY.jpg",
                                                   "https://i.imgur.com/YYP19oj.jpg",
                                                   "https://i.imgur.com/3v0h5pQ.jpg",
                                                   "https://i.imgur.com/R0LOR9l.jpg",
                                                   "https://i.imgur.com/nhqV5Kp.png"]))
            new_embed.set_footer(text="A devil just spawned")

        return new_embed

    @tasks.loop(minutes=1)
    async def background_loop(self):
        channel = self.bot.get_channel(self.config()['boss_channel_id'])
        latest_messages = [m async for m in channel.history(limit=1)]

        if not latest_messages:
            boss_message = None
        else:
            latest_message = latest_messages[0]

            if latest_message.author.id != self.bot.user.id:
                boss_message = None
            elif len(latest_message.embeds) == 0:
                boss_message = None
            else:
                latest_message_embed = latest_message.embeds[0]
                if latest_message_embed.color == discord.Color.green():
                    boss_message = latest_message
                else:
                    boss_message = None

        if boss_message:
            reaction: discord.Reaction = boss_message.reactions[0]
            bangs = reaction.count
            boss_life = self.config()['required_bangs']

            if bangs >= boss_life:
                # Kill the boss
                users = [u async for u in reaction.users()]
                ids = [u.id for u in users]
                discordusers: List[DiscordUser] = await DiscordUser.filter(discord_id__in=ids).only('boss_kills', 'discord_id').all()

                for discorduser in discordusers:
                    discorduser.boss_kills += 1
                    await FoieGras.give_to(discorduser)
                    await discorduser.save(update_fields=['boss_kills'])

                new_embed = discord.Embed(
                    title=random.choice(["The Devil was defeated !"]),
                    color=discord.Color.red(),
                    description=f"Praise the {bangs} players who helped in this battle. Check your inventories with `dh!inv` for these drops.",
                )
                if "nhqV5Kp.png" in str(boss_message.embeds[0].image.url):
                    # Special case the llama.
                    new_embed.set_image(url="https://i.imgur.com/8OkElP1.jpg")
                else:
                    new_embed.set_image(url=random.choice(["https://i.imgur.com/wS58q8G.jpg",
                                                           "https://i.imgur.com/5FfDSkt.jpg"]))
                new_embed.add_field(name="Health", value=f"0/{boss_life}")

                time_delta = timezone.now() - boss_message.created_at
                new_embed.set_footer(text=f"The Devil lived for {format_timedelta(time_delta, locale='en_US')}.")

                await boss_message.edit(embed=new_embed)
            else:
                new_embed = await self.create_boss_embed(bangs=bangs, boss_message=boss_message)

                await boss_message.edit(embed=new_embed)

        else:
            if random.randint(1, self.boss_every_n_minutes) == 1:
                self.iterations_spawn += 1
                await self.spawn_boss()
            else:
                self.iterations_no_spawn += 1

    async def spawn_boss(self):
        self.bot.logger.info("Spawning the Devil...")
        channel = self.bot.get_channel(self.config()['boss_channel_id'])

        boss_message = await channel.send(embed=await self.create_boss_embed(), )
        await boss_message.add_reaction("🔫")
        self.bot.logger.debug("A Devil has spawned, logging that to the channel logs...")

        ping_role_id = self.config()['role_ping_id']

        log_embed = discord.Embed(
            title="A Devil has spawned in the server.",
            color=discord.Color.dark_magenta(),
            description=f"Go in the {channel.mention} and click the 🔫 reaction to banish it back to Hell and claim free inventory items."
        )

        log_embed.add_field(name="Subscribe/Unsubscribe", value="To (un)subscribe from these alerts, go to the #roles•for•all channel.")

        await self.bot.log_to_channel(content=f"<@&{ping_role_id}>", embed=log_embed, allowed_mentions=discord.AllowedMentions(roles=True, users=False, everyone=False))
        self.bot.logger.info("Devil spawned, logging message sent!")

    @background_loop.before_loop
    async def before(self):
        await self.bot.wait_until_ready()


setup = DuckBoss.setup
