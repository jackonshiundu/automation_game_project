import unittest
import tempfile         
import os               
import json 
from get_game_data import find_all_game_paths, create_dir, get_name_from_path,  create_Json_metadata

#test to create a temporary directory and check if it is created successfully
class TestCreateDir(unittest.TestCase):
    def test_create_directory_if_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            new_dir=os.path.join(tmp,"new_folder")

            create_dir(new_dir)
            self.assertTrue(os.path.exists(new_dir))

class TestFindAllGamePaths(unittest.TestCase):
    """ test to check if the function find_all_game_paths correctly identifies directories with "game" in their name and ignores others """
    def test_find_dirs_wwith_game_in_their_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.mkdir(os.path.join(tmp,"chess_game"))
            os.mkdir(os.path.join(tmp,"scrabble_game"))
            os.mkdir(os.path.join(tmp,"music_folder"))

            finded_paths=find_all_game_paths(tmp)

            self.assertEqual(len(finded_paths), 2)
            self.assertTrue(any("chess_game" in path for path in finded_paths))
            self.assertTrue(any("scrabble_game" in path for path in finded_paths))
    
    """ test to check if the function find_all_game_paths correctly ignores directories that do not contain "game" in their name """
    def test_ignores_all_non_game_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.mkdir(os.path.join(tmp,"music_folder"))
            os.mkdir(os.path.join(tmp,"documents"))

            finded_paths=find_all_game_paths(tmp)

            self.assertEqual(len(finded_paths), 0)

class TestGetNameFromPath(unittest.TestCase):
    """ test to check if the function get_name_from_path correctly removes the specified string from the directory names """
    def test_remove_game_from_dir_names(self):
        paths=[
            "/path/to/chess_game",
            "/path/to/scrabble_game",
            "/path/to/music_folder"
        ]
        expected_names=[
            "chess",
            "scrabble",
            "music_folder"
        ]

        new_names=get_name_from_path(paths, "_game")

        self.assertEqual(new_names, expected_names)

class TestCreateJsonMetadata(unittest.TestCase):
    def test_create_json_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_path=os.path.join(tmp,"metadata.json")
            game_dirs=["chess", "scrabble"]

            create_Json_metadata(json_path, game_dirs)
            self.assertTrue(os.path.exists(json_path))
    

    def test_json_contains_correct_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_path=os.path.join(tmp,"metadata.json")
            game_dirs=["chess", "scrabble"]

            create_Json_metadata(json_path, game_dirs)

            with open(json_path, "r") as f:
                data=json.load(f)
            
            self.assertEqual(data["gameNames"], game_dirs)
            self.assertEqual(data["numberOfGames"], len(game_dirs))

if __name__ == "__main__":
    unittest.main()