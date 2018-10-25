import os
import shutil
import argparse
import random
import csv
import numpy as np
import os

dir_percentage = {'train': 0.6, 'test': 0.2, 'valid': 0.2}  # 60% : 20% : 20%


def move_to_validation():
    rand = np.random.rand(1)
    if rand < dir_percentage['train']:
        return False
    if dir_percentage['train'] < rand > dir_percentage['train'] + dir_percentage['test']:
        return False
    return True


# usage:
# python sampler.py --csv labels.csv
# only handles .jpg files for now

# python create_validation.py --sample 25 --data /Users/foo/Documents/Data
# assumes file structure like this [valid => [label1 => [ab,c]]]
# input parameter train-first

# assumes file structure like this [label1 => ['valid', 'train'], label2 => ['valid', 'train']]
# input parameter label-first

def create_sample(dir, sample_size=100, labeled=True):
    dir_list = get_immediate_subdirectories(dir)
    if 'train' not in dir_list:
        raise Exception('no training folder')

    os.chdir(dir)
    # what if dir exists
    if not os.path.exists('valid'):
        os.mkdir('valid')
    os.chdir('train')
    dir_list = get_immediate_subdirectories(dir)
    print(dir_list)
    for label in dir_list:
        if label.startswith('.'):
            continue  # skip hidden dirs
        if '_sample' in label:
            continue
        if label == 'train':
            path = os.path.join(*[dir, label])
            os.chdir(path)
            dir_list = get_immediate_subdirectories(path)
            # print(dir_list)
            for foo in dir_list:
                sub_path = os.path.join(*[path, foo])
                # print(foo)
                os.chdir(sub_path)
                files = os.listdir(sub_path)
                # print(sub_path)
                for file in files:
                    # print(file)
                    if move_to_validation():
                        new_path = sub_path.replace('train', 'valid')

                        if not os.path.exists(new_path):
                            os.mkdir(new_path)
                        move_from = os.path.join(*[sub_path, file])
                        move_to = os.path.join(*[new_path, file])
                        # print(move_to)
                        try:
                            shutil.copy(move_from, move_to)
                        except Exception as e:
                            print(e)


            os.getcwd()

        # sample_dir = os.path.join(*[dir, label + '_sample'])

        # if not os.path.exists(sample_dir):
        # os.mkdir(sample_dir)
        # sub_dirs = os.listdir()  # valid, train, test
        #
        # for sub_dir in sub_dirs:
        #     current_dir = os.path.join(*[dir, label, sub_dir])
        #     files = os.listdir(current_dir)
        #     sample_files = random.sample(files, sample_size)
        #
        #     sample_sub_dir = os.path.join(*[dir, sample_dir, sub_dir])
        #     # if not os.path.exists(sample_sub_dir):
        #     # os.mkdir(sample_sub_dir)
        #
        #     for sample_file in sample_files:
        #         copy_from = os.path.join(*[dir, label, sub_dir, sample_file])
        #         copy_to = os.path.join(*[dir, sample_dir, sub_dir, sample_file])
        #         # try:
        #         # shutil.copy(copy_from, copy_to)
        #         # except Exception as e:
        #         #     print(e)


# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
def get_immediate_subdirectories(data_directory):
    return [name for name in os.listdir(data_directory)
            if os.path.isdir(os.path.join(data_directory, name))]


parser = argparse.ArgumentParser(
    description="Copy portion of the dataset to create sample dataset, so we can experiment faster")
parser.add_argument("--csv", type=str, help="Creates sample from csv file with labels and moves files")
parser.add_argument("--sample", type=int, default=200, help="Sample size, default=200")
parser.add_argument("--data", type=str, default=os.getcwd(), help="Path to data, default=cwd")
args = parser.parse_args()

create_sample(args.data, args.sample)
