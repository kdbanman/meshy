import numpy as np

class ConwayEnv:

    # Class method to initialize as a glider
    @classmethod
    def init_glider(cls, width, height):
        if width < 4 or height < 4:
            raise ValueError('Environment must be at least 4x4 for glider.')

        # Initialize the environment
        env = cls(width, height)
        env[1, 2] = 1
        env[2, 3] = 1
        env[3, 1:4] = 1
        return env
    
    # Class method to initialize as a methuselah
    @classmethod
    def init_methuselah(cls, width, height):
        if width < 5 or height < 5:
            raise ValueError('Environment must be at least 5x5 for methuselah.')

        center_x = width // 2
        center_y = height // 2

        env = cls(width, height)
        env[center_y, center_x - 1:center_x + 2] = 1
        env[center_y + 1, center_x] = 1
        return env
    
    # Class method to initialize as an r-pentomino methuselah
    @classmethod
    def init_r_pentomino(cls, width, height):
        if width < 4 or height < 4:
            raise ValueError('Environment must be at least 4x4 for r-pentomomino methuselah.')

        center_x = width // 2
        center_y = height // 2

        env = cls(width, height)
        env[center_y - 1, center_x + 1] = 1
        env[center_y, center_x - 1:center_x + 2] = 1
        env[center_y + 1, center_x] = 1
        return env
    
    # Class method to initialize with a large cross
    @classmethod
    def init_cross(cls, width, height, bar_length=None):
        if width < 3 or height < 3:
            raise ValueError('Environment must be at least 3x3 for cross.')

        center_x = width // 2
        center_y = height // 2

        if bar_length is None:
            bar_length = min(width, height) // 2 - 1

        env = cls(width, height)
        env[center_y, center_x - bar_length + 1:center_x + bar_length] = 1
        env[center_y - bar_length + 1:center_y + bar_length, center_x] = 1
        return env
    
    # Class method to initialize as a random environment
    @classmethod
    def init_random(cls, width, height, p=0.5, seed=None):
        env = cls(width, height)

        if seed is not None:
            np.random.seed(seed)

        idx = np.random.rand(height, width) < p

        # Set outer perimeter of idx to False
        idx[0, :] = False
        idx[-1, :] = False
        idx[:, 0] = False
        idx[:, -1] = False

        env[idx] = 1
        
        return env

    def __init__(self, width, height):
        self.env = np.zeros((height, width), dtype=np.uint8)

    def test_render(self):
        print(self.env)

    def step(self, warn_on_perimeter=False):
        """
        Apply one step of Conway's Game of Life with implicit zero padding.
        """
        if warn_on_perimeter:
            if np.any(self[0, :]) or np.any(self[-1, :]) or np.any(self[:, 0]) or np.any(self[:, -1]):
                print('WARNING: Live yerimeter cells encountered.')

        # Compute the number of neighbours for each cell
        neighbours_count = np.zeros(self.env.shape, dtype=int)
        for i in range(self.env.shape[0]):
            for j in range(self.env.shape[1]):
                neighbours_count[i, j] = np.sum(self[i - 1 : i + 2, j - 1 : j + 2]) - self[i, j]

        # Apply the rules of the game
        new_env = ConwayEnv(self.env.shape[1], self.env.shape[0])
        new_env[np.logical_and(self.env == 1, neighbours_count < 2)] = 0
        new_env[np.logical_and(self.env == 1, np.logical_or(neighbours_count == 2, neighbours_count == 3))] = 1
        new_env[np.logical_and(self.env == 1, neighbours_count > 3)] = 0
        new_env[np.logical_and(self.env == 0, neighbours_count == 3)] = 1

        return new_env
    
    def steps(self, n_steps, warn_on_perimeter=False):
        """
        Apply n_steps steps of Conway's Game of Life.
        Returns all steps in a list.
        """
        steps = [self]

        for i in range(n_steps):
            steps.append(steps[i].step(warn_on_perimeter))

        return steps
    
    # Delegate subscripting to the underlying environment
    def __getitem__(self, key):
        return self.env[key]
    
    def __setitem__(self, key, value):
        self.env[key] = value
    
    # Delegate slicing to the underlying environment
    def __getslice__(self, i, j):
        return self.env[i:j]
    
    def __setslice__(self, i, j, value):
        self.env[i:j] = value
    
    # Delegate all ndarray properties to the underlying environment
    def __getattr__(self, name):
        return getattr(self.env, name)

    def __str__(self):
        return str(self.env).replace('0', '.').replace('1', 'X')

    def __repr__(self):
        return repr(self.env)


def test():
    for step in ConwayEnv.init_glider(7, 7).steps(3):
        print(step)

    print('')
    for step in ConwayEnv.init_methuselah(9, 9).steps(5):
        print(step)
    
    print('')
    for step in ConwayEnv.init_r_pentomino(7, 7).steps(5):
        print(step)
    
    print('')
    for step in ConwayEnv.init_random(7, 7).steps(5):
        print(step)

    print('')
    for step in ConwayEnv.init_cross(10, 10).steps(5):
        print(step)


if __name__ == '__main__':
    test()
