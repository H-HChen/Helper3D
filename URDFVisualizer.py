from src import (
    URDFParser,
    URDFTree
)

if __name__ == "__main__":
    URDF_file = "../../data/43074/mobility.urdf"
    # Parse the URDF file
    parser = URDFParser(URDF_file)
    parser.parse()
    # Construct the URDF tree
    links = parser.links
    joints = parser.joints
    