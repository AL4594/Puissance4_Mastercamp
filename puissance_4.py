import time
import copy

class state():
    def __init__(self, grille=None, joueur="1"):
        if grille is None:
            self.grille = [[' ' for _ in range(12)] for _ in range(6)]
        elif any(
                any(grille[ligne][col] != ' ' and any(grille[l][col] == ' ' for l in range(ligne + 1, 6))
                    for ligne in range(6))
                for col in range(12)
        ):
            print("Grille invalide : pions flottants détectés. Une grille vide sera utilisée.")
            self.grille = [[' ' for _ in range(12)] for _ in range(6)]
        else:
            self.grille = grille
        self.joueur = joueur

    def Terminal_test(self) -> bool:
        return self.gagnant() is not None or all(self.grille[0][col] != ' ' for col in range(len(self.grille[0])))

    def Utility(self, joueur_vise: str) -> int:
        gagnant = self.gagnant()
        if gagnant == joueur_vise:
            return 100000
        elif gagnant and gagnant != joueur_vise:
            return -100000
        else:
            return self.heuristic(joueur_vise)

    def Actions(self, joueur: str) -> list[int]:
        return [col for col in range(len(self.grille[0])) if self.grille[0][col] == ' ']

    def Result(self, col_choice: int, joueur: str) -> "state":
        if self.Terminal_test():
            print("the game is over")
            return None
        if self.grille[0][col_choice] != ' ':
            print("the column is full invalid choice")
            return None
        # on doit check quelle est la ligne la plus basse dans laquelle la piece va tomber dans la colonne choisie et retourner le state apres avoir changé
        lowest_line=next(i for i in range(5,-1,-1) if self.grille[i][col_choice] == ' ')
        grille= copy.deepcopy(self.grille)
        grille[lowest_line][col_choice]=joueur
        return state(grille=grille, joueur=self.Adversaire(joueur))


    def gagnant(self):
        lignes = len(self.grille)
        colonnes = len(self.grille[0])
        for row in range(lignes):
            for col in range(colonnes):
                if self.grille[row][col] == ' ':
                    continue
                joueur = self.grille[row][col]
                if col <= colonnes - 4 and all(self.grille[row][col + i] == joueur for i in range(4)):
                    return joueur
                if row <= lignes - 4 and all(self.grille[row + i][col] == joueur for i in range(4)):
                    return joueur
                if row >= 3 and col <= colonnes - 4 and all(self.grille[row - i][col + i] == joueur for i in range(4)):
                    return joueur
                if row <= lignes - 4 and col <= colonnes - 4 and all(
                        self.grille[row + i][col + i] == joueur for i in range(4)):
                    return joueur
        return None

    def heuristic(self, joueur_vise: str) -> int:
        lignes = len(self.grille)
        colonnes = len(self.grille[0])
        score = 0
        adversaire = 'X' if joueur_vise == 'O' else 'O'

        def eval_line(line):
            count_j = line.count(joueur_vise)
            count_a = line.count(adversaire)
            if count_j > 0 and count_a == 0:
                return 10 ** count_j
            elif count_a > 0 and count_j == 0:
                return -(10 ** count_a)
            return 0

        for row in range(lignes):
            for col in range(colonnes - 3):
                ligne = [self.grille[row][col + i] for i in range(4)]
                score += eval_line(ligne)

        for col in range(colonnes):
            for row in range(lignes - 3):
                colonne = [self.grille[row + i][col] for i in range(4)]
                score += eval_line(colonne)

        for row in range(3, lignes):
            for col in range(colonnes - 3):
                diag1 = [self.grille[row - i][col + i] for i in range(4)]
                score += eval_line(diag1)

        for row in range(lignes - 3):
            for col in range(colonnes - 3):
                diag2 = [self.grille[row + i][col + i] for i in range(4)]
                score += eval_line(diag2)

        return score

    def Display(self):
        print("\n  " + " ".join(str(i) for i in range(12)))
        for row in self.grille:
            print(" |" + "|".join(self.rendu(cell) for cell in row) + "|")

    def rendu(self, cell: str) -> str:
        if cell == '1':
            return 'X'
        elif cell == '-1':
            return 'O'
        else:
            return ' '

    def Adversaire(self, joueur: str) -> str:
        return "-1" if joueur == "1" else "1"

    def Gagnant(self):
        return self.gagnant()


MAX_DEPTH = 4


def max_value(s: "state", alpha: float, beta: float, joueur: str, depth: int) -> int:
    if s.Terminal_test() or depth == 0:
        return s.Utility(joueur_vise=joueur)
    v = float('-inf')
    for action in s.Actions(s.joueur):  # attention, joueur courant dans s
        v = max(v, min_value(s.Result(action, s.joueur), alpha, beta, joueur, depth - 1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(s: "state", alpha: float, beta: float, joueur: str, depth: int) -> int:
    if s.Terminal_test() or depth == 0:
        return s.Utility(joueur_vise=joueur)
    v = float('inf')
    for action in s.Actions(s.joueur):
        v = min(v, max_value(s.Result(action, s.joueur), alpha, beta, joueur, depth - 1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def alphabeta_decision(s: "state", joueur: str):
    best_score = float('-inf')
    best_action = None
    alpha = float('-inf')
    beta = float('inf')
    for action in s.Actions(s.joueur):
        value = min_value(s.Result(action, s.joueur), alpha, beta, joueur, MAX_DEPTH - 1)
        if value > best_score:
            best_score = value
            best_action = action
        alpha = max(alpha, best_score)
    return best_action


def play():
    current_player = input("Qui commence ? (j pour joueur, i pour IA) : ").lower()
    joueur_humain = "1" if current_player == 'j' else "-1"
    joueur_ia = "-1" if joueur_humain == "1" else "1"

    s = state(joueur=joueur_humain if current_player == 'j' else joueur_ia)
    nb_tours = 0
    s.Display()

    while not s.Terminal_test():
        print(f"\nTour du joueur {'X' if s.joueur == '1' else 'O'}")

        if s.joueur == joueur_humain:
            valid = False
            while not valid:
                try:
                    col = int(input("Entrez la colonne (0-11) : "))
                    if col in s.Actions(s.joueur):
                        s = s.Result(col, s.joueur)  # Ce Result alterne déjà le joueur
                        valid = True
                    else:
                        print("Colonne pleine ou invalide.")
                except ValueError:
                    print("Veuillez entrer un entier entre 0 et 11.")
        else:
            print("IA réfléchit...")
            start = time.time()
            action = alphabeta_decision(s, s.joueur)  # On passe s.joueur, pas joueur_ia
            end = time.time()
            print(f"L'IA a joué la colonne {action} en {end - start:.2f} secondes")
            s = s.Result(action, s.joueur)

        s.Display()
        nb_tours += 1  # Pas besoin d'inverser le joueur ici

    gagnant = s.Gagnant()
    if gagnant:
        print(f"\n🎉 Le joueur {'X' if gagnant == '1' else 'O'} a gagné !")
    else:
        print("\nMatch nul.")

    print("⏹ Fin de la partie.")


def main():
    """s=state()
        s.display()
        print(s.Actions(joueur="1"))"""

    """s2=state(grille = [
    ['-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1'],
    ['1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1'],
    [' ', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' '],
    ['-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1'],
    ['1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1'],
    ['-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1'],
    ]
    )"""

    """s3 = state(grille=[
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '-1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', '-1', '-1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['1', '-1', '1', '1', '-1', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    )
    print(s3.Terminal_test(), s3.Actions(joueur="-1"))
    s3.Result(col_choice=2, joueur="1").Display()"""

    play()


if __name__ == '__main__':
    main()
