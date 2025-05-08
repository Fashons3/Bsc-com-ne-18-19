import asyncio
import os
from urllib.parse import parse_qs

async def handle_client(reader, writer):
    request = (await reader.read(1024)).decode()

    if not request:
        writer.close()
        await writer.wait_closed()
        return

    method, path, _ = request.split('\r\n')[0].split()

    if method == 'GET':
        if path == '/':
            with open('templates/index.html', 'r', encoding='utf-8') as f:
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + f.read()
                writer.write(response.encode())
        elif path == '/register':
            with open('templates/register.html', 'r', encoding='utf-8') as f:
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + f.read()
                writer.write(response.encode())
        elif path.startswith('/assets/'):
            file_path = path.lstrip('/')
            if os.path.exists(file_path):
                
                if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.gif'):
                    content_type = 'image/gif'
                else:
                    content_type = 'application/octet-stream'

                with open(file_path, 'rb') as f:
                    content = f.read()
                header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
                writer.write(header.encode() + content)

    elif method == 'POST' and path == '/submit':
        body = request.split('\r\n\r\n', 1)[1]
        form = parse_qs(body)
        username = form['username'][0]
        email = form['email'][0]

        with open('db.txt', 'a', encoding='utf-8') as f:
            f.write(f"{username} {email}\n")

        response = (
            "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            "<html><body><h2>Registration Successful!</h2></body></html>"
        )
        writer.write(response.encode())

    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8085)
    print("Serving on http://127.0.0.1:8085")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
