# 🚀 Guide de Démarrage Rapide - PromptMaster

## ⚡ Installation en 3 étapes

### 1. Installer les dépendances

```powershell
pip install -r requirements.txt
```

### 2. Initialiser la base de données

```powershell
python database.py
```

Ceci créera le fichier `promptmaster.db` et ajoutera 6 prompts d'exemple.

### 3. Lancer l'application

```powershell
python main.py
```

## 🎯 Utilisation

### Raccourcis Clavier

| Touche | Action |
|--------|--------|
| `Ctrl + Space` | Ouvrir/Fermer PromptMaster |
| `Échap` | Fermer la fenêtre |
| `↑` / `↓` | Naviguer dans les résultats |
| `Entrée` | Copier le prompt sélectionné |
| `Double-clic` | Éditer un prompt |

### Workflow Recommandé

1. **Rechercher** : Tapez quelques mots-clés
2. **Sélectionner** : Utilisez les flèches ou la souris
3. **Copier** : Appuyez sur `Entrée`
4. **Utiliser** : Collez avec `Ctrl + V` n'importe où

### Ajouter un Nouveau Prompt

1. Cliquez sur le bouton **"➕ Nouveau"**
2. Remplissez les champs :
   - **Titre** : Un nom court et descriptif
   - **Catégorie** : Pour organiser vos prompts
   - **Tags** : Mots-clés séparés par des virgules
   - **Contenu** : Le texte complet du prompt
3. Cliquez sur **"💾 Enregistrer"**

### Éditer un Prompt

- **Double-cliquez** sur n'importe quel prompt dans la liste
- Modifiez les champs souhaités
- Cliquez sur **"💾 Enregistrer"** ou **"🗑️ Supprimer"**

## 💡 Exemples de Prompts

### Développement
```
Titre: Debug Assistant
Catégorie: Développement
Tags: debug, troubleshooting, python

Contenu:
Analysez ce bug : [DESCRIPTION]. Identifiez la cause probable, 
proposez une solution pas à pas, expliquez comment reproduire 
le bug, et suggérez des tests pour éviter qu'il ne se reproduise.
```

### Marketing
```
Titre: Email Marketing
Catégorie: Marketing
Tags: email, marketing, copywriting

Contenu:
Rédigez un email marketing convaincant pour promouvoir [PRODUIT]. 
Le ton doit être professionnel mais chaleureux, avec un 
call-to-action clair et une structure : accroche, bénéfices, 
preuve sociale, offre, urgence.
```

## 🔧 Personnalisation

### Changer le Raccourci Clavier

Éditez `main.py`, ligne ~18 :

```python
self.HOTKEYS = {
    keyboard.Key.ctrl_l,
    keyboard.Key.space
}
```

Remplacez par exemple par `Ctrl + Shift + Space` :

```python
self.HOTKEYS = {
    keyboard.Key.ctrl_l,
    keyboard.Key.shift,
    keyboard.Key.space
}
```

### Modifier le Thème

Éditez `gui.py`, méthode `apply_styles()` (ligne ~93) :

```python
# Couleurs Dracula (par défaut)
background-color: #282a36;  # Fond
border: 2px solid #bd93f9;   # Bordure violet
color: #f8f8f2;              # Texte blanc

# Alternative : Thème Clair
background-color: #ffffff;   # Fond blanc
border: 2px solid #3b82f6;   # Bordure bleue
color: #1f2937;              # Texte sombre
```

## 📊 Statistiques d'Utilisation

Chaque fois que vous utilisez un prompt (Entrée), son compteur d'utilisation augmente. 
Les prompts les plus utilisés apparaissent en premier dans les résultats.

Vous pouvez voir le compteur sous forme d'étoiles : ✨ 5

## 🗄️ Gestion de la Base de Données

### Backup

```powershell
copy promptmaster.db backup_$(Get-Date -Format 'yyyyMMdd').db
```

### Reset

Pour recommencer avec une base vide :

```powershell
del promptmaster.db
python database.py
```

### Export

Pour exporter vos prompts (ajoutez ce code à `database.py`) :

```python
import json

def export_to_json(filename="prompts_export.json"):
    db = DatabaseManager()
    prompts = db.get_all_prompts()
    
    data = []
    for p in prompts:
        data.append({
            "title": p[1],
            "content": p[2],
            "category": p[3],
            "tags": p[4]
        })
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ {len(data)} prompts exportés vers {filename}")
```

## 🐛 Dépannage

### L'application ne démarre pas

```powershell
# Vérifier Python
python --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Tester les imports
python -c "from PySide6.QtWidgets import QApplication; print('OK')"
```

### Le raccourci Ctrl+Space ne fonctionne pas

1. Vérifiez qu'aucune autre application n'utilise ce raccourci
2. Essayez de lancer en administrateur (clic droit → Exécuter en tant qu'administrateur)
3. Sur certains systèmes, `Ctrl+Space` est réservé pour changer de langue

**Solution** : Changez le raccourci dans `main.py` (voir "Personnalisation" ci-dessus)

### La fenêtre n'apparaît pas au centre

Vérifiez la configuration multi-écrans. Éditez `gui.py`, méthode `center_on_screen()` :

```python
def center_on_screen(self):
    # Pour forcer un écran spécifique
    screens = QApplication.screens()
    screen = screens[0].geometry()  # Premier écran
    # screen = screens[1].geometry()  # Deuxième écran
    
    x = (screen.width() - self.width()) // 2
    y = (screen.height() - self.height()) // 3
    self.move(x, y)
```

## 📦 Créer un Exécutable

Pour distribuer PromptMaster sans Python :

```powershell
# Installer PyInstaller
pip install pyinstaller

# Créer l'exécutable
pyinstaller --onefile --windowed --name PromptMaster main.py

# L'exécutable sera dans le dossier dist/
.\dist\PromptMaster.exe
```

### Lancer au Démarrage

1. Créer un raccourci vers `PromptMaster.exe`
2. Appuyer sur `Win + R`
3. Taper `shell:startup` et appuyer sur Entrée
4. Coller le raccourci dans ce dossier

## 🎓 Astuces Pro

### Variables dans les Prompts

Utilisez des placeholders comme `[PRODUIT]`, `[DESCRIPTION]`, etc. dans vos prompts :

```
Créez une API pour [PROJET] qui gère [FONCTIONNALITÉ]...
```

Quand vous collez le prompt, remplacez simplement les placeholders.

### Organiser par Projets

Utilisez les catégories pour séparer vos prompts par projet :

- `Projet-ClientA`
- `Projet-SiteWeb`
- `Personnel`

### Hotkeys Numériques (Future Feature)

Vous pourriez ajouter des raccourcis `Ctrl+1`, `Ctrl+2`, etc. pour vos 10 prompts favoris.

## 📚 Ressources

- **Documentation complète** : Voir `README.md`
- **Code source** : Tous les fichiers sont commentés
- **SQLite** : https://www.sqlite.org/
- **PySide6** : https://doc.qt.io/qtforpython/

## 💬 Support

Pour toute question :
1. Consultez le `README.md`
2. Vérifiez les messages d'erreur dans le terminal
3. Créez une issue sur GitHub

---

**Bon prompt ! 🎯**
