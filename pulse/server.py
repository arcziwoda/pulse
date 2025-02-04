import asyncio

READ_SIZE = 4096


class Request:
    def __init__(self, raw_data: bytes): ...


class Response:
    def build(self) -> bytes: ...


class Router:
    def route(self, request: Request) -> Response: ...


class RequestParser:
    def parse(self, message: str) -> Request: ...


class RequestHandler:
    def __init__(self):
        self.router = Router()
        self.parser = RequestParser()

    async def handle(self, data: bytes) -> bytes:
        request = Request(data)
        response = self.router.route(request)
        return response.build()


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

        response = await self.handler.handle(data)

        writer.write(response)
        await writer.drain()

        writer.close()
        await writer.wait_closed()


async def main():
    server = Server("localhost", 8080)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
