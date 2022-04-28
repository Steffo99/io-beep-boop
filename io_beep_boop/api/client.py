import httpx
import time
import datetime
import functools
import typing as t
import pkg_resources

from . import models


MODEL = t.TypeVar("MODEL")


def extract_data(model: t.Type[MODEL]) -> t.Callable[[t.Callable[..., httpx.Response]], t.Callable[..., MODEL]]:
    """
    Decorator which captures errors occurring inside methods of :class:`.IOServiceClient` and converts the received data into its corresponding model.
    """

    def decorator(f: t.Callable[..., httpx.Response]) -> t.Callable[..., MODEL]:

        @functools.wraps(f)
        def decorated(*args, **kwargs):
            response: httpx.Response = f(*args, **kwargs)
            response.raise_for_status()
            data = response.json()
            return model(**data)
        
        return decorated
    
    return decorator


class IOServiceClient(httpx.Client):
    """
    Simplified wrapper for the `IO App API <https://developer.io.italia.it/openapi.html>`_.
    """

    def __init__(self, token: str, base_url: str = "https://api.io.italia.it/api/v1", user_agent: t.Optional[str] = None) -> None:
        """
        Create a new :class:`.IOAppService`.

        :param token: The token to use when performing requests to the API. On registration of a new service, two tokens are provided, and either may be used.
        :param base_url: The base URL of the IO App API. Defaults to ``https://api.io.italia.it/api/v1``.
        """

        super().__init__(
            base_url=base_url,
            headers={
                "User-Agent": user_agent or f"io-beep-boop/{pkg_resources.get_distribution('io-beep-boop').version}",
                "Ocp-Apim-Subscription-Key": token,
            }
        )

    @extract_data(models.SendMessageResponse)
    def send_legal_message(self, fiscal_code: str, content: models.MessageContent, legal_mail: str, time_to_live: int = 3600, default_addresses: t.Optional[models.DefaultAddresses] = None):
        """
        Send a message to the user with the given ``fiscal_code`` on behalf of the service identified by the PEC given in ``legal_mail``.

        .. seealso::

            https://developer.io.italia.it/openapi.html#operation/submitLegalMessageforUserWithFiscalCodeInBodyOnBehalfOfService
        """

        return self.post(f"/legal-messages/{legal_mail}", json={
            "time_to_live": time_to_live,
            "content": content,
            "default_addresses": default_addresses,
            "fiscal_code": fiscal_code,
        })

    @extract_data(models.SendMessageResponse)
    def send_message(self, fiscal_code: str, content: models.MessageContent, time_to_live: int = 3600, default_addresses: t.Optional[models.DefaultAddresses] = None):
        """
        Send a message to the user with the given ``fiscal_code``.

        .. seealso::

            https://developer.io.italia.it/openapi.html#operation/submitMessageforUser
        """
        
        return self.post(f"/messages/{fiscal_code}", json={
            "time_to_live": time_to_live,
            "content": content,
            "default_addresses": default_addresses,
        })

    @extract_data(models.SendMessageResponse)
    def get_message(self, fiscal_code: str, message_id: str):
        """
        Get the message with the given ``message_id`` addressed to the user with the given ``fiscal_code``.

        .. seealso::

            https://developer.io.italia.it/openapi.html#operation/getMessage
        """

        return self.get(f"/messages/{fiscal_code}/{message_id}")

    @extract_data(models.UserProfile)
    def get_profile(self, fiscal_code: str):
        """
        Get the profile of the user with the given ``fiscal_code``.

        .. seealso::

            https://developer.io.italia.it/openapi.html#operation/getProfile
        """

        return self.get(f"/profiles/{fiscal_code}")

    @extract_data(models.SubscriptionsFeed)
    def get_subscriptions_on_day(self, date: datetime.date):
        """
        Get a list of hashed fiscal codes which subscribed and unsubscribed from the service on the given ``date``.

        .. warning::

            Requires special authorization.

        .. seealso::
        
            https://developer.io.italia.it/openapi.html#operation/getSubscriptionsFeedForDate
        """

        return self.get(f"/subscriptions-feed/{date.strftime('%Y-%m-%d')}")

    # TODO: Service-level endpoints - since it seems weird to me that a service can spawn endless clones of itself?


__all__ = (
    "IOServiceClient",
)
