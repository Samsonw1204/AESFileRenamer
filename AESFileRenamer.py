from pathlib import Path


STANDARD_NAMES = [
    "Lifeguard Introductions",
    "Skill Evaluation 1--Attempt 1",
    "Skill Evaluation 1--Attempt 2",
    "Skill Evaluation 2--Attempt 1",
    "Skill Evaluation 2--Attempt 2",
    "Skill Evaluation 3--Attempt 1",
    "Skill Evaluation 3--Attempt 2",
]


def get_video_files(folder: Path) -> list[Path]:
    video_extensions = {".mp4", ".mov", ".m4v"}

    videos = [
        file for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in video_extensions
    ]

    return sorted(videos, key=lambda file: file.stat().st_mtime)


def build_standard_rename_plan(videos: list[Path]) -> list[tuple[Path, Path]]:
    if len(videos) != len(STANDARD_NAMES):
        raise ValueError(
            f"Standard mode expects exactly {len(STANDARD_NAMES)} videos, "
            f"but found {len(videos)} videos."
        )

    rename_plan = []

    for old_file, new_base_name in zip(videos, STANDARD_NAMES):
        new_file = old_file.with_name(f"{new_base_name}{old_file.suffix.upper()}")
        rename_plan.append((old_file, new_file))

    return rename_plan


def check_rename_plan(rename_plan: list[tuple[Path, Path]]) -> None:
    new_paths = [new for _, new in rename_plan]

    if len(new_paths) != len(set(new_paths)):
        raise ValueError("Two or more files would be renamed to the same filename.")

    for old_file, new_file in rename_plan:
        if new_file.exists() and old_file != new_file:
            raise FileExistsError(f"Target file already exists: {new_file.name}")


def print_rename_plan(rename_plan: list[tuple[Path, Path]]) -> None:
    print("\nRename preview:")
    print("-" * 60)

    for old_file, new_file in rename_plan:
        print(f"{old_file.name}  ->  {new_file.name}")

    print("-" * 60)


def execute_rename_plan(rename_plan: list[tuple[Path, Path]]) -> None:
    for old_file, new_file in rename_plan:
        old_file.rename(new_file)


def run_standard_mode(folder: Path) -> None:
    videos = get_video_files(folder)

    print("\nVideos found in order:")
    for index, video in enumerate(videos, start=1):
        print(f"{index}. {video.name}")

    rename_plan = build_standard_rename_plan(videos)
    check_rename_plan(rename_plan)
    print_rename_plan(rename_plan)

    confirm = input('\nType "YES" to rename these files: ').strip()

    if confirm == "YES":
        execute_rename_plan(rename_plan)
        print("\nDone. Files renamed successfully.")
    else:
        print("\nCanceled. No files were renamed.")


def run_advanced_mode(folder: Path) -> None:
    print("\nAdvanced mode is not built yet.")
    print("For now, use standard mode only.")


def main() -> None:
    print("AES File Renamer")
    print("================")

    folder_input = input("\nEnter the folder path containing the videos: ").strip().strip('"')
    folder = Path(folder_input)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"This is not a folder: {folder}")

    mode = input(
        "\nPress Enter for standard mode, or type A for advanced options: "
    ).strip().lower()

    if mode == "":
        run_standard_mode(folder)
    elif mode == "a":
        run_advanced_mode(folder)
    else:
        print("\nInvalid option. No files were renamed.")


if __name__ == "__main__":
    main()