from Load_Balance.Loader import Loader
from Manifest import Manifest
import os
from ContainerData import ContainerData

path = "Manifests/"

manifest = Manifest(path, "ShipCase3")
manifest.read_manifest()
loader = Loader(manifest)
moves = loader.load_unload([
            ContainerData("Bat", "00532"),
            ContainerData("Rat", "06317"),
            ],[
            ContainerData("Cow", "00000"),
            ])

for move in moves:
    print(move)