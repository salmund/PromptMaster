"""
Gestionnaire de contexte pour PromptMaster.
Détecte l'application active, capture le texte sélectionné, et fournit des recommandations contextuelles.
"""

import pyperclip
import time
from typing import Optional, Dict, List
from datetime import datetime

try:
    import win32gui
    import win32process
    import psutil
    WINDOWS_SUPPORT = True
except ImportError:
    WINDOWS_SUPPORT = False
    print("⚠️ win32gui non disponible. Installez pywin32 pour le support complet du contexte.")

try:
    from pynput.keyboard import Key, Controller as KeyboardController
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


class ContextManager:
    """Gère le contexte de l'utilisateur pour des recommandations intelligentes."""
    
    def __init__(self, db_manager=None):
        """
        Initialise le gestionnaire de contexte.
        
        Args:
            db_manager: Instance de DatabaseManager pour les recommandations
        """
        self.db = db_manager
        self.keyboard = KeyboardController() if PYNPUT_AVAILABLE else None
        
        # Mapping d'applications vers catégories
        self.app_categories = {
            'code.exe': 'Développement',
            'vscode.exe': 'Développement',
            'pycharm64.exe': 'Développement',
            'sublime_text.exe': 'Développement',
            'notepad++.exe': 'Développement',
            
            'chrome.exe': 'Navigation',
            'firefox.exe': 'Navigation',
            'msedge.exe': 'Navigation',
            'brave.exe': 'Navigation',
            
            'slack.exe': 'Communication',
            'teams.exe': 'Communication',
            'discord.exe': 'Communication',
            
            'notion.exe': 'Productivité',
            'onenote.exe': 'Productivité',
            'obsidian.exe': 'Productivité',
            
            'word.exe': 'Rédaction',
            'winword.exe': 'Rédaction',
            'excel.exe': 'Rédaction',
            
            'figma.exe': 'Design',
            'photoshop.exe': 'Design',
        }
        
        # Mots-clés pour détecter le type de site web
        self.web_keywords = {
            'github': ['Développement', 'git'],
            'stackoverflow': ['Développement', 'code'],
            'linkedin': ['Business', 'professionnel'],
            'twitter': ['Marketing', 'social'],
            'facebook': ['Marketing', 'social'],
            'gmail': ['Communication', 'email'],
            'outlook': ['Communication', 'email'],
            'notion': ['Productivité', 'notes'],
            'figma': ['Design', 'ui'],
            'canva': ['Design', 'marketing'],
            'docs.google': ['Rédaction', 'document'],
            'youtube': ['Vidéo', 'contenu'],
        }
    
    def get_active_window_info(self) -> Dict[str, str]:
        """
        Récupère les informations sur la fenêtre active.
        
        Returns:
            Dict avec app_name, window_title, process_name, category
        """
        if not WINDOWS_SUPPORT:
            return {
                'app_name': 'Unknown',
                'window_title': '',
                'process_name': 'unknown',
                'category': None
            }
        
        try:
            # Obtenir le handle de la fenêtre active
            hwnd = win32gui.GetForegroundWindow()
            
            # Obtenir le titre de la fenêtre
            window_title = win32gui.GetWindowText(hwnd)
            
            # Obtenir le PID du processus
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Obtenir le nom du processus
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                app_name = process.name().replace('.exe', '').title()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = 'unknown'
                app_name = 'Unknown'
            
            # Déterminer la catégorie
            category = self.app_categories.get(process_name.lower())
            
            # Analyse du titre pour les navigateurs
            if category == 'Navigation':
                for keyword, tags in self.web_keywords.items():
                    if keyword in window_title.lower():
                        category = tags[0]
                        break
            
            return {
                'app_name': app_name,
                'window_title': window_title,
                'process_name': process_name,
                'category': category,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"Erreur lors de la récupération du contexte : {e}")
            return {
                'app_name': 'Unknown',
                'window_title': '',
                'process_name': 'unknown',
                'category': None
            }
    
    def capture_selected_text(self) -> Optional[str]:
        """
        Capture le texte actuellement sélectionné dans n'importe quelle application.
        Utilise Ctrl+C pour copier temporairement la sélection.
        
        Returns:
            Le texte sélectionné ou None si aucun texte n'est sélectionné
        """
        if not self.keyboard:
            return None
        
        try:
            # Sauvegarder le presse-papiers actuel
            old_clipboard = ""
            try:
                old_clipboard = pyperclip.paste()
            except:
                pass
            
            # Vider le presse-papiers
            pyperclip.copy("")
            
            # Petit délai pour s'assurer que le presse-papiers est vide
            time.sleep(0.1)
            
            # Créer un nouveau controller keyboard temporaire pour éviter les conflits
            temp_keyboard = KeyboardController()
            
            # Simuler Ctrl+C pour copier la sélection
            temp_keyboard.press(Key.ctrl)
            time.sleep(0.05)
            temp_keyboard.press('c')
            temp_keyboard.release('c')
            temp_keyboard.release(Key.ctrl)
            
            # Attendre que le texte soit copié
            time.sleep(0.2)
            
            # Récupérer le texte copié
            selected_text = pyperclip.paste()
            
            # Restaurer l'ancien presse-papiers
            if old_clipboard:
                time.sleep(0.05)
                pyperclip.copy(old_clipboard)
            
            # Retourner le texte seulement s'il n'est pas vide et différent de l'ancien
            if selected_text and selected_text.strip() and selected_text != old_clipboard:
                return selected_text.strip()
            
            return None
            
        except Exception as e:
            print(f"Erreur lors de la capture du texte : {e}")
            return None
    
    def get_contextual_prompts(self, limit: int = 10) -> List[tuple]:
        """
        Récupère les prompts les plus pertinents selon le contexte actuel.
        
        Args:
            limit: Nombre maximum de prompts à retourner
            
        Returns:
            Liste de tuples (id, title, content, category, tags, usage_count)
        """
        if not self.db:
            return []
        
        context = self.get_active_window_info()
        category = context.get('category')
        window_title = context.get('window_title', '').lower()
        
        all_prompts = self.db.get_all_prompts()
        
        # Scoring des prompts
        scored_prompts = []
        for prompt in all_prompts:
            prompt_id, title, content, prompt_cat, tags, usage_count = prompt
            score = usage_count * 2  # Score de base avec usage_count
            
            # Bonus si la catégorie correspond
            if category and prompt_cat == category:
                score += 50
            
            # Bonus si des mots du titre de la fenêtre sont dans le titre ou tags
            if tags:
                for word in window_title.split():
                    if len(word) > 3:  # Mots significatifs seulement
                        if word in title.lower() or word in tags.lower():
                            score += 10
            
            # Bonus si utilisé récemment (usage_count élevé)
            if usage_count > 5:
                score += 20
            
            scored_prompts.append((score, prompt))
        
        # Trier par score décroissant
        scored_prompts.sort(key=lambda x: x[0], reverse=True)
        
        # Retourner les meilleurs prompts
        return [prompt for score, prompt in scored_prompts[:limit]]
    
    def get_context_summary(self) -> str:
        """
        Génère un résumé textuel du contexte actuel.
        
        Returns:
            String décrivant le contexte
        """
        context = self.get_active_window_info()
        app_name = context.get('app_name', 'Unknown')
        category = context.get('category', 'Général')
        window_title = context.get('window_title', '')
        
        if window_title:
            # Limiter la longueur du titre
            if len(window_title) > 50:
                window_title = window_title[:47] + "..."
            return f"📍 {app_name} • {category or 'Général'} • {window_title}"
        else:
            return f"📍 {app_name} • {category or 'Général'}"
    
    def extract_keywords_from_text(self, text: str, max_keywords: int = 5) -> List[str]:
        """
        Extrait des mots-clés d'un texte pour suggérer des tags.
        
        Args:
            text: Le texte à analyser
            max_keywords: Nombre maximum de mots-clés
            
        Returns:
            Liste de mots-clés
        """
        # Mots communs à ignorer
        stopwords = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais',
            'est', 'sont', 'a', 'ont', 'pour', 'dans', 'sur', 'avec', 'sans',
            'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
        }
        
        # Nettoyer et découper le texte
        words = text.lower().replace('\n', ' ').split()
        
        # Compter les occurrences
        word_count = {}
        for word in words:
            # Nettoyer le mot
            word = ''.join(c for c in word if c.isalnum())
            # Ignorer les mots courts et les stopwords
            if len(word) > 3 and word not in stopwords:
                word_count[word] = word_count.get(word, 0) + 1
        
        # Trier par fréquence
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        # Retourner les mots les plus fréquents
        return [word for word, count in sorted_words[:max_keywords]]
    
    def suggest_category_from_context(self) -> Optional[str]:
        """
        Suggère une catégorie basée sur le contexte actuel.
        
        Returns:
            Nom de la catégorie suggérée ou None
        """
        context = self.get_active_window_info()
        return context.get('category')
    
    def suggest_tags_from_text(self, text: str) -> str:
        """
        Suggère des tags basés sur le texte et le contexte.
        
        Args:
            text: Le texte du prompt
            
        Returns:
            String de tags séparés par des virgules
        """
        keywords = self.extract_keywords_from_text(text, max_keywords=5)
        
        # Ajouter le contexte de l'application
        context = self.get_active_window_info()
        app_name = context.get('app_name', '').lower()
        
        if app_name and app_name not in keywords:
            keywords.insert(0, app_name)
        
        return ','.join(keywords[:5])


# Fonction utilitaire pour installer pywin32 si nécessaire
def check_dependencies():
    """Vérifie et suggère l'installation des dépendances manquantes."""
    missing = []
    
    if not WINDOWS_SUPPORT:
        missing.append('pywin32')
    
    if not PYNPUT_AVAILABLE:
        missing.append('pynput')
    
    if missing:
        print("\n⚠️ Dépendances manquantes pour les fonctionnalités avancées :")
        for dep in missing:
            print(f"   - {dep}")
        print("\nInstallez-les avec :")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


if __name__ == "__main__":
    # Test du module
    print("=== Test du Context Manager ===\n")
    
    if check_dependencies():
        cm = ContextManager()
        
        print("📍 Contexte actuel :")
        context = cm.get_active_window_info()
        for key, value in context.items():
            if key != 'timestamp':
                print(f"   {key}: {value}")
        
        print(f"\n{cm.get_context_summary()}")
        
        print("\n🔍 Test de capture de texte sélectionné :")
        print("   Sélectionnez du texte et appuyez sur Entrée...")
        input()
        
        selected = cm.capture_selected_text()
        if selected:
            print(f"   ✓ Texte capturé : {selected[:100]}...")
            
            keywords = cm.extract_keywords_from_text(selected)
            print(f"   Mots-clés : {', '.join(keywords)}")
        else:
            print("   ✗ Aucun texte sélectionné")
