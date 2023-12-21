''' file metadata printer script '''
import os

def file_and_dir_getter():
    print("Please provide the full file path for which to extract metadata:")
    loc_file = input("> ")
    return loc_file

def metadata_dumper(loc_file):
    metadata = os.stat(loc_file)
    for piece in range(0, len(metadata) - 1):
        print(metadata[piece])
    print(metadata)

def main():
    loc_file = file_and_dir_getter()
    metadata_dumper(loc_file)

main()