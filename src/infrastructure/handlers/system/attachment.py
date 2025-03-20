from infrastructure.handlers.base.base_handler import BaseHandler
from domain.apps.system.models import Attachment


class AttachmentHandler(BaseHandler):
    model = Attachment