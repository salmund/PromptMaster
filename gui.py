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
    LineEdit, ComboBox, EditableComboBox, MessageBoxBase, BodyLabel, SubtitleLabel,
    TitleLabel, CaptionLabel, PrimaryPushButton, TransparentPushButton,
    setTheme, Theme, isDarkTheme, setThemeColor, SplitFluentWindow,
    InfoBar, InfoBarPosition, CardWidget, ScrollArea
)

from database import DatabaseManager


class PromptMasterWindow(FluentWindow):
    """Fenêtre principale de PromptMaster avec Fluent Design - Version simplifiée."""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_prompts = []
        
        self.init_ui()
        self.init_navigation()
        self.load_all_prompts()
    
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
        
        # En-tête avec titre
        header_layout = QHBoxLayout()
        
        # Titre
        title = TitleLabel("🎯 PromptMaster")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
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
        self.results_list.currentItemChanged.connect(self.on_selection_changed)
        list_layout.addWidget(self.results_list)
        
        content_layout.addWidget(list_card, 4)
        
        # Panneau d'édition dans une card
        preview_card = CardWidget()
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(20, 20, 20, 20)
        preview_layout.setSpacing(12)
        
        # Titre du prompt (éditable)
        title_layout = QVBoxLayout()
        title_hint = CaptionLabel("Titre")
        title_hint.setStyleSheet("color: #6272a4;")
        title_layout.addWidget(title_hint)
        
        self.preview_title = LineEdit()
        self.preview_title.setPlaceholderText("Titre du prompt...")
        self.preview_title.textChanged.connect(self.on_title_changed)
        title_layout.addWidget(self.preview_title)
        preview_layout.addLayout(title_layout)
        
        # Catégorie et tags (éditables)
        meta_layout = QHBoxLayout()
        
        cat_layout = QVBoxLayout()
        cat_hint = CaptionLabel("Catégorie")
        cat_hint.setStyleSheet("color: #6272a4;")
        cat_layout.addWidget(cat_hint)
        self.preview_category = LineEdit()
        self.preview_category.setPlaceholderText("Catégorie...")
        self.preview_category.textChanged.connect(self.on_meta_changed)
        cat_layout.addWidget(self.preview_category)
        meta_layout.addLayout(cat_layout)
        
        tags_layout = QVBoxLayout()
        tags_hint = CaptionLabel("Tags")
        tags_hint.setStyleSheet("color: #6272a4;")
        tags_layout.addWidget(tags_hint)
        self.preview_tags = LineEdit()
        self.preview_tags.setPlaceholderText("tag1, tag2...")
        self.preview_tags.textChanged.connect(self.on_meta_changed)
        tags_layout.addWidget(self.preview_tags)
        meta_layout.addLayout(tags_layout)
        
        preview_layout.addLayout(meta_layout)
        
        # Contenu (éditable)
        content_hint = CaptionLabel("Contenu • Édition automatique")
        content_hint.setStyleSheet("color: #8be9fd;")
        preview_layout.addWidget(content_hint)
        
        self.preview_content = TextEdit()
        self.preview_content.setReadOnly(False)
        self.preview_content.setPlaceholderText("Sélectionnez un prompt pour l'éditer...")
        self.preview_content.textChanged.connect(self.on_content_changed)
        preview_layout.addWidget(self.preview_content)
        
        content_layout.addWidget(preview_card, 6)
        
        layout.addLayout(content_layout, 1)
        
        # Footer
        footer = CaptionLabel("↵ Copier | Del Supprimer | ↑↓ Naviguer | Échap Fermer • 💾 Sauvegarde automatique")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #6272a4;")
        layout.addWidget(footer)
        
        # Variables pour l'autosave
        self.current_prompt_id = None
        self.autosave_timer = QTimer()
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.timeout.connect(self.save_current_prompt)
        self.is_loading = False  # Flag pour éviter les sauvegardes pendant le chargement
        
        # Ajouter à la fenêtre en tant que widget central
        self.search_interface.setObjectName("searchInterface")
        self.addSubInterface(self.search_interface, FluentIcon.SEARCH, "Recherche", NavigationItemPosition.TOP)
    
    def center_on_screen(self):
        """Centre la fenêtre sur l'écran."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 3
        self.move(x, y)
    
    def load_all_prompts(self):
        """Charge tous les prompts."""
        all_prompts = self.db.get_all_prompts()
        # Trier par usage décroissant puis par titre
        self.current_prompts = sorted(all_prompts, key=lambda x: (-x[5], x[1].lower()))
        self.update_results_list()
    
    def on_search(self, text: str):
        """Gère la recherche en temps réel."""
        if text.strip():
            self.current_prompts = self.db.search_prompts(text)
        else:
            self.load_all_prompts()
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
                self.load_prompt_for_editing(prompt_id)
    
    def load_prompt_for_editing(self, prompt_id: int):
        """Charge un prompt pour édition inline."""
        self.is_loading = True  # Bloquer l'autosave pendant le chargement
        self.current_prompt_id = prompt_id
        
        prompt = self.db.get_prompt_by_id(prompt_id)
        
        if prompt:
            _, title, content, category, tags, usage_count = prompt
            
            self.preview_title.setText(title)
            self.preview_category.setText(category or "")
            self.preview_tags.setText(tags or "")
            self.preview_content.setPlainText(content)
            
            # Réactiver l'autosave après chargement
            QTimer.singleShot(100, lambda: setattr(self, 'is_loading', False))
        else:
            self.clear_preview()
    
    def clear_preview(self):
        """Efface la prévisualisation."""
        self.is_loading = True
        self.current_prompt_id = None
        self.preview_title.clear()
        self.preview_category.clear()
        self.preview_tags.clear()
        self.preview_content.clear()
        self.is_loading = False
    
    def on_title_changed(self):
        """Déclenche l'autosave quand le titre change."""
        if not self.is_loading and self.current_prompt_id:
            self.autosave_timer.start(1000)  # Sauvegarder après 1 seconde d'inactivité
    
    def on_meta_changed(self):
        """Déclenche l'autosave quand catégorie/tags changent."""
        if not self.is_loading and self.current_prompt_id:
            self.autosave_timer.start(1000)
    
    def on_content_changed(self):
        """Déclenche l'autosave quand le contenu change."""
        if not self.is_loading and self.current_prompt_id:
            self.autosave_timer.start(800)  # Plus rapide pour le contenu
    
    def save_current_prompt(self):
        """Sauvegarde automatique du prompt en cours d'édition."""
        if not self.current_prompt_id or self.is_loading:
            return
        
        title = self.preview_title.text().strip()
        content = self.preview_content.toPlainText().strip()
        category = self.preview_category.text().strip()
        tags = self.preview_tags.text().strip()
        
        if not title or not content:
            return
        
        # Mettre à jour en base
        self.db.update_prompt(
            self.current_prompt_id,
            title=title,
            content=content,
            category=category,
            tags=tags
        )
        
        # Mettre à jour la liste sans perdre la sélection
        current_row = self.results_list.currentRow()
        search_text = self.search_input.text()
        
        if search_text.strip():
            self.current_prompts = self.db.search_prompts(search_text)
        else:
            self.load_all_prompts()
        
        self.update_results_list()
        self.results_list.setCurrentRow(current_row)
        
        # Feedback discret
        print(f"💾 Sauvegardé : {title[:30]}...")
    
    def on_enter_pressed(self):
        """Copie le prompt sélectionné."""
        if self.current_prompt_id:
            prompt = self.db.get_prompt_by_id(self.current_prompt_id)
            if prompt:
                content = prompt[2]
                clipboard = QApplication.clipboard()
                clipboard.setText(content)
                
                self.db.increment_usage(self.current_prompt_id)
                
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
    
    def show_add_dialog(self):
        """Affiche le dialogue d'ajout."""
        dialog = PromptEditorDialog(self, self.db)
        if dialog.exec():
            self.load_all_prompts()
            self.search_input.clear()
    
    def delete_prompt_quick(self, item):
        """Supprime rapidement un prompt avec confirmation."""
        from qfluentwidgets import MessageBox
        
        row = self.results_list.row(item)
        if hasattr(self, 'prompt_ids') and row in self.prompt_ids:
            prompt_id = self.prompt_ids[row]
            prompt = self.db.get_prompt_by_id(prompt_id)
            
            if prompt:
                title = prompt[1]
                
                # Dialogue de confirmation
                msg_box = MessageBox(
                    "Confirmer la suppression",
                    f"Voulez-vous vraiment supprimer '{title}' ?",
                    self
                )
                msg_box.yesButton.setText("Supprimer")
                msg_box.cancelButton.setText("Annuler")
                
                if msg_box.exec():
                    self.db.delete_prompt(prompt_id)
                    
                    InfoBar.success(
                        title="Succès",
                        content=f"Prompt '{title}' supprimé !",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                    
                    # Recharger la liste
                    search_text = self.search_input.text()
                    if search_text.strip():
                        self.on_search(search_text)
                    else:
                        self.load_all_prompts()
                    
                    # Garder le focus
                    self.search_input.setFocus()
    
    def keyPressEvent(self, event):
        """Gère les raccourcis clavier."""
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key.Key_Delete:
            # Supprimer le prompt sélectionné
            current_item = self.results_list.currentItem()
            if current_item:
                self.delete_prompt_quick(current_item)
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
        self.load_all_prompts()


class PromptEditorDialog(MessageBoxBase):
    """Dialogue Fluent pour ajouter un prompt."""
    
    def __init__(self, parent, db: DatabaseManager):
        super().__init__(parent)
        
        self.db = db
        
        # Titre du dialogue
        self.titleLabel = SubtitleLabel("➕ Nouveau Prompt")
        
        # Créer les widgets
        self.init_ui()
        
        # Configurer le dialogue
        self.widget.setMinimumWidth(600)
        
        # Ajouter les boutons
        self.yesButton.setText("💾 Enregistrer")
        self.cancelButton.setText("Annuler")
        
        self.yesButton.clicked.connect(self.save_prompt)
    
    def init_ui(self):
        """Initialise l'interface du dialogue."""
        # Ajouter le titre
        self.viewLayout.addWidget(self.titleLabel)
        
        # Titre du prompt
        title_label = BodyLabel("Titre du prompt")
        self.viewLayout.addWidget(title_label)
        
        self.title_input = LineEdit()
        self.title_input.setPlaceholderText("Ex: API REST Python")
        self.title_input.setClearButtonEnabled(True)
        self.viewLayout.addWidget(self.title_input)
        
        # Catégorie
        cat_label = BodyLabel("Catégorie (optionnel)")
        self.viewLayout.addWidget(cat_label)
        
        self.category_input = EditableComboBox()
        categories = [""] + self.db.get_categories() + ["Développement", "Marketing", "Rédaction", "Business", "Design", "Communication"]
        self.category_input.addItems(list(dict.fromkeys(categories)))
        self.category_input.setPlaceholderText("Choisissez ou créez une catégorie")
        self.viewLayout.addWidget(self.category_input)
        
        # Tags
        tags_label = BodyLabel("Tags (optionnel, séparés par des virgules)")
        self.viewLayout.addWidget(tags_label)
        
        self.tags_input = LineEdit()
        self.tags_input.setPlaceholderText("python, api, rest")
        self.tags_input.setClearButtonEnabled(True)
        self.viewLayout.addWidget(self.tags_input)
        
        # Contenu
        content_label = BodyLabel("Contenu du prompt")
        self.viewLayout.addWidget(content_label)
        
        self.content_input = TextEdit()
        self.content_input.setPlaceholderText("Écrivez votre prompt ici...")
        self.content_input.setMinimumHeight(200)
        self.viewLayout.addWidget(self.content_input)
        
        # Focus sur le titre
        self.title_input.setFocus()
    
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
        
        self.db.add_prompt(title, content, category, tags)
        InfoBar.success(
            title="Succès",
            content="Prompt créé avec succès !",
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
