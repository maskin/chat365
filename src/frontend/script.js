document.addEventListener('DOMContentLoaded', () => {

    const addBroadcastBtn = document.getElementById('addBroadcastBtn');
    const modal = document.getElementById('addModal');
    const closeBtn = document.querySelector('.close-btn');
    const addForm = document.getElementById('addForm');
    const broadcastList = document.getElementById('broadcastList');
    const recordBtn = document.getElementById('recordBtn');

    const API_URL = 'http://127.0.0.1:5001/api';

    // --- Modal Logic ---
    addBroadcastBtn.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // --- API Functions ---
    async function loadBroadcasts() {
        try {
            const response = await fetch(`${API_URL}/broadcasts`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const broadcasts = await response.json();
            
            broadcastList.innerHTML = ''; // Clear existing list
            broadcasts.forEach(b => {
                const item = document.createElement('div');
                item.className = 'broadcast-item';
                item.innerHTML = `
                    <div>
                        <strong>${new Date(b.scheduled_at).toLocaleString()}</strong>
                        <p>${b.content.substring(0, 100)}...</p>
                        <small>Priority: ${b.priority} | Status: ${b.status}</small>
                    </div>
                    <div>
                        <button>Delete</button>
                    </div>
                `;
                broadcastList.appendChild(item);
            });
        } catch (error) {
            console.error("Failed to load broadcasts:", error);
            broadcastList.innerHTML = '<p>Error loading broadcasts.</p>';
        }
    }

    addForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(addForm);
        const data = {
            content: formData.get('content'),
            scheduled_at: new Date(formData.get('scheduled_at')).toISOString(),
            priority: parseInt(formData.get('priority'), 10)
        };

        try {
            const response = await fetch(`${API_URL}/broadcasts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            modal.style.display = 'none';
            addForm.reset();
            loadBroadcasts(); // Refresh the list

        } catch (error) {
            console.error("Failed to create broadcast:", error);
            alert('Error creating broadcast.');
        }
    });

    // --- Voice Recognition (Placeholder) ---
    recordBtn.addEventListener('click', () => {
        alert('音声認識機能は現在開発中です。');
        // TODO: Implement Web Speech API (SpeechRecognition)
    });

    // Initial load
    loadBroadcasts();
});
