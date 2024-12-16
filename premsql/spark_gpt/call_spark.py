# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Dragon
@Version        :  WIN10, Python3.7.9
------------------------------------
@IDE            ： PyCharm
@Description    :  
@CreateTime     :  12/14/2024 10:55 AM
------------------------------------
"""

import json
import asyncio
import websockets
from auth_utils import AuthUtils


async def main():
    # Generate authenticated URL
    ws_url = AuthUtils.assemble_request_url(
        "ws://36.111.151.113:33013/1qaz",
        "1DB3D20E8CD062209E88",
        "5C1C7540A47543A8B19CABE63B191BE9"
    )

    async def message_handler(websocket):
        try:
            while True:
                message = await websocket.recv()
                response = json.loads(message)

                if response["header"]["code"] != 0:
                    return

                status = response["payload"]["choices"]["status"]
                if status == 2:
                    return

                print(message)
        except websockets.exceptions.ConnectionClosed:
            pass

    try:
        async with websockets.connect(ws_url) as websocket:
            # Prepare request data
            api_request = {
                "header": {
                    "traceId": "spark-demo-test"
                },
                "chat": {
                    "max_tokens": 2048,
                    "temperature": 0.1,
                    "top_k": 5
                },
                "payload": {
                    "message": {
                        "text": [
                            {
                                "content": "今天天气怎么样",
                                "role": "user"
                            }
                        ]
                    }
                }
            }

            # Send request
            await websocket.send(json.dumps(api_request))

            # Handle messages
            await message_handler(websocket)

    except Exception as e:
        print(f"Error: {str(e)}")

    print("end")


if __name__ == "__main__":
    asyncio.run(main())