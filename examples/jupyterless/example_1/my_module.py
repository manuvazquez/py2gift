
import py2gift.question
import py2gift.tex
import py2gift.file
import py2gift.util
import numpy as np
import matplotlib.pylab as plt
    
class MatrixProduct(py2gift.question.NumericalQuestionGenerator):
    
    def setup(self):
        
        A = self.prng.rand(2, 2)
        B = self.prng.rand(2, 2)

        self.statement.fill(
            A=A,
            B=B
        )
        
        product = A @ B
        
        self.feedback.fill(
            product=product,
            diagonal=py2gift.tex.enumerate_math(np.diag(product))
        )
        
        self.solution = product.trace()
        self.error = '10%'

class EnergySignal(py2gift.question.MultipleChoiceQuestionGenerator):
    
    def setup(self):
        
        # a random number for the slope...
        slope = self.prng.randint(1, 6) 
        
        # ...and another one for the width
        width = self.prng.randint(3, 10) 
        
        x = np.arange(width)
        y = slope*x
        
        extra = 4
        
        x = np.r_[np.arange(-extra, 0), x, np.arange(width-1, width + (extra - 1))]
        y = np.r_[np.zeros(extra), y, np.zeros(extra)]

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title('$x(t)$')
        
        # picture must be saved as an svg...
        signal = 'signal.svg'
        
        # ...but care must be taken so that every random picture has a different name
        signal = py2gift.file.unique_name(signal)
        
        fig.savefig(signal, transparent=True)
        
        # after the file is created, we don't need it anymore (and it's taking up resources)
        plt.close()
        
        self.statement.fill(signal=signal)
        
        # since `np.arange` stops right before the argument,
        width -= 1
        
        squared_slope = slope**2
        
        self.feedback.fill(
            width=width,
            slope=slope,
            squared_slope=squared_slope
        )
        
        solution = width**3 * squared_slope / 3
        
        # whatever is passed as the "right answer" must be a string...
        self.right_answer = py2gift.tex.from_number(solution, precision=3, fixed_point_format=True)
        
        # ...and so must the wrong "answers"; for generating wrong answers we use the
        # method `wrong_numerical_solutions_from_correct_one` from `py2gift.util` module
        self.wrong_answers = py2gift.util.wrong_numerical_solutions_from_correct_one(
            solution=solution, n=7,
            min_sep=0.5*solution,
            max_sep=solution,
            precision=3, fixed_point_format=True,
            bin_width=0.5,
            lower_bound=0, unique=True, prng = self.prng)
        

