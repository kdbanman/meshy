import numpy as np

from stl import mesh

from conways import ConwayEnv
from mesh_util import create_mesh_cube


def naive_cubes(steps, include_perimeter=False):
    cubes = []
    for z, step in enumerate(steps):
        for x in range(step.shape[0]):
            for y in range(step.shape[1]):
                if step[x,y] == 1:
                    cubes.append(create_mesh_cube([x, y, z]))
    
    if include_perimeter:
        # At z=0, add a cube for each perimeter cell
        cubes.append(create_mesh_cube([0, 0, 0]))
        cubes.append(create_mesh_cube([0, step.shape[1] - 1, 0]))
        cubes.append(create_mesh_cube([step.shape[0] - 1, 0, 0]))
        cubes.append(create_mesh_cube([step.shape[0] - 1, step.shape[1] - 1, 0]))
    
    return mesh.Mesh(np.concatenate([cube.data for cube in cubes]))


def efficient_cubes(steps):
    """
    Iterate over the cells in steps, and create cubes for the cells that are alive,
    but don't create vertices or faces between cubes adjacent in the same step.
    """
    vertices = []

    for z, step in enumerate(steps):
        for x in range(step.shape[0]):
            for y in range(step.shape[1]):
                if step[x,y] == 1:
                    vertices.append([x, y, z])


def test():
    naive_cubes(
        ConwayEnv
            .init_glider(10, 10)
            .steps(40)
    ).save('meshes/glider_naive_cubes.stl')

    naive_cubes(
        ConwayEnv
            .init_methuselah(11, 11)
            .steps(15)
    ).save('meshes/methuselah_naive_cubes.stl')

    naive_cubes(
        ConwayEnv
            .init_r_pentomino(50, 50)
            .steps(50)
    ).save('meshes/r_pentomino_naive_cubes.stl')


def big_pentomino():
    naive_cubes(
        ConwayEnv
            .init_r_pentomino(100, 100)
            .steps(700)
    ).save('meshes/r_pentomino_naive_cubes_big.stl')


def big_cross():
    naive_cubes(
        ConwayEnv
            .init_cross(80, 80, 35)
            .steps(50, warn_on_perimeter=True)
    ).save('meshes/cross_naive_cubes_big.stl')


def big_random():
    naive_cubes(
        ConwayEnv
            .init_random(30, 30)
            .steps(100)
    ).save('meshes/random_naive_cubes_big.stl')


if __name__ == '__main__':
    big_random()
