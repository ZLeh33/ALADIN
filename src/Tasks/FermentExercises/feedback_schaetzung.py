import json

def feedback_schatzung():
    # Lade Lösung aus der JSON-Datei
    with open('src/Tasks/FermentExercises/feed_s1_loesung.json', 'r') as loesung_file:
        loesung = json.load(loesung_file)
    
    # Lade Schätzung aus der JSON-Datei
    with open('src/Tasks/FermentExercises/nutzer_eingaben.json', 'r') as schatzung_file:
        schatzung = json.load(schatzung_file)
    
    # Vergleiche die Schätzungen mit den Lösungen für jede Phase
    for phase in loesung:
        print(f"Vergleich für {phase}:")
        
        # Hole die Lösung und Schätzung für diese Phase
        phase_loesung = loesung[phase]
        phase_schatzung = schatzung.get(phase)
        
        if phase_schatzung is None:
            print(f"Keine Schätzung für {phase} gefunden!")
            continue
        
        # Besondere Behandlung für den Fall, dass die Lösung 0 ist
        if phase_loesung == 0:
            if phase_schatzung == 0:
                print(f"Erfolgreich! Deine Schätzung für {phase} ist korrekt (beide sind 0).")
            else:
                print(f"Falsch! Deine Schätzung für {phase} ist nicht korrekt. Versuche es noch einmal.")
            continue
        
        # Berechne die relative Differenz, wenn die Lösung nicht null ist
        differenz = abs(phase_schatzung - phase_loesung)
        relative_differenz = differenz / abs(phase_loesung) * 100
        
        # Bestimme, wie nah die Schätzung an der Lösung ist
        if relative_differenz <= 20:
            print(f"Erfolgreich! Deine Schätzung von {phase_schatzung} für {phase} ist nahe genug an der Lösung.")
        elif 20 < relative_differenz <= 50:
            print(f"Du bist nah dran! Deine Schätzung von {phase_schatzung} für {phase} ist entfernt von der Lösung.")
        elif 50 < relative_differenz <= 100:
            print(f"Versuche es noch einmal! Deine Schätzung von {phase_schatzung} für {phase} ist entfernt von der Lösung.")
        else:
            if phase_schatzung < phase_loesung:
                print(f"Du musst höher schätzen! Deine Schätzung von {phase_schatzung} für {phase} ist mehr als 100% entfernt.")
            else:
                print(f"Du musst niedriger schätzen! Deine Schätzung von {phase_schatzung} für {phase} ist mehr als 100% entfernt.")
