// Composant de gestion des fichiers

// Classe FileManager
export class FileManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.files = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadFiles();
    }

    setupEventListeners() {
        // Gestionnaire pour le bouton de partage de fichier
        document.getElementById('share-file-button')?.addEventListener('click', () => {
            this.showShareModal();
        });

        // Gestionnaire pour le formulaire de partage
        document.getElementById('share-file-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFileShare(e);
        });
    }

    async loadFiles() {
        try {
            const response = await fetch('/api/files');
            const data = await response.json();
            this.files = data;
            this.renderFiles();
        } catch (error) {
            console.error('Erreur lors du chargement des fichiers:', error);
            this.showError('Erreur lors du chargement des fichiers');
        }
    }

    renderFiles() {
        if (!this.container) return;

        this.container.innerHTML = '';
        
        if (this.files.length === 0) {
            this.container.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-gray-500">Aucun fichier partagé pour le moment</p>
                </div>
            `;
            return;
        }

        this.files.forEach(file => {
            const fileElement = this.createFileElement(file);
            this.container.appendChild(fileElement);
        });
    }

    createFileElement(file) {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'file-item bg-white rounded-lg shadow-sm p-4 mb-4';
        fileDiv.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-semibold text-lg mb-2">${file.name}</h3>
                    <p class="text-sm text-gray-600">${file.description || 'Pas de description'}</p>
                    <div class="flex items-center mt-2 text-sm">
                        <span class="text-gray-500">Type: </span>
                        <span class="font-medium">${file.type}</span>
                    </div>
                    <div class="flex items-center mt-1 text-sm">
                        <span class="text-gray-500">Partagé par: </span>
                        <span class="font-medium">${file.shared_by?.name || 'Non spécifié'}</span>
                    </div>
                </div>
                <div class="flex flex-col items-end space-y-2">
                    <button onclick="downloadFile('${file.id}')" 
                            class="bg-primary text-white px-4 py-2 rounded-md hover:bg-secondary transition-colors">
                        Télécharger
                    </button>
                </div>
            </div>
        `;
        return fileDiv;
    }

    async handleFileShare(e) {
        const formData = new FormData(e.target);
        try {
            const response = await fetch('/api/files', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                this.showSuccess('Fichier partagé avec succès');
                this.loadFiles();
                this.hideShareModal();
            } else {
                throw new Error('Erreur lors du partage du fichier');
            }
        } catch (error) {
            console.error('Erreur lors du partage:', error);
            this.showError('Erreur lors du partage du fichier');
        }
    }

    showShareModal() {
        const modal = document.getElementById('shareFileModal');
        if (modal) {
            modal.style.display = 'block';
        }
    }

    hideShareModal() {
        const modal = document.getElementById('shareFileModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    showSuccess(message) {
        const notification = document.createElement('div');
        notification.className = 'success-notification bg-green-100 text-green-800 p-4 rounded-lg mb-4';
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    showError(message) {
        const notification = document.createElement('div');
        notification.className = 'error-notification bg-red-100 text-red-800 p-4 rounded-lg mb-4';
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
}

// Fonction utilitaire pour télécharger un fichier
async function downloadFile(fileId) {
    try {
        const response = await fetch(`/api/files/${fileId}/download`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.headers.get('content-disposition')?.split('filename=')[1] || `file-${fileId}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Erreur lors du téléchargement:', error);
        new FileManager('files-container').showError('Erreur lors du téléchargement du fichier');
    }
}
