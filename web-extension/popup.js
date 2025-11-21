document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusIndicator = document.getElementById('statusIndicator');
    const siteStatus = document.getElementById('siteStatus');
    
    // Initialize popup
    updateStatus();
    checkCurrentSite();
    
    // Button event listeners
    startBtn.addEventListener('click', function() {
        chrome.runtime.sendMessage({action: 'startGestureDetection'}, function(response) {
            console.log('Started gesture detection:', response);
            updateStatus();
        });
    });
    
    stopBtn.addEventListener('click', function() {
        chrome.runtime.sendMessage({action: 'stopGestureDetection'}, function(response) {
            console.log('Stopped gesture detection:', response);
            updateStatus();
        });
    });
    
    function updateStatus() {
        chrome.runtime.sendMessage({action: 'getStatus'}, function(response) {
            if (response && response.isListening) {
                statusIndicator.classList.add('active');
                startBtn.style.display = 'none';
                stopBtn.style.display = 'block';
            } else {
                statusIndicator.classList.remove('active');
                startBtn.style.display = 'block';
                stopBtn.style.display = 'none';
            }
        });
    }
    
    function checkCurrentSite() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs.length > 0) {
                const url = tabs[0].url;
                if (url.includes('youtube.com')) {
                    siteStatus.textContent = 'YouTube ✓';
                    siteStatus.className = 'supported-site';
                } else if (url.includes('netflix.com')) {
                    siteStatus.textContent = 'Netflix ✓';
                    siteStatus.className = 'supported-site';
                } else {
                    siteStatus.textContent = 'Not Supported';
                    siteStatus.className = 'unsupported-site';
                }
            }
        });
    }
    
    // Update status periodically
    setInterval(updateStatus, 2000);
});