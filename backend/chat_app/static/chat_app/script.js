/**
 * Culina AI Chat Interface - Production-ready JavaScript
 * Handles chat UI interactions, message display, and API communication
 * 
 * Command: Loads automatically when index.html is rendered
 * Command: Sends messages via GET /api/chat/?message=<message>
 */

// Command: Initialize chat interface on page load
window.addEventListener('DOMContentLoaded', function() {
    addWelcomeMessage();
    initializeAnimations();
    updateStatusIndicator();
});

// Command: Initialize UI animations and status updates
function initializeAnimations() {
    // Add entrance animation to container
    const container = document.querySelector('.chat-container');
    container.style.animation = 'containerFadeIn 0.8s ease-out';
    
    // Initialize real-time status updates (every 5 seconds)
    setInterval(updateStatusIndicator, 5000);
}

function updateStatusIndicator() {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');
    
    // Simulate real-time status (you can replace with actual connection status)
    if (statusDot && statusText) {
        statusDot.style.animation = 'statusPulse 2s ease-in-out infinite';
        statusText.textContent = 'Online';
    }
}

function addWelcomeMessage() {
    const chatBox = document.getElementById("chat-box");
    setTimeout(() => {
        const welcomeMessage = createAIMessage("Welcome I'm Culina AI , your cooking assistant. I can help you with recipes, cooking tips, meal planning, and any food-related questions. How can I assist you today?");
        chatBox.appendChild(welcomeMessage);
        scrollToBottom();
    }, 500);
}

function createUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = getCurrentTime();
    
    content.appendChild(timestamp);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    return messageDiv;
}

function createAIMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '<i class="fas fa-mortar-pestle"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = getCurrentTime();
    
    content.appendChild(timestamp);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    return messageDiv;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

function createTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.id = 'typing-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '<i class="fas fa-mortar-pestle"></i>';
    
    const dots = document.createElement('div');
    dots.className = 'typing-dots';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        dots.appendChild(dot);
    }
    
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(dots);
    
    return typingDiv;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function typeMessage(element, text, speed = 30) {
    return new Promise((resolve) => {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                resolve();
            }
        }
        
        type();
    });
}

function scrollToBottom() {
    const chatBox = document.getElementById("chat-box");
    requestAnimationFrame(() => {
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: 'smooth'
        });
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function createRippleEffect(button) {
    const ripple = document.createElement('div');
    ripple.className = 'button-ripple';
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Command: Send user message to backend API and display response
// Command: GET /api/chat/?message=<encoded_message>
async function sendMessage() {
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const message = input.value.trim();
    
    if (!message) return;

    // Create ripple effect
    createRippleEffect(sendBtn);

    // Disable input and button
    input.disabled = true;
    sendBtn.disabled = true;
    sendBtn.style.opacity = '0.6';

    // Show user message with animation
    const chatBox = document.getElementById("chat-box");
    const userMessage = createUserMessage(message);
    chatBox.appendChild(userMessage);
    input.value = "";
    
    // Smooth scroll
    setTimeout(scrollToBottom, 100);

    // Show typing indicator
    setTimeout(() => {
        const typingIndicator = createTypingIndicator();
        chatBox.appendChild(typingIndicator);
        scrollToBottom();
    }, 300);

    try {
        // Send message to backend API
        const response = await fetch(`/api/chat/?message=${encodeURIComponent(message)}`);
        const data = await response.json();

        // Remove typing indicator with fade out
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                typingIndicator.remove();
            }, 300);
        }

        // Create AI message with typing effect
        const aiMessage = document.createElement('div');
        aiMessage.className = 'message ai';
        aiMessage.style.opacity = '0';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-mortar-pestle"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        aiMessage.appendChild(avatar);
        aiMessage.appendChild(content);
        chatBox.appendChild(aiMessage);
        
        // Fade in message
        setTimeout(() => {
            aiMessage.style.transition = 'opacity 0.3s ease-in';
            aiMessage.style.opacity = '1';
        }, 50);
        
        // Type out the message with real-time effect
        await typeMessage(content, data.response, 15);
        
        // Add timestamp after typing
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = getCurrentTime();
        content.appendChild(timestamp);
        
        scrollToBottom();

    } catch (error) {
        console.error('Error:', error);
        
        // Remove typing indicator
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        
        const errorMessage = createAIMessage("Sorry, I encountered an error. Please try again.");
        chatBox.appendChild(errorMessage);
        scrollToBottom();
    } finally {
        // Re-enable input and button
        input.disabled = false;
        sendBtn.disabled = false;
        sendBtn.style.opacity = '1';
        input.focus();
    }
}

// Add fade out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.9);
        }
    }
`;
document.head.appendChild(style);
