import trimesh

# This function doesn't copy the geometry. Modify based on https://github.com/mikedh/trimesh/blob/main/trimesh/scene/scene.py#L1194
# The original function has something wrong with the geometry copy
def scene_transform_copy(mesh):
    """
    Return a deep copy of the current scene
    Returns
    ----------
    copied : trimesh.Scene
        Copy of the current scene
    """
    # Doesn't copy the geometry
    geometry = mesh.geometry

    if not hasattr(mesh, "_camera") or mesh._camera is None:
        # if no camera set don't include it
        camera = None
    else:
        # otherwise get a copy of the camera
        camera = mesh.camera.copy()
    # create a new scene with copied geometry and graph
    copied = trimesh.Scene(
        geometry=geometry,
        graph=mesh.graph.copy(),
        metadata=mesh.metadata.copy(),
        camera=camera,
    )
    return copied


class MeshNode:
    def __init__(self):
        self.mesh = None
        self.geometry = None

    def addMesh(self, scene, mesh):
        if self.mesh == None:
            self.mesh = scene
            self.geometry = mesh
        else:
            self.mesh = trimesh.scene.scene.append_scenes([self.mesh, mesh])
            self.geometry = trimesh.util.concatenate(self.geometry, mesh)

    def addMeshFile(self, mesh_file, scale=[1., 1., 1.]):
        # Read the mesh from obj file
        if mesh_file.startswith("default_"):
            mesh_file = mesh_file.lstrip("default_")
            if mesh_file == "box":
                mesh = trimesh.creation.box(extents=scale)
            else:
                raise RuntimeError("Creation not set")
        else:
            mesh = trimesh.load(mesh_file)
            mesh.apply_scale(scale)
        if not isinstance(mesh, trimesh.Scene):
            scene = trimesh.Scene()
            scene.add_geometry(mesh)
        else:
            scene = mesh.copy()
            mesh = list(mesh.geometry.values())[0]

        self.addMesh(scene, mesh)

    def getMesh(self, worldMatrix, scene):
        if self.mesh == None:
            return None
        if scene:
            new_mesh = scene_transform_copy(self.mesh)
        else:
            new_mesh = self.geometry.copy()
        new_mesh.apply_transform(worldMatrix)
        return new_mesh
