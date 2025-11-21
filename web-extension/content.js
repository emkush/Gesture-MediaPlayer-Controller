console.log("Gesture-controlled media player loaded!");

// Utility function to wait for YouTube elements to load
function waitForElement(selector, timeout = 5000) {
    return new Promise((resolve) => {
        const element = document.querySelector(selector);
        if (element) {
            resolve(element);
            return;
        }
        
        const observer = new MutationObserver((mutations, obs) => {
            const element = document.querySelector(selector);
            if (element) {
                obs.disconnect();
                resolve(element);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        setTimeout(() => {
            observer.disconnect();
            resolve(null);
        }, timeout);
    });
}

// CRITICAL: Function to ensure YouTube volume controls are visible and interactive
async function ensureVolumeControlsVisible() {
    console.log('Ensuring volume controls are visible...');
    
    // Find the volume area that needs to be hovered
    const volumeAreas = [
        document.querySelector('.ytp-volume-area'),
        document.querySelector('.ytp-chrome-controls .ytp-volume-area'),
        document.querySelector('[class*="volume-area"]'),
        document.querySelector('.ytp-chrome-controls'),
    ].filter(Boolean);
    
    if (volumeAreas.length === 0) {
        console.log('No volume area found to hover over');
        return;
    }
    
    // Hover over each volume area to make controls visible
    for (const volumeArea of volumeAreas) {
        console.log('Hovering over volume area:', volumeArea.className);
        
        // Simulate mouse enter to show volume controls
        volumeArea.dispatchEvent(new MouseEvent('mouseenter', {
            bubbles: true,
            cancelable: true,
            view: window
        }));
        
        volumeArea.dispatchEvent(new MouseEvent('mouseover', {
            bubbles: true,
            cancelable: true,
            view: window
        }));
        
        // Force focus to ensure interactivity
        if (volumeArea.focus) {
            volumeArea.focus();
        }
    }
    
    // Wait for the volume controls to appear
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // Check if volume slider is now visible
    const volumeSlider = document.querySelector('.ytp-volume-slider');
    const volumePanel = document.querySelector('.ytp-volume-panel');
    
    console.log('Volume controls visibility check:', {
        volumeSlider: !!volumeSlider,
        volumeSliderVisible: volumeSlider?.offsetParent !== null,
        volumePanel: !!volumePanel,
        volumePanelVisible: volumePanel?.offsetParent !== null
    });
    
    // If still not visible, try alternative approach
    if (!volumeSlider || volumeSlider.offsetParent === null) {
        console.log('Volume slider still not visible, trying alternative approach...');
        
        // Try hovering over the entire player controls area
        const playerControls = document.querySelector('.ytp-chrome-controls') || 
                             document.querySelector('#movie_player');
        
        if (playerControls) {
            playerControls.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
            playerControls.dispatchEvent(new MouseEvent('mousemove', { bubbles: true }));
            
            // Wait a bit more
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    }
    
    return true;
}

// Function to keep volume controls visible during interaction
function keepVolumeControlsVisible(duration = 2000) {
    const volumeAreas = [
        document.querySelector('.ytp-volume-area'),
        document.querySelector('.ytp-chrome-controls .ytp-volume-area'),
        document.querySelector('.ytp-chrome-controls')
    ].filter(Boolean);
    
    if (volumeAreas.length === 0) return;
    
    console.log('Keeping volume controls visible for', duration, 'ms');
    
    // Keep sending mouseenter events periodically to maintain visibility
    const keepAliveInterval = setInterval(() => {
        volumeAreas.forEach(volumeArea => {
            volumeArea.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
            volumeArea.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
        });
    }, 200);
    
    // Stop after the specified duration
    setTimeout(() => {
        clearInterval(keepAliveInterval);
        console.log('Stopped keeping volume controls visible');
    }, duration);
}

// Debug function to check YouTube player state
function debugYouTubeState() {
    const video = document.querySelector('video');
    const player = document.querySelector('#movie_player');
    const muteButton = document.querySelector('.ytp-mute-button');
    const volumeSlider = document.querySelector('.ytp-volume-slider');
    
    console.log('YouTube Debug Info:', {
        video: !!video,
        videoVolume: video?.volume,
        videoMuted: video?.muted,
        player: !!player,
        muteButton: !!muteButton,
        muteButtonVisible: muteButton?.offsetParent !== null,
        volumeSlider: !!volumeSlider,
        volumeSliderVisible: volumeSlider?.offsetParent !== null
    });
}

// Add visual indicator that extension is active
const indicator = document.createElement('div');
indicator.id = 'gesture-indicator';
indicator.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: rgba(0, 255, 0, 0.8);
    color: white;
    padding: 8px 12px;
    border-radius: 20px;
    font-family: Arial, sans-serif;
    font-size: 12px;
    z-index: 10000;
    display: none;
`;
indicator.textContent = '👋 Gesture Control Active';
document.body.appendChild(indicator);

// Show indicator for 3 seconds when page loads
setTimeout(() => {
    indicator.style.display = 'block';
    setTimeout(() => {
        indicator.style.display = 'none';
    }, 3000);
}, 1000);

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Received gesture message:', message);
    
    switch (message.action) {
        case 'pause_play':
            handlePausePlay();
            showGestureNotification('🖐️ Palm gesture - Play/Pause');
            break;
        case 'volume_up':
            handleVolumeUp();
            showGestureNotification('👍 Volume Up');
            break;
        case 'volume_down':
            handleVolumeDown();
            showGestureNotification('👎 Volume Down');
            break;
        case 'mute':
            handleMute();
            showGestureNotification('✊ Mute/Unmute');
            break;
        default:
            console.log('Unknown gesture action:', message.action);
    }
    return true;
});

function handlePausePlay() {
    const currentUrl = window.location.href;
    
    if (currentUrl.includes('youtube.com')) {
        handleYouTubePausePlay();
    } else if (currentUrl.includes('netflix.com')) {
        handleNetflixPausePlay();
    }
}

function handleYouTubePausePlay() {
    // First try direct video element approach
    const video = document.querySelector('video');
    if (video) {
        if (video.paused) {
            video.play();
            console.log('YouTube video played directly by gesture');
        } else {
            video.pause();
            console.log('YouTube video paused directly by gesture');
        }
        return;
    }
    
    // Try multiple YouTube button selectors
    const selectors = [
        'button[data-title-no-tooltip="Play"]',
        'button[data-title-no-tooltip="Pause"]',
        'button[title="Play (k)"]',
        'button[title="Pause (k)"]',
        '.ytp-play-button',
        'button.ytp-play-button',
        '[aria-label*="Play"]',
        '[aria-label*="Pause"]'
    ];
    
    let playButton = null;
    for (const selector of selectors) {
        playButton = document.querySelector(selector);
        if (playButton) break;
    }
    
    if (playButton) {
        playButton.click();
        console.log('YouTube play/pause button triggered by gesture');
    } else {
        // Fallback: try keyboard shortcut
        document.body.dispatchEvent(new KeyboardEvent('keydown', {
            key: 'k',
            code: 'KeyK',
            keyCode: 75,
            which: 75,
            bubbles: true
        }));
        console.log('YouTube keyboard shortcut (k) triggered by gesture');
    }
}

function handleNetflixPausePlay() {
    // First try direct video element approach
    const video = document.querySelector('video');
    if (video) {
        if (video.paused) {
            video.play();
            console.log('Netflix video played directly by gesture');
        } else {
            video.pause();
            console.log('Netflix video paused directly by gesture');
        }
        return;
    }
    
    // Try multiple Netflix button selectors
    const selectors = [
        'button[data-uia="control-play-pause-play"]',
        'button[data-uia="control-play-pause-pause"]',
        'button[aria-label="Play"]',
        'button[aria-label="Pause"]',
        '.button-nfplayerPlay',
        '.button-nfplayerPause',
        '[data-uia*="play"]'
    ];
    
    let playButton = null;
    for (const selector of selectors) {
        playButton = document.querySelector(selector);
        if (playButton) break;
    }
    
    if (playButton) {
        playButton.click();
        console.log('Netflix play/pause button triggered by gesture');
    } else {
        // Fallback: try spacebar (common media control)
        document.body.dispatchEvent(new KeyboardEvent('keydown', {
            key: ' ',
            code: 'Space',
            keyCode: 32,
            which: 32,
            bubbles: true
        }));
        console.log('Netflix spacebar shortcut triggered by gesture');
    }
}

function handleVolumeUp() {
    const currentUrl = window.location.href;
    
    if (currentUrl.includes('youtube.com')) {
        handleYouTubeVolumeUp();
    } else if (currentUrl.includes('netflix.com')) {
        handleNetflixVolumeUp();
    }
}

function handleVolumeDown() {
    const currentUrl = window.location.href;
    
    if (currentUrl.includes('youtube.com')) {
        handleYouTubeVolumeDown();
    } else if (currentUrl.includes('netflix.com')) {
        handleNetflixVolumeDown();
    }
}

function handleMute() {
    const currentUrl = window.location.href;
    
    if (currentUrl.includes('youtube.com')) {
        handleYouTubeMute();
    } else if (currentUrl.includes('netflix.com')) {
        handleNetflixMute();
    }
}

async function handleYouTubeVolumeUp() {
    console.log('Attempting YouTube volume up...');
    
    // CRITICAL: First ensure volume controls are visible
    await ensureVolumeControlsVisible();
    
    // Keep controls visible during our interaction
    keepVolumeControlsVisible(3000);
    
    // Method 1: Try to access YouTube's player API directly
    try {
        // Check if YouTube player API is available
        if (window.ytInitialPlayerResponse || window.ytplayer) {
            console.log('YouTube player API detected');
        }
        
        // Try to find the player instance
        const playerElement = document.querySelector('#movie_player');
        if (playerElement && playerElement.getPlayerState) {
            const currentVolume = playerElement.getVolume();
            const newVolume = Math.min(100, currentVolume + 10);
            playerElement.setVolume(newVolume);
            console.log(`YouTube volume set via player API: ${currentVolume}% → ${newVolume}%`);
            return;
        }
    } catch (e) {
        console.log('YouTube player API not available:', e.message);
    }
    
    // Method 2: Simulate mouse wheel scroll on volume slider
    const volumeSlider = document.querySelector('.ytp-volume-slider') || 
                        document.querySelector('.ytp-volume-panel') ||
                        document.querySelector('.ytp-volume-area');
    
    if (volumeSlider) {
        console.log('Found volume slider, attempting mouse wheel simulation');
        
        // Simulate wheel scroll up for volume increase
        const wheelEvent = new WheelEvent('wheel', {
            deltaY: -120, // Negative for scroll up (volume increase)
            bubbles: true,
            cancelable: true
        });
        
        volumeSlider.dispatchEvent(wheelEvent);
        console.log('Volume wheel event dispatched');
        
        // Wait a bit to see if it worked
        await new Promise(resolve => setTimeout(resolve, 100));
        const video = document.querySelector('video');
        if (video) {
            console.log(`Volume after wheel event: ${(video.volume * 100).toFixed(0)}%`);
        }
        return;
    }
    
    // Method 3: Try clicking volume up areas (controls should now be visible)
    const volumeControls = [
        '.ytp-volume-slider',
        '.ytp-volume-panel',
        '.ytp-volume-area .ytp-volume-slider',
        'div[class*="volume"] input[type="range"]'
    ];
    
    console.log('Looking for volume controls to click...');
    
    for (const selector of volumeControls) {
        const control = document.querySelector(selector);
        if (control) {
            const isVisible = control.offsetParent !== null;
            console.log(`Found volume control: ${selector}, visible: ${isVisible}`);
            
            if (isVisible) {
                // If it's a range input, increment its value
                if (control.tagName === 'INPUT' && control.type === 'range') {
                    const currentValue = parseFloat(control.value) || 50;
                    const newValue = Math.min(100, currentValue + 10);
                    control.value = newValue;
                    control.dispatchEvent(new Event('input', { bubbles: true }));
                    control.dispatchEvent(new Event('change', { bubbles: true }));
                    console.log(`Volume range input updated: ${currentValue} → ${newValue}`);
                    return;
                }
                
                // Try clicking on the right side of the slider (for volume up)
                const rect = control.getBoundingClientRect();
                
                // Get current volume to calculate better click position
                const video = document.querySelector('video');
                const currentVolumePercent = video ? video.volume * 100 : 50;
                const targetVolumePercent = Math.min(100, currentVolumePercent + 15);
                
                // Click at position representing target volume
                const clickX = rect.left + (rect.width * (targetVolumePercent / 100));
                const clickY = rect.top + (rect.height / 2);
                
                console.log(`Clicking volume slider at ${targetVolumePercent}% position (${clickX}, ${clickY})`);
                
                control.dispatchEvent(new MouseEvent('click', {
                    clientX: clickX,
                    clientY: clickY,
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
                
                // Also try mousedown/mouseup sequence
                control.dispatchEvent(new MouseEvent('mousedown', {
                    clientX: clickX,
                    clientY: clickY,
                    bubbles: true
                }));
                
                control.dispatchEvent(new MouseEvent('mouseup', {
                    clientX: clickX,
                    clientY: clickY,
                    bubbles: true
                }));
                
                console.log('Volume slider click events dispatched');
                return;
            }
        }
    }
    
    // Method 4: Direct video element manipulation with extensive event triggering
    const video = document.querySelector('video');
    if (video) {
        const currentVolume = video.volume;
        const newVolume = Math.min(1.0, currentVolume + 0.1);
        
        console.log(`Direct video volume change: ${(currentVolume * 100).toFixed(0)}% → ${(newVolume * 100).toFixed(0)}%`);
        
        video.volume = newVolume;
        
        // Dispatch multiple events to ensure YouTube notices
        const events = ['volumechange', 'loadedmetadata', 'canplay', 'progress'];
        events.forEach(eventType => {
            video.dispatchEvent(new Event(eventType, { bubbles: true }));
        });
        
        // Force a UI update by temporarily changing another property
        setTimeout(() => {
            video.dispatchEvent(new Event('timeupdate', { bubbles: true }));
        }, 50);
        
        return;
    }
    
    // Method 5: Enhanced keyboard shortcut with multiple targets
    console.log('Trying enhanced keyboard shortcuts...');
    
    // Focus different possible targets
    const targets = [
        document.querySelector('#movie_player'),
        document.querySelector('.html5-video-player'),
        document.querySelector('video'),
        document.body
    ];
    
    for (const target of targets) {
        if (target) {
            target.focus();
            
            // Try both ArrowUp (YouTube's volume control) and + key
            const keyEvents = [
                { key: 'ArrowUp', code: 'ArrowUp', keyCode: 38 },
                { key: '+', code: 'Equal', keyCode: 187, shiftKey: true },
                { key: '=', code: 'Equal', keyCode: 187 }
            ];
            
            keyEvents.forEach(({ key, code, keyCode, shiftKey = false }) => {
                const event = new KeyboardEvent('keydown', {
                    key: key,
                    code: code,
                    keyCode: keyCode,
                    which: keyCode,
                    shiftKey: shiftKey,
                    bubbles: true,
                    cancelable: true
                });
                
                target.dispatchEvent(event);
            });
            
            console.log(`Keyboard events sent to ${target.tagName || target.constructor.name}`);
        }
    }
}

async function handleYouTubeVolumeDown() {
    console.log('Attempting YouTube volume down...');
    
    // CRITICAL: First ensure volume controls are visible
    await ensureVolumeControlsVisible();
    
    // Keep controls visible during our interaction
    keepVolumeControlsVisible(3000);
    
    // Method 1: Try to access YouTube's player API directly
    try {
        // Check if YouTube player API is available
        if (window.ytInitialPlayerResponse || window.ytplayer) {
            console.log('YouTube player API detected');
        }
        
        // Try to find the player instance
        const playerElement = document.querySelector('#movie_player');
        if (playerElement && playerElement.getPlayerState) {
            const currentVolume = playerElement.getVolume();
            const newVolume = Math.max(0, currentVolume - 10);
            playerElement.setVolume(newVolume);
            console.log(`YouTube volume set via player API: ${currentVolume}% → ${newVolume}%`);
            return;
        }
    } catch (e) {
        console.log('YouTube player API not available:', e.message);
    }
    
    // Method 2: Simulate mouse wheel scroll on volume slider
    const volumeSlider = document.querySelector('.ytp-volume-slider') || 
                        document.querySelector('.ytp-volume-panel') ||
                        document.querySelector('.ytp-volume-area');
    
    if (volumeSlider) {
        console.log('Found volume slider, attempting mouse wheel simulation');
        
        // Simulate wheel scroll down for volume decrease
        const wheelEvent = new WheelEvent('wheel', {
            deltaY: 120, // Positive for scroll down (volume decrease)
            bubbles: true,
            cancelable: true
        });
        
        volumeSlider.dispatchEvent(wheelEvent);
        console.log('Volume wheel event dispatched');
        
        // Wait a bit to see if it worked
        await new Promise(resolve => setTimeout(resolve, 100));
        const video = document.querySelector('video');
        if (video) {
            console.log(`Volume after wheel event: ${(video.volume * 100).toFixed(0)}%`);
        }
        return;
    }
    
    // Method 3: Try clicking volume down areas (controls should now be visible)
    const volumeControls = [
        '.ytp-volume-slider',
        '.ytp-volume-panel',
        '.ytp-volume-area .ytp-volume-slider',
        'div[class*="volume"] input[type="range"]'
    ];
    
    console.log('Looking for volume controls to click...');
    
    for (const selector of volumeControls) {
        const control = document.querySelector(selector);
        if (control) {
            const isVisible = control.offsetParent !== null;
            console.log(`Found volume control: ${selector}, visible: ${isVisible}`);
            
            if (isVisible) {
                // If it's a range input, decrement its value
                if (control.tagName === 'INPUT' && control.type === 'range') {
                    const currentValue = parseFloat(control.value) || 50;
                    const newValue = Math.max(0, currentValue - 10);
                    control.value = newValue;
                    control.dispatchEvent(new Event('input', { bubbles: true }));
                    control.dispatchEvent(new Event('change', { bubbles: true }));
                    console.log(`Volume range input updated: ${currentValue} → ${newValue}`);
                    return;
                }
                
                // Try clicking on the left side of the slider (for volume down)
                const rect = control.getBoundingClientRect();
                
                // Get current volume to calculate better click position
                const video = document.querySelector('video');
                const currentVolumePercent = video ? video.volume * 100 : 50;
                const targetVolumePercent = Math.max(0, currentVolumePercent - 15);
                
                // Click at position representing target volume
                const clickX = rect.left + (rect.width * (targetVolumePercent / 100));
                const clickY = rect.top + (rect.height / 2);
                
                console.log(`Clicking volume slider at ${targetVolumePercent}% position (${clickX}, ${clickY})`);
                
                control.dispatchEvent(new MouseEvent('click', {
                    clientX: clickX,
                    clientY: clickY,
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
                
                // Also try mousedown/mouseup sequence
                control.dispatchEvent(new MouseEvent('mousedown', {
                    clientX: clickX,
                    clientY: clickY,
                    bubbles: true
                }));
                
                control.dispatchEvent(new MouseEvent('mouseup', {
                    clientX: clickX,
                    clientY: clickY,
                    bubbles: true
                }));
                
                console.log('Volume slider click events dispatched');
                return;
            }
        }
    }
    
    // Method 4: Direct video element manipulation with extensive event triggering
    const video = document.querySelector('video');
    if (video) {
        const currentVolume = video.volume;
        const newVolume = Math.max(0.0, currentVolume - 0.1);
        
        console.log(`Direct video volume change: ${(currentVolume * 100).toFixed(0)}% → ${(newVolume * 100).toFixed(0)}%`);
        
        video.volume = newVolume;
        
        // Dispatch multiple events to ensure YouTube notices
        const events = ['volumechange', 'loadedmetadata', 'canplay', 'progress'];
        events.forEach(eventType => {
            video.dispatchEvent(new Event(eventType, { bubbles: true }));
        });
        
        // Force a UI update by temporarily changing another property
        setTimeout(() => {
            video.dispatchEvent(new Event('timeupdate', { bubbles: true }));
        }, 50);
        
        return;
    }
    
    // Method 5: Enhanced keyboard shortcut with multiple targets
    console.log('Trying enhanced keyboard shortcuts...');
    
    // Focus different possible targets
    const targets = [
        document.querySelector('#movie_player'),
        document.querySelector('.html5-video-player'),
        document.querySelector('video'),
        document.body
    ];
    
    for (const target of targets) {
        if (target) {
            target.focus();
            
            // Try both ArrowDown (YouTube's volume control) and - key
            const keyEvents = [
                { key: 'ArrowDown', code: 'ArrowDown', keyCode: 40 },
                { key: '-', code: 'Minus', keyCode: 189 },
                { key: '_', code: 'Minus', keyCode: 189, shiftKey: true }
            ];
            
            keyEvents.forEach(({ key, code, keyCode, shiftKey = false }) => {
                const event = new KeyboardEvent('keydown', {
                    key: key,
                    code: code,
                    keyCode: keyCode,
                    which: keyCode,
                    shiftKey: shiftKey,
                    bubbles: true,
                    cancelable: true
                });
                
                target.dispatchEvent(event);
            });
            
            console.log(`Keyboard events sent to ${target.tagName || target.constructor.name}`);
        }
    }
}

async function handleYouTubeMute() {
    // Method 1: Direct mute button click - This should update the UI properly
    const muteButtonSelectors = [
        'button.ytp-mute-button',
        '.ytp-mute-button',
        'button[data-title-no-tooltip="Mute"]',
        'button[data-title-no-tooltip="Unmute"]',
        'button[aria-label*="Mute"]',
        'button[aria-label*="Unmute"]',
        '.ytp-volume-area button'
    ];
    
    for (const selector of muteButtonSelectors) {
        const muteButton = document.querySelector(selector);
        if (muteButton && muteButton.offsetParent !== null) { // Check if visible
            // Ensure the button is interactable
            muteButton.focus();
            muteButton.click();
            console.log('YouTube mute button clicked by gesture');
            
            // Give YouTube time to update its UI
            setTimeout(() => {
                const video = document.querySelector('video');
                if (video) {
                    console.log(`YouTube is now ${video.muted ? 'muted' : 'unmuted'}`);
                }
            }, 100);
            return;
        }
    }
    
    // Method 2: Wait for mute button to appear and then click it
    const muteButton = await waitForElement('button.ytp-mute-button', 2000);
    if (muteButton) {
        muteButton.click();
        console.log('YouTube mute button found and clicked by gesture');
        return;
    }
    
    // Method 3: Use keyboard shortcut - most reliable method
    const player = document.querySelector('#movie_player') || document.querySelector('.html5-video-player');
    if (player) {
        // Focus the player to ensure keyboard events work
        player.focus();
        
        // YouTube's official mute shortcut is 'M' key
        const keyEvent = new KeyboardEvent('keydown', {
            key: 'm',
            code: 'KeyM',
            keyCode: 77,
            which: 77,
            bubbles: true,
            cancelable: true
        });
        
        // Send to both player and document
        player.dispatchEvent(keyEvent);
        document.dispatchEvent(keyEvent);
        
        // Also send keyup event for completeness
        const keyUpEvent = new KeyboardEvent('keyup', {
            key: 'm',
            code: 'KeyM',
            keyCode: 77,
            which: 77,
            bubbles: true,
            cancelable: true
        });
        
        player.dispatchEvent(keyUpEvent);
        document.dispatchEvent(keyUpEvent);
        
        console.log('YouTube mute keyboard shortcut (M) triggered by gesture');
        
        // Check result after a short delay
        setTimeout(() => {
            const video = document.querySelector('video');
            if (video) {
                console.log(`YouTube is now ${video.muted ? 'muted' : 'unmuted'} after keyboard shortcut`);
            }
        }, 200);
        return;
    }
    
    // Method 4: Direct video element manipulation as last resort
    const video = document.querySelector('video');
    if (video) {
        const wasMuted = video.muted;
        video.muted = !video.muted;
        
        // Trigger all possible events to notify YouTube
        video.dispatchEvent(new Event('volumechange', { bubbles: true }));
        video.dispatchEvent(new Event('play', { bubbles: true }));
        video.dispatchEvent(new Event('pause', { bubbles: true }));
        
        console.log(`YouTube ${video.muted ? 'muted' : 'unmuted'} by direct video manipulation`);
    }
}

function handleNetflixVolumeUp() {
    // First try direct video element approach
    const video = document.querySelector('video');
    if (video) {
        video.volume = Math.min(1.0, video.volume + 0.1);
        console.log(`Netflix volume set to ${(video.volume * 100).toFixed(0)}% by gesture`);
        return;
    }
    
    // Try Netflix-specific button selectors
    const volumeUpSelectors = [
        'button[data-uia="control-volume-up"]',
        '[aria-label*="Volume up"]',
        '[aria-label*="Increase volume"]'
    ];
    
    let volumeButton = null;
    for (const selector of volumeUpSelectors) {
        volumeButton = document.querySelector(selector);
        if (volumeButton) break;
    }
    
    if (volumeButton) {
        volumeButton.click();
        console.log('Netflix volume up button triggered by gesture');
    } else {
        // Fallback: arrow up
        document.body.dispatchEvent(new KeyboardEvent('keydown', {
            key: 'ArrowUp',
            code: 'ArrowUp',
            keyCode: 38,
            which: 38,
            bubbles: true
        }));
        console.log('Netflix volume up keyboard shortcut triggered by gesture');
    }
}

function handleNetflixVolumeDown() {
    // First try direct video element approach
    const video = document.querySelector('video');
    if (video) {
        video.volume = Math.max(0.0, video.volume - 0.1);
        console.log(`Netflix volume set to ${(video.volume * 100).toFixed(0)}% by gesture`);
        return;
    }
    
    // Try Netflix-specific button selectors
    const volumeDownSelectors = [
        'button[data-uia="control-volume-down"]',
        '[aria-label*="Volume down"]',
        '[aria-label*="Decrease volume"]'
    ];
    
    let volumeButton = null;
    for (const selector of volumeDownSelectors) {
        volumeButton = document.querySelector(selector);
        if (volumeButton) break;
    }
    
    if (volumeButton) {
        volumeButton.click();
        console.log('Netflix volume down button triggered by gesture');
    } else {
        // Fallback: arrow down
        document.body.dispatchEvent(new KeyboardEvent('keydown', {
            key: 'ArrowDown',
            code: 'ArrowDown',
            keyCode: 40,
            which: 40,
            bubbles: true
        }));
        console.log('Netflix volume down keyboard shortcut triggered by gesture');
    }
}

function handleNetflixMute() {
    // First try direct video element approach
    const video = document.querySelector('video');
    if (video) {
        video.muted = !video.muted;
        console.log(`Netflix ${video.muted ? 'muted' : 'unmuted'} by gesture`);
        return;
    }
    
    // Try Netflix-specific button selectors
    const muteSelectors = [
        'button[data-uia="control-mute"]',
        'button[data-uia="control-unmute"]',
        '[aria-label*="Mute"]',
        '[aria-label*="Unmute"]'
    ];
    
    let muteButton = null;
    for (const selector of muteSelectors) {
        muteButton = document.querySelector(selector);
        if (muteButton) break;
    }
    
    if (muteButton) {
        muteButton.click();
        console.log('Netflix mute button triggered by gesture');
    } else {
        // Fallback: try 'm' key
        document.body.dispatchEvent(new KeyboardEvent('keydown', {
            key: 'm',
            code: 'KeyM',
            keyCode: 77,
            which: 77,
            bubbles: true
        }));
        console.log('Netflix mute keyboard shortcut triggered by gesture');
    }
}

function showGestureNotification(message) {
    // Debug YouTube state when gesture is triggered
    if (window.location.href.includes('youtube.com')) {
        debugYouTubeState();
    }
    
    // Create temporary notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 50px;
        right: 10px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        z-index: 10001;
        max-width: 250px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove notification after 2 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 2000);
}

// Add keyboard shortcuts info
function addKeyboardShortcutsInfo() {
    const info = document.createElement('div');
    info.style.cssText = `
        position: fixed;
        bottom: 10px;
        left: 10px;
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 8px;
        border-radius: 4px;
        font-family: Arial, sans-serif;
        font-size: 10px;
        z-index: 9999;
        opacity: 0.6;
    `;
    info.innerHTML = `
        <strong>Gesture Controls:</strong><br>
        🖐️ Palm = Play/Pause<br>
        👍 Thumbs Up = Volume Up<br>
        👎 Thumbs Down = Volume Down<br>
        ✊ Fist = Mute/Unmute
    `;
    document.body.appendChild(info);
    
    // Hide after 5 seconds
    setTimeout(() => {
        if (info.parentNode) {
            info.parentNode.removeChild(info);
        }
    }, 5000);
}

// Show shortcuts info when page loads
setTimeout(addKeyboardShortcutsInfo, 2000);