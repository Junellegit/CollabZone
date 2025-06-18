# CollabZone - Plan de Développement Complet 

## Phase 1 : Amélioration de l'UI/UX (Terminée)

### 1.1 Design System Moderne
- [x] **Palette de couleurs** : Dégradés modernes (violet → bleu, orange → rose)
- [x] **Animations** : Transitions fluides, hover effects, loading states
- [x] **Dark mode** : Support du thème sombre
- [x] **Composants réutilisables** : Cards, boutons, modals
- [x] **Typographie** : Inter ou Poppins depuis Google Fonts
- [x] **Icons** : Heroicons ou Feather Icons

### 1.2 Dashboard Amélioré
- [x] **Stats cards** avec animations au chargement
- [x] **Graphiques** de progression des projets (Chart.js)
- [x] **Timeline** des activités récentes
- [x] **Quick actions** : Créer projet, ajouter tâche
- [x] **Filtres et recherche** intelligente

### 1.3 Notifications
- [x] **Toast notifications** (succès, erreur, info)
- [x] **Badge de notifications** dans la navbar
- [x] **Centre de notifications** avec historique
- [x] **Notifications temps réel** via WebSocket
- [x] **Sons subtils** pour les notifications importantes

---

## Phase 2 : Système de Profil (EN COURS)

### Checklist d'avancement
- [x] **Page profil utilisateur** : Intégration de la page `profile.html` dans Flask.
- [x] **Upload d'avatar (frontend)** : Gestion complète côté client (preview, suppression) avec `localStorage`.
- [x] **Formulaire profil (frontend)** : Formulaire pour la bio et les compétences, sauvegardé dans `localStorage`.
- [x] **Stats et timeline (mock)** : Affichage de données fictives pour les statistiques et l'activité.
- [x] **Gestion des préférences utilisateur (frontend)** : UI pour le mode sombre, notifications et langue, sauvegardée dans `localStorage`.
- [x] **Harmonisation UI/UX** : Refonte des pages login/signup et de la navbar pour une cohérence globale.
- [ ] **Endpoint Flask pour l'upload d'avatar (API REST)** : Le backend n'est pas encore connecté.
- [x] **Documentation et changelog phase 2** : Le présent document a été mis à jour.

### Changelog Phase 2
- **Backend** : Ajout de la route Flask `/profile` pour servir la page profil utilisateur et correction du `BuildError`.
- **UI/UX** : 
  - Refonte complète de la **navbar** avec intégration du logo et amélioration de la visibilité des boutons.
  - Refonte des pages **login** et **signup** pour correspondre au design system (glassmorphism, dark mode, responsive).
  - Création de la page **profil** avec upload d'avatar, formulaire et statistiques (données mock).
- **Fonctionnalités** : Ajout de la section **Préférences utilisateur** sur la page profil pour gérer le mode sombre, les notifications et la langue. Les préférences sont stockées localement (`localStorage`).

### Documentation : Upload d'Avatar (Frontend)
- **Fichier concerné** : `templates/profile.html`
- **Composant Alpine.js** : `avatarUpload()`
- **Fonctionnement** : L'image sélectionnée par l'utilisateur est lue par le `FileReader` et convertie en une chaîne de caractères **Base64**. Cette chaîne est ensuite stockée dans le `localStorage` sous la clé `avatarUrl`. L'image n'est **pas** envoyée à un serveur. Le composant gère l'affichage de l'aperçu, le changement d'image et sa suppression du `localStorage`.

> **Note :** La Phase 2 a permis de construire toutes les fonctionnalités du profil utilisateur côté frontend. La prochaine étape majeure sera de connecter ces fonctionnalités à un backend robuste.

## 📋 Phase 3 : Gestion Avancée des Projets

### 3.1 Vue Projet avec Onglets
```
[Vue Kanban] [Membres] [Fichiers] [Chat] [Paramètres]
```

### 3.2 Onglet Kanban Amélioré
- **Création de tâches** : Modal avec formulaire complet
  - Titre, description, priorité, deadline
  - Assignation multiple
  - Tags/Labels colorés
  - Pièces jointes
- **Drag & Drop** amélioré avec preview
- **Filtres** : Par assigné, priorité, tags
- **Vue calendrier** alternative
- **Sous-tâches** et dépendances

### 3.3 Onglet Membres
- **Liste des membres** avec rôles et status (en ligne/hors ligne)
- **Permissions granulaires** :
  - Admin : Tout
  - Prof : Gérer membres, modifier projet
  - Étudiant : Contribuer
- **Invitations** par email ou lien
- **Historique** des changements de rôles

### 3.4 Onglet Fichiers
- **Upload drag & drop** multiple
- **Prévisualisation** (images, PDF, vidéos)
- **Dossiers** et organisation
- **Versioning** des fichiers
- **Commentaires** sur les fichiers
- **Recherche** dans les fichiers

### 3.5 Onglet Chat
- **Messages en temps réel** avec WebSocket
- **Indicateur "typing..."** 
- **Réactions emoji** aux messages
- **Mentions** @username
- **Formatage** : Markdown, code blocks
- **Partage de fichiers** dans le chat
- **Historique** searchable
- **Notifications sonores** optionnelles

## 🔔 Phase 4 : Système de Notifications

### 4.1 Types de Notifications
- **Projet** : Nouveau membre, deadline proche
- **Tâche** : Assignation, changement de status
- **Chat** : Mentions, messages directs
- **Fichiers** : Nouveau upload, commentaire

### 4.2 Canaux de Notification
- **In-app** : Toasts et badges
- **Email** : Digest quotidien/hebdomadaire
- **Push** : Notifications navigateur (optionnel)

## 🎯 Phase 5 : Fonctionnalités Avancées

### 5.1 Analytics et Rapports
- **Burndown charts** pour les projets
- **Velocity tracking** de l'équipe
- **Export PDF** des rapports
- **Tableaux de bord** personnalisables

### 5.2 Intégrations
- **GitHub/GitLab** : Lier les commits aux tâches
- **Google Calendar** : Sync des deadlines
- **Slack/Discord** : Notifications externes

### 5.3 Mobile Responsive
- **PWA** : Installation sur mobile
- **Touch gestures** pour le Kanban
- **Navigation** adaptée mobile

## 💻 Stack Technique Recommandée

### Frontend
- **Alpine.js** : Pour l'interactivité (léger, pas de build)
- **HTMX** : Pour les updates partielles
- **Chart.js** : Graphiques
- **Sortable.js** : Drag & drop (déjà en place)
- **Tailwind CSS** : Styling (déjà en place)

### Backend (déjà en place)
- **Flask** + **Flask-SocketIO**
- **SQLAlchemy** + **SQLite**
- **Flask-Login** pour l'auth

### Nouvelles dépendances
- **Flask-Mail** : Envoi d'emails
- **Pillow** : Traitement d'images
- **PyJWT** : Tokens pour API
- **Flask-Limiter** : Rate limiting

## 🚀 Ordre de Développement Suggéré

1. **Semaine 1-2** : UI/UX moderne + Dashboard
2. **Semaine 3** : Profil utilisateur + Paramètres
3. **Semaine 4** : Création/édition de tâches
4. **Semaine 5** : Système de membres et permissions
5. **Semaine 6** : Chat temps réel amélioré
6. **Semaine 7** : Gestion des fichiers
7. **Semaine 8** : Notifications et polish final

## 🎁 Fonctionnalités Bonus

- **Templates de projets** : Démarrage rapide
- **Pomodoro timer** intégré aux tâches
- **Mode focus** : Masquer les distractions
- **Shortcuts clavier** : Navigation rapide
- **API REST** : Pour intégrations futures
- **Webhooks** : Automatisations
- **Mode présentation** : Pour les démos