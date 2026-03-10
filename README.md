# Game Data Mover

This project finds folders that have the word **game** in their name and copies them into a new target folder that you specify when running the script.

## How to Run

```bash
python get_game_data.py data target
```

- `data` — your source folder (where your game folders live- Inthis case its already created)
- `target` — where the copied folders will be moved to

---

## Functions Walkthrough

### `find_all_game_paths(source)`
Walks through the source folder and collects the paths of any folder that has the word **"game"** in its name.

```
data/
  chess_game/    found
  snake_game/    found
  music/         skipped
```

---

### `create_dir(path)`
Creates the target folder if it doesn't already exist. If it does exist, it leaves it alone.

---

### `get_name_from_path(paths, to_string)`
Strips the `_game` part from each folder name so the copied folder has a cleaner name.

```
chess_game  →  chess
snake_game  →  snake
```

---

### `copy_and_overwrite(source, target)`
Copies a game folder into the target. If a folder with the same name already exists at the target, it deletes it first then copies fresh.

---

### `create_Json_metadata(path, game_dirs)`
Creates a `metadata.json` file inside the target folder that keeps a record of what was copied.

```json
{
  "gameNames": ["chess", "snake"],
  "numberOfGames": 2
}
```

---

### `main(source, target)`
The function that ties everything together. It runs all the above steps in order:
1. Creates the target folder
2. Finds all game folders in source
3. Cleans up their names
4. Copies each one to target
5. Writes the metadata file