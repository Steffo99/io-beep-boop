from pydantic import BaseModel
from typing import Optional
from datetime import datetime as DateTime
from datetime import date as Date


class IOModel(BaseModel):
    pass


class Payee(IOModel):
    fiscal_code: str


class PaymentData(IOModel):
    amount: int
    notice_number: str
    invalid_after_due_date: bool
    payee: Payee


class PrescriptionData(IOModel):
    nre: str
    iup: str
    prescriber_fiscal_code: str


class LegalData(IOModel): 
    sender_email_from: str
    has_attachment: bool
    message_unique_id: str
    original_message_url: str
    pec_server_service_id: str


class EuCovidCert(IOModel):
    auth_code: str


class MessageContent(IOModel):
    subject: str
    markdown: str
    payment_data: Optional[PaymentData]
    prescription_data: Optional[PrescriptionData]
    legal_data: Optional[LegalData]
    eu_covid_cert: Optional[EuCovidCert]
    due_date: DateTime


class DefaultAddresses(IOModel):
    email: str


class SendMessageResponse(IOModel):
    id: str


class NotificationStatus(IOModel):
    email: str


class GetMessageResponse(IOModel):
    message: MessageContent
    notification: NotificationStatus


class UserProfile(IOModel):
    sender_allowed: bool


class SubscriptionsFeed(IOModel):
    date_utc: Date
    subscriptions: list[str]
    unsubscriptions: list[str]


__all__ = (
    "Payee",
    "PaymentData",
    "PrescriptionData",
    "LegalData",
    "EuCovidCert",
    "MessageContent",
    "DefaultAddresses",
    "SendMessageResponse",
    "NotificationStatus",
    "GetMessageResponse",
    "UserProfile",
    "SubscriptionsFeed",
)
