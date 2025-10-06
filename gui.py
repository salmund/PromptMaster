"""
Interface graphique Fluent Design pour PromptMaster.
Application moderne avec PySide6-Fluent-Widgets.
"""

import sys
from PySide6.QtCore import Qt, QTimer, Signal, QSize
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon

from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, FluentIcon,
    SearchLineEdit, ListWidget, PushButton, TextEdit,
    LineEdit, ComboBox, Dialog, BodyLabel, SubtitleLabel,
    TitleLabel, CaptionLabel, PrimaryPushButton, TransparentPushButton,
    setTheme, Theme, isDarkTheme, setThemeColor, SplitFluentWindow,
    InfoBar, InfoBarPosition, CardWidget, ScrollArea
)

from database import DatabaseManager
from context_manager import ContextManager


class PromptMasterWindow(FluentWindow):
    """Fenêtre principale de PromptMaster avec Fluent Design."""
    
    def __init__(self, selected_text: str = None):
        super().__init__()
        self.db = DatabaseManager()
        self.context_manager = ContextManager(self.db)
        self.current_prompts = []
        self.selected_text = selected_text
        
        self.init_ui()
        self.init_navigation()
        
        # Si du texte est sélectionné, ouvrir le dialogue d'ajout
        if selected_text:
            QTimer.singleShot(200, self.show_add_dialog_with_text)
        else:
            self.load_contextual_prompts()
    
    def init_ui(self):
        """Initialise l'interface utilisateur."""
        # Configuration de la fenêtre
        self.setWindowTitle("PromptMaster")
        self.setWindowIcon(QIcon())
        
        # Dimensions
        self.resize(1000, 700)
        self.center_on_screen()
        
        # Thème sombre par défaut
        setTheme(Theme.DARK)
        setThemeColor('#bd93f9')  # Violet Dracula
        
        # Interface principale
        self.create_main_interface()
    
    def init_navigation(self):
        """Initialise la barre de navigation."""
        # Navigation principale (masquée pour rester simple)
        self.navigationInterface.setMinimumExpandWidth(1500)  # Ne s'expand jamais
        self.navigationInterface.setExpandWidth(200)
        
        # Cacher le toggle pour garder l'interface simple
        self.navigationInterface.setCollapsible(False)
    
    def create_main_interface(self):
        """Crée l'interface principale de recherche."""
        # Widget principal
        self.search_interface = QWidget()
        layout = QVBoxLayout(self.search_interface)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # En-tête avec titre et contexte
        header_layout = QHBoxLayout()
        
        # Titre
        title = TitleLabel("🎯 PromptMaster")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Contexte
        self.context_label = CaptionLabel("")
        self.context_label.setStyleSheet("color: #8be9fd; padding: 8px 12px; background: rgba(98, 114, 164, 0.2); border-radius: 4px;")
        header_layout.addWidget(self.context_label)
        
        # Bouton nouveau
        add_btn = PrimaryPushButton("➕ Nouveau")
        add_btn.setFixedWidth(120)
        add_btn.clicked.connect(self.show_add_dialog)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Barre de recherche
        self.search_input = SearchLineEdit()
        self.search_input.setPlaceholderText("🔍 Recherchez vos prompts...")
        self.search_input.textChanged.connect(self.on_search)
        self.search_input.returnPressed.connect(self.on_enter_pressed)
        self.search_input.setFixedHeight(45)
        layout.addWidget(self.search_input)
        
        # Conteneur pour liste et prévisualisation
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Liste des résultats dans une card
        list_card = CardWidget()
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(5, 5, 5, 5)
        
        self.results_list = ListWidget()
        self.results_list.setAlternatingRowColors(True)
        self.results_list.itemClicked.connect(self.on_item_clicked)
        self.results_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.results_list.currentItemChanged.connect(self.on_selection_changed)
        list_layout.addWidget(self.results_list)
        
        content_layout.addWidget(list_card, 4)
        
        # Panneau de prévisualisation dans une card
        preview_card = CardWidget()
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        preview_layout.setSpacing(12)
        
        # Titre du prompt
        self.preview_title = SubtitleLabel("Sélectionnez un prompt")
        self.preview_title.setWordWrap(True)
        preview_layout.addWidget(self.preview_title)
        
        # Métadonnées
        self.preview_meta = CaptionLabel("")
        self.preview_meta.setStyleSheet("color: #8be9fd;")
        preview_layout.addWidget(self.preview_meta)
        
        # Contenu
        self.preview_content = TextEdit()
        self.preview_content.setReadOnly(True)
        preview_layout.addWidget(self.preview_content)
        
        content_layout.addWidget(preview_card, 6)
        
        layout.addLayout(content_layout, 1)
        
        # Footer
        footer = CaptionLabel("↵ Copier | Double-clic Éditer | ↑↓ Naviguer | Échap Fermer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #6272a4;")
        layout.addWidget(footer)
        
        # Ajouter à la fenêtre en tant que widget central
        self.search_interface.setObjectName("searchInterface")
        self.addSubInterface(self.search_interface, FluentIcon.SEARCH, "Recherche", NavigationItemPosition.TOP)
        
        # Mettre à jour le contexte
        self.update_context_display()
    
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
    
    def on_search(self, text: str):
        """Gère la recherche en temps réel."""
        if text.strip():
            self.current_prompts = self.db.search_prompts(text)
        else:
            self.load_contextual_prompts()
        self.update_results_list()
    
    def update_results_list(self):
        """Met à jour la liste des résultats."""
        self.results_list.clear()
        
        for prompt in self.current_prompts:
            prompt_id, title, content, category, tags, usage_count = prompt
            
            display_text = f"{title}"
            if category:
                display_text += f"  •  {category}"
            if usage_count > 0:
                display_text += f"  •  ✨ {usage_count}"
            
            # Utiliser la méthode correcte de ListWidget de Fluent
            self.results_list.addItem(display_text)
            # Stocker l'ID dans une structure parallèle
            if not hasattr(self, 'prompt_ids'):
                self.prompt_ids = {}
            self.prompt_ids[self.results_list.count() - 1] = prompt_id
        
        if self.results_list.count() > 0:
            self.results_list.setCurrentRow(0)
    
    def on_selection_changed(self, current, previous):
        """Gère le changement de sélection."""
        if current:
            row = self.results_list.row(current)
            if hasattr(self, 'prompt_ids') and row in self.prompt_ids:
                prompt_id = self.prompt_ids[row]
                self.update_preview(prompt_id)
    
    def update_preview(self, prompt_id: int):
        """Met à jour la prévisualisation."""
        prompt = self.db.get_prompt_by_id(prompt_id)
        
        if prompt:
            _, title, content, category, tags, usage_count = prompt
            
            self.preview_title.setText(title)
            
            meta_parts = []
            if category:
                meta_parts.append(f"📁 {category}")
            if tags:
                meta_parts.append(f"🏷️ {tags}")
            if usage_count > 0:
                meta_parts.append(f"✨ {usage_count} utilisations")
            
            self.preview_meta.setText("  •  ".join(meta_parts) if meta_parts else "")
            self.preview_content.setPlainText(content)
        else:
            self.preview_title.setText("Sélectionnez un prompt")
            self.preview_meta.setText("")
            self.preview_content.setPlainText("")
    
    def on_enter_pressed(self):
        """Copie le prompt sélectionné."""
        current_item = self.results_list.currentItem()
        if current_item:
            self.copy_prompt_to_clipboard(current_item)
    
    def on_item_clicked(self, item):
        """Gère le clic simple."""
        pass
    
    def on_item_double_clicked(self, item):
        """Ouvre l'éditeur en double-clic."""
        row = self.results_list.row(item)
        if hasattr(self, 'prompt_ids') and row in self.prompt_ids:
            prompt_id = self.prompt_ids[row]
            self.show_edit_dialog(prompt_id)
    
    def copy_prompt_to_clipboard(self, item):
        """Copie le prompt dans le presse-papiers."""
        row = self.results_list.row(item)
        if hasattr(self, 'prompt_ids') and row in self.prompt_ids:
            prompt_id = self.prompt_ids[row]
            prompt = self.db.get_prompt_by_id(prompt_id)
        
        if prompt:
            content = prompt[2]
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            
            self.db.increment_usage(prompt_id)
            
            InfoBar.success(
                title="Succès",
                content="Prompt copié dans le presse-papiers !",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            
            QTimer.singleShot(500, self.hide)
    
    def show_add_dialog_with_text(self):
        """Affiche le dialogue d'ajout avec texte pré-rempli."""
        dialog = PromptEditorDialog(self, self.db, self.context_manager,
                                    prefill_content=self.selected_text)
        if dialog.exec():
            self.load_contextual_prompts()
            self.search_input.clear()
    
    def show_add_dialog(self):
        """Affiche le dialogue d'ajout."""
        dialog = PromptEditorDialog(self, self.db, self.context_manager)
        if dialog.exec():
            self.load_contextual_prompts()
            self.search_input.clear()
    
    def show_edit_dialog(self, prompt_id: int):
        """Affiche le dialogue d'édition."""
        dialog = PromptEditorDialog(self, self.db, self.context_manager, prompt_id)
        if dialog.exec():
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
    
    def showEvent(self, event):
        """Appelé quand la fenêtre s'affiche."""
        super().showEvent(event)
        self.search_input.setFocus()
        self.search_input.clear()
        self.update_context_display()
        if not self.selected_text:
            self.load_contextual_prompts()


class PromptEditorDialog(Dialog):
    """Dialogue Fluent pour éditer/créer un prompt."""
    
    def __init__(self, parent, db: DatabaseManager, context_manager: ContextManager = None,
                 prompt_id: int = None, prefill_content: str = None):
        super().__init__(parent=parent)
        self.db = db
        self.context_manager = context_manager
        self.prompt_id = prompt_id
        self.prefill_content = prefill_content
        
        self.setTitleBarVisible(True)
        self.titleBar.titleLabel.setText("Nouveau Prompt" if not prompt_id else "Éditer le Prompt")
        
        self.init_ui()
        
        if prompt_id:
            self.load_prompt()
        elif prefill_content:
            self.prefill_from_text()
    
    def init_ui(self):
        """Initialise l'interface du dialogue."""
        self.widget.setMinimumSize(700, 650)
        
        layout = QVBoxLayout(self.widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre
        title_layout = QVBoxLayout()
        title_label = BodyLabel("Titre du prompt")
        title_layout.addWidget(title_label)
        
        self.title_input = LineEdit()
        self.title_input.setPlaceholderText("Ex: API REST Python")
        self.title_input.setClearButtonEnabled(True)
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)
        
        # Catégorie
        cat_layout = QVBoxLayout()
        cat_header = QHBoxLayout()
        cat_label = BodyLabel("Catégorie")
        cat_header.addWidget(cat_label)
        
        if self.context_manager:
            suggest_cat_btn = TransparentPushButton("💡 Suggérer")
            suggest_cat_btn.setFixedWidth(100)
            suggest_cat_btn.clicked.connect(self.suggest_category)
            cat_header.addWidget(suggest_cat_btn)
        
        cat_header.addStretch()
        cat_layout.addLayout(cat_header)
        
        self.category_input = ComboBox()
        self.category_input.setEditable(True)
        categories = [""] + self.db.get_categories() + ["Développement", "Marketing", "Rédaction", "Business", "Design", "Communication"]
        self.category_input.addItems(list(dict.fromkeys(categories)))
        self.category_input.setPlaceholderText("Choisissez ou créez une catégorie")
        cat_layout.addWidget(self.category_input)
        layout.addLayout(cat_layout)
        
        # Tags
        tags_layout = QVBoxLayout()
        tags_header = QHBoxLayout()
        tags_label = BodyLabel("Tags (séparés par des virgules)")
        tags_header.addWidget(tags_label)
        
        if self.context_manager:
            suggest_tags_btn = TransparentPushButton("💡 Suggérer")
            suggest_tags_btn.setFixedWidth(100)
            suggest_tags_btn.clicked.connect(self.suggest_tags)
            tags_header.addWidget(suggest_tags_btn)
        
        tags_header.addStretch()
        tags_layout.addLayout(tags_header)
        
        self.tags_input = LineEdit()
        self.tags_input.setPlaceholderText("python, api, rest")
        self.tags_input.setClearButtonEnabled(True)
        tags_layout.addWidget(self.tags_input)
        layout.addLayout(tags_layout)
        
        # Contenu
        content_layout = QVBoxLayout()
        content_label = BodyLabel("Contenu du prompt")
        content_layout.addWidget(content_label)
        
        self.content_input = TextEdit()
        self.content_input.setPlaceholderText("Écrivez votre prompt ici...")
        content_layout.addWidget(self.content_input)
        layout.addLayout(content_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        if self.prompt_id:
            delete_btn = PushButton("🗑️ Supprimer")
            delete_btn.clicked.connect(self.delete_prompt)
            buttons_layout.addWidget(delete_btn)
        
        buttons_layout.addStretch()
        
        cancel_btn = PushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = PrimaryPushButton("💾 Enregistrer")
        save_btn.clicked.connect(self.save_prompt)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
        # Focus sur le titre
        self.title_input.setFocus()
    
    def prefill_from_text(self):
        """Pré-remplit avec le texte sélectionné."""
        if self.prefill_content:
            self.content_input.setPlainText(self.prefill_content)
            
            if self.context_manager:
                suggested_cat = self.context_manager.suggest_category_from_context()
                if suggested_cat:
                    index = self.category_input.findText(suggested_cat)
                    if index >= 0:
                        self.category_input.setCurrentIndex(index)
                    else:
                        self.category_input.setCurrentText(suggested_cat)
                
                suggested_tags = self.context_manager.suggest_tags_from_text(self.prefill_content)
                self.tags_input.setText(suggested_tags)
            
            self.title_input.setFocus()
    
    def suggest_category(self):
        """Suggère une catégorie."""
        if self.context_manager:
            suggested = self.context_manager.suggest_category_from_context()
            if suggested:
                index = self.category_input.findText(suggested)
                if index >= 0:
                    self.category_input.setCurrentIndex(index)
                else:
                    self.category_input.setCurrentText(suggested)
    
    def suggest_tags(self):
        """Suggère des tags."""
        if self.context_manager:
            content = self.content_input.toPlainText()
            if content:
                suggested = self.context_manager.suggest_tags_from_text(content)
                self.tags_input.setText(suggested)
    
    def load_prompt(self):
        """Charge un prompt existant."""
        prompt = self.db.get_prompt_by_id(self.prompt_id)
        if prompt:
            self.title_input.setText(prompt[1])
            self.content_input.setPlainText(prompt[2])
            if prompt[3]:
                index = self.category_input.findText(prompt[3])
                if index >= 0:
                    self.category_input.setCurrentIndex(index)
                else:
                    self.category_input.setCurrentText(prompt[3])
            if prompt[4]:
                self.tags_input.setText(prompt[4])
    
    def save_prompt(self):
        """Enregistre le prompt."""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        category = self.category_input.currentText().strip()
        tags = self.tags_input.text().strip()
        
        if not title:
            InfoBar.warning(
                title="Attention",
                content="Le titre ne peut pas être vide",
                parent=self
            )
            return
        
        if not content:
            InfoBar.warning(
                title="Attention",
                content="Le contenu ne peut pas être vide",
                parent=self
            )
            return
        
        if self.prompt_id:
            self.db.update_prompt(self.prompt_id, title, content, category, tags)
            InfoBar.success(
                title="Succès",
                content="Prompt modifié avec succès",
                parent=self.parent()
            )
        else:
            self.db.add_prompt(title, content, category, tags)
            InfoBar.success(
                title="Succès",
                content="Prompt créé avec succès",
                parent=self.parent()
            )
        
        self.accept()
    
    def delete_prompt(self):
        """Supprime le prompt."""
        if self.prompt_id:
            self.db.delete_prompt(self.prompt_id)
            InfoBar.success(
                title="Succès",
                content="Prompt supprimé",
                parent=self.parent()
            )
            self.accept()


def main():
    """Point d'entrée de l'application."""
    app = QApplication(sys.argv)
    
    # Configuration
    app.setApplicationName("PromptMaster")
    app.setOrganizationName("PromptMaster")
    
    window = PromptMasterWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
