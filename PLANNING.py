import random
import itertools
import csv

def generer_binomes(nombre_etudiants):
    """Générer tous les binômes possibles"""
    return list(itertools.combinations(range(1, nombre_etudiants + 1), 2))

def creer_planning(nombre_etudiants):
    # Ajouter un étudiant fictif si le nombre est impair
    if nombre_etudiants % 2 != 0:
        print("Ajout d'un étudiant fictif pour équilibrer les binômes.")
        nombre_etudiants += 1

    nombre_tp = nombre_etudiants // 2  # Nombre de TP par semaine
    nombre_semaines = nombre_tp  # Nombre de semaines = nombre de TP

    tps = [chr(65 + i) for i in range(nombre_tp)]  # Générer les TP A, B, C...
    binomes = generer_binomes(nombre_etudiants)
    random.shuffle(binomes)  # Mélanger les binômes
    planning = []  # Stocker le planning final
    binomes_utilises = set()  # Suivre les binômes déjà utilisés globalement

    tirages_rates = 0  # Compteur des tirages ratés

    while True:
        planning.clear()
        binomes_utilises.clear()
        tirage_reussi = True

        for semaine in range(1, nombre_semaines + 1):
            semaine_planning = []
            tp_restants = tps[:]
            etudiants_utilises = set()  # Suivre les étudiants déjà utilisés cette semaine

            random.shuffle(binomes)  # Remélanger les binômes à chaque semaine

            for binome in binomes:
                if not tp_restants:  # Plus de TP disponibles
                    break

                if (
                    binome not in binomes_utilises and  # Binôme non utilisé globalement
                    binome[0] not in etudiants_utilises and  # Étudiant 1 non utilisé cette semaine
                    binome[1] not in etudiants_utilises  # Étudiant 2 non utilisé cette semaine
                ):
                    # Assigner un TP au binôme
                    tp = tp_restants.pop(0)
                    semaine_planning.append((binome, tp))
                    etudiants_utilises.update(binome)
                    binomes_utilises.add(binome)

            # Si une semaine est invalide (pas assez de binômes), recommencer depuis le début
            if len(semaine_planning) != nombre_tp:
                tirages_rates += 1
                tirage_reussi = False
                break

            planning.append(semaine_planning)

        if tirage_reussi:
            break  # Sortir de la boucle si le tirage est réussi

    return planning, nombre_semaines, tps, tirages_rates

def afficher_planning(planning, nombre_semaines, tps):
    """Afficher le planning final"""
    print(f"Planning final sur {nombre_semaines} semaines :\n")
    for semaine_index, semaine in enumerate(planning, start=1):
        print(f"Semaine {semaine_index} :")
        semaine = sorted(semaine, key=lambda x: tps.index(x[1]))  # Trier les TP dans l'ordre
        for binome, tp in semaine:
            print(f"TP {tp} : Étudiants {binome[0]} et {binome[1]}")
        print()

def exporter_csv(planning, nombre_semaines):
    """Exporter le planning en fichier CSV"""
    with open("planning_tp.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Semaine", "TP", "Étudiant 1", "Étudiant 2"])
        for semaine_index, semaine in enumerate(planning, start=1):
            for binome, tp in semaine:
                csvwriter.writerow([f"Semaine {semaine_index}", tp, binome[0], binome[1]])
    print("Planning exporté dans le fichier 'planning_tp.csv'.")

def main():
    nombre_etudiants = int(input("Entrez le nombre d'étudiants : "))
    planning, nombre_semaines, tps, tirages_rates = creer_planning(nombre_etudiants)
    print(f"\nNombre total de tirages ratés : {tirages_rates}")
    afficher_planning(planning, nombre_semaines, tps)
    
    choix = input("Souhaitez-vous exporter le planning au format CSV ? (o/n) : ").strip().lower()
    if choix == "o":
        exporter_csv(planning, nombre_semaines)
    else:
        print("Exportation annulée.")

if __name__ == "__main__":
    main()
