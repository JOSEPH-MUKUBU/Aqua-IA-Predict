import pandas as pd
import numpy as np
import random
import os

def generate_water_data(num_samples=5000):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    for _ in range(num_samples):
        # Base probabilities for conditions
        condition = random.choices(
            ['Normal', 'Stagnation', 'Corrosion', 'Contamination', 'Pression Faible'],
            weights=[0.6, 0.1, 0.1, 0.1, 0.1]
        )[0]
        
        if condition == 'Normal':
            ph = np.random.normal(7.2, 0.3)
            turbidity = max(0.1, np.random.normal(0.5, 0.2))
            conductivity = np.random.normal(400, 100)
            chlorine = np.random.normal(1.0, 0.3)
            temperature = np.random.normal(15, 3)
            pressure = np.random.normal(3.0, 0.3)
            flow = np.random.normal(300, 50)
            risk_index = random.randint(0, 15)
            
        elif condition == 'Stagnation':
            ph = np.random.normal(7.5, 0.4)
            turbidity = np.random.normal(1.2, 0.5)
            conductivity = np.random.normal(450, 100)
            chlorine = max(0.0, np.random.normal(0.1, 0.1)) # Low chlorine
            temperature = np.random.normal(22, 2) # Higher temp
            pressure = np.random.normal(2.5, 0.3)
            flow = max(10, np.random.normal(30, 10)) # Low flow
            risk_index = random.randint(40, 70)
            
        elif condition == 'Corrosion':
            ph = min(6.4, np.random.normal(6.0, 0.4)) # Low pH
            turbidity = np.random.normal(2.5, 0.8)
            conductivity = np.random.normal(900, 200) # High conductivity
            chlorine = np.random.normal(0.8, 0.3)
            temperature = np.random.normal(16, 3)
            pressure = np.random.normal(2.8, 0.4)
            flow = np.random.normal(250, 60)
            risk_index = random.randint(50, 80)
            
        elif condition == 'Contamination':
            ph = np.random.normal(7.0, 0.8)
            turbidity = np.random.normal(6.0, 2.0) # High turbidity
            conductivity = np.random.normal(1200, 300) # High conductivity
            chlorine = max(0.0, np.random.normal(0.05, 0.05)) # Very low chlorine
            temperature = np.random.normal(18, 4)
            pressure = np.random.normal(2.9, 0.3)
            flow = np.random.normal(300, 50)
            risk_index = random.randint(80, 100)
            
        elif condition == 'Pression Faible':
            ph = np.random.normal(7.2, 0.3)
            turbidity = np.random.normal(0.8, 0.3)
            conductivity = np.random.normal(400, 100)
            chlorine = np.random.normal(0.9, 0.3)
            temperature = np.random.normal(15, 3)
            pressure = max(0.5, np.random.normal(1.2, 0.3)) # Low pressure
            flow = max(20, np.random.normal(80, 20)) # Low flow
            risk_index = random.randint(20, 50)

        # Boundaries
        ph = max(0, min(14, ph))
        turbidity = max(0, turbidity)
        conductivity = max(0, conductivity)
        chlorine = max(0, chlorine)
        temperature = max(-10, min(50, temperature))
        pressure = max(0, pressure)
        flow = max(0, flow)

        data.append({
            'ph': round(ph, 2),
            'turbidity': round(turbidity, 2),
            'conductivity': round(conductivity, 2),
            'chlorine': round(chlorine, 2),
            'temperature': round(temperature, 2),
            'pressure': round(pressure, 2),
            'flow': round(flow, 2),
            'Risk_Index': risk_index,
            'Probable_Cause': condition
        })
        
    df = pd.DataFrame(data)
    
    save_path = os.path.join(os.path.dirname(__file__), 'water_quality_data.csv')
    df.to_csv(save_path, index=False)
    print(f"Donnees simulees generees : {save_path}")

if __name__ == '__main__':
    generate_water_data()
