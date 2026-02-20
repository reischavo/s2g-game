// ============================================
// MOHAWK DEVELOPMENT - LIVE CHAT WIDGET
// Ultra Modern Canlı Destek Sistemi - Socket.IO Entegrasyonu
// ============================================

(function() {
    'use strict';
    
    // Socket.IO bağlantısı
    const socket = io();
    
    // Session ID oluştur (misafir kullanıcılar için)
    let sessionId = localStorage.getItem('chat_session_id');
    if (!sessionId) {
        sessionId = 'guest_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('chat_session_id', sessionId);
    }
    
    // Random kadın müşteri temsilcisi isimleri
    const representativeNames = [
        'Rümeysa', 'Zeynep', 'Ayşe', 'Fatma', 'Elif', 'Merve', 'Selin', 
        'Büşra', 'Esra', 'Gamze', 'Hilal', 'İrem', 'Kübra', 'Melike',
        'Nisa', 'Özge', 'Pınar', 'Rabia', 'Seda', 'Tuğba', 'Yasemin'
    ];
    
    // Her oturum için random temsilci seç ve kaydet
    let representativeName = localStorage.getItem('chat_representative');
    if (!representativeName) {
        representativeName = representativeNames[Math.floor(Math.random() * representativeNames.length)];
        localStorage.setItem('chat_representative', representativeName);
    }
    
    // Live Chat Widget HTML
    const chatHTML = `
        <div id="mohawk-chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; font-family: 'Inter', sans-serif;">
            <!-- Chat Button -->
            <div id="chat-button" style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #7b2cbf, #9d4edd); box-shadow: 0 10px 30px rgba(123, 44, 191, 0.5); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s; animation: pulse 2s infinite; position: relative;">
                <i class="fas fa-comments" style="color: #fff; font-size: 1.5rem;"></i>
                <span id="unread-badge" style="display: none; position: absolute; top: -5px; right: -5px; background: #ff006e; color: #fff; border-radius: 50%; width: 24px; height: 24px; font-size: 0.75rem; font-weight: 700; display: flex; align-items: center; justify-content: center;">0</span>
            </div>
            
            <!-- Chat Window -->
            <div id="chat-window" style="display: none; position: absolute; bottom: 80px; right: 0; width: 380px; height: 550px; background: linear-gradient(135deg, rgba(26, 26, 46, 0.98), rgba(10, 10, 15, 0.98)); backdrop-filter: blur(30px); border: 2px solid rgba(123, 44, 191, 0.5); border-radius: 24px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8); overflow: hidden; animation: slideUp 0.3s ease-out;">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #7b2cbf, #9d4edd); padding: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #fff; font-size: 1.3rem; font-weight: 700; letter-spacing: 0.5px;">
                            ${representativeName}
                        </h3>
                        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9rem; font-weight: 500;">
                            <span id="online-indicator" style="display: inline-block; width: 8px; height: 8px; background: #06ffa5; border-radius: 50%; margin-right: 0.5rem; animation: blink 1.5s infinite;"></span>
                            Müşteri Temsilcisi
                        </p>
                    </div>
                    <button id="close-chat" style="background: none; border: none; color: #fff; font-size: 1.5rem; cursor: pointer; opacity: 0.8; transition: all 0.3s;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <!-- Messages -->
                <div id="chat-messages" style="height: 380px; overflow-y: auto; padding: 1.5rem; background: rgba(10, 10, 15, 0.5);">
                    <div id="welcome-message" style="text-align: center; padding: 3rem 1.5rem; color: #888;">
                        <div style="width: 80px; height: 80px; margin: 0 auto 1.5rem; background: linear-gradient(135deg, #7b2cbf, #9d4edd); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(123, 44, 191, 0.4);">
                            <i class="fas fa-user-circle" style="font-size: 3rem; color: #fff;"></i>
                        </div>
                        <p style="margin: 0; font-size: 1.1rem; color: #fff; font-weight: 600;">Merhaba!</p>
                        <p style="margin: 1rem 0 0 0; font-size: 0.95rem; color: #aaa; line-height: 1.6;">Size nasıl yardımcı olabilirim?</p>
                    </div>
                </div>
                
                <!-- Input -->
                <div style="padding: 1rem; background: rgba(26, 26, 46, 0.8); border-top: 1px solid rgba(123, 44, 191, 0.3);">
                    <div style="display: flex; gap: 0.75rem;">
                        <input type="text" id="chat-input" placeholder="Mesajınızı yazın..." style="flex: 1; padding: 0.85rem 1rem; background: rgba(10, 10, 15, 0.8); border: 2px solid rgba(123, 44, 191, 0.3); border-radius: 12px; color: #fff; font-size: 0.95rem; outline: none; transition: all 0.3s;">
                        <button id="send-message" style="padding: 0.85rem 1.25rem; background: linear-gradient(135deg, #7b2cbf, #9d4edd); border: none; border-radius: 12px; color: #fff; font-size: 1rem; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 15px rgba(123, 44, 191, 0.4);">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                    <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <button class="quick-reply" data-message="Hesap satın almak istiyorum" style="padding: 0.5rem 1rem; background: rgba(123, 44, 191, 0.2); border: 1px solid rgba(123, 44, 191, 0.5); border-radius: 20px; color: #9d4edd; font-size: 0.8rem; cursor: pointer; transition: all 0.3s;">
                            Hesap Satın Al
                        </button>
                        <button class="quick-reply" data-message="Ödeme sorunu yaşıyorum" style="padding: 0.5rem 1rem; background: rgba(123, 44, 191, 0.2); border: 1px solid rgba(123, 44, 191, 0.5); border-radius: 20px; color: #9d4edd; font-size: 0.8rem; cursor: pointer; transition: all 0.3s;">
                            Ödeme Sorunu
                        </button>
                        <button class="quick-reply" data-message="Hesap teslim süresi ne kadar?" style="padding: 0.5rem 1rem; background: rgba(123, 44, 191, 0.2); border: 1px solid rgba(123, 44, 191, 0.5); border-radius: 20px; color: #9d4edd; font-size: 0.8rem; cursor: pointer; transition: all 0.3s;">
                            Teslimat Süresi
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            @keyframes pulse {
                0%, 100% { transform: scale(1); box-shadow: 0 10px 30px rgba(123, 44, 191, 0.5); }
                50% { transform: scale(1.05); box-shadow: 0 15px 40px rgba(123, 44, 191, 0.7); }
            }
            
            @keyframes slideUp {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            #chat-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            #chat-messages::-webkit-scrollbar-track {
                background: rgba(10, 10, 15, 0.5);
            }
            
            #chat-messages::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #7b2cbf, #9d4edd);
                border-radius: 3px;
            }
            
            #chat-input:focus {
                border-color: #7b2cbf;
                box-shadow: 0 0 0 3px rgba(123, 44, 191, 0.2);
            }
            
            #send-message:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(123, 44, 191, 0.6);
            }
            
            .quick-reply:hover {
                background: rgba(123, 44, 191, 0.3);
                border-color: #7b2cbf;
                transform: translateY(-2px);
            }
            
            #chat-button:hover {
                transform: scale(1.1);
            }
            
            @media (max-width: 768px) {
                #chat-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 100px);
                    right: 20px;
                    left: 20px;
                }
            }
        </style>
    `;
    
    // Widget'ı sayfaya ekle
    document.addEventListener('DOMContentLoaded', function() {
        document.body.insertAdjacentHTML('beforeend', chatHTML);
        
        const chatButton = document.getElementById('chat-button');
        const chatWindow = document.getElementById('chat-window');
        const closeChat = document.getElementById('close-chat');
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-message');
        const chatMessages = document.getElementById('chat-messages');
        const quickReplies = document.querySelectorAll('.quick-reply');
        const welcomeMessage = document.getElementById('welcome-message');
        
        // Socket.IO event listeners
        socket.on('connect', () => {
            console.log('✅ Socket.IO connected');
            socket.emit('join_chat', { session_id: sessionId });
        });
        
        socket.on('admin_reply', (data) => {
            console.log('📨 Admin reply received:', data);
            addMessage(data.message, 'admin', representativeName);
            
            // Chat kapalıysa bildirim göster
            if (chatWindow.style.display === 'none') {
                showUnreadBadge();
            }
        });
        
        // Önceki mesajları yükle
        loadPreviousMessages();
        
        // Chat aç/kapat
        chatButton.addEventListener('click', function() {
            const isOpen = chatWindow.style.display !== 'none';
            chatWindow.style.display = isOpen ? 'none' : 'block';
            if (!isOpen) {
                chatInput.focus();
                hideUnreadBadge();
            }
        });
        
        closeChat.addEventListener('click', function() {
            chatWindow.style.display = 'none';
        });
        
        // Mesaj gönder
        async function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            chatInput.value = '';
            
            try {
                const response = await fetch('/api/chat/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        session_id: sessionId
                    })
                });
                
                const result = await response.json();
                if (!result.success) {
                    console.error('Mesaj gönderilemedi:', result.message);
                }
            } catch (error) {
                console.error('Hata:', error);
            }
        }
        
        sendButton.addEventListener('click', sendMessage);
        
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Hızlı yanıtlar
        quickReplies.forEach(button => {
            button.addEventListener('click', function() {
                const message = this.getAttribute('data-message');
                chatInput.value = message;
                sendMessage();
            });
        });
        
        // Mesaj ekle
        function addMessage(text, sender, senderName = null) {
            // Welcome message'ı kaldır
            if (welcomeMessage) {
                welcomeMessage.remove();
            }
            
            const messageDiv = document.createElement('div');
            messageDiv.style.cssText = `
                margin-bottom: 1.5rem;
                display: flex;
                flex-direction: column;
                ${sender === 'user' ? 'align-items: flex-end;' : 'align-items: flex-start;'}
            `;
            
            // Admin mesajında temsilci ismini göster
            if (sender === 'admin' && senderName) {
                const nameTag = document.createElement('div');
                nameTag.style.cssText = `
                    font-size: 0.8rem;
                    color: #9d4edd;
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    padding: 0 0.5rem;
                `;
                nameTag.textContent = senderName + ' - Müşteri Temsilcisi';
                messageDiv.appendChild(nameTag);
            }
            
            const bubble = document.createElement('div');
            bubble.style.cssText = `
                max-width: 75%;
                padding: 1rem 1.5rem;
                border-radius: ${sender === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px'};
                ${sender === 'user' 
                    ? 'background: linear-gradient(135deg, #7b2cbf, #9d4edd); color: #fff; box-shadow: 0 4px 15px rgba(123, 44, 191, 0.3);' 
                    : 'background: rgba(26, 26, 46, 0.9); color: #fff; border: 1px solid rgba(123, 44, 191, 0.4); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);'}
                font-size: 0.95rem;
                line-height: 1.6;
                animation: slideUp 0.3s ease-out;
                position: relative;
            `;
            
            bubble.textContent = text;
            messageDiv.appendChild(bubble);
            
            // Zaman damgası
            const timeStamp = document.createElement('div');
            timeStamp.style.cssText = `
                font-size: 0.75rem;
                color: #666;
                margin-top: 0.5rem;
                padding: 0 0.5rem;
            `;
            const now = new Date();
            timeStamp.textContent = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
            messageDiv.appendChild(timeStamp);
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Önceki mesajları yükle
        async function loadPreviousMessages() {
            try {
                const response = await fetch(`/api/chat/messages?session_id=${sessionId}`);
                const result = await response.json();
                
                if (result.success && result.messages.length > 0) {
                    result.messages.forEach(msg => {
                        addMessage(msg.message, msg.sender_type, msg.sender_type === 'admin' ? representativeName : null);
                    });
                }
            } catch (error) {
                console.error('Mesajlar yüklenemedi:', error);
            }
        }
        
        // Okunmamış mesaj badge'i
        function showUnreadBadge() {
            const badge = document.getElementById('unread-badge');
            if (badge) {
                badge.style.display = 'flex';
                const current = parseInt(badge.textContent) || 0;
                badge.textContent = current + 1;
            }
        }
        
        function hideUnreadBadge() {
            const badge = document.getElementById('unread-badge');
            if (badge) {
                badge.style.display = 'none';
                badge.textContent = '0';
            }
        }
    });
})();
