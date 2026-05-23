# Aqua IA Predict - Documentation Technique et Script Video (Defi 2)

## 1. Methodologie et Architecture de la Solution
Notre solution vise a predire en temps reel la degradation de la qualite de l'eau potable en combinant des donnees multisensorielles et l'Intelligence Artificielle.

### Generation de l'Indice de Risque et Identification de la Cause
- **Jeu de Donnees Simule** : Un script Python (`simulate_data.py`) a ete utilise pour generer 5000 echantillons de donnees (pH, turbidite, conductivite, chlore, temperature, pression, debit). Les donnees integrent differents cas de figure (Normal, Stagnation, Corrosion, Contamination, Pression Faible).
- **Modele IA (Scikit-Learn)** :
  - **Regression (Indice de Risque)** : Un `RandomForestRegressor` predit le pourcentage de risque (0 a 100).
  - **Classification (Cause Probable)** : Un `RandomForestClassifier` identifie la cause racine parmi les 5 categories. Les modeles sont serialises avec `joblib`.

### Integration Temps Reel
- **Backend (FastAPI)** : L'API expose un endpoint `/predict` qui execute les deux modeles immediatement. Un endpoint `/simulate` agit comme un jumeau numerique, simulant aleatoirement (avec priorite pour les etats normaux) les probabilites de valeurs de capteurs (un capteur reel viendrait simplement frapper le meme endpoint avec ses metrics).
- **Frontend Interactif** : Une interface moderne (Glassmorphism, Dark mode, zero framework CSS externe lourd) ecrite en HTML/CSS/JS vanille.
  - Interroge l'API toutes les 1.5 secondes.
  - Utilise `Chart.js` pour tracer l'evolution historique des parametres (pH et Turbidite par exemple).
  - Met a jour dynamiquement la jauge de risque, le panneau Textuel de la Cause probable, et des badges dynamiques.

---

## 2. Script de la Demonstration Video (3 minutes)

**[0:00 - 0:30] Introduction**
- *Ecran* : Diapositive de titre "Aqua IA Predict - IA-Night".
- *Voix-off* : "Bonjour, voici notre prototype concu pour repondre au Defi 2 concernant l'eau. Notre objectif : anticiper la contamination de l'eau potable grace a l'apprentissage automatique et des donnees multisensorielles."

**[0:30 - 1:15] Le Tableau de Bord en Temps Reel (Cas Normal)**
- *Ecran* : Affichage du Dashboard Web de l'application. On y voit le graphique lineaire qui se deplace, l'indice de risque tres bas.
- *Voix-off* : "Nous observons ici notre interface de surveillance en temps reel. Notre backend FastAPI alimente ce dashboard avec un flux de capteurs: pH, turbidite, pression... Actuellement, tout est dans les limites. L'Indice de risque est minime (Alarme Verte)."

**[1:15 - 2:00] Simulation d'une Degradation**
- *Ecran* : On rafraichit la page pour tomber sur un cas avec un indice de risque eleve (Le random simulateur met la situation au hasard, ou alors le code de demonstration a ete fixe pour montrer ce stade).
- *Voix-off* : "Voyez ce qu'il se passe lors d'une soudaine deviation. Nos deux Random Forest associes (Classification et Regression) vont automatiquement voir ce motif suspect d'anomalies. Immédiatement, l'Indice de Risque passe en zone jaune ou rouge et l'alerte commence a s'afficher."

**[2:00 - 2:40] Alertes Precoces et Cause Probable**
- *Ecran* : Zoom centre sur l'encadre specifiant "Contamination" ou "Corrosion".
- *Voix-off* : "Notre modele depasse la simple detection d'anomalie : l'un de nos algorithmes indique la cause la plus probable par classification afin de diagnostiquer s'il s'agit du manque de chlore (stagnation), de debits anormaux ou d'une forte echelle alcaline (corrosion) etc. La ville peut ainsi agir avant un probleme sanitaire."

**[2:40 - 3:00] Conclusion**
- *Ecran* : Les donnees de la maquette qui defilent lentement en mode normal.
- *Voix-off* : "L'association de Scikit-Learn sans fioriture avec un serveur FastAPI asynchrone rend ce modele de protection proactive extremement leger, evolutif, fondé sur la donnee. Merci de votre attention."
