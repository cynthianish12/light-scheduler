import asyncio
import websockets
import json
import subprocess
from datetime import datetime

connected_clients = set()

async def handle_schedule(websocket):
    """Handle WebSocket connection with just the websocket parameter"""
    connected_clients.add(websocket)
    print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            try:
                data = json.loads(message)
                
                if data.get('type') == 'set_schedule':
                    # Validate times
                    try:
                        on_time = datetime.strptime(data['onTime'], '%H:%M').time()
                        off_time = datetime.strptime(data['offTime'], '%H:%M').time()
                        
                        # Validate off time is after on time
                        if off_time <= on_time:
                            await websocket.send(json.dumps({
                                'type': 'error',
                                'message': 'OFF time must be after ON time'
                            }))
                            continue
                            
                        # Publish to MQTT
                        mqtt_message = json.dumps({
                            'onTime': data['onTime'],
                            'offTime': data['offTime']
                        })
                        
                        try:
                            subprocess.run([
                                'mosquitto_pub',
                                '-t', 'light/schedule',
                                '-m', mqtt_message
                            ], check=True)
                            
                            print(f"Published to MQTT: {mqtt_message}")
                            
                            # Send acknowledgment back to client
                            await websocket.send(json.dumps({
                                'type': 'schedule_ack',
                                'onTime': data['onTime'],
                                'offTime': data['offTime']
                            }))
                            
                        except subprocess.CalledProcessError as e:
                            error_msg = f"Failed to publish to MQTT: {str(e)}"
                            await websocket.send(json.dumps({
                                'type': 'error',
                                'message': error_msg
                            }))
                            
                    except ValueError as e:
                        await websocket.send(json.dumps({
                            'type': 'error',
                            'message': 'Invalid time format. Use HH:MM'
                        }))
                        
            except json.JSONDecodeError as e:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Invalid JSON format'
                }))
                
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    # Create server without the path parameter requirement
    async with websockets.serve(
        handle_schedule,  # handler function
        "localhost",      # host
        8765,             # port
    ):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())