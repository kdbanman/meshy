from conways import ConwayEnv

def r_pentomino(size, steps):
    ConwayEnv\
        .init_r_pentomino(size, size)\
        .steps(steps)


def minimum_pentomino_size(steps):
    """
    Use binary search to find smallest size that doesn't crash for r_pentomino (raises ValueError)
    Start from the crashing size and double it until it doesn't crash anymore, then back off by half
    the difference between the last crashing size and the current size.
    """
    size_crashes = 1
    size_finishes = None

    while size_finishes is None or size_finishes - size_crashes > 1:
        if size_finishes is None:
            size = size_crashes * 2
        else:
            size = (size_crashes + size_finishes) // 2

        try:
            print(f'{size}', end='', flush=True)
            r_pentomino(size, steps)
            print('✅', end='', flush=True)

            size_finishes = size
        except ValueError:
            print('❌', end='', flush=True)
            size_crashes = size
    
    print(f'\nMinimum size for steps {steps} is {size_finishes}')

    return size_finishes


if __name__ == '__main__':
    steps = range(100, 1100, 100)
    min_sizes = []

    for step in steps:
        print(f'Searching for minimum given {step} steps...')
        min_sizes.append(minimum_pentomino_size(step))
        print('')
    
    print(f'Steps:          {steps}')
    print(f'Minimum sizes:  {min_sizes}')
