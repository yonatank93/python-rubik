from .. import Solver
from Move import Move
from Cubie import Sticker
from Printer import TtyPrinter

class WhiteFaceSolver(Solver):
    def solution(self):
        solution = []
        pprint = TtyPrinter(self.cube, True)
        # There are 4 down-corners
        for i in range(4):
            front_color = self.cube.cubies['F'].facings['F']
            right_color = self.cube.cubies['R'].facings['R']
            print i, "Searching (F)", front_color, "(R)", right_color

            goal_cubie = self.cube.search_by_colors('W', front_color, right_color)
            print i, "Is at", goal_cubie

            step_solution = []
            goal_cubie_obj = self.cube.cubies[goal_cubie]
            if goal_cubie == 'DFR':
                if goal_cubie_obj.color_facing('W') == 'F':
                    step_solution.append("R")
                    step_solution.append("U'")
                    step_solution.append("R'")
                elif goal_cubie_obj.color_facing('W') == 'R':
                    step_solution.append("R")
                    step_solution.append("U")
                    step_solution.append("R'")
                    step_solution.append("U'")
            elif goal_cubie == 'DFL':
                if goal_cubie_obj.color_facing('W') == 'F':
                    step_solution.append("L'")
                    step_solution.append("U")
                    step_solution.append("L")
                    step_solution.append("U'")
                elif goal_cubie_obj.color_facing('W') in ['L', 'D']:
                    step_solution.append("L'")
                    step_solution.append("U'")
                    step_solution.append("L")
            elif goal_cubie == 'BDL':
                if goal_cubie_obj.color_facing('W') in ['B', 'D']:
                    step_solution.append("B'")
                    step_solution.append("U2")
                    step_solution.append("B")
                elif goal_cubie_obj.color_facing('W') == 'L':
                    step_solution.append("B'")
                    step_solution.append("U")
                    step_solution.append("B")
                    step_solution.append("U2")
            elif goal_cubie == 'BDR':
                if goal_cubie_obj.color_facing('W') in ['B', 'D']:
                    step_solution.append("B")
                    step_solution.append("U")
                    step_solution.append("B'")
                elif goal_cubie_obj.color_facing('W') == 'R':
                    step_solution.append("B")
                    step_solution.append("U'")
                    step_solution.append("B'")
                    step_solution.append("U")
            else:
                # Cubie is in upper face, place it on FRU
                if goal_cubie == 'BRU':
                    step_solution.append("U")
                elif goal_cubie == 'BLU':
                    step_solution.append("U2")
                elif goal_cubie == 'FLU':
                    step_solution.append("U'")
                # else is already at FRU
            
            for m in step_solution:
                self.cube.move(Move(m))
            # Cubie is at FRU, place it at DRU with correct orientation
            print i, "(1) Partially applying", step_solution
            solution.extend(step_solution)
            step_solution = []

            if self.cube.cubies['FRU'].color_facing('W') == 'F':
                step_solution.append("F'")
                step_solution.append("U'")
                step_solution.append("F")
            elif self.cube.cubies['FRU'].color_facing('W') == 'R':
                step_solution.append("R")
                step_solution.append("U")
                step_solution.append("R'")
            elif self.cube.cubies['FRU'].color_facing('W') == 'U':
                step_solution.append("R")
                step_solution.append("U2")
                step_solution.append("R'")
                step_solution.append("U'")
                step_solution.append("R")
                step_solution.append("U")
                step_solution.append("R'")
            
            print i, "(2) Partially applying", step_solution
            for m in step_solution:
                self.cube.move(Move(m))
            solution.extend(step_solution)
            # Cubie is placed, move to next
            pprint.pprint()
            print i, "Applying Y"
            solution.append('Y')
            self.cube.move(Move('Y'))
        return solution