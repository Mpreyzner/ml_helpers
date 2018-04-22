import os
import shutil
import sys
import random


# usage:
# python sampler "path_to_data"

def create_sample(dir, sample_size=100):
    dir_list = get_immediate_subdirectories(dir)
    for label in dir_list:
        if '_sample' in label:
            continue

        sample_dir = os.path.join(*[dir, label + '_sample'])

        if not os.path.exists(sample_dir):
            os.mkdir(sample_dir)
        sub_dirs = os.listdir(os.path.join(*[dir, label]))  # valid, train, test

        for sub_dir in sub_dirs:
            current_dir = os.path.join(*[dir, label, sub_dir])
            files = os.listdir(current_dir)
            sample_files = random.sample(files, sample_size)

            sample_sub_dir = os.path.join(*[dir, sample_dir, sub_dir])
            if not os.path.exists(sample_sub_dir):
                os.mkdir(sample_sub_dir)

            for sample_file in sample_files:
                copy_from = os.path.join(*[dir, label, sub_dir, sample_file])
                copy_to = os.path.join(*[dir, sample_dir, sub_dir, sample_file])
                try:
                    shutil.copy(copy_from, copy_to)
                except Exception as e:
                    print(e)


def create_sample_from_csv(sample_size=200):
    return False


# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
def get_immediate_subdirectories(data_directory):
    return [name for name in os.listdir(data_directory)
            if os.path.isdir(os.path.join(data_directory, name))]


if len(sys.argv) > 2:
    create_sample(sys.argv[1], int(sys.argv[2]))
else:
    create_sample(sys.argv[1])
