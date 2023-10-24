import asyncio
import websockets
import json
import os
 
mock_datas = ["AVERAGE-6024.json", "BEST-DATA.json", "HEALTH-6024.json", "PIZZA.json", "TOP3-RANKING.json", "TOP3.json", "VERSUS.json"]

average_6024 = {}
best_data = {}
health_6024 = {} 
pizza = {} 
top3_ranking = {} 
top3 = {}
versus = {}

datas = [average_6024, best_data, health_6024, pizza, top3_ranking, top3, versus]

current_path = os.path.dirname(os.path.abspath(__file__))

for index, mock_data in enumerate(mock_datas):
    path_data = os.path.join(current_path, 'MOCK', mock_data)

    # FIRST TIME
    try:
        with open(path_data, 'r') as file:
            datas[index] = json.load(file)
            # print(datas)

    except FileNotFoundError:
        print("n consegui encontrar o arquivo")

async def send_data_ws(data, websocket):
    try:
        await websocket.send(json.dumps(data))
        # print(json.dumps(data))

    except websockets.exceptions.ConnectionClosed:
        print('Conexão fechada pelo cliente.')

async def watch_changes(path_json, websocket):
    last_change = os.path.getmtime(path_json)

    while True:
        current_change = os.path.getmtime(path_json)

        if current_change > last_change:
            with open(path_json, "r") as file:
                data = json.load(file)
                await send_data_ws(data, websocket)

            last_change = current_change

        await asyncio.sleep(1)

# create handler for each connection

async def handler(websocket, path):
 
    # recive = await websocket.recv()

    # print(recive)

    # reply = json.dumps(data)

    for data in datas:
        await websocket.send(json.dumps(data))

    await asyncio.gather(*[watch_changes(os.path.join(current_path, 'MOCK', mock_data), websocket) for mock_data in mock_datas])
    # print(path_data)
    
    # for mock_data in mock_datas:
        # await asyncio.create_task(watch_changes(os.path.join(current_path, 'MOCK', 'BEST-DATA.json'), mock_data))


start_server = websockets.serve(handler, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()