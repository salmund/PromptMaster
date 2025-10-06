"""
Module de gestion de la base de données SQLite pour PromptMaster.
Gère le stockage et la récupération des prompts.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional


class DatabaseManager:
    """Gestionnaire de base de données pour PromptMaster."""
    
    def __init__(self, db_path: str = "promptmaster.db"):
        """
        Initialise le gestionnaire de base de données.
        
        Args:
            db_path: Chemin vers le fichier de base de données SQLite
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Crée et retourne une connexion à la base de données."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Crée la table prompts si elle n'existe pas."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✓ Base de données initialisée : {self.db_path}")
    
    def add_prompt(self, title: str, content: str, category: Optional[str] = None, 
                   tags: Optional[str] = None) -> int:
        """
        Ajoute un nouveau prompt dans la base de données.
        
        Args:
            title: Titre du prompt
            content: Contenu complet du prompt
            category: Catégorie du prompt (optionnel)
            tags: Tags séparés par des virgules (optionnel)
            
        Returns:
            L'ID du prompt créé
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO prompts (title, content, category, tags)
            VALUES (?, ?, ?, ?)
        """, (title, content, category, tags))
        
        prompt_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✓ Prompt ajouté : '{title}' (ID: {prompt_id})")
        return prompt_id
    
    def search_prompts(self, query: str) -> List[Tuple]:
        """
        Recherche des prompts par titre, contenu ou tags.
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste de tuples (id, title, content, category, tags, usage_count)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT id, title, content, category, tags, usage_count
            FROM prompts
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? OR category LIKE ?
            ORDER BY usage_count DESC, created_at DESC
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_all_prompts(self) -> List[Tuple]:
        """
        Récupère tous les prompts de la base de données.
        
        Returns:
            Liste de tuples (id, title, content, category, tags, usage_count)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content, category, tags, usage_count
            FROM prompts
            ORDER BY usage_count DESC, created_at DESC
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Tuple]:
        """
        Récupère un prompt spécifique par son ID.
        
        Args:
            prompt_id: ID du prompt
            
        Returns:
            Tuple (id, title, content, category, tags, usage_count) ou None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content, category, tags, usage_count
            FROM prompts
            WHERE id = ?
        """, (prompt_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def update_prompt(self, prompt_id: int, title: Optional[str] = None, 
                     content: Optional[str] = None, category: Optional[str] = None,
                     tags: Optional[str] = None) -> bool:
        """
        Met à jour un prompt existant.
        
        Args:
            prompt_id: ID du prompt à modifier
            title: Nouveau titre (optionnel)
            content: Nouveau contenu (optionnel)
            category: Nouvelle catégorie (optionnel)
            tags: Nouveaux tags (optionnel)
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        # Récupérer le prompt actuel
        current = self.get_prompt_by_id(prompt_id)
        if not current:
            print(f"✗ Prompt ID {prompt_id} introuvable")
            return False
        
        # Utiliser les valeurs actuelles si les nouvelles ne sont pas fournies
        new_title = title if title is not None else current[1]
        new_content = content if content is not None else current[2]
        new_category = category if category is not None else current[3]
        new_tags = tags if tags is not None else current[4]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE prompts
            SET title = ?, content = ?, category = ?, tags = ?
            WHERE id = ?
        """, (new_title, new_content, new_category, new_tags, prompt_id))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Prompt mis à jour : ID {prompt_id}")
        return True
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """
        Supprime un prompt de la base de données.
        
        Args:
            prompt_id: ID du prompt à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        if deleted:
            print(f"✓ Prompt supprimé : ID {prompt_id}")
        else:
            print(f"✗ Prompt ID {prompt_id} introuvable")
        
        return deleted
    
    def increment_usage(self, prompt_id: int):
        """
        Incrémente le compteur d'utilisation d'un prompt.
        
        Args:
            prompt_id: ID du prompt utilisé
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE prompts
            SET usage_count = usage_count + 1
            WHERE id = ?
        """, (prompt_id,))
        
        conn.commit()
        conn.close()
    
    def get_categories(self) -> List[str]:
        """
        Récupère toutes les catégories uniques.
        
        Returns:
            Liste des catégories
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT category
            FROM prompts
            WHERE category IS NOT NULL AND category != ''
            ORDER BY category
        """)
        
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return categories


# Fonction pratique pour les tests
def populate_sample_data():
    """Ajoute des prompts d'exemple pour tester l'application."""
    db = DatabaseManager()
    
    sample_prompts = [
        {
            "title": "API REST Python",
            "content": "Créez une API REST complète en Python avec FastAPI incluant : authentification JWT, endpoints CRUD, validation des données avec Pydantic, documentation automatique Swagger, et gestion des erreurs.",
            "category": "Développement",
            "tags": "python,api,fastapi,rest"
        },
        {
            "title": "Email Marketing",
            "content": "Rédigez un email marketing convaincant pour promouvoir [PRODUIT]. Le ton doit être professionnel mais chaleureux, avec un call-to-action clair et une structure : accroche, bénéfices, preuve sociale, offre, urgence.",
            "category": "Marketing",
            "tags": "email,marketing,copywriting"
        },
        {
            "title": "Code Review Checklist",
            "content": "Effectuez une revue de code complète en vérifiant : lisibilité et conventions de nommage, gestion des erreurs, sécurité, performance, tests unitaires, documentation, et possibles bugs ou edge cases.",
            "category": "Développement",
            "tags": "code-review,qualité,best-practices"
        },
        {
            "title": "Article de Blog SEO",
            "content": "Écrivez un article de blog optimisé SEO sur [SUJET] avec : titre accrocheur avec mot-clé principal, introduction engageante, structure H2/H3, méta-description, mots-clés secondaires naturellement intégrés, et conclusion avec CTA.",
            "category": "Rédaction",
            "tags": "seo,blog,content,rédaction"
        },
        {
            "title": "Débug Assistant",
            "content": "Analysez ce bug : [DESCRIPTION]. Identifiez la cause probable, proposez une solution pas à pas, expliquez comment reproduire le bug, et suggérez des tests pour éviter qu'il ne se reproduise.",
            "category": "Développement",
            "tags": "debug,troubleshooting,python"
        },
        {
            "title": "Présentation Pitch",
            "content": "Créez un pitch de présentation de 3 minutes pour [PROJET/PRODUIT] avec : problème résolu, solution unique, marché cible, avantage compétitif, business model, et demande claire.",
            "category": "Business",
            "tags": "pitch,présentation,startup"
        }
    ]
    
    for prompt in sample_prompts:
        db.add_prompt(**prompt)
    
    print(f"\n✓ {len(sample_prompts)} prompts d'exemple ajoutés !")


if __name__ == "__main__":
    # Test du module
    print("=== Test du module Database ===\n")
    
    db = DatabaseManager()
    
    # Ajouter des données d'exemple si la base est vide
    all_prompts = db.get_all_prompts()
    if len(all_prompts) == 0:
        print("Base de données vide. Ajout de prompts d'exemple...\n")
        populate_sample_data()
    
    # Test de recherche
    print("\n=== Test de recherche : 'python' ===")
    results = db.search_prompts("python")
    for prompt in results:
        print(f"  • {prompt[1]} ({prompt[3]})")
    
    print("\n=== Toutes les catégories ===")
    categories = db.get_categories()
    for cat in categories:
        print(f"  • {cat}")
