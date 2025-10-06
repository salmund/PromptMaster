"""
Tests unitaires pour PromptMaster.
Testez les fonctionnalités principales de la base de données.
"""

import unittest
import os
import tempfile
from database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Tests pour la classe DatabaseManager."""
    
    def setUp(self):
        """Prépare un environnement de test propre."""
        # Créer une base de données temporaire pour les tests
        self.test_db = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db')
        self.test_db.close()
        self.db = DatabaseManager(self.test_db.name)
    
    def tearDown(self):
        """Nettoie après chaque test."""
        # Supprimer la base de données temporaire
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_add_prompt(self):
        """Test d'ajout d'un prompt."""
        prompt_id = self.db.add_prompt(
            title="Test Prompt",
            content="Ceci est un test",
            category="Test",
            tags="test,unitaire"
        )
        
        self.assertIsNotNone(prompt_id)
        self.assertGreater(prompt_id, 0)
    
    def test_get_prompt_by_id(self):
        """Test de récupération d'un prompt par ID."""
        # Ajouter un prompt
        prompt_id = self.db.add_prompt(
            title="Prompt Test",
            content="Contenu test",
            category="Catégorie",
            tags="tag1,tag2"
        )
        
        # Récupérer le prompt
        prompt = self.db.get_prompt_by_id(prompt_id)
        
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt[1], "Prompt Test")
        self.assertEqual(prompt[2], "Contenu test")
        self.assertEqual(prompt[3], "Catégorie")
        self.assertEqual(prompt[4], "tag1,tag2")
    
    def test_search_prompts(self):
        """Test de recherche de prompts."""
        # Ajouter plusieurs prompts
        self.db.add_prompt("Python API", "Créer une API en Python", "Dev", "python,api")
        self.db.add_prompt("Email Marketing", "Email pour marketing", "Marketing", "email")
        self.db.add_prompt("Python Debug", "Debugger Python", "Dev", "python,debug")
        
        # Rechercher "python"
        results = self.db.search_prompts("python")
        self.assertEqual(len(results), 2)
        
        # Rechercher "email"
        results = self.db.search_prompts("email")
        self.assertEqual(len(results), 1)
        
        # Rechercher quelque chose qui n'existe pas
        results = self.db.search_prompts("inexistant")
        self.assertEqual(len(results), 0)
    
    def test_update_prompt(self):
        """Test de mise à jour d'un prompt."""
        # Ajouter un prompt
        prompt_id = self.db.add_prompt(
            title="Original",
            content="Contenu original"
        )
        
        # Mettre à jour
        success = self.db.update_prompt(
            prompt_id,
            title="Modifié",
            content="Contenu modifié"
        )
        
        self.assertTrue(success)
        
        # Vérifier la modification
        prompt = self.db.get_prompt_by_id(prompt_id)
        self.assertEqual(prompt[1], "Modifié")
        self.assertEqual(prompt[2], "Contenu modifié")
    
    def test_delete_prompt(self):
        """Test de suppression d'un prompt."""
        # Ajouter un prompt
        prompt_id = self.db.add_prompt(
            title="À supprimer",
            content="Ce prompt sera supprimé"
        )
        
        # Supprimer
        success = self.db.delete_prompt(prompt_id)
        self.assertTrue(success)
        
        # Vérifier qu'il n'existe plus
        prompt = self.db.get_prompt_by_id(prompt_id)
        self.assertIsNone(prompt)
    
    def test_increment_usage(self):
        """Test d'incrémentation du compteur d'utilisation."""
        # Ajouter un prompt
        prompt_id = self.db.add_prompt(
            title="Popular",
            content="Prompt populaire"
        )
        
        # Vérifier le compteur initial
        prompt = self.db.get_prompt_by_id(prompt_id)
        self.assertEqual(prompt[5], 0)  # usage_count à l'index 5
        
        # Incrémenter 3 fois
        for _ in range(3):
            self.db.increment_usage(prompt_id)
        
        # Vérifier le nouveau compteur
        prompt = self.db.get_prompt_by_id(prompt_id)
        self.assertEqual(prompt[5], 3)
    
    def test_get_categories(self):
        """Test de récupération des catégories uniques."""
        # Ajouter des prompts avec différentes catégories
        self.db.add_prompt("Test 1", "Contenu", "Développement", "")
        self.db.add_prompt("Test 2", "Contenu", "Marketing", "")
        self.db.add_prompt("Test 3", "Contenu", "Développement", "")
        self.db.add_prompt("Test 4", "Contenu", "Rédaction", "")
        
        # Récupérer les catégories
        categories = self.db.get_categories()
        
        self.assertEqual(len(categories), 3)
        self.assertIn("Développement", categories)
        self.assertIn("Marketing", categories)
        self.assertIn("Rédaction", categories)
    
    def test_get_all_prompts(self):
        """Test de récupération de tous les prompts."""
        # Ajouter plusieurs prompts
        self.db.add_prompt("Prompt 1", "Contenu 1")
        self.db.add_prompt("Prompt 2", "Contenu 2")
        self.db.add_prompt("Prompt 3", "Contenu 3")
        
        # Récupérer tous les prompts
        all_prompts = self.db.get_all_prompts()
        
        self.assertEqual(len(all_prompts), 3)
    
    def test_search_by_tags(self):
        """Test de recherche par tags."""
        # Ajouter des prompts avec des tags
        self.db.add_prompt("API", "API content", "Dev", "python,rest,api")
        self.db.add_prompt("Email", "Email content", "Marketing", "email,marketing")
        
        # Rechercher par tag
        results = self.db.search_prompts("rest")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "API")
    
    def test_usage_count_ordering(self):
        """Test que les prompts les plus utilisés apparaissent en premier."""
        # Ajouter 3 prompts
        id1 = self.db.add_prompt("Prompt 1", "Contenu 1")
        id2 = self.db.add_prompt("Prompt 2", "Contenu 2")
        id3 = self.db.add_prompt("Prompt 3", "Contenu 3")
        
        # Utiliser le prompt 3 le plus souvent
        for _ in range(5):
            self.db.increment_usage(id3)
        
        # Utiliser le prompt 1 un peu
        for _ in range(2):
            self.db.increment_usage(id1)
        
        # Le prompt 2 n'est jamais utilisé
        
        # Récupérer tous les prompts (triés par usage)
        prompts = self.db.get_all_prompts()
        
        # Vérifier l'ordre : id3 (5), id1 (2), id2 (0)
        self.assertEqual(prompts[0][0], id3)
        self.assertEqual(prompts[1][0], id1)
        self.assertEqual(prompts[2][0], id2)


def run_tests():
    """Lance tous les tests."""
    # Créer une suite de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabaseManager)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ Tous les tests sont passés avec succès !")
    else:
        print("❌ Certains tests ont échoué")
        print(f"   Échecs : {len(result.failures)}")
        print(f"   Erreurs : {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
