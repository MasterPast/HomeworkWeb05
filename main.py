import asyncio
import websockets


async def hello():
    
    open_socket = True
    uri = 'ws://localhost:8765'
    
    while open_socket == True:
        async with websockets.connect(uri, ping_timeout=20) as websocket:
            
            name = input('Send to server <<< ')
            if name == 'exit':
                await websocket.send('ByeBye')
                break

            await websocket.send(name)
            print(f'>>> {name}')

            greeting = await websocket.recv()
            print(f'<<< {greeting}')

if __name__ == '__main__':
    asyncio.run(hello())