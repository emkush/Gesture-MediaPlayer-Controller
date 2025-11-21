// Background script for gesture-controlled media player
let gestureSocket = null;
let isListening = false;

// Initialize gesture detection when extension loads
chrome.runtime.onStartup.addListener(() => {
    console.log('Gesture-controlled media player extension started');
});

chrome.runtime.onInstalled.addListener(() => {
    console.log('Gesture-controlled media player extension installed');
});

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'startGestureDetection') {
        startGestureDetection();
        sendResponse({status: 'started'});
    } else if (message.action === 'stopGestureDetection') {
        stopGestureDetection();
        sendResponse({status: 'stopped'});
    } else if (message.action === 'getStatus') {
        sendResponse({isListening: isListening});
    }
    return true;
});

function startGestureDetection() {
    if (isListening) return;
    
    isListening = true;
    console.log('Starting gesture detection...');
    
    // Try to connect to the Python gesture recognition server
    connectToGestureServer();
}

function stopGestureDetection() {
    if (!isListening) return;
    
    isListening = false;
    console.log('Stopping gesture detection...');
    
    if (gestureSocket) {
        gestureSocket.close();
        gestureSocket = null;
    }
}

function connectToGestureServer() {
    console.log('Connecting to gesture detection server...');
    
    let lastGestureTimestamp = 0;
    
    // Poll the Python API server for gestures
    const checkInterval = setInterval(async () => {
        if (!isListening) {
            clearInterval(checkInterval);
            return;
        }
        
        try {
            // Check for new gestures from the Python server
            const response = await fetch('http://localhost:8081/gesture', {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Check if we have a new gesture (different timestamp)
                if (data.gesture && data.timestamp && data.timestamp > lastGestureTimestamp) {
                    lastGestureTimestamp = data.timestamp;
                    
                    // Check if gesture is recent (within last 5 seconds)
                    const now = Date.now() / 1000;
                    if (now - data.timestamp < 5) {
                        console.log('New gesture received:', data.gesture, 'at', new Date(data.timestamp * 1000));
                        handleGestureDetected(data.gesture);
                    }
                }
            } else {
                console.log('Server responded with status:', response.status);
            }
        } catch (error) {
            console.log('Could not connect to gesture server:', error.message);
            console.log('Make sure to start: python gesture_api_server.py');
        }
    }, 1000); // Check every 1 second
}

function handleGestureDetected(gesture) {
    console.log(`Gesture detected: ${gesture}`);
    
    // Map gesture names to actions
    const gestureActionMap = {
        'palm_pause_play': 'pause_play',
        'fist_mute': 'mute',
        'thumbs_up_like': 'volume_up',
        'thumbs_down_dislike': 'volume_down',
        'fingers_up_volume_up': 'volume_up',
        'fingers_down_volume_down': 'volume_down',
        // Legacy support
        'palm': 'pause_play'
    };
    
    const action = gestureActionMap[gesture];
    if (!action) {
        console.log('Unknown gesture:', gesture);
        return;
    }
    
    // Send command to active tab
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        if (tabs.length > 0) {
            const tab = tabs[0];
            
            // Check if it's a supported media site
            if (tab.url.includes('youtube.com') || tab.url.includes('netflix.com')) {
                console.log(`Sending ${action} command to ${tab.url}`);
                chrome.tabs.sendMessage(tab.id, {
                    action: action,
                    gesture: gesture,
                    timestamp: Date.now()
                }).catch(error => {
                    console.log('Error sending message to content script:', error);
                });
            } else {
                console.log('Not a supported media site:', tab.url);
            }
        }
    });
}