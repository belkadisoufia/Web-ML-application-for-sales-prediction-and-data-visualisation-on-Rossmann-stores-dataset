# 📊 Rossmann Sales Prediction & Analytics - PFE

## 📝 À propos du projet
Ce projet de fin d'études (PFE) consiste en une solution complète d'analyse et de prévision des ventes pour la chaîne de magasins **Rossmann**. L'application combine la puissance du **Machine Learning** pour l'anticipation des revenus et la **Business Intelligence** pour le pilotage stratégique.

---

## 🚀 Fonctionnalités principales

### 1. Prévisions de Ventes (Machine Learning)
L'application intègre un modèle **XGBoost** entraîné sur les données historiques de Rossmann. 
* **Analyse multi-facteurs :** Prise en compte des promotions, de la concurrence, des jours fériés et de la saisonnalité.
* **Prédictions personnalisées :** Possibilité de générer des prévisions par magasin et par période spécifique.

### 2. Visualisation & Dashboarding
Une section dédiée à l'analyse de données (BI) via **Microsoft Power BI** :
* **Dashboard Live :** Consultation en temps réel des KPI (Chiffre d'affaires, nombre de clients).
* **Analyse Comparative :** Classement des meilleurs magasins (Top 10) et évolution annuelle.
* **Exportation :** Accès au fichier source `.pbix` pour des analyses hors-ligne.

---

## 🛠️ Technologies utilisées

* **Backend :** Python 3.x
* **Modélisation :** XGBoost (Algorithme de Gradient Boosting)
* **Interface Web :** Streamlit (ou Flask/Django selon votre implémentation)
* **Data Visualisation :** Microsoft Power BI
* **Gestion de versions :** Git & GitHub

---

## 📸 Aperçu de l'interface

### 🏠 Page d'Accueil
Interface intuitive permettant de naviguer entre le module de prédiction et le tableau de bord analytique.
![Accueil](acceuil.jpg)

### 🔮 Module de Prédiction
Interface de saisie pour l'algorithme XGBoost affichant les ventes totales et moyennes prévues.
![Prédiction](prediction.jpg)

### 📈 Dashboard Analytique
Visualisations interactives incluant la répartition des ventes par type de magasin et par année.
![Dashboard](dashboard.png)

### 📥 Espace Téléchargement
Section permettant de consulter le dashboard en mode Live ou de télécharger le rapport complet.
![Téléchargement](telecharger_dashboard.jpg)

---

## 📁 Structure du dépôt

* `/data` : Datasets utilisés pour l'entraînement.
* `/models` : Modèles pré-entraînés (XGBoost).
* `/notebooks` : Analyse exploratoire des données (EDA).
* `/src` : Code source de l'application web.
* `/reports` : Fichiers Power BI (.pbix).

---

## ⚙️ Installation

1. Clonez le projet :
   ```bash
   git clone [https://github.com/votre-utilisateur/rossmann-sales-prediction.git](https://github.com/votre-utilisateur/rossmann-sales-prediction.git)
