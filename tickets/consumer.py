from channels.consumer import AsyncConsumer


class ServiceDeskConsumer(AsyncConsumer):
    """Отвечает за получение запросов."""

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
    
    async def websocket_receive(self, data):
        await self.send({
            "type": "websocket.send",
            "text": "hello from django"
        })
    async def websocket_disconnect(self, event):
        pass        