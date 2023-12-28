import numpy as np
from stl import mesh


def create_mesh_cube(offset):
    """
    Create a mesh for a cube with a given offset.
    """
    # Define the 8 vertices of the cube
    vertices = np.array([
        [0, 0, 0],  # 0
        [1, 0, 0],  # 1
        [1, 1, 0],  # 2
        [0, 1, 0],  # 3
        [0, 0, 1],  # 4
        [1, 0, 1],  # 5
        [1, 1, 1],  # 6
        [0, 1, 1],  # 7
    ])

    # Define the 12 triangles composing the cube
    faces = np.array([
        [0, 3, 1],
        [1, 3, 2],
        [0, 4, 7],
        [0, 7, 3],
        [4, 5, 6],
        [4, 6, 7],
        [5, 1, 2],
        [5, 2, 6],
        [2, 3, 6],
        [3, 7, 6],
        [0, 1, 5],
        [0, 5, 4],
    ])

    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]

    # Translate the mesh
    cube.x += offset[0]
    cube.y += offset[1]
    cube.z += offset[2]

    return cube


def test():
    cube_1 = create_mesh_cube([0, 0, 0])
    cube_2 = create_mesh_cube([4, 0, 0])

    cube = mesh.Mesh(np.concatenate([cube_1.data, cube_2.data]))

    # Write the mesh to file "cube.stl"
    cube.save('meshes/cube.stl')


if __name__ == '__main__':
    test()
