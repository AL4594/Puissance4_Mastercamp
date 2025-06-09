from copy import deepcopy


class state():
    def __init__(self, grille=None, joueur="X"):
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


    def display(self)->None:
        print("    " + "  ".join(f"{i:2}" for i in range(12)))
        print("   " + "-" * (4 * 12 + 1))
        for i, ligne in enumerate(self.grille):
            print(f"{i:2} | " + " | ".join(ligne) + " |")
            print("   " + "-" * (4 * 12 + 1))

    def Actions(self, joueur: str) -> list[int]:
        return [col for col in range(12) if self.grille[0][col] == ' ']

    def Terminal_test(self) -> bool:
        return sum(1 for i in range(6) for j in range(12) if self.grille[i][j] != ' ')>41 or self.gagnant() != None or all(cell != ' ' for ligne in self.grille for cell in ligne)

    def gagnant(self) -> str:
        #retourne l'éventuel gagnant si la condition est respectée
        lignes = 6
        cols = 12
        for i in range(lignes):
            for j in range(cols):
                joueur = self.grille[i][j]
                if joueur == ' ':
                    continue

                #horizontal
                if j <= cols - 4 and all(self.grille[i][j + k] == joueur for k in range(4)):
                    return joueur

                #vertical
                if i <= lignes - 4 and all(self.grille[i + k][j] == joueur for k in range(4)):
                    return joueur

                #diagonale ↘
                if i <= lignes - 4 and j <= cols - 4 and all(self.grille[i + k][j + k] == joueur for k in range(4)):
                    return joueur

                #diagonale ↙
                if i <= lignes - 4 and j >= 3 and all(self.grille[i + k][j - k] == joueur for k in range(4)):
                    return joueur

        return None

    def Result(self, col_choice: int, joueur: str) -> "state":
        if self.Terminal_test():
            print("the game is over")
            return None
        if self.grille[0][col_choice] != ' ':
            print("the column is full invalid choice")
            return None
        # on doit check quelle est la ligne la plus basse dans laquelle la piece va tomber dans la colonne choisie et retourner le state apres avoir changé
        lowest_line=next(i for i in range(5,0,-1) if self.grille[i][col_choice] == ' ')
        grille=deepcopy(self.grille)
        grille[lowest_line][col_choice]=joueur
        return state(grille=grille, joueur=joueur)

def main():
    """s=state()
    s.display()
    print(s.Actions(joueur="X"))"""

    """s2=state(grille = [
    ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'],
    ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'],
    [' ', ' ', ' ', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
    ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'],
    ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'],
    ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X'],
    ]
    )"""

    s3=state(grille = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'O', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'X', 'O', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['X', 'O', 'X', 'X', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    )
    print(s3.Terminal_test(),s3.Actions(joueur="O"))
    s3.Result(col_choice=2, joueur="X").display()


if __name__ == '__main__':
    main()