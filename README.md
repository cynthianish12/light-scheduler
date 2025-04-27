# Light Scheduler Project

A web-based interface to schedule lights using WebSocket and MQTT.

## Features

- Set ON and OFF times for lights via a web interface
- Real-time communication via WebSocket
- MQTT integration for IoT communication
- Arduino integration for physical light control

 [UI Diagram](./there.png)
  [Terminal running](./here.png)
## Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js (for serving the frontend)
- Mosquitto MQTT broker
- Arduino IDE (for uploading sketch to Arduino)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cynthianish12/light-scheduler.git
   cd light-scheduler