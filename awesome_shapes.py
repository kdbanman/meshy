


from conways import ConwayEnv
from render import naive_cubes


def sweet_castle_cross():
    naive_cubes(
        ConwayEnv
            .init_cross(80, 80, 30)
            .steps(50, warn_on_perimeter=True)
    ).save('meshes/cross_sweet_castle.stl')


if __name__ == '__main__':
    sweet_castle_cross()