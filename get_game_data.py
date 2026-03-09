import os
import json
import shutil
from subprocess import run, PIPE
import sys

GAME_DIR_PATTERN="game"

#function to find all game paths in the source directory
def find_all_game_paths(source):
    game_paths=[]

    for root,dirs,files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path=os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths
#function to create the destination directory ifit doesn't exist
def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

#function to get thenames and remove the games from the folder name
def get_name_from_path(paths,to_sring):
    new_names=[]
    for path in paths:
        _,dir_name=os.path.split(path)
        new_dir_name=dir_name.replace(to_sring,"")

        new_names.append(new_dir_name)

    return new_names

#function to copy the game data from the source to the target directory
def copy_and_overwrite(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)

    shutil.copytree(source, target)

#Function to make Json Metadatafiles
def create_Json_metadata(path, game_dirs):
    data={
        "gameNames":game_dirs,
        "numberOfGames":len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)

#function to copy the game data from the source to the target directory
def main(source, target):
    cwd=os.getcwd()
    source_path=os.path.join(cwd, source)
    target_path=os.path.join(cwd, target)

    game_paths=find_all_game_paths(source_path)

    new_game_dirs=get_name_from_path(game_paths, "_game")
    
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path= os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
    
    json_path=os.path.join(target_path, "metadata.json")
    create_Json_metadata(json_path,new_game_dirs)
    create_dir(target_path)


if __name__=="__main__":
    args = sys.argv

    if len(args) != 3:
        raise Exception("You must pass a source directory and a destination directory")

    source, target= args[1:]
    main(source, target)