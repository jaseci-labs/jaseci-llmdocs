"""WebSocket handler for real-time updates."""

include:jac walkers.pipeline;

import:py json;

async walker ws_connect {
    """WS /ws - WebSocket connection handler."""

    has __specs__: dict = {
        "path": "/ws",
        "methods": ["WEBSOCKET"]
    };

    has websocket: object;

    can enter with `root entry {
        manager = get_ws_manager();
        manager.connect(self.websocket);

        try {
            await self.websocket.accept();

            await self.websocket.send_text(json.dumps({
                "event": "connected",
                "timestamp": time(),
                "data": {"message": "WebSocket connected to jac-llmdocs"}
            }));

            while True {
                try {
                    data = await self.websocket.receive_text();
                    message = json.loads(data);

                    if message.get("type") == "ping" {
                        await self.websocket.send_text(json.dumps({
                            "event": "pong",
                            "timestamp": time(),
                            "data": {}
                        }));
                    }
                } except Exception {
                    break;
                }
            }
        } finally {
            manager.disconnect(self.websocket);
        }
    }
}
