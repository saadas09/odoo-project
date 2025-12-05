# Hotel Reservation System - Odoo 16 Module

## Description

Complete hotel reservation management module for Odoo 16 with the following features:

- ✅ Hotel room management
- ✅ Client management
- ✅ Reservation management
- ✅ Automatic price calculation
- ✅ Overlapping reservation prevention
- ✅ Booking.com and Airbnb API synchronization with Mock API for testing
- ✅ Web interface for client reservations
- ✅ Automatic synchronization CRON jobs

## Quick Start with Mock API

### 1. Install Mock API Dependencies

```powershell
cd "C:\Program Files\Odoo 16.0.20230101\server\odoo\addons\hotel_reservation_system\mock_api"
pip install -r requirements.txt
```

### 2. Start Mock API Server

```powershell
uvicorn server:app --reload --port 8000
```

### 3. Configure Odoo

In Odoo, navigate to: **Settings > Technical > Parameters > System Parameters**

Create parameter:
- Key: `hotel_reservation.mock_api_endpoint`
- Value: `http://localhost:8000`

### 4. Create Sample Rooms

Navigate to: **Hotel > Configuration > Rooms**

Create rooms matching the mock API data:
- Room 101 (Deluxe Suite)
- Room 205 (Ocean View Room)
- Room 310 (Family Suite)

### 5. Test Synchronization

Navigate to: **Hotel > Reservations**

Click the buttons in the toolbar:
- **"Sync Booking.com"** - Syncs 3 Booking.com reservations
- **"Sync Airbnb"** - Syncs 3 Airbnb reservations

Check results in: **Hotel > Configuration > API Synchronization**

📖 **Detailed Documentation**: See `mock_api/README.md` for complete mock API documentation.

## Module Structure

```
hotel_reservation_system/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── hotel_room.py
│   ├── hotel_client.py
│   ├── hotel_reservation.py
│   └── api_synchronization.py
├── controllers/
│   ├── __init__.py
│   └── portal.py
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── room_views.xml
│   ├── client_views.xml
│   ├── reservation_views.xml
│   ├── menus.xml
│   └── portal_templates.xml
└── data/
    └── scheduled_jobs.xml
```

## Installation

1. **Copier le module dans le répertoire addons d'Odoo**
   ```bash
   cp -r hotel_reservation_system /path/to/odoo/addons/
   ```

2. **Redémarrer le serveur Odoo**
   ```bash
   ./odoo-bin -c /path/to/odoo.conf
   ```

3. **Activer le mode développeur**
   - Aller dans Paramètres → Activer le mode développeur

4. **Mettre à jour la liste des applications**
   - Aller dans Applications → Mettre à jour la liste des applications

5. **Installer le module**
   - Rechercher "Hotel Reservation System"
   - Cliquer sur "Installer"

## Configuration

### Configuration des API

Pour activer la synchronisation avec Booking.com et Airbnb, vous devez configurer les paramètres système :

1. Aller dans **Paramètres → Technique → Paramètres système**

2. Créer les paramètres suivants :

   **Pour Booking.com :**
   - `hotel_reservation.booking_api_key` : Votre clé API Booking.com
   - `hotel_reservation.booking_api_endpoint` : URL de l'API Booking.com

   **Pour Airbnb :**
   - `hotel_reservation.airbnb_api_key` : Votre clé API Airbnb
   - `hotel_reservation.airbnb_api_endpoint` : URL de l'API Airbnb

### Configuration des CRON Jobs

Les tâches CRON sont créées automatiquement lors de l'installation :

1. **Synchronisation Booking.com** - Toutes les heures
2. **Synchronisation Airbnb** - Toutes les heures
3. **Synchronisation des disponibilités** - Toutes les heures

Pour les gérer :
- Aller dans **Paramètres → Technique → Automatisation → Actions planifiées**

## Utilisation

### Gestion des Chambres

1. Aller dans **Hotel Reservation System → Rooms**
2. Créer une nouvelle chambre avec :
   - Nom de la chambre
   - Numéro de chambre
   - Type (Single, Double, Suite)
   - Prix par nuit
   - Capacité
   - Statut (Available, Occupied, Maintenance)

### Gestion des Clients

1. Aller dans **Hotel Reservation System → Clients**
2. Créer un nouveau client avec :
   - Nom
   - Email
   - Téléphone
   - Numéro de passeport

### Gestion des Réservations

1. Aller dans **Hotel Reservation System → Reservations**
2. Créer une nouvelle réservation :
   - Sélectionner un client
   - Sélectionner une chambre
   - Définir les dates d'arrivée et de départ
   - Le prix total est calculé automatiquement
3. Confirmer la réservation

### Interface Web

Les clients peuvent réserver directement via l'interface web :

- **Formulaire de réservation** : `/hotel/reservation/form`
- **Liste des chambres** : `/hotel/rooms`

## Fonctionnalités Détaillées

### Modèle hotel.room

**Champs :**
- `name` : Nom de la chambre
- `room_number` : Numéro de chambre (unique)
- `room_type` : Type (single, double, suite)
- `price_per_night` : Prix par nuit
- `capacity` : Capacité
- `status` : Statut (available, occupied, maintenance)

**Méthodes :**
- `calculate_total_price()` : Calcul du prix total selon le nombre de nuits
- `check_availability()` : Vérification de la disponibilité pour des dates données

### Modèle hotel.client

**Champs :**
- `name` : Nom du client
- `email` : Email (unique, validé)
- `phone` : Téléphone (validé)
- `passport_number` : Numéro de passeport

**Contraintes :**
- Validation du format email
- Validation du format téléphone

### Modèle hotel.reservation

**Champs :**
- `name` : Numéro de réservation (auto-généré)
- `client_id` : Client (Many2one)
- `room_id` : Chambre (Many2one)
- `check_in` : Date d'arrivée
- `check_out` : Date de départ
- `total_price` : Prix total (calculé automatiquement)
- `status` : Statut (draft, confirmed, cancelled)
- `nights` : Nombre de nuits (calculé)

**Fonctionnalités :**
- Calcul automatique du prix total
- Validation des dates (check-out > check-in, pas de dates passées)
- Prévention des chevauchements de réservations
- Mise à jour automatique du statut de la chambre
- Actions : Confirmer, Annuler, Remettre en brouillon

### Modèle api.synchronization

**Méthodes :**
- `sync_booking_reservations()` : Synchronisation avec Booking.com
- `sync_airbnb_reservations()` : Synchronisation avec Airbnb
- `sync_availabilities()` : Mise à jour des disponibilités sur les plateformes

## Vues et Rapports

### Vues disponibles

- **Tree View** : Liste des enregistrements avec filtres
- **Form View** : Formulaire de détail
- **Kanban View** : Vue en cartes
- **Calendar View** : Calendrier des réservations
- **Pivot View** : Analyse croisée des réservations
- **Graph View** : Graphiques statistiques

### Filtres et Groupements

**Chambres :**
- Par statut (Available, Occupied, Maintenance)
- Par type de chambre

**Réservations :**
- Par statut (Draft, Confirmed, Cancelled)
- Par période (Current, Upcoming, Past)
- Par client, chambre, date

## Sécurité

### Droits d'accès

Le module définit deux groupes d'utilisateurs :

1. **Utilisateurs (base.group_user)** :
   - Lecture et écriture sur les chambres, clients et réservations
   - Lecture seule sur les synchronisations API

2. **Administrateurs (base.group_system)** :
   - Tous les droits (CRUD complet)

3. **Public (base.group_public)** :
   - Lecture des chambres
   - Création de clients et réservations (pour l'interface web)

## Tests et Validation

### Tests recommandés

1. **Test de chevauchement** :
   - Créer une réservation pour une chambre
   - Tenter de créer une autre réservation pour la même chambre avec des dates qui se chevauchent
   - Vérifier que le système empêche la création

2. **Test de calcul de prix** :
   - Créer une réservation
   - Vérifier que le prix total = prix par nuit × nombre de nuits

3. **Test de statut de chambre** :
   - Confirmer une réservation
   - Vérifier que le statut de la chambre passe à "Occupied"
   - Annuler la réservation
   - Vérifier que le statut revient à "Available"

## API et Intégrations

### Configuration Booking.com

Le module est préparé pour l'intégration avec l'API Booking.com. Les méthodes suivantes sont implémentées :

- Récupération des réservations
- Mise à jour des disponibilités
- Création automatique de clients et réservations

### Configuration Airbnb

Le module est préparé pour l'intégration avec l'API Airbnb. Les méthodes suivantes sont implémentées :

- Récupération des réservations
- Mise à jour du calendrier de disponibilité
- Création automatique de clients et réservations

**Note** : Les appels API réels sont commentés dans le code. Décommentez et configurez avec vos identifiants réels pour activer la synchronisation.

## Dépendances

- Odoo 17.0
- Module `base`
- Module `mail`
- Module `portal`
- Module `web`

## Support et Contribution

Pour toute question ou contribution :
1. Créer une issue sur le dépôt
2. Soumettre une pull request

## Licence

LGPL-3

## Auteur

Your Company

## Version

17.0.1.0.0

---

**Note importante** : Ce module est prêt à être utilisé. Les intégrations API avec Booking.com et Airbnb nécessitent la configuration de vos propres clés API et l'adaptation aux spécifications exactes de leurs API respectives.
