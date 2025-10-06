"""
Gestionnaire de raccourci clavier global pour PromptMaster.
Écoute Ctrl+Space pour afficher/masquer l'application avec capture du texte sélectionné.
"""

import sys
from pynput import keyboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, QTimer
from gui import PromptMasterWindow
from context_manager import ContextManager


class HotkeyListener(QObject):
    """Gestionnaire de raccourci clavier global."""
    
    # Signal pour communiquer avec le thread Qt
    toggle_signal = Signal()
    
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.window = None
        self.context_manager = ContextManager()
        self.current_keys = set()
        self.hotkey_triggered = False  # Flag pour éviter les doubles triggers
        
        # Connecter le signal au slot
        self.toggle_signal.connect(self._toggle_window_slot)
        
        # Combinaison de touches : Ctrl + Space
        self.HOTKEYS = {
            keyboard.Key.ctrl_l,
            keyboard.Key.space
        }
        
        # Alternative : Ctrl droit
        self.HOTKEYS_ALT = {
            keyboard.Key.ctrl_r,
            keyboard.Key.space
        }
    
    def on_press(self, key):
        """Appelé quand une touche est pressée."""
        self.current_keys.add(key)
        
        # Déclencher seulement quand Space est pressée ET Ctrl est déjà enfoncé
        if key == keyboard.Key.space and not self.hotkey_triggered:
            if (keyboard.Key.ctrl_l in self.current_keys or 
                keyboard.Key.ctrl_r in self.current_keys):
                self.hotkey_triggered = True
                self.toggle_signal.emit()
    
    def on_release(self, key):
        """Appelé quand une touche est relâchée."""
        # Réinitialiser le flag quand Space est relâché
        if key == keyboard.Key.space:
            self.hotkey_triggered = False
        
        # Enlever la touche de l'ensemble
        self.current_keys.discard(key)
    
    def _toggle_window_slot(self):
        """Slot appelé dans le thread Qt pour afficher/cacher la fenêtre."""
        if self.window and self.window.isVisible():
            # Cacher la fenêtre
            self.window.hide()
            print("🔽 Fenêtre masquée")
        else:
            # Capturer le texte sélectionné avant d'afficher la fenêtre
            selected_text = self.context_manager.capture_selected_text()
            
            # Si du texte est sélectionné, recréer la fenêtre pour ouvrir le dialogue
            if selected_text:
                print(f"📝 Texte capturé : {selected_text[:50]}...")
                if self.window:
                    self.window.close()
                    self.window.deleteLater()
                self.window = PromptMasterWindow(selected_text=selected_text)
            # Sinon, créer la fenêtre si elle n'existe pas encore
            elif not self.window:
                print("🔼 Fenêtre affichée")
                self.window = PromptMasterWindow()
            else:
                print("🔼 Fenêtre réaffichée")
            
            # Afficher et mettre au premier plan
            self.window.show()
            self.window.activateWindow()
            self.window.raise_()
    
    def start(self):
        """Démarre l'écoute des événements clavier."""
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        print("✓ Raccourci clavier activé : Ctrl + Space")
    
    def stop(self):
        """Arrête l'écoute des événements clavier."""
        if hasattr(self, 'listener'):
            self.listener.stop()


def main():
    """Point d'entrée de l'application avec raccourci global."""
    app = QApplication(sys.argv)
    
    # Configurer le raccourci clavier
    hotkey_listener = HotkeyListener(app)
    hotkey_listener.start()
    
    # Message de bienvenue
    print("\n" + "="*50)
    print("🎯 PromptMaster est démarré !")
    print("="*50)
    print("Appuyez sur Ctrl + Space pour afficher l'application")
    print("Sélectionnez du texte avant d'appuyer sur Ctrl + Space")
    print("pour l'ajouter directement comme nouveau prompt !")
    print("Appuyez sur Échap pour la fermer")
    print("="*50 + "\n")
    
    # Ne PAS créer la fenêtre au démarrage
    # L'utilisateur appuiera sur Ctrl+Space pour l'ouvrir
    
    # Lancer l'application
    try:
        sys.exit(app.exec())
    finally:
        hotkey_listener.stop()


if __name__ == "__main__":
    main()
