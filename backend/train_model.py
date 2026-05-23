import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
import os

def train_and_save_models():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'water_quality_data.csv')
    
    if not os.path.exists(data_path):
        print("Erreur : Fichier de donnees non trouve. Executez simulate_data.py d'abord.")
        return

    df = pd.read_csv(data_path)
    
    # Features (X)
    X = df[['ph', 'turbidity', 'conductivity', 'chlorine', 'temperature', 'pressure', 'flow']]
    
    # Targets (y)
    y_cause = df['Probable_Cause']
    y_risk = df['Risk_Index']
    
    # Split
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_cause, test_size=0.2, random_state=42)
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X, y_risk, test_size=0.2, random_state=42)
    
    # Train Classifier (Cause)
    print("Entrainement du classificateur de cause probable...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_c, y_train_c)
    
    y_pred_c = clf.predict(X_test_c)
    print("\nRapport de classification (Cause) :")
    print(classification_report(y_test_c, y_pred_c))
    
    # Train Regressor (Risk Index)
    print("Entrainement du regresseur d'indice de risque...")
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train_r, y_train_r)
    
    y_pred_r = reg.predict(X_test_r)
    print("\nPerformances du regresseur (Indice de Risque) :")
    print(f"MSE: {mean_squared_error(y_test_r, y_pred_r):.2f}")
    print(f"R2 : {r2_score(y_test_r, y_pred_r):.2f}")
    
    # Save models
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(clf, os.path.join(models_dir, 'cause_classifier.joblib'))
    joblib.dump(reg, os.path.join(models_dir, 'risk_regressor.joblib'))
    
    print(f"\nModeles sauvegardes dans le dossier '{models_dir}'.")

if __name__ == '__main__':
    train_and_save_models()
