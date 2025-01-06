import optuna
import numpy as np
from scipy.integrate import solve_ivp
from differentialgleichung import ODE_Bioreactor_Monod
from numbers import Number
def objective(trial, t_start, t_end, y0, consts, t_span, feed_values):
    
    
    try:
        #die zu optimierenden Parameter
        # Hole den aktuellen Wert für feed_S1 aus feed_values
        feed_S1 = trial.suggest_categorical("feed_S1", feed_values)
        #feed_S1 = feed_values[trial.number]
        #feed_S1 = trial.suggest_float('feed_S1', low=0, high=5, step=0.05)  
        #feed_S1 = round(trial.suggest_float('feed_S1', low=0, high=5), 1)
        #feed_S1 = trial.suggest_categorical('feed_S1', [i * 0.1 for i in range(0, 51)])  # Werte von 0.0 bis 5.0 in Schritten von 0.1
        #feed_S1 = trial.suggest_categorical('feed_S1', [0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8])
        # # Setze die initialen Werte in y0
        consts[19]  =   feed_S1
        
        sol = solve_ivp(ODE_Bioreactor_Monod, [t_start, t_end], y0, args=(consts,), t_eval=t_span)
        cx_max =  np.max(sol.y[0])  
        cp_max =  np.max(sol.y[3])  
        cs       =   y0[1]
        # Ziel: Maximiere cx und minimiere cp
        # Sicherstellen, dass cx > 20 g/L und cp < 10 g/L
        if cx_max <= 20:
            objective_value = float('inf')  # Ungültiger Wert, wenn cx <= 20
        elif cp_max >= 10:
            objective_value = float('inf')  # Ungültiger Wert, wenn cp >= 10
        else:
            # Ziel: Maximiere cx und minimiere cp
            objective_value = - cx_max - cp_max   # Negative Werte, da Optuna minimiert
            # Maximieren von cx und Minimieren von cp mit Gewichtung
            #objective_value = -cx_max + 0.1 * cp_min
            if sol.success:
                trial.set_user_attr("sol", sol)  # Speichert die Lösung im Trial
                trial.set_user_attr("cs",cs)
        
        return objective_value
    except Exception as e:
        print(f"Fehler in der Optimierung: {e}")
        return float('nan')  # oder einen anderen Platzhalter