import argparse
import os

LATEST_FILELIST = "./filelists/4_03.txt"


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-p", "--path", required=True)
    p.add_argument("-f", "--filelist")

    args = p.parse_args()
    return args


def get_intersect(modlist, filelist, mods_path):
    intersect_mods = {}

    for mod in modlist:
        local_scripts = []
        local_script_path = os.path.join(mods_path, mod, "content")
        for root, dirs, files in os.walk(local_script_path):
            for file in files:
                local_scripts.append(os.path.relpath(os.path.join(root, file), start=local_script_path))

        intersect_scripts = []
        for file in set(local_scripts).intersection(filelist):
            intersect_scripts.append(file)

        if len(intersect_scripts) == 0:
            continue

        intersect_scripts.sort()
        intersect_mods[mod] = intersect_scripts

    return intersect_mods


def print_intersect(mod_dict):
    for mod in mod_dict:
        print("### " + mod + "\n")
        for file in mod_dict[mod]:
            print("- " + file)
        print()


def main():
    args = parse_args()

    if os.path.exists(args.path):
        mods_path = args.path
    else:
        exit(1)

    if args.filelist:
        if not os.path.exists(args.filelist):
            exit(1)
        filelist_path = args.filelist
    elif os.path.exists(LATEST_FILELIST):
        filelist_path = LATEST_FILELIST
    else:
        exit(1)

    # Get modlist
    modlist = os.listdir(mods_path)
    if "mod0000_MergedFiles" in modlist:
        modlist.remove("mod0000_MergedFiles")

    # Get filelist
    with open(filelist_path) as f:
        filelist = f.read().splitlines()

    # Find files present in both modlist and filelist
    intersect_mods = get_intersect(modlist, filelist, mods_path)
    print_intersect(intersect_mods)


if __name__ == "__main__":
    main()
