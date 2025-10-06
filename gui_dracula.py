"""
Interface graphique principale de PromptMaster avec fonctionnalités avancées.
Application style Raycast pour rechercher et utiliser des prompts avec contexte intelligent.
"""

import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QListWidget, QListWidgetItem, QLabel,
                             QPushButton, QTextEdit, QDialog, QComboBox, QSplitter,
                             QScrollArea, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QClipboard, QTextOption
from database import DatabaseManager
from context_manager import ContextManager


class PromptMasterWindow(QWidget):
    """Fenêtre principale de PromptMaster."""
    
    def __init__(self, selected_text: str = None):
        super().__init__()
        self.db = DatabaseManager()
        self.context_manager = ContextManager(self.db)
        self.current_prompts = []
        self.selected_text = selected_text  # Texte sélectionné au lancement
        self.init_ui()
        
        # Si du texte est sélectionné, ouvrir directement le dialogue d'ajout
        if selected_text:
            QTimer.singleShot(200, self.show_add_dialog_with_text)
        else:
            self.load_contextual_prompts()
    
    def init_ui(self):
        """Initialise l'interface utilisateur."""
        # Configuration de la fenêtre
        self.setWindowTitle("PromptMaster")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Dimensions agrandies pour la prévisualisation
        self.setFixedSize(900, 600)
        self.center_on_screen()
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Container avec style
        container = QWidget()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Header avec titre et contexte
        header_layout = QHBoxLayout()
        title_label = QLabel("🎯 PromptMaster")
        title_label.setObjectName("title")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Indicateur de contexte
        self.context_label = QLabel("")
        self.context_label.setObjectName("contextLabel")
        header_layout.addWidget(self.context_label)
        
        # Bouton d'ajout
        add_btn = QPushButton("➕ Nouveau")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.show_add_dialog)
        add_btn.setFixedWidth(100)
        header_layout.addWidget(add_btn)
        
        container_layout.addLayout(header_layout)
        
        # Champ de recherche
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("🔍 Recherchez vos prompts...")
        self.search_input.textChanged.connect(self.on_search)
        self.search_input.returnPressed.connect(self.on_enter_pressed)
        container_layout.addWidget(self.search_input)
        
        # Splitter pour liste et prévisualisation
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("mainSplitter")
        
        # Liste des résultats
        self.results_list = QListWidget()
        self.results_list.setObjectName("resultsList")
        self.results_list.itemClicked.connect(self.on_item_clicked)
        self.results_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.results_list.currentItemChanged.connect(self.on_selection_changed)
        splitter.addWidget(self.results_list)
        
        # Panneau de prévisualisation
        preview_container = QWidget()
        preview_container.setObjectName("previewContainer")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(10, 10, 10, 10)
        preview_layout.setSpacing(8)
        
        # Titre de la prévisualisation
        self.preview_title = QLabel("Aucun prompt sélectionné")
        self.preview_title.setObjectName("previewTitle")
        self.preview_title.setWordWrap(True)
        preview_layout.addWidget(self.preview_title)
        
        # Métadonnées
        self.preview_meta = QLabel("")
        self.preview_meta.setObjectName("previewMeta")
        preview_layout.addWidget(self.preview_meta)
        
        # Séparateur
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        preview_layout.addWidget(separator)
        
        # Contenu de la prévisualisation
        self.preview_content = QTextEdit()
        self.preview_content.setObjectName("previewContent")
        self.preview_content.setReadOnly(True)
        self.preview_content.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        preview_layout.addWidget(self.preview_content)
        
        splitter.addWidget(preview_container)
        
        # Ratio 40/60 pour liste/prévisualisation
        splitter.setStretchFactor(0, 40)
        splitter.setStretchFactor(1, 60)
        
        container_layout.addWidget(splitter)
        
        # Footer avec instructions
        footer_label = QLabel("↵ Copier | Double-clic pour éditer | ↑↓ Naviguer | Molette Défiler | Échap pour fermer")
        footer_label.setObjectName("footer")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(footer_label)
        
        main_layout.addWidget(container)
        self.setLayout(main_layout)
        
        # Appliquer les styles
        self.apply_styles()
        
        # Mettre à jour le contexte
        self.update_context_display()
    
    def apply_styles(self):
        """Applique le thème Dracula à l'interface."""
        self.setStyleSheet("""
            QWidget#container {
                background-color: #282a36;
                border-radius: 12px;
                border: 2px solid #44475a;
            }
            
            QLabel#title {
                color: #f8f8f2;
                font-size: 22px;
                font-weight: bold;
                padding: 5px;
            }
            
            QLabel#contextLabel {
                color: #8be9fd;
                font-size: 11px;
                padding: 5px;
                background-color: #44475a;
                border-radius: 4px;
            }
            
            QLineEdit#searchInput {
                background-color: #44475a;
                border: 2px solid #6272a4;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                color: #f8f8f2;
            }
            
            QLineEdit#searchInput:focus {
                border: 2px solid #bd93f9;
            }
            
            QSplitter#mainSplitter {
                background-color: transparent;
            }
            
            QListWidget#resultsList {
                background-color: #1e1f29;
                border: 1px solid #44475a;
                border-radius: 8px;
                padding: 5px;
                color: #f8f8f2;
                font-size: 14px;
            }
            
            QListWidget#resultsList::item {
                padding: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            
            QListWidget#resultsList::item:hover {
                background-color: #44475a;
            }
            
            QListWidget#resultsList::item:selected {
                background-color: #bd93f9;
                color: #282a36;
                font-weight: bold;
            }
            
            QWidget#previewContainer {
                background-color: #1e1f29;
                border: 1px solid #44475a;
                border-radius: 8px;
            }
            
            QLabel#previewTitle {
                color: #50fa7b;
                font-size: 16px;
                font-weight: bold;
            }
            
            QLabel#previewMeta {
                color: #8be9fd;
                font-size: 11px;
            }
            
            QFrame#separator {
                background-color: #44475a;
            }
            
            QTextEdit#previewContent {
                background-color: #282a36;
                border: 1px solid #44475a;
                border-radius: 6px;
                padding: 10px;
                color: #f8f8f2;
                font-size: 13px;
                line-height: 1.6;
            }
            
            QLabel#footer {
                color: #6272a4;
                font-size: 10px;
                padding: 5px;
            }
            
            QPushButton#addButton {
                background-color: #50fa7b;
                color: #282a36;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QPushButton#addButton:hover {
                background-color: #5fff87;
            }
            
            QPushButton#addButton:pressed {
                background-color: #3de064;
            }
        """)
    
    def center_on_screen(self):
        """Centre la fenêtre sur l'écran."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 3
        self.move(x, y)
    
    def update_context_display(self):
        """Met à jour l'affichage du contexte."""
        context_summary = self.context_manager.get_context_summary()
        self.context_label.setText(context_summary)
    
    def load_contextual_prompts(self):
        """Charge les prompts en fonction du contexte."""
        self.current_prompts = self.context_manager.get_contextual_prompts(limit=50)
        self.update_results_list()
    
    def load_all_prompts(self):
        """Charge tous les prompts dans la liste."""
        self.current_prompts = self.db.get_all_prompts()
        self.update_results_list()
    
    def on_search(self, text: str):
        """Gère la recherche en temps réel."""
        if text.strip():
            self.current_prompts = self.db.search_prompts(text)
        else:
            # Si recherche vide, afficher les prompts contextuels
            self.load_contextual_prompts()
        
        self.update_results_list()
    
    def update_results_list(self):
        """Met à jour la liste des résultats affichés."""
        self.results_list.clear()
        
        for prompt in self.current_prompts:
            prompt_id, title, content, category, tags, usage_count = prompt
            
            # Formater l'affichage
            display_text = f"{title}"
            if category:
                display_text += f" • {category}"
            if usage_count > 0:
                display_text += f" • ✨ {usage_count}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, prompt_id)
            self.results_list.addItem(item)
        
        # Sélectionner le premier élément automatiquement
        if self.results_list.count() > 0:
            self.results_list.setCurrentRow(0)
    
    def on_selection_changed(self, current, previous):
        """Gère le changement de sélection dans la liste."""
        if current:
            prompt_id = current.data(Qt.ItemDataRole.UserRole)
            self.update_preview(prompt_id)
    
    def update_preview(self, prompt_id: int):
        """Met à jour la prévisualisation du prompt."""
        prompt = self.db.get_prompt_by_id(prompt_id)
        
        if prompt:
            _, title, content, category, tags, usage_count = prompt
            
            # Titre
            self.preview_title.setText(title)
            
            # Métadonnées
            meta_parts = []
            if category:
                meta_parts.append(f"📁 {category}")
            if tags:
                meta_parts.append(f"🏷️ {tags}")
            if usage_count > 0:
                meta_parts.append(f"✨ Utilisé {usage_count} fois")
            
            self.preview_meta.setText(" • ".join(meta_parts) if meta_parts else "")
            
            # Contenu
            self.preview_content.setText(content)
        else:
            self.preview_title.setText("Aucun prompt sélectionné")
            self.preview_meta.setText("")
            self.preview_content.setText("")
    
    def on_enter_pressed(self):
        """Gère l'appui sur Entrée : copie le prompt sélectionné."""
        current_item = self.results_list.currentItem()
        if current_item:
            self.copy_prompt_to_clipboard(current_item)
    
    def on_item_clicked(self, item):
        """Gère le clic simple sur un élément."""
        # La prévisualisation se met à jour automatiquement via on_selection_changed
        pass
    
    def on_item_double_clicked(self, item):
        """Gère le double-clic sur un élément : ouvre l'éditeur."""
        prompt_id = item.data(Qt.ItemDataRole.UserRole)
        self.show_edit_dialog(prompt_id)
    
    def copy_prompt_to_clipboard(self, item):
        """Copie le contenu d'un prompt dans le presse-papiers."""
        prompt_id = item.data(Qt.ItemDataRole.UserRole)
        prompt = self.db.get_prompt_by_id(prompt_id)
        
        if prompt:
            content = prompt[2]
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            
            # Incrémenter l'usage
            self.db.increment_usage(prompt_id)
            
            # Feedback visuel
            self.show_feedback("✓ Copié dans le presse-papiers !")
            
            # Fermer la fenêtre après un court délai
            QTimer.singleShot(500, self.hide)
    
    def show_feedback(self, message: str):
        """Affiche un message de feedback temporaire."""
        original_placeholder = self.search_input.placeholderText()
        self.search_input.setPlaceholderText(message)
        QTimer.singleShot(2000, lambda: self.search_input.setPlaceholderText(original_placeholder))
    
    def show_add_dialog_with_text(self):
        """Affiche le dialogue d'ajout avec le texte sélectionné pré-rempli."""
        dialog = PromptEditorDialog(self, self.db, self.context_manager, 
                                    prefill_content=self.selected_text)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_contextual_prompts()
            self.search_input.clear()
    
    def show_add_dialog(self):
        """Affiche le dialogue pour ajouter un nouveau prompt."""
        dialog = PromptEditorDialog(self, self.db, self.context_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_contextual_prompts()
            self.search_input.clear()
    
    def show_edit_dialog(self, prompt_id: int):
        """Affiche le dialogue pour éditer un prompt existant."""
        dialog = PromptEditorDialog(self, self.db, self.context_manager, prompt_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_contextual_prompts()
            self.on_search(self.search_input.text())
    
    def keyPressEvent(self, event):
        """Gère les raccourcis clavier."""
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key.Key_Down:
            current_row = self.results_list.currentRow()
            if current_row < self.results_list.count() - 1:
                self.results_list.setCurrentRow(current_row + 1)
        elif event.key() == Qt.Key.Key_Up:
            current_row = self.results_list.currentRow()
            if current_row > 0:
                self.results_list.setCurrentRow(current_row - 1)
        else:
            super().keyPressEvent(event)
    
    def wheelEvent(self, event):
        """Gère la molette de la souris pour le défilement."""
        # Transmettre l'événement de molette à la liste de résultats
        if self.results_list.underMouse():
            self.results_list.wheelEvent(event)
        else:
            super().wheelEvent(event)
    
    def showEvent(self, event):
        """Appelé quand la fenêtre est affichée."""
        super().showEvent(event)
        self.search_input.setFocus()
        self.search_input.clear()
        self.update_context_display()
        if not self.selected_text:
            self.load_contextual_prompts()


class PromptEditorDialog(QDialog):
    """Dialogue pour ajouter ou éditer un prompt."""
    
    def __init__(self, parent, db: DatabaseManager, context_manager: ContextManager = None,
                 prompt_id: int = None, prefill_content: str = None):
        super().__init__(parent)
        self.db = db
        self.context_manager = context_manager
        self.prompt_id = prompt_id
        self.prefill_content = prefill_content
        self.init_ui()
        
        if prompt_id:
            self.load_prompt()
        elif prefill_content:
            self.prefill_from_text()
    
    def init_ui(self):
        """Initialise l'interface du dialogue."""
        self.setWindowTitle("Nouveau Prompt" if not self.prompt_id else "Éditer le Prompt")
        self.setModal(True)
        self.setFixedSize(700, 600)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Titre
        title_label = QLabel("Titre:")
        title_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(title_label)
        
        self.title_input = QLineEdit()
        self.title_input.setStyleSheet("""
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 14px;
        """)
        layout.addWidget(self.title_input)
        
        # Catégorie avec suggestion contextuelle
        category_layout = QHBoxLayout()
        category_label = QLabel("Catégorie:")
        category_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        category_layout.addWidget(category_label)
        
        # Bouton pour suggestion de catégorie
        if self.context_manager:
            suggest_cat_btn = QPushButton("💡 Suggérer")
            suggest_cat_btn.setStyleSheet("""
                background-color: #6272a4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            """)
            suggest_cat_btn.clicked.connect(self.suggest_category)
            category_layout.addWidget(suggest_cat_btn)
        
        category_layout.addStretch()
        layout.addLayout(category_layout)
        
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        categories = [""] + self.db.get_categories() + ["Développement", "Marketing", "Rédaction", "Business", "Autre"]
        self.category_input.addItems(list(dict.fromkeys(categories)))  # Supprimer les doublons
        self.category_input.setStyleSheet("""
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 14px;
        """)
        layout.addWidget(self.category_input)
        
        # Tags avec suggestion
        tags_layout = QHBoxLayout()
        tags_label = QLabel("Tags (séparés par des virgules):")
        tags_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        tags_layout.addWidget(tags_label)
        
        # Bouton pour suggestion de tags
        if self.context_manager:
            suggest_tags_btn = QPushButton("💡 Suggérer")
            suggest_tags_btn.setStyleSheet("""
                background-color: #6272a4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            """)
            suggest_tags_btn.clicked.connect(self.suggest_tags)
            tags_layout.addWidget(suggest_tags_btn)
        
        tags_layout.addStretch()
        layout.addLayout(tags_layout)
        
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("python, api, rest")
        self.tags_input.setStyleSheet("""
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 14px;
        """)
        layout.addWidget(self.tags_input)
        
        # Contenu
        content_label = QLabel("Contenu du prompt:")
        content_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
        layout.addWidget(content_label)
        
        self.content_input = QTextEdit()
        self.content_input.setStyleSheet("""
            background-color: #44475a;
            border: 2px solid #6272a4;
            border-radius: 6px;
            padding: 8px;
            color: #f8f8f2;
            font-size: 14px;
        """)
        layout.addWidget(self.content_input)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        if self.prompt_id:
            delete_btn = QPushButton("🗑️ Supprimer")
            delete_btn.setStyleSheet("""
                background-color: #ff5555;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            """)
            delete_btn.clicked.connect(self.delete_prompt)
            buttons_layout.addWidget(delete_btn)
        
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setStyleSheet("""
            background-color: #6272a4;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setStyleSheet("""
            background-color: #50fa7b;
            color: #282a36;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
        """)
        save_btn.clicked.connect(self.save_prompt)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #282a36;")
    
    def prefill_from_text(self):
        """Pré-remplit le dialogue avec le texte sélectionné."""
        if self.prefill_content:
            self.content_input.setText(self.prefill_content)
            
            # Suggérer automatiquement catégorie et tags
            if self.context_manager:
                suggested_cat = self.context_manager.suggest_category_from_context()
                if suggested_cat:
                    self.category_input.setCurrentText(suggested_cat)
                
                suggested_tags = self.context_manager.suggest_tags_from_text(self.prefill_content)
                self.tags_input.setText(suggested_tags)
            
            # Mettre le focus sur le titre
            self.title_input.setFocus()
    
    def suggest_category(self):
        """Suggère une catégorie basée sur le contexte."""
        if self.context_manager:
            suggested = self.context_manager.suggest_category_from_context()
            if suggested:
                self.category_input.setCurrentText(suggested)
    
    def suggest_tags(self):
        """Suggère des tags basés sur le contenu."""
        if self.context_manager:
            content = self.content_input.toPlainText()
            if content:
                suggested = self.context_manager.suggest_tags_from_text(content)
                self.tags_input.setText(suggested)
    
    def load_prompt(self):
        """Charge les données d'un prompt existant."""
        prompt = self.db.get_prompt_by_id(self.prompt_id)
        if prompt:
            self.title_input.setText(prompt[1])
            self.content_input.setText(prompt[2])
            if prompt[3]:
                self.category_input.setCurrentText(prompt[3])
            if prompt[4]:
                self.tags_input.setText(prompt[4])
    
    def save_prompt(self):
        """Enregistre le prompt."""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        category = self.category_input.currentText().strip()
        tags = self.tags_input.text().strip()
        
        if not title or not content:
            return
        
        if self.prompt_id:
            self.db.update_prompt(self.prompt_id, title, content, category, tags)
        else:
            self.db.add_prompt(title, content, category, tags)
        
        self.accept()
    
    def delete_prompt(self):
        """Supprime le prompt."""
        if self.prompt_id:
            self.db.delete_prompt(self.prompt_id)
            self.accept()


def main():
    """Point d'entrée de l'application."""
    app = QApplication(sys.argv)
    
    # Configuration de la police
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = PromptMasterWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
