# 📋 Changelog - PromptMaster

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

## [3.2.0] - 2025-10-08

### 🚀 Philosophie : Simplicité et Vitesse Avant Tout

Cette version représente un **pivot majeur** vers la simplicité et la performance pure.

### ✅ Ajouté
- Toggle ultra-rapide Ctrl+Space (<100ms)
- Dialogue d'ajout avec MessageBoxBase (Fluent Design)
- Documentation mise à jour pour v3.2

### 🔄 Modifié
- **Interface simplifiée** : Suppression du label de contexte
- **Chargement optimisé** : `load_all_prompts()` remplace `load_contextual_prompts()`
- **Tri intelligent** : Par usage décroissant puis alphabétique
- **Dialogue d'ajout** : Migration vers MessageBoxBase pour meilleure intégration Fluent

### ❌ Supprimé
- **Capture de texte automatique** : Causait des délais et erreurs KeyboardInterrupt
- **Système de contexte** : Scoring, détection d'application, suggestions automatiques
- **ContextManager** : Plus utilisé dans l'interface principale
- **Méthode `update_context_display()`** : Plus de contexte à afficher
- **Méthode `show_add_dialog_with_text()`** : Plus de pré-remplissage

### 🐛 Corrigé
- Erreur `KeyboardInterrupt` lors de la capture de texte
- Conflit entre pynput listener et simulation de touches
- Délais d'affichage de la fenêtre (maintenant instantané)
- Erreur `AttributeError: 'widget'` dans le dialogue (migration vers MessageBoxBase)
- Erreur `setEditable` sur ComboBox (migration vers EditableComboBox)

### 📊 Impact Performance
- **Avant v3.2** : ~200-300ms pour ouvrir (avec capture texte)
- **Après v3.2** : <100ms pour ouvrir (sans capture texte)
- **Gain** : 66% plus rapide

---

## [3.1.0] - 2025-10-06

### ✨ Édition Sans Friction

### ✅ Ajouté
- **Édition inline** : Modification directe dans le panneau de prévisualisation
- **Autosave** : Sauvegarde automatique après 0.8-1s d'inactivité
- **Champs éditables** : Titre, catégorie, tags, contenu
- **Timer de debouncing** : Évite les sauvegardes multiples
- **Protection `is_loading`** : Pas de sauvegarde pendant la navigation
- Documentation `INLINE_EDITING.md`

### 🔄 Modifié
- Panneau de prévisualisation → Panneau d'édition
- Labels statiques → LineEdit et TextEdit éditables
- Footer simplifié : mention "💾 Sauvegarde automatique"

### ❌ Supprimé
- Dialogues d'édition complexes
- Double-clic pour éditer (remplacé par clic simple)
- Raccourci `E` pour éditer (plus nécessaire)
- Bouton "Enregistrer" (automatique maintenant)

### 📊 Métriques
- **Édition d'un prompt** : 3 actions → 1 action (66% de réduction)
- **Temps pour éditer 5 prompts** : 25s → 10s (60% plus rapide)

---

## [3.0.0] - 2025-10-05

### 🎨 Migration Fluent Design

### ✅ Ajouté
- **PySide6-Fluent-Widgets** : Remplacement de PyQt6/PySide6 basique
- **FluentWindow** : Fenêtre principale avec navigation
- **CardWidget** : Cards avec ombres pour liste et prévisualisation
- **InfoBar** : Notifications toast élégantes
- **SearchLineEdit** : Barre de recherche Fluent
- **Theme support** : Dark/Light theme avec couleur d'accent
- Documentation `FLUENT_DESIGN.md`
- Documentation `GUIDE_VISUEL.md`

### 🔄 Modifié
- Migration PyQt6 → PySide6-Fluent-Widgets
- Design Windows 10 → Windows 11 Fluent
- Notifications simples → InfoBars modernes
- Dialogues basiques → Dialogues Fluent

### 🐛 Corrigé
- Erreur DLL avec PyQt6 sur Windows
- `ListWidget.addItem()` retourne None (API Fluent différente)
- Solution : dictionnaire `prompt_ids` parallèle pour stocker les IDs
- `addSubInterface` nécessite `objectName` (ajouté)

### 📦 Dépendances
- Ajout : `PySide6-Fluent-Widgets==1.6.3`
- Remplacement : `PyQt6` → `PySide6>=6.6.0`

---

## [2.0.0] - 2025-10-04

### 🧠 Intelligence Contextuelle

### ✅ Ajouté
- **Capture de texte sélectionné** : Ctrl+C simulation avec pynput
- **Détection de contexte** : Application active, fenêtre, processus
- **Scoring intelligent** : Algorithme de pertinence multi-critères
- **Prévisualisation temps réel** : Split layout avec panneau de droite
- **Suggestions automatiques** : Catégorie et tags basés sur le contexte
- **ContextManager** : Classe dédiée à la détection et scoring
- Documentation `NOUVELLES_FONCTIONNALITES.md`

### 🔄 Modifié
- Interface simple → Split layout (40/60)
- Recherche basique → Recherche contextuelle
- Ajout manuel → Ajout avec pré-remplissage

### 📦 Dépendances
- Ajout : `pywin32==306`, `psutil==5.9.8`

### 🎯 Fonctionnalités Contextuelles
- Détection : VS Code, Chrome, Firefox, Edge, Notion, Slack, Teams, Discord
- Sites web : GitHub, Stack Overflow, ChatGPT, Google Docs
- Scoring : Catégorie (+10), Tags (+5), Titre (+3), Usage (+2)

---

## [1.0.0] - 2025-10-03

### 🎉 Version Initiale

### ✅ Ajouté
- **Recherche full-text** : SQLite FTS5 pour recherche rapide
- **Raccourci global** : Ctrl+Space avec pynput
- **Base de données** : SQLite avec table `prompts`
- **CRUD complet** : Créer, Lire, Modifier, Supprimer
- **Compteur d'usage** : Suivi des prompts les plus utilisés
- **Interface PyQt6** : Fenêtre de recherche basique
- **Copie presse-papiers** : Avec pyperclip
- **Organisation** : Catégories et tags
- **Prompts d'exemple** : 6 prompts pré-chargés

### 📦 Dépendances Initiales
```
PyQt6==6.6.1
pynput==1.7.6
pyperclip==1.8.2
```

### 📁 Structure
```
database.py        # Gestion SQLite
gui.py            # Interface PyQt6
main.py           # Point d'entrée + hotkey
requirements.txt  # Dépendances
README.md         # Documentation
```

### 🎯 Objectif Initial
Créer un "Raycast pour prompts" - Un launcher rapide pour accéder à ses prompts favoris.

---

## Format du Changelog

Ce changelog suit les principes de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

### Types de Changements
- **✅ Ajouté** : Nouvelles fonctionnalités
- **🔄 Modifié** : Changements de fonctionnalités existantes
- **❌ Supprimé** : Fonctionnalités retirées
- **🐛 Corrigé** : Corrections de bugs
- **🔒 Sécurité** : Corrections de vulnérabilités

---

**PromptMaster** - De l'idée simple à l'outil raffiné, toujours en évolution. 🚀
