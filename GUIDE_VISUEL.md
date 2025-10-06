# 📖 Guide Visuel - PromptMaster v2.0

## 🎯 Vue d'ensemble de l'interface

### Nouvelle Interface avec Prévisualisation

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  🎯 PromptMaster         📍 Chrome • Développement • GitHub         ➕ Nouveau  │
├────────────────────────────────────────────────────────────────────────────────┤
│  🔍 Recherchez vos prompts...                                                  │
├─────────────────────────────────┬──────────────────────────────────────────────┤
│ LISTE DES RÉSULTATS (40%)       │ PRÉVISUALISATION (60%)                       │
│                                 │                                              │
│ ┌─────────────────────────────┐ │ ┌──────────────────────────────────────────┐ │
│ │ API REST Python • Dév ✨ 15 │ │ │ 📌 API REST Python                       │ │
│ │ Debug Assistant • Dév ✨ 8  │ │ │ 📁 Développement • 🏷️ python,api,rest   │ │
│ │ Email Marketing • Mark ✨ 5 │ │ │ ──────────────────────────────────────── │ │
│ │ Code Review • Dév ✨ 3      │ │ │                                          │ │
│ │ Article SEO • Rédac         │ │ │ Créez une API REST complète en Python    │ │
│ │ Pitch Business • Bus        │ │ │ avec FastAPI incluant :                  │ │
│ │                             │ │ │                                          │ │
│ │                             │ │ │ - Authentification JWT                   │ │
│ │                             │ │ │ - Endpoints CRUD                         │ │
│ │                             │ │ │ - Validation des données avec Pydantic   │ │
│ │                             │ │ │ - Documentation automatique Swagger      │ │
│ │                             │ │ │ - Gestion des erreurs                    │ │
│ │                             │ │ │                                          │ │
│ │                             │ │ │ [Scrollable si contenu long...]          │ │
│ └─────────────────────────────┘ │ └──────────────────────────────────────────┘ │
└─────────────────────────────────┴──────────────────────────────────────────────┤
│  ↵ Copier | Double-clic pour éditer | ↑↓ Naviguer | Molette Défiler | Échap    │
└────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Workflows Illustrés

### Workflow 1 : Capture de Texte Sélectionné

```
ÉTAPE 1 : Vous êtes sur un site web
┌────────────────────────────────────┐
│  Chrome - Medium.com               │
│  ─────────────────────────────────  │
│  Article : "10 Best AI Prompts"    │
│                                    │
│  [Texte sélectionné en bleu :]    │
│  "Act as an expert developer and   │
│   create a comprehensive guide..."  │
│                                    │
└────────────────────────────────────┘
         ↓ Vous appuyez sur Ctrl+Space

ÉTAPE 2 : PromptMaster s'ouvre en mode création
┌────────────────────────────────────────────┐
│  ➕ Nouveau Prompt                         │
│  ──────────────────────────────────────── │
│  Titre: [Curseur ici - tapez le titre]   │
│                                           │
│  Catégorie: [Développement] 💡 Suggérer   │
│                                           │
│  Tags: developer,guide,expert 💡 Suggérer │
│                                           │
│  Contenu:                                 │
│  ┌───────────────────────────────────┐   │
│  │ Act as an expert developer and    │   │
│  │ create a comprehensive guide...   │   │
│  │ [DÉJÀ PRÉ-REMPLI !]               │   │
│  └───────────────────────────────────┘   │
│                                           │
│       [Annuler]  [💾 Enregistrer]         │
└────────────────────────────────────────────┘
         ↓ Vous tapez un titre et Enter

ÉTAPE 3 : Prompt enregistré !
┌────────────────────────────────────┐
│  ✓ Prompt ajouté avec succès !     │
└────────────────────────────────────┘
```

**⏱️ Temps total : 10 secondes !**

### Workflow 2 : Recherche Contextuelle

```
ÉTAPE 1 : Vous codez dans VS Code
┌────────────────────────────────────┐
│  VS Code - main.py                 │
│  ─────────────────────────────────  │
│  def create_api():                 │
│      # Vous voulez un prompt API   │
│                                    │
└────────────────────────────────────┘
         ↓ Ctrl+Space

ÉTAPE 2 : Prompts contextuels affichés
┌─────────────────────────────────────────────────────────┐
│  📍 VS Code • Développement                              │
│  ─────────────────────────────────────────────────────  │
│  🔍 [Recherche vide]                                    │
│  ─────────────────────────────────────────────────────  │
│  PROMPTS RECOMMANDÉS (triés par pertinence) :          │
│  ✅ API REST Python • Dév ✨ 15  [SCORE: 120]          │
│  ✅ Debug Assistant • Dév ✨ 8   [SCORE: 82]           │
│  ✅ Code Review • Dév ✨ 3       [SCORE: 76]           │
│  ⬜ Email Marketing • Mark ✨ 5  [SCORE: 10]           │
│                                                         │
│  Les prompts de DÉVELOPPEMENT sont en haut !           │
└─────────────────────────────────────────────────────────┘
         ↓ Vous tapez "api"

ÉTAPE 3 : Résultats filtrés
┌─────────────────────────────────────────────────────────┐
│  🔍 api                                                  │
│  ─────────────────────────────────────────────────────  │
│  ┌─ API REST Python ✨ 15 │ [Prévisualisation:]        │
│  │                         │ Créez une API REST...      │
│  │                         │ avec FastAPI incluant...   │
│  └─────────────────────────┴────────────────────────────┘
└─────────────────────────────────────────────────────────┘
         ↓ Enter

ÉTAPE 4 : Copié !
┌────────────────────────────────────┐
│  ✓ Copié dans le presse-papiers !  │
└────────────────────────────────────┘
```

**⏱️ Temps total : 5 secondes !**

## 🎨 Système de Couleurs

### Thème Dracula

```
┌──────────────────────────────────────┐
│  Fond principal : #282a36 (Noir)     │
│  Fond secondaire : #1e1f29 (+ foncé) │
│  Bordures : #44475a (Gris)           │
│  Accent : #bd93f9 (Violet)           │
│  Success : #50fa7b (Vert)            │
│  Info : #8be9fd (Cyan)               │
│  Texte : #f8f8f2 (Blanc cassé)       │
│  Texte secondaire : #6272a4 (Gris)   │
└──────────────────────────────────────┘
```

### Codes Couleur par Élément

```
Élément                     Couleur         Usage
────────────────────────────────────────────────────
Titre "PromptMaster"       #f8f8f2 (Blanc)  Header
Contexte "📍 Chrome..."    #8be9fd (Cyan)   Info contextuelle
Bouton "Nouveau"           #50fa7b (Vert)   Action positive
Champ recherche            #44475a (Gris)   Input
  └─ Focus                 #bd93f9 (Violet) State actif
Liste résultats            #1e1f29 (Noir+)  Background
  └─ Sélection             #bd93f9 (Violet) Highlight
Prévisualisation
  ├─ Titre                 #50fa7b (Vert)   Emphasis
  ├─ Métadonnées           #8be9fd (Cyan)   Info
  └─ Contenu               #f8f8f2 (Blanc)  Texte principal
Footer instructions        #6272a4 (Gris)   Aide discrète
```

## 📊 Système de Scoring

### Comment les prompts sont classés

```
PROMPT: "API REST Python"
──────────────────────────────────────────

Base Score:
  usage_count × 2 = 15 × 2 = 30 points

Bonus Contexte:
  ✅ Catégorie = "Développement" (VS Code détecté)
     +50 points

Bonus Mots-clés:
  ✅ "python" dans titre de fenêtre "main.py"
     +10 points
  ✅ "api" mentionné dans code visible
     +10 points

Bonus Popularité:
  ✅ usage_count > 5
     +20 points

SCORE TOTAL: 120 points
────────────────────────────────────────────
```

### Exemple de Classement

```
VOUS ÊTES SUR: VS Code - main.py

Ranking:
1. API REST Python (Dév) ✨ 15      → Score: 120
   └─ Catégorie match + Populaire + Mots-clés

2. Debug Assistant (Dév) ✨ 8       → Score: 82
   └─ Catégorie match + Mots-clés

3. Code Review (Dév) ✨ 3           → Score: 76
   └─ Catégorie match

4. Email Marketing (Mark) ✨ 5      → Score: 10
   └─ Juste le score de base

5. Pitch Business (Bus) ✨ 0        → Score: 0
   └─ Pas pertinent pour le contexte
```

## 🔍 Détection de Contexte

### Applications Détectées

```
┌─────────────────────────────────────────────────────┐
│  VOUS OUVREZ PROMPTMASTER DEPUIS...                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📝 VS Code                                         │
│  └─→ 📍 VS Code • Développement                    │
│       Prompts de dev en premier                     │
│                                                     │
│  🌐 Chrome - github.com/user/repo                   │
│  └─→ 📍 Chrome • Développement • GitHub            │
│       Prompts de code/git en premier                │
│                                                     │
│  📧 Outlook - Inbox                                 │
│  └─→ 📍 Outlook • Communication                     │
│       Prompts d'email en premier                    │
│                                                     │
│  🎨 Figma - Design System                           │
│  └─→ 📍 Figma • Design                              │
│       Prompts de design en premier                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## ⌨️ Raccourcis Visuels

```
┌────────────────────────────────────────────────┐
│  RACCOURCIS CLAVIER                            │
├────────────────────────────────────────────────┤
│                                                │
│  Ctrl + Space    🚀 Ouvrir/Fermer              │
│                  (+ capture texte sélectionné) │
│                                                │
│  ↑ / ↓           📜 Naviguer dans la liste     │
│                  (prévisualisation suit)       │
│                                                │
│  Enter           📋 Copier le prompt           │
│                                                │
│  Double-clic     ✏️ Éditer le prompt           │
│                                                │
│  Molette         🔄 Défiler                    │
│                  (liste ou contenu)            │
│                                                │
│  Échap           ❌ Fermer                      │
│                                                │
└────────────────────────────────────────────────┘
```

## 💡 Suggestions Automatiques

### Boutons "💡 Suggérer"

```
LORS DE LA CRÉATION D'UN PROMPT:

┌──────────────────────────────────────┐
│  Catégorie: [          ] 💡 Suggérer │
│             ↑ Vide                   │
└──────────────────────────────────────┘
         ↓ Clic sur 💡 Suggérer

ANALYSE DU CONTEXTE:
✅ Application active: VS Code
✅ Fenêtre: "main.py - Python"
→ Suggestion: "Développement"

┌──────────────────────────────────────┐
│  Catégorie: [Développement] 💡       │
│             ↑ Auto-rempli !          │
└──────────────────────────────────────┘
```

```
┌──────────────────────────────────────┐
│  Tags: [                    ] 💡     │
│         ↑ Vide                       │
└──────────────────────────────────────┘
         ↓ Clic sur 💡 Suggérer

ANALYSE DU CONTENU:
"Créez une API REST en Python avec 
 FastAPI incluant authentification..."

Extraction de mots-clés:
✅ python (fréquence: 3)
✅ api (fréquence: 2)
✅ rest (fréquence: 2)
✅ fastapi (fréquence: 1)
✅ authentification (fréquence: 1)

┌──────────────────────────────────────┐
│  Tags: [python,api,rest,fastapi] 💡  │
│         ↑ Auto-généré !              │
└──────────────────────────────────────┘
```

## 📈 Statistiques Visuelles

### Compteur d'Utilisation

```
┌─────────────────────────────────────┐
│  Liste des prompts:                 │
│                                     │
│  API REST Python • Dév ✨ 15        │
│  └─→ Utilisé 15 fois = ⭐⭐⭐⭐⭐   │
│                                     │
│  Email Marketing • Mark ✨ 5        │
│  └─→ Utilisé 5 fois = ⭐⭐⭐         │
│                                     │
│  Nouveau Prompt • Autre             │
│  └─→ Jamais utilisé = (pas d'étoile)│
│                                     │
└─────────────────────────────────────┘
```

---

**Guide créé pour PromptMaster v2.0** 🎯
