document.addEventListener('DOMContentLoaded', function() {
    const onTimeInput = document.getElementById('on-time');
    const offTimeInput = document.getElementById('off-time');
    const submitBtn = document.getElementById('submit-btn');
    const statusDiv = document.getElementById('status');
    const currentOnSpan = document.getElementById('current-on');
    const currentOffSpan = document.getElementById('current-off');
    
    // Connect to WebSocket server
    const socket = new WebSocket('ws://localhost:8765');
    
    socket.onopen = function(e) {
        console.log('Connected to WebSocket server');
    };
    
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'schedule_ack') {
            showStatus('Schedule set successfully!', 'success');
            currentOnSpan.textContent = data.onTime || 'Not set';
            currentOffSpan.textContent = data.offTime || 'Not set';
        } else if (data.type === 'error') {
            showStatus(data.message, 'error');
        }
    };
    
    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
        } else {
            console.log('Connection died');
            showStatus('Connection lost. Please refresh the page.', 'error');
        }
    };
    
    socket.onerror = function(error) {
        console.log(`WebSocket error: ${error}`);
        showStatus('Connection error. Please try again.', 'error');
    };
    
    submitBtn.addEventListener('click', function() {
        const onTime = onTimeInput.value;
        const offTime = offTimeInput.value;
        
        if (!onTime || !offTime) {
            showStatus('Please set both ON and OFF times', 'error');
            return;
        }
        
        const schedule = {
            type: 'set_schedule',
            onTime: onTime,
            offTime: offTime
        };
        
        socket.send(JSON.stringify(schedule));
    });
    
    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = 'status ' + type;
    }
});