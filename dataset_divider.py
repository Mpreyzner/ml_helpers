import os
import shutil
import numpy as np
import sys

# usage:
# python dataset_divider "path_to_data"

dirs = ['train', 'test', 'valid']
dir_percentage = {'train': 0.6, 'test': 0.2, 'valid': 0.2}  # 60% : 20% : 20%


def divide(dir):
    if not os.path.exists(dir):
        raise Exception
    os.chdir(dir)
    dir_list = get_immediate_subdirectories(dir)

    for label in dir_list:
        files = os.listdir(label)

        for curr in dirs:
            if not os.path.exists(curr):
                os.chdir(label)
                os.mkdir(curr)
                os.chdir('..')

        for file in files:
            rand = np.random.rand(1)
            if rand < dir_percentage['train']:
                dest = 'train'
            elif dir_percentage['train'] < rand > dir_percentage['train'] + dir_percentage['test']:
                dest = 'test'
            else:
                dest = 'valid'
            try:
                move_from = dir + '/' + label + '/' + file
                move_to = dir + '/' + label + '/' + dest + '/' + file
                shutil.move(move_from, move_to)
            except Exception as e:
                print(e)


# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
def get_immediate_subdirectories(data_directory):
    return [name for name in os.listdir(data_directory)
            if os.path.isdir(os.path.join(data_directory, name))]


divide(sys.argv[1])
