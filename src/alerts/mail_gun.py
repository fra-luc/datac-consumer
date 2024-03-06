from dataclasses import dataclass

import aiohttp
from pydantic_settings import BaseSettings, SettingsConfigDict

from alerts.interface import AlertsInterface


class MailGunSettings(BaseSettings):
    """
    Settings for the MailGun service
    """

    domain_name: str
    """
    The MailGun domain name ('sandbox*.mailgun.org')
    """
    recipients: list[str]
    """
    The list of alerts recipients
    """
    api_key: str
    """
    The MailGun API key for the domain
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="mail_gun_", extra="allow")


@dataclass
class MailGunAlerts(AlertsInterface):
    settings: MailGunSettings

    async def notify_feed_download_failure(self, exc: Exception):
        await self.__send_mail("⚠️ Feed Download Failure", "testo")

    async def __send_mail(self, subject: str, text: str):
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"https://api.mailgun.net/v3/{self.settings.domain_name}/messages",
                auth=aiohttp.BasicAuth("api", self.settings.api_key),
                data={
                    "from": f"🚌 datac alerts <mailgun@{self.settings.domain_name}>",
                    "to": self.settings.recipients,
                    "subject": subject,
                    "text": text,
                },
            )
