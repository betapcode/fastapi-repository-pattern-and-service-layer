from sqlalchemy.orm import Session
from services.notificationfilter_service import NotificationFilterService
from services.offer_service import OfferService
from services.notification_service import NotificationService
from schemas.notification import NotificationInput
from .context import Context
from .email_notification import EmailNotificationStrategy


def create_notifications(db: Session) -> None:

    notification_filters = NotificationFilterService(db).get_all_active()

    # Iterate through all active notification_filters objects
    for filter in notification_filters:

        # Get filtered offers
        offers = OfferService(db).get_all(
            offset=1,
            page_size=100,
            # category=filter.category,
            # sub_category=filter.sub_category,
            # building_type=filter.building_type,
            # price_min=filter.price_min,
            # price_max=filter.price_max,
            # area_min=filter.area_min,
            # area_max=filter.area_max,
            # rooms=filter.rooms,
            # furniture=filter.furniture,
            # floor=filter.floor,
            # query=filter.query,
        )

        notification_input = NotificationInput(
            user_id=filter.user_id,
            title=f"New offers for {filter.category}",
            message=f"There are {len(offers.offers)} offers for {filter.category}",
        )

        notification_service = NotificationService(db)
        notification_object = notification_service.create(notification_input)

        # Update notification object with offers
        offers_ids = [offer.get("id") for offer in offers.offers]
        notification_service.update_offers(notification_object.id, offers_ids)

        # Send notification (currently only by e-mail)
        context = Context(EmailNotificationStrategy())
        context.send_notification(notification_object)

