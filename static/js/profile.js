// Alpine.js component for avatar upload (backend connection)
function avatarUpload() {
  return {
    avatarUrl: '',
    loading: false,
    
    init() {
      // Get initial avatar URL from the user data
      this.avatarUrl = document.body.getAttribute('data-avatar-url') || '';
    },
    
    onFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;

      this.loading = true;
      const formData = new FormData();
      formData.append('avatar', file);

      fetch('/projects/profile/avatar', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.avatarUrl = data.avatar_url + '?t=' + new Date().getTime();
          showNotification('success', 'Succès', 'Avatar mis à jour avec succès');
        } else {
          showNotification('error', 'Erreur', data.error || 'Erreur lors de l\'upload');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('error', 'Erreur', 'Une erreur réseau est survenue');
      })
      .finally(() => {
        this.loading = false;
      });
    },
    
    removeAvatar() {
      if (confirm('Êtes-vous sûr de vouloir supprimer votre avatar ?')) {
        // For now, just clear the avatar
        this.avatarUrl = '';
        // TODO: Add backend endpoint to remove avatar
      }
    }
  }
}

// Alpine.js component for profile form (DB sync)
function profileForm() {
  return {
    profile: {
      first_name: '',
      last_name: '',
      bio: '',
    },
    loading: false,
    
    init() {
      // Load initial data from the page
      const userData = window.userData || {};
      this.profile.first_name = userData.first_name || '';
      this.profile.last_name = userData.last_name || '';
      this.profile.bio = userData.bio || '';
    },
    
    saveProfile() {
      this.loading = true;
      
      fetch('/projects/profile/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.profile)
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification('success', 'Succès', data.message);
        } else {
          showNotification('error', 'Erreur', data.error || 'Erreur lors de la sauvegarde');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('error', 'Erreur', 'Une erreur est survenue');
      })
      .finally(() => {
        this.loading = false;
      });
    }
  }
}

// Alpine.js component for user preferences
function userPreferences() {
  return {
    preferences: {
      notifications: { email: true, push: false },
      language: 'fr',
    },
    
    init() {
      // Load preferences from localStorage
      const savedNotifications = localStorage.getItem('preferences_notifications');
      const savedLanguage = localStorage.getItem('preferences_language');
      
      if (savedNotifications) {
        this.preferences.notifications = JSON.parse(savedNotifications);
      }
      if (savedLanguage) {
        this.preferences.language = savedLanguage;
      }
      
      // Watch for changes and save to localStorage
      this.$watch('preferences', (value) => {
        localStorage.setItem('preferences_notifications', JSON.stringify(value.notifications));
        localStorage.setItem('preferences_language', value.language);
        // In the future, also sync with backend
      }, { deep: true });
    },
    
    toggleNotification(type) {
      this.preferences.notifications[type] = !this.preferences.notifications[type];
    }
  }
}