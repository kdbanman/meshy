import numpy as np
from stl import mesh


def supported_mesh_center(neighborhood):
    """
    Map a 3x3x3 binary grid to a mesh in the center of the grid.

    The goal of this is to generate a 3D printable mesh from a 3D binary grid.
    That means
    - each ON cell should be filled (i.e. enclosed by faces, inward from normals.)
    - each OFF cell should be empty (i.e. not enclosed by faces.)
    - an OFF cell can be filled (with a 45 degree angle) if it is supporting an ON cell above.

    It is assumed that if the central cell is ON, and no cell below is ON, then we are at the bottom.
    (i.e. ON cells only appear next to ON neighbors below them, or at the bottom of the grid.)

    Note:
    - Even though a 3x3x3 von Neumann neighborhood is passed in, the columns on the diagonals are ignored.
    - Neighborhood is indexed [z, x, y]
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

    # Define the faces and 45 degree upward diagonals
    XY_bottom = np.array([
        [0, 3, 1],
        [1, 3, 2],
    ])
    YZ_back = np.array([
        [0, 4, 7],
        [0, 7, 3],
    ])
    XY_top = np.array([
        [4, 5, 6],
        [4, 6, 7],
    ])
    YZ_front = np.array([
        [5, 1, 2],
        [5, 2, 6],
    ])
    XZ_right = np.array([
        [2, 3, 6],
        [3, 7, 6],
    ])
    XZ_left = np.array([
        [0, 1, 5],
        [0, 5, 4],
    ])
    ZfY_diagonal = np.array([
        [0, 6, 1],
        [0, 7, 6],
    ])
    ZfX_diagonal = np.array([
        [0, 6, 5],
        [0, 3, 6],
    ])
    ZbY_diagonal = np.array([
        [2, 5, 4],
        [2, 4, 3],
    ])
    ZbX_diagonal = np.array([
        [1, 4, 7],
        [1, 7, 2],
    ])

    # TODO: This is going to get real bad.
    # - Numerical indexing is hard to keep track of.
    # - We're just writing down a tree with 4096 nodes.
    #
    # Rotating and reflecting to check for matches cuts down by a factor of 8, so 512 nodes.  Still nuts.
    faces = []
    if neighborhood[1, 1, 1] == 1:
        if neighborhood[1, 2, 1] == 0:
            if neighborhood[2, 1, 1] == 0:
                faces.append(XY_bottom)
            faces.append(YZ_front)

    faces = np.concatenate(faces)

    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j], :]


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
