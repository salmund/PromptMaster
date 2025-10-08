# 🎯 PromptMaster v3.2 - Simple, Rapide, Sans Friction

**PromptMaster** est un gestionnaire de prompts ultra-rapide et minimaliste avec **édition inline**, **sauvegarde automatique**, et **design Microsoft Fluent**. Inspiré de Raycast, optimisé pour la vitesse et la simplicité.

![Version](https://img.shields.io/badge/version-3.2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Design](https://img.shields.io/badge/design-Fluent-purple)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ v3.2 - Simplicité Absolue

### 🚀 Philosophie : Zéro Friction
- **Toggle instantané** : Ctrl+Space s'ouvre en <100ms, aucun délai
- **Aucune complexité** : Plus de capture automatique, plus de scoring, juste l'essentiel
- **Édition directe** : Cliquez, modifiez, c'est sauvegardé automatiquement
- **Interface épurée** : Recherche → Édite → Copie. C'est tout.

### 📝 Fonctionnalités Principales

#### Édition Sans Friction
- **Édition inline** : Modifiez titre, catégorie, tags et contenu directement dans l'interface
- **Autosave** : Sauvegarde automatique 0.8s après votre dernière modification
- **Aucun dialogue** : Tout se passe dans la fenêtre principale
- **Navigation fluide** : Utilisez ↑↓ pour naviguer, les modifications sont déjà enregistrées

#### Interface Ultra-Rapide
- **Ctrl+Space** : Ouvrir/Fermer instantanément
- **Recherche temps réel** : Tapez, les résultats s'affichent immédiatement
- **Prévisualisation live** : Le prompt s'affiche à droite pendant que vous naviguez
- **Enter pour copier** : Un simple Enter et le prompt est dans votre presse-papiers

#### Gestion Simple
- **Ajout facile** : Bouton ➕ Nouveau → Remplissez → Ctrl+Enter
- **Suppression rapide** : Touche Del → Confirmation → Supprimé
- **Organisation** : Catégories et tags optionnels pour retrouver vos prompts
- **Tri intelligent** : Les prompts les plus utilisés remontent automatiquement

## 🎨 Design Fluent (v3.0)
- **Microsoft Fluent Design System** : Interface moderne Windows 11
- **PySide6-Fluent-Widgets** : Composants premium
- **Thème sombre** : Design élégant avec accent violet (#bd93f9)
- **Cards et ombres** : Profondeur visuelle professionnelle

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Windows (pour l'instant - support macOS/Linux à venir)

### Installation Rapide

```powershell
# Cloner le projet
git clone https://github.com/salmund/PromptMaster.git
cd PromptMaster

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### Dépendances
```
PySide6>=6.6.0
PySide6-Fluent-Widgets>=1.6.3
pynput>=1.7.6
pyperclip>=1.8.2
```

## 🎮 Guide d'Utilisation

### Démarrage Rapide

1. **Lancer l'application**
   ```powershell
   python main.py
   ```

2. **Ouvrir avec Ctrl+Space**
   - L'application démarre en arrière-plan
   - Appuyez sur `Ctrl+Space` n'importe où
   - La fenêtre apparaît instantanément

3. **Ajouter votre premier prompt**
   - Cliquez sur `➕ Nouveau`
   - Remplissez le titre et le contenu
   - `Ctrl+Enter` ou cliquez sur Enregistrer

4. **Utiliser un prompt**
   - `Ctrl+Space` pour ouvrir
   - Tapez pour rechercher
   - `↑↓` pour naviguer
   - `Enter` pour copier dans le presse-papiers
   - `Échap` pour fermer

### Workflow Quotidien

```
Scénario : Utiliser un prompt ChatGPT

1. Ctrl+Space                    → Fenêtre s'ouvre
2. Tapez "chatgpt"              → Résultats filtrés
3. ↓ pour sélectionner          → Prévisualisation à droite
4. Enter                        → Copié !
5. Collez dans ChatGPT          → Profit

Temps total : 3 secondes ⚡
```

### Édition en Temps Réel

```
Scénario : Améliorer un prompt existant

1. Ctrl+Space                    → Ouvrir
2. Cliquez sur le prompt        → S'affiche à droite
3. Modifiez le contenu          → Tapez directement
4. Attendez 0.8s                → Sauvegardé automatiquement !
5. ↓ pour le prompt suivant     → Déjà enregistré

Aucun bouton "Enregistrer" nécessaire 🎯
```

## ⌨️ Raccourcis Clavier

| Raccourci | Action |
|-----------|--------|
| `Ctrl+Space` | Ouvrir/Fermer l'application |
| `↑` `↓` | Naviguer entre les prompts |
| `Enter` | Copier le prompt sélectionné |
| `Del` | Supprimer le prompt |
| `Échap` | Fermer la fenêtre |
| `Ctrl+Enter` | Enregistrer (dans le dialogue d'ajout) |

**Pas de raccourci pour sauvegarder l'édition inline → C'est automatique !** ✨

## 📊 Fonctionnalités Détaillées

### Recherche Intelligente
- **Full-text search** : Recherche dans titre, contenu, catégorie et tags
- **Temps réel** : Les résultats s'affichent pendant que vous tapez
- **Tri automatique** : Les prompts les plus utilisés en premier

### Édition Inline
- **Tous les champs éditables** : Titre, catégorie, tags, contenu
- **Autosave intelligent** : Debouncing pour éviter les sauvegardes inutiles
- **Protection** : Pas de sauvegarde pendant le chargement
- **Feedback discret** : Message console uniquement

### Organisation
- **Catégories** : Organisez par thème (Développement, Marketing, etc.)
- **Tags** : Ajoutez plusieurs tags séparés par des virgules
- **Compteur d'usage** : Suivez vos prompts les plus utilisés
- **Tri intelligent** : Tri par usage décroissant puis alphabétique

## 📁 Structure du Projet

```
PromptMaster/
├── main.py                      # Point d'entrée avec hotkey
├── gui.py                       # Interface Fluent (v3.2 simplifiée)
├── database.py                  # Gestion SQLite
├── context_manager.py           # Détection contexte (non utilisé en v3.2)
├── promptmaster.db              # Base de données SQLite
├── requirements.txt             # Dépendances
└── docs/
    ├── README.md                # Ce fichier
    ├── QUICKSTART.md            # Guide de démarrage
    ├── INLINE_EDITING.md        # Guide édition inline
    └── FLUENT_DESIGN.md         # Guide Fluent Design
```

## 🔧 Configuration

### Changer le Thème

Éditez `gui.py` ligne ~44 :

```python
# Thème sombre (par défaut)
setTheme(Theme.DARK)

# Thème clair
setTheme(Theme.LIGHT)
```

### Changer la Couleur d'Accent

Éditez `gui.py` ligne ~45 :

```python
# Violet Dracula (par défaut)
setThemeColor('#bd93f9')

# Autres couleurs
setThemeColor('#0078D4')  # Bleu Windows
setThemeColor('#FF6B6B')  # Rouge
setThemeColor('#4ECDC4')  # Turquoise
```

### Changer le Raccourci Clavier

Éditez `main.py` lignes ~19-28 pour changer la combinaison de touches.

## 💡 Conseils Pro

### Nommage des Prompts
- **Titres courts et descriptifs** : "API REST Python" plutôt que "Comment créer une API REST en Python"
- **Le contenu est dans la prévisualisation** : Le titre sert juste à identifier

### Organisation
- **Catégories larges** : Développement, Marketing, Design, etc.
- **Tags spécifiques** : python, api, rest, fastapi, etc.
- **Consistance** : Utilisez toujours les mêmes noms de catégories

### Performance
- **Les prompts les plus utilisés remontent** : Pas besoin de favoris manuels
- **Recherche partielle** : 2-3 lettres suffisent grâce à la prévisualisation
- **Navigation clavier** : Plus rapide que la souris

## 🐛 Dépannage

### L'application ne démarre pas
```powershell
# Vérifier Python
python --version  # Doit être 3.8+

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Ctrl+Space ne fonctionne pas
- Vérifiez qu'aucune autre application n'utilise ce raccourci
- Essayez de relancer l'application
- Vérifiez les messages dans le terminal

### Les modifications ne sont pas sauvegardées
- Attendez 0.8s après votre dernière modification
- Vérifiez les messages de sauvegarde dans le terminal
- La base de données est dans `promptmaster.db`

## � Historique des Versions

### v3.2 (Actuel) - Simplicité Absolue
- ✅ Suppression capture de texte automatique → Plus de délais
- ✅ Suppression système de contexte → Interface simplifiée
- ✅ Toggle ultra-rapide → <100ms
- ✅ Dialogue d'ajout simplifié → MessageBoxBase
- ✅ Documentation mise à jour

### v3.1 - Édition Sans Friction
- ✅ Édition inline avec autosave
- ✅ Suppression des dialogues d'édition
- ✅ Workflow ultra-fluide

### v3.0 - Design Fluent
- ✅ Migration vers PySide6-Fluent-Widgets
- ✅ Interface Windows 11 moderne
- ✅ Thème sombre/clair

### v2.0 - Intelligence Contextuelle
- ⚠️ Capture de texte (supprimée en v3.2)
- ⚠️ Détection de contexte (supprimée en v3.2)
- ✅ Prévisualisation temps réel (gardée)

### v1.0 - Version Initiale
- ✅ Recherche full-text
- ✅ Raccourci global Ctrl+Space
- ✅ Base de données SQLite

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir des issues pour signaler des bugs
- Proposer des nouvelles fonctionnalités
- Soumettre des pull requests

## 📄 Licence

MIT License - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **Microsoft** : Fluent Design System
- **Qt Company** : PySide6 framework
- **zhiyiYo** : PySide6-Fluent-Widgets
- **Raycast** : Inspiration du concept

---

**PromptMaster v3.2 - Simple. Rapide. Sans friction. 🚀**

Créé avec ❤️ pour les utilisateurs qui veulent juste que ça marche.

- **Microsoft Fluent Design System** : Look moderne Windows 11
- **PySide6-Fluent-Widgets** : Composants premium et professionnels
- **Effets Acryliques** : Transparence et flou élégants
- **Animations Fluides** : Transitions naturelles et smooth
- **InfoBars Modernes** : Notifications toast élégantes
- **Cards avec Ombres** : Profondeur visuelle
- **Thème Sombre/Clair** : Basculez en une ligne de code

### 🆕 Fonctionnalités v2.0 (Toujours présentes)

- 📋 **Capture de texte sélectionné** : Sélectionnez du texte n'importe où, appuyez sur `Ctrl + Space`, et il est automatiquement ajouté comme nouveau prompt !
- 🧠 **Contexte intelligent** : Détecte votre application active (VS Code, navigateur, etc.) et recommande les prompts les plus pertinents
- 👁️ **Prévisualisation en temps réel** : Voir le contenu complet du prompt pendant la recherche dans un panneau dédié
- 💡 **Suggestions automatiques** : Catégorie et tags suggérés automatiquement selon le contexte
- 🎯 **Scoring intelligent** : Les prompts les plus pertinents pour votre contexte apparaissent en premier

### ⚡ Fonctionnalités de Base

- 🔍 **Recherche instantanée** : Trouvez vos prompts en temps réel
- ⌨️ **Raccourci global** : `Ctrl + Space` pour ouvrir l'application de n'importe où
- 📋 **Copie automatique** : Le prompt est copié dans votre presse-papiers
- 🏷️ **Organisation** : Catégories et tags pour classer vos prompts
- 📊 **Statistiques d'utilisation** : Suivez vos prompts les plus utilisés
- 🎨 **Interface moderne** : Design Dracula élégant et professionnel
- ✏️ **Édition facile** : Ajoutez, modifiez ou supprimez vos prompts

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- Windows 10/11 (adaptable pour macOS et Linux)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

```powershell
cd C:\Users\louis\Documents\PromptMaster
```

2. **Créer un environnement virtuel (recommandé)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Installer les dépendances**

```powershell
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancement de l'application

```powershell
python main.py
```

### Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| `Ctrl + Space` | Afficher/Masquer PromptMaster |
| `Ctrl + Space` (avec texte sélectionné) | Créer un prompt avec le texte |
| `↑` / `↓` | Naviguer dans les résultats |
| `Enter` | Copier le prompt sélectionné |
| `Double-clic` | Éditer un prompt |
| `Molette` | Défiler dans la liste ou le contenu |
| `Échap` | Fermer la fenêtre |

### Workflow typique

**Sans sélection :**
1. Appuyez sur **Ctrl + Space** n'importe où dans Windows
2. Les prompts contextuels s'affichent automatiquement selon votre application active
3. Tapez quelques mots pour affiner la recherche
4. Utilisez les flèches pour sélectionner et voir la prévisualisation
5. Appuyez sur **Enter** pour copier le prompt
6. Collez-le où vous voulez avec **Ctrl + V**

**Avec sélection (NOUVEAU) :**
1. Sélectionnez du texte dans n'importe quelle application
2. Appuyez sur **Ctrl + Space**
3. L'interface de création s'ouvre avec le texte pré-rempli
4. Catégorie et tags suggérés automatiquement
5. Ajoutez un titre et enregistrez !

**Temps total : ~10 secondes !** ⚡

## 📁 Structure du projet

```
PromptMaster/
│
├── database.py              # Gestion de la base de données SQLite
├── gui.py                   # Interface graphique PySide6 avec prévisualisation
├── main.py                  # Point d'entrée avec raccourci global
├── context_manager.py       # 🆕 Détection contexte et capture texte
├── requirements.txt         # Dépendances Python
├── README.md                # Documentation
├── NOUVELLES_FONCTIONNALITES.md  # 🆕 Guide des fonctionnalités v2.0
├── QUICKSTART.md            # Guide de démarrage rapide
│
└── promptmaster.db          # Base de données (créée automatiquement)
```

## 🛠️ Architecture

### Backend (database.py)

- **DatabaseManager** : Classe principale pour gérer SQLite
- Opérations CRUD complètes (Create, Read, Update, Delete)
- Recherche full-text dans titre, contenu, tags et catégorie
- Compteur d'utilisation pour trier par pertinence

### Frontend (gui.py)

- **PromptMasterWindow** : Fenêtre principale de recherche
- **PromptEditorDialog** : Dialogue d'édition/création
- Design moderne avec thème Dracula
- Navigation au clavier optimisée

### Intégration système (main.py)

- **HotkeyListener** : Écoute le raccourci `Ctrl + Space`
- Fonctionne en arrière-plan avec `pynput`
- Toggle show/hide de la fenêtre

## 💡 Exemples de prompts inclus

L'application vient avec des exemples de prompts dans différentes catégories :

- **Développement** : API REST, Code Review, Debugging
- **Marketing** : Email marketing, SEO
- **Business** : Pitch de présentation
- **Rédaction** : Articles de blog optimisés SEO

## 🎨 Personnalisation

### Modifier le thème

Éditez les styles dans `gui.py`, méthode `apply_styles()` :

```python
background-color: #282a36;  # Fond principal
border: 2px solid #bd93f9;   # Bordures
color: #f8f8f2;              # Texte
```

### Changer le raccourci clavier

Modifiez dans `main.py`, classe `HotkeyListener` :

```python
self.HOTKEYS = {
    keyboard.Key.ctrl_l,
    keyboard.Key.alt_l,  # Par exemple : Ctrl + Alt
    keyboard.Key.space
}
```

## 📦 Créer un exécutable

Pour distribuer PromptMaster sans installer Python :

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name PromptMaster --icon=icon.ico main.py
```

L'exécutable sera dans le dossier `dist/`.

### Lancer au démarrage de Windows

1. Créer un raccourci vers `PromptMaster.exe`
2. Appuyer sur `Win + R`, taper `shell:startup`
3. Coller le raccourci dans ce dossier

## 🔧 Développement

### Ajouter des fonctionnalités

Quelques idées d'amélioration :

- [ ] Import/Export de prompts (JSON, CSV)
- [ ] Synchronisation cloud (Dropbox, Google Drive)
- [ ] Variables dans les prompts (ex: `{nom_projet}`)
- [ ] Historique des prompts utilisés
- [ ] Favoris avec raccourcis numériques
- [ ] Mode sombre/clair
- [ ] Support multi-langues

### Tester le module database

```powershell
python database.py
```

### Tester l'interface sans raccourci global

```powershell
python gui.py
```

## 📝 Base de données

### Structure de la table `prompts`

| Champ | Type | Description |
|-------|------|-------------|
| id | INTEGER | Clé primaire auto-incrémentée |
| title | TEXT | Titre du prompt |
| content | TEXT | Contenu complet |
| category | TEXT | Catégorie (optionnelle) |
| tags | TEXT | Tags séparés par virgules |
| created_at | TIMESTAMP | Date de création |
| usage_count | INTEGER | Nombre d'utilisations |

### Backup de la base

```powershell
copy promptmaster.db promptmaster_backup.db
```

## 🐛 Troubleshooting

### L'application ne se lance pas

```powershell
# Vérifier que Python est installé
python --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Le raccourci Ctrl + Space ne fonctionne pas

- Vérifiez qu'aucune autre application n'utilise ce raccourci
- Essayez de lancer l'application en administrateur
- Vérifiez les permissions de `pynput`

### Problèmes d'affichage

```powershell
# Réinstaller PyQt6
pip uninstall PyQt6
pip install PyQt6
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- Inspiré par [Raycast](https://www.raycast.com/)
- Thème basé sur [Dracula](https://draculatheme.com/)
- Interface construite avec [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)

## 📧 Contact

Pour toute question ou suggestion :
- Créer une issue sur GitHub
- Email : votre-email@example.com

---

**Fait avec ❤️ et Python**
