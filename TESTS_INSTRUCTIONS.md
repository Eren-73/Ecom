# 📋 Instructions pour Exécuter les Tests

## 🎯 Problème Résolu

**Symptôme** : Le terminal affiche "Ran 30 tests" mais seulement 28 tests sont listés dans la sortie.

**Solution** : Utiliser le niveau de verbosité `-v 2` pour afficher **tous les tests** avec leurs descriptions complètes.

## ✅ Méthodes d'Exécution

### Méthode 1 : Commande Directe (Recommandée)
```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
venv\Scripts\activate.bat    # Windows CMD
# ou
source venv/bin/activate     # Linux/Mac

# Exécuter les tests avec verbosité complète
python manage.py test tests -v 2
```

### Méthode 2 : Scripts Automatiques

**Windows** :
```bash
run_tests.bat
```

**Linux/Mac** :
```bash
chmod +x run_tests.sh
./run_tests.sh
```

**Python** :
```bash
python run_tests.py
```

## 📊 Résultat Attendu

Avec `-v 2`, vous devriez voir **tous les 30 tests** listés :

### Tests Unitaires - Models (8 tests)
1. ✅ test_creation_profil_vendeur
2. ✅ test_creation_profil_client_champs_optionnels
3. ✅ test_propriete_stock_disponible
4. ✅ test_methode_liste_tags
5. ✅ test_generation_numero_commande
6. ✅ test_calcul_prix_total_article
7. ✅ test_calcul_total_panier
8. ✅ test_calcul_prix_total_article_panier

### Tests Unitaires - Accounts (6 tests)
9. ✅ test_inscription_vendeur_reussie
10. ✅ test_inscription_client_reussie
11. ✅ test_connexion_vendeur_reussie
12. ✅ test_connexion_client_reussie
13. ✅ test_affichage_dashboard_avec_produits_et_commandes
14. ✅ test_affichage_dashboard_avec_commandes

### Tests Unitaires - Products (5 tests)
15. ✅ test_affichage_tous_produits_actifs
16. ✅ test_filtrage_par_categorie
17. ✅ test_affichage_detail_produit
18. ✅ test_creation_produit_reussie
19. ✅ test_modification_produit_reussie

### Tests Unitaires - Orders (3 tests)
20. ✅ test_ajout_produit_au_panier
21. ✅ test_affichage_panier_avec_articles
22. ✅ test_checkout_reussi

### Tests Fonctionnels (2 tests)
23. ✅ test_parcours_client_complet
24. ✅ test_parcours_vendeur_complet

### Tests d'Intégration (6 tests)
25. ✅ test_relation_vendeur_produit
26. ✅ test_panier_avec_produits
27. ✅ test_commande_avec_produits
28. ✅ test_relation_client_panier
29. ✅ test_relation_client_commandes
30. ✅ test_integration_complete

## 🔍 Niveaux de Verbosité

- `-v 0` : Aucune sortie (silencieux)
- `-v 1` : Sortie minimale (défaut) - peut masquer certains tests
- `-v 2` : **Sortie complète** - affiche tous les tests avec descriptions ✅
- `-v 3` : Sortie très détaillée (debug)

## ⚠️ Note Importante

Les 2 tests qui n'apparaissaient pas dans la sortie par défaut sont :
- `test_creation_profil_client_champs_optionnels`
- `test_propriete_stock_disponible`

Ces tests sont **bien exécutés** (d'où le total de 30), mais nécessitent `-v 2` pour être **affichés** dans la sortie du terminal.

