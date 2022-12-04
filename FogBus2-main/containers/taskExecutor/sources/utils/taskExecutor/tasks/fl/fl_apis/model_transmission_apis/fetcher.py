"""Request remote model & download to local file storage"""
from ..relationship_apis.model_pointer import model_pointer
from ...communications.router import router
from ...communications.handlers.model_communication_handlers import model_communication_handler


class fetcher:
    @staticmethod
    def fetch_remote(self_uuid, remote_ptr: model_pointer, additional_args=None):
        r = router.get_default_router()
        r.send(remote_ptr.address, model_communication_handler.name, {
            "sub_event": model_communication_handler.sub_event.fetch_model_weights,
            "reply_uuid": self_uuid,
            "remote_uuid": remote_ptr.uuid,
            "additional_args": additional_args
        })