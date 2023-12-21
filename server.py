import asyncio
import websockets

async def hello(websockets):
    name = await websockets.recv()
    print(f'<<< {name}')

    greeting = f'Hello {name}!!!'
    await websockets.send(greeting)
    print(f'>>> {greeting}')

async def main():
    async with websockets.serve(hello, 'localhost', 8765):
        await asyncio.Future() 

if __name__ == '__main__':
    asyncio.run(main())   