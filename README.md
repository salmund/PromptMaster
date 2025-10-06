# 🎯 PromptMaster v3.0 - Fluent Design

**PromptMaster** est un gestionnaire de prompts rapide et élégant avec **intelligence contextuelle** et **design Microsoft Fluent**, inspiré de Raycast. Accédez instantanément à vos prompts favoris avec un simple raccourci clavier !

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Design](https://img.shields.io/badge/design-Fluent-purple)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Nouveautés v3.0 - Design Fluent

### 🎨 Interface Complètement Redesignée
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
