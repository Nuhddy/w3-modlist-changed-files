import os

# GAME_PATH = "C://Games//GOG//The Witcher 3 Wild Hunt GOTY//mods"
GAME_PATH = "/mnt/c/Games/GOG/The Witcher 3 Wild Hunt GOTY/mods"

if __name__ == "__main__":
    mod_list = os.listdir(GAME_PATH)
    mod_list.remove("mod0000_MergedFiles")

    with open("files.txt") as f:
        updated_scripts = f.read().splitlines()

    for mod in mod_list:
        script_list = []
        script_path = os.path.join(GAME_PATH, mod, "content/scripts")
        for root, dirs, files in os.walk(script_path):
            for file in files:
                script_list.append(os.path.relpath(os.path.join(root, file), start=script_path))

        changed_scripts = []
        for file in set(script_list).intersection(updated_scripts):
            changed_scripts.append(file)

        if len(changed_scripts) == 0:
            continue

        print("# " + mod)
        changed_scripts.sort()
        for file in changed_scripts:
            print("- " + file)
        print()
