// Alpine.js composant pour l'upload d'avatar (connexion backend)
function avatarUpload() {
  return {
    avatarUrl: document.body.getAttribute('data-avatar-url') || '',
    onFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('avatar', file);

      fetch('/profile/avatar', {
        method: 'POST',
        body: formData,
        // Headers CSRF si nécessaire, ex: 'X-CSRFToken': '{{ csrf_token() }}'
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          this.avatarUrl = data.avatar_url + '?t=' + new Date().getTime(); // Cache busting
        } else {
          console.error('Upload failed:', data.error);
          alert('Erreur lors de l'upload: ' + data.error);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Une erreur réseau est survenue.');
      });
    },
    removeAvatar() {
      // TODO: Appeler un endpoint backend pour supprimer le fichier
      this.avatarUrl = '';
      // Pour l'instant, on ne fait que vider l'URL côté client
    }
  }
}

// Alpine.js composant pour le formulaire profil (stockage local)
function profileForm() {
  return {
    profile: {
      nom: localStorage.getItem('profile_nom') || '',
      bio: localStorage.getItem('profile_bio') || '',
      competences: localStorage.getItem('profile_competences') || '',
    },
    saveProfile() {
      localStorage.setItem('profile_nom', this.profile.nom);
      localStorage.setItem('profile_bio', this.profile.bio);
      localStorage.setItem('profile_competences', this.profile.competences);
      alert('Profil enregistré !');
    }
  }
}

// Alpine.js component for user preferences (localStorage)
function userPreferences() {
  return {
    preferences: {
      notifications: JSON.parse(localStorage.getItem('preferences_notifications')) || { email: true },
      language: localStorage.getItem('preferences_language') || 'fr',
    },
    init() {
      this.$watch('preferences', (value) => {
        localStorage.setItem('preferences_notifications', JSON.stringify(value.notifications));
        localStorage.setItem('preferences_language', value.language);
      }, { deep: true });
    },
    toggleNotification(type) {
        if(this.preferences.notifications[type] === undefined) {
          this.preferences.notifications[type] = true;
        } else {
          this.preferences.notifications[type] = !this.preferences.notifications[type];
        }
    }
  }
}

document.addEventListener('alpine:init', () => {
  feather.replace();
});
