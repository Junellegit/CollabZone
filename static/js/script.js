const socket = io();

// Gestion des tâches
let tasks = [];

function loadTasks() {
    fetch('/api/tasks')
        .then(response => response.json())
        .then(data => {
            tasks = data;
            renderTasks();
        });
}

function renderTasks() {
    const tasksContainer = document.querySelector('.tasks-container');
    if (!tasksContainer) return;
    
    tasksContainer.innerHTML = `
        <div class="bg-white rounded-lg shadow p-4">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold">Tâches</h2>
                <button onclick="openAddTaskModal()" class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    Nouvelle tâche
                </button>
            </div>
            <div class="space-y-4">
                ${tasks.map(task => `
                    <div class="bg-gray-50 p-4 rounded-lg">
                        <div class="flex justify-between items-start">
                            <div>
                                <h3 class="font-semibold">${task.title}</h3>
                                <p class="text-gray-600">${task.description || 'Aucune description'}</p>
                                <p class="text-sm text-gray-500">Status: ${task.status}</p>
                            </div>
                            <div class="flex space-x-2">
                                <button onclick="editTask(${task.id})" class="text-blue-500 hover:text-blue-700">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                                    </svg>
                                </button>
                                <button onclick="deleteTask(${task.id})" class="text-red-500 hover:text-red-700">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Modal pour ajouter une tâche
function openAddTaskModal() {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
    modal.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 class="text-xl font-bold mb-4">Nouvelle tâche</h2>
            <form onsubmit="addTask(event)">
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">Titre</label>
                    <input type="text" id="task-title" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary" required>
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">Description</label>
                    <textarea id="task-description" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary" rows="3"></textarea>
                </div>
                <div class="flex justify-end space-x-2">
                    <button type="button" onclick="closeModal(this)" class="px-4 py-2 text-gray-600 hover:text-gray-800">Annuler</button>
                    <button type="submit" class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary">Créer</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
}

function addTask(event) {
    event.preventDefault();
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;
    
    fetch('/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description })
    })
    .then(response => response.json())
    .then(data => {
        closeModal(event.target.closest('.bg-black'));
        loadTasks();
    });
}

function editTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
    modal.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 class="text-xl font-bold mb-4">Modifier la tâche</h2>
            <form onsubmit="updateTask(event, ${taskId})">
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">Titre</label>
                    <input type="text" id="edit-task-title" value="${task.title}" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary" required>
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">Description</label>
                    <textarea id="edit-task-description" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary" rows="3">${task.description}</textarea>
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 mb-2">Status</label>
                    <select id="edit-task-status" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary">
                        <option value="todo" ${task.status === 'todo' ? 'selected' : ''}>À faire</option>
                        <option value="in-progress" ${task.status === 'in-progress' ? 'selected' : ''}>En cours</option>
                        <option value="completed" ${task.status === 'completed' ? 'selected' : ''}>Terminé</option>
                    </select>
                </div>
                <div class="flex justify-end space-x-2">
                    <button type="button" onclick="closeModal(this)" class="px-4 py-2 text-gray-600 hover:text-gray-800">Annuler</button>
                    <button type="submit" class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary">Mettre à jour</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
}

function updateTask(event, taskId) {
    event.preventDefault();
    const title = document.getElementById('edit-task-title').value;
    const description = document.getElementById('edit-task-description').value;
    const status = document.getElementById('edit-task-status').value;
    
    fetch(`/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description, status })
    })
    .then(response => response.json())
    .then(data => {
        closeModal(event.target.closest('.bg-black'));
        loadTasks();
    });
}

function deleteTask(taskId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) return;
    
    fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        loadTasks();
    });
}

function closeModal(element) {
    element.remove();
}

// Gestion des messages
function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value;
    if (message) {
        socket.emit('message', message);
        input.value = '';
    }
}

socket.on('message', (msg) => {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.textContent = msg;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
});

// Gestion du dropdown de la navbar
document.getElementById('user-menu-button').addEventListener('click', () => {
    const menu = document.getElementById('user-menu');
    menu.classList.toggle('hidden');
});

// Gestion du menu flottant
document.getElementById('floating-menu-button').addEventListener('click', () => {
    const menu = document.getElementById('floating-menu');
    menu.classList.toggle('hidden');
});

// Fermer les menus en cliquant ailleurs
document.addEventListener('click', (e) => {
    const userMenu = document.getElementById('user-menu');
    const userButton = document.getElementById('user-menu-button');
    const floatingMenu = document.getElementById('floating-menu');
    const floatingButton = document.getElementById('floating-menu-button');
    
    // Fermer le menu utilisateur
    if (!userButton.contains(e.target) && !userMenu.contains(e.target)) {
        userMenu.classList.add('hidden');
    }
    
    // Fermer le menu flottant
    if (!floatingButton.contains(e.target) && !floatingMenu.contains(e.target)) {
        floatingMenu.classList.add('hidden');
    }
});

// Gestion de l'ouverture des onglets
function openTab(tabName) {
    // Masquer tous les contenus
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Afficher le contenu de l'onglet sélectionné
    document.getElementById(tabName).classList.remove('hidden');
    
    // Afficher le bouton "Nouvelle tâche" uniquement sur l'onglet "Tâches"
    const addTaskBtn = document.getElementById('add-task-btn');
    if (tabName === 'tasks') {
        addTaskBtn.style.display = 'inline-block';
    } else {
        addTaskBtn.style.display = 'none';
    }
    
    // Mettre à jour la liste des tâches si on est sur l'onglet "Tâches"
    if (tabName === 'tasks') {
        updateTasksList();
    }
}

// Fonction pour ouvrir un modal
function openModal(content) {
    const modalContainer = document.getElementById('modal-container');
    const modalContent = document.getElementById('modal-content');
    const modalBackdrop = document.getElementById('modal-backdrop');
    
    modalContent.innerHTML = content;
    modalContainer.classList.remove('hidden');
    
    // Ajouter l'écouteur d'événement pour la fermeture en cliquant sur le backdrop
    modalBackdrop.addEventListener('click', () => {
        closeModal();
    });
    
    // Ajouter l'écouteur d'événement pour la fermeture en appuyant sur Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}

// Fonction pour fermer le modal
function closeModal() {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.add('hidden');
    
    // Supprimer les écouteurs d'événements
    const modalBackdrop = document.getElementById('modal-backdrop');
    modalBackdrop.removeEventListener('click', closeModal);
    document.removeEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}

// Gestion de l'ajout de tâches
document.getElementById('add-task-btn').addEventListener('click', () => {
    const modalContent = `
        <div class="bg-white p-6 rounded-lg shadow w-96">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-lg font-medium">Nouvelle tâche</h2>
                <button type="button" onclick="closeModal()" class="text-gray-400 hover:text-gray-500">
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            <form id="task-form">
                <div class="mb-4">
                    <label for="task-title" class="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                    <input type="text" id="task-title" name="title" 
                           class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300" 
                           required>
                </div>
                <div class="mb-4">
                    <label for="task-description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea id="task-description" name="description"
                              class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
                              rows="3"></textarea>
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="closeModal()" 
                            class="px-4 py-2 text-gray-700 hover:text-gray-900">Annuler</button>
                    <button type="submit" class="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded">Créer</button>
                </div>
            </form>
        </div>
    `;
    openModal(modalContent);

    // Gestion du formulaire de tâche
    document.getElementById('task-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(Object.fromEntries(formData))
            });
            if (response.ok) {
                closeModal();
                // Mettre à jour la liste des tâches
                updateTasksList();
            } else {
                alert('Erreur lors de la création de la tâche');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la création de la tâche');
        }
    });
});

// Gestion de la fermeture du modal en cliquant à l'extérieur
const modalContainer = document.getElementById('modal-container');
const modalBackdrop = document.getElementById('modal-backdrop');

if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
        // Vérifier que l'utilisateur clique directement sur le backdrop
        if (e.target === modalBackdrop) {
            closeModal();
        }
    });
}

// Fonction pour mettre à jour la liste des tâches
async function updateTasksList() {
    try {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        const tasksList = document.getElementById('tasks-list');
        
        if (tasks.length === 0) {
            tasksList.innerHTML = `
                <div class="bg-white p-6 rounded-lg shadow text-center">
                    <p class="text-gray-600">Aucune tâche assignée pour le moment</p>
                </div>
            `;
            return;
        }
        
        tasksList.innerHTML = tasks.map(task => `
            <div class="bg-white p-6 rounded-lg shadow mb-4">
                <div class="flex justify-between items-start">
                    <div>
                        <h3 class="text-lg font-medium">${task.title}</h3>
                        <p class="text-gray-600 mt-2">${task.description || 'Pas de description'}</p>
                        <div class="mt-4">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${getStatusColor(task.status)}-100 text-${getStatusColor(task.status)}-800">
                                ${task.status}
                            </span>
                        </div>
                        <p class="mt-2 text-sm text-gray-500">
                            Créée le ${new Date(task.created_at).toLocaleDateString()}
                        </p>
                    </div>
                    <div class="flex items-center space-x-4">
                        <button onclick="openEditTaskModal(${task.id})" class="text-gray-600 hover:text-gray-900">
                            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                            </svg>
                        </button>
                        <button onclick="deleteTask(${task.id})" class="text-red-600 hover:text-red-900">
                            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Fonction pour obtenir la couleur du statut
function getStatusColor(status) {
    switch (status.toLowerCase()) {
        case 'todo':
            return 'blue';
        case 'in_progress':
            return 'yellow';
        case 'done':
            return 'green';
        default:
            return 'gray';
    }
}

// Fonction pour ouvrir le modal d'édition
function openEditTaskModal(taskId) {
    // À implémenter
    console.log('Éditer la tâche:', taskId);
}

// Fonction pour supprimer une tâche
async function deleteTask(taskId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            updateTasksList();
        } else {
            alert('Erreur lors de la suppression de la tâche');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la suppression de la tâche');
    }
}

// Basculer entre les onglets
function openTab(tabName) {
    // Masquer tous les contenus
    const contents = document.querySelectorAll('.tab-content > div');
    contents.forEach(content => content.classList.add('hidden'));
    
    // Afficher le contenu correspondant
    const content = document.getElementById(tabName);
    if (content) {
        content.classList.remove('hidden');
        
        // Charger les tâches si on ouvre l'onglet des tâches
        if (tabName === 'tasks') {
            loadTasks();
        }
    }
    
    // Mettre à jour l'affichage du bouton d'ajout de tâche
    const addTaskBtn = document.getElementById('add-task-btn');
    if (addTaskBtn) {
        addTaskBtn.classList.add('hidden');
        if (tabName === 'tasks') {
            addTaskBtn.classList.remove('hidden');
        }
    }
    
    // Mettre à jour les boutons d'onglets
    const buttons = document.querySelectorAll('.border-b ul li button');
    buttons.forEach(button => {
        // Supprimer toutes les classes actives
        button.classList.remove('active');
        button.classList.remove('border-primary');
        button.classList.add('border-transparent');
        
        // Mettre à jour le texte et l'effet de survol
        button.classList.remove('text-gray-900');
        button.classList.add('text-gray-500');
        button.classList.add('hover:text-gray-600');
        button.classList.add('hover:border-gray-300');
    });
    
    // Trouver le bouton correspondant et l'activer
    const currentButton = document.querySelector(`button[onclick*="openTab('${tabName}')"]`);
    if (currentButton) {
        // Ajouter les classes actives
        currentButton.classList.add('active');
        currentButton.classList.add('border-primary');
        currentButton.classList.remove('border-transparent');
        
        // Mettre à jour le texte
        currentButton.classList.add('text-gray-900');
        currentButton.classList.remove('text-gray-500');
        currentButton.classList.remove('hover:text-gray-600');
        currentButton.classList.remove('hover:border-gray-300');
    }
}

// Charger les tâches au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});

// Gestion des événements Socket.IO pour les tâches
socket.on('task_added', (task) => {
    tasks.push(task);
    renderTasks();
});

socket.on('task_updated', (task) => {
    const index = tasks.findIndex(t => t.id === task.id);
    if (index !== -1) {
        tasks[index] = task;
        renderTasks();
    }
});

socket.on('task_deleted', (taskId) => {
    tasks = tasks.filter(task => task.id !== taskId);
    renderTasks();
});