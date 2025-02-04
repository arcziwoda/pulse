import asyncio

READ_SIZE = 4096


class RequestHandler:
    async def handle(self, messsage: str) -> str:
        print(f"Received message: {messsage}")
        return "Hello from server!"


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.handler = RequestHandler()

    async def run(self):
        server = await asyncio.start_server(
            self.handle_connection, host=self.host, port=self.port
        )
        async with server:
            await server.serve_forever()

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        data = await reader.read(READ_SIZE)
        message = data.decode()

        response = await self.handler.handle(message)

        writer.write(response.encode())
        await writer.drain()

        writer.close()
        await writer.wait_closed()


async def main():
    server = Server("localhost", 8080)
    await server.run()


asyncio.run(main())
