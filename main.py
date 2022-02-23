from fileinput import filename
import json
import os
import sys
import re

print("Texture Atlas Generator by @justash01")
print("GitHub: https://github.com/justash01" "\n")

unsupportedChars = [ ":", "\\", "/", "*", "?", '"', "<", ">", "|", "{", "}", "(", ")", "[", "]", "\\", "/", "-", ]

if os.path.isfile("config.json"):
    with open("config.json") as config_file:
        config = json.load(config_file)

    terrainAtlasPath = config["block_textures_path"]
    itemAtlasPath = config["item_textures_path"]

    itemAtlas = {}
    itemAtlas["texture_name"] = "atlas.items"
    itemAtlas["resource_pack_name"] = config["resource_pack_name.item"]
    itemAtlas["texture_data"] = {}

    terrainAtlas = {}
    terrainAtlas["texture_name"] = "atlas.terrain"
    terrainAtlas["resource_pack_name"] = config["resource_pack_name.terrain"]
    terrainAtlas["padding"] = config["padding"]
    terrainAtlas["num_mip_levels"] = config["num_mip_levels"]
    terrainAtlas["texture_data"] = {}

    print(
        "What do you want to generate an texture atlas for?\n"
        "1. Terrain\n"
        "2. Items\n"
        "3. Exit\n"
    )
    choice = input("Enter your choice: ")

    while choice not in ["1", "2", "3"]:
        print("Invalid choice, try again\n")
        choice = input("Enter your choice: ")

    if choice == "1":
        print("Generating terrain atlas...")
        for root, dirs, files in os.walk(terrainAtlasPath):
            for file in files:
                for extension in config["supportedTextures"]:
                    if file.endswith(extension):
                        filename = os.path.splitext(file)[0]
                        filename = filename.lower()
                        filename = re.sub(r"\s ", "_", filename)
                        for char in unsupportedChars:
                            filename = filename.replace(char, "_")
                        filepath = os.path.join(root, file)
                        filepath = filepath[: -len(extension)]
                        filepath = filepath.replace("\\", "/")

                        terrainAtlas["texture_data"][filename] = {}
                        terrainAtlas["texture_data"][filename]["textures"] = filepath

        with open(os.path.join("textures", "terrain_texture.json"), "w") as outfile:
            json.dump(terrainAtlas, outfile, indent=config["indent"])
            os.startfile(os.path.join("textures"))
            sys.exit()

    elif choice == "2":
        print("Generating item atlas...")
        for root, dirs, files in os.walk(itemAtlasPath):
            for file in files:
                for extension in config["supportedTextures"]:
                    if file.endswith(extension):
                        filename = os.path.splitext(file)[0]
                        filename = filename.lower()
                        filename = re.sub(r"\s ", "_", filename)
                        for char in unsupportedChars:
                            filename = filename.replace(char, "_")
                        filepath = os.path.join(root, file)
                        filepath = filepath[: -len(extension)]
                        filepath = filepath.replace("\\", "/")

                        itemAtlas["texture_data"][filename] = {}
                        itemAtlas["texture_data"][filename]["textures"] = filepath

        with open(os.path.join("textures", "item_texture.json"), "w") as outfile:
            json.dump(itemAtlas, outfile, indent=config["indent"])
            os.startfile(os.path.join("textures"))
            sys.exit()
    elif choice == "3":
        print("Exiting...")
        sys.exit()
else:
    print("config.json not found")
    sys.exit()
