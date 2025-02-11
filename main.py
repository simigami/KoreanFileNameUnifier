import os
import argparse
import tkinter as tk
from tkinter import filedialog
import unicodedata


def normalize_filename(filename):
    """자모 분리된 한글을 정규화하여 원래대로 복구"""
    return unicodedata.normalize('NFC', filename)


def fix_filenames_in_directory(directory, recursive=False):
    """디렉토리 내 모든 파일의 이름을 정규화"""
    for root, _, files in os.walk(directory):
        for filename in files:
            normalized = normalize_filename(filename)
            if filename != normalized:
                src = os.path.join(root, filename)
                dst = os.path.join(root, normalized)
                os.rename(src, dst)
                print(f'Renamed: {src} -> {dst}')
        if not recursive:
            break  # recursive 옵션 없으면 하위 폴더 탐색 X


def fix_single_file(file_path):
    """단일 파일 이름 정규화"""
    directory, filename = os.path.split(file_path)
    normalized = normalize_filename(filename)
    if filename != normalized:
        new_path = os.path.join(directory, normalized)
        os.rename(file_path, new_path)
        print(f'Renamed: {file_path} -> {new_path}')


def cli_mode():
    parser = argparse.ArgumentParser(description="Fix Hangul filenames")
    parser.add_argument("path", help="File or directory path")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search files recursively")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        fix_filenames_in_directory(args.path, args.recursive)
    elif os.path.isfile(args.path):
        fix_single_file(args.path)
    else:
        print("Invalid path")


def gui_mode():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(title="Select a file")
    if path:
        fix_single_file(path)
    else:
        path = filedialog.askdirectory(title="Select a folder")
        if path:
            fix_filenames_in_directory(path, recursive=True)


def main():
    import sys
    if len(sys.argv) > 1:
        cli_mode()
    else:
        gui_mode()


if __name__ == "__main__":
    main()
