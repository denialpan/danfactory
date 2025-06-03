import zipfile
import os
import argparse
from tqdm import tqdm  # install with: pip install tqdm


def filter_zip_by_keep_list(zip_path, keep_prefixes):
    temp_zip_path = zip_path + '.tmp'

    with zipfile.ZipFile(zip_path, 'r') as zip_read:
        all_items = zip_read.infolist()

        # Determine which files to keep
        kept_items = [
            item for item in all_items
            if any(item.filename.startswith(prefix.rstrip('/') + '/') or item.filename == prefix for prefix in keep_prefixes)
        ]

        with zipfile.ZipFile(temp_zip_path, 'w') as zip_write:
            for item in tqdm(kept_items, desc="Filtering ZIP contents", unit="file"):
                zip_write.writestr(item, zip_read.read(item.filename))

    os.replace(temp_zip_path, zip_path)
    print(f"\n✅ Retained only folders/files: {keep_prefixes} in {zip_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Keep only specified folders/files in a ZIP archive.")
    parser.add_argument("--zip", required=True, help="Path to the .zip file")
    parser.add_argument("--pack", required=True,
                        choices=["server", "client"], help="Type of pack: server or client")
    args = parser.parse_args()

    # Define separate keep lists based on the pack type
    keep_prefixes_by_pack = {
        "server": {
            "mods",
            "run.sh",
            "run.bat",
            "neoforge-21.1.174-installer.jar",
            "config",
            "server.properties",
            "server-icon.png",
        },
        "client": {
            "minecraft/config",
            "minecraft/mods",
            "minecraft/resourcepacks",
            "minecraft/debug",
            "minecraft/defaultconfgs",
            "instance.cfg",
            "mmc-pack.json",
            "server.png"
        }
    }

    keep_prefixes = keep_prefixes_by_pack[args.pack]

    print(
        f"⚠️  WARNING: This operation will permanently delete everything in the ZIP except these {args.pack} items:")
    for prefix in keep_prefixes:
        print(f" - {prefix}/")
    print("This action is irreversible unless you have a backup.\n")

    confirm = input(
        "Are you sure you want to continue? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        return

    filter_zip_by_keep_list(args.zip, keep_prefixes)


if __name__ == "__main__":
    main()
