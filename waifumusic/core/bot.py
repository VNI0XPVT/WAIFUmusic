from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class waifu(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")

        super().__init__(
            name="AnonXMusic",
            api_id=int(config.API_ID),
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,

            # 🔥 IMPORTANT FIX
            in_memory=False,  # NEVER True for log groups

            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        # 🔒 LOGGER_ID safety check
        try:
            log_id = int(config.LOGGER_ID)
        except Exception:
            LOGGER(__name__).error("LOGGER_ID is missing or invalid.")
            exit()

        # 📩 Send startup log message
        try:
            await self.send_message(
                chat_id=log_id,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )

        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot cannot access log group/channel. "
                "Make sure bot is added and promoted as admin."
            )
            exit()

        except ValueError:
            LOGGER(__name__).error(
                "Invalid LOGGER_ID or peer not resolved. "
                "Tag the bot once in log group."
            )
            exit()

        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot failed to access log group.\nReason: {type(ex).__name__}"
            )
            exit()

        # 👮 Admin check
        try:
            member = await self.get_chat_member(log_id, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as ADMIN in the log group/channel."
                )
                exit()
        except Exception:
            LOGGER(__name__).error("Failed to verify admin status in log group.")
            exit()

        LOGGER(__name__).info(f"Music Bot Started Successfully as {self.name}")

    async def stop(self):
        await super().stop()

