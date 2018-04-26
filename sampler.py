import os
import shutil
import argparse
import random
import csv


# usage:
# python sampler.py --csv labels.csv
# assumes file structure like this ['valid', 'train']

# python sampler.py --sample 25 --data /Users/foo/Documents/Data
# assumes file structure like this [label1 => ['valid', 'train'], label2 => ['valid', 'train']]

def create_sample(dir, sample_size=100, labeled=True):
    dir_list = get_immediate_subdirectories(dir)
    for label in dir_list:
        if label.startswith('.'):
            continue  # skip hidden dirs
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


def create_sample_from_csv(filename, sample_size=200, files_dir='train', extension='jpg'):
    #broken for now, for some reason makes a sample out of .git folder :P
    f = open(filename, mode='r')
    reader = csv.reader(f)
    sample_file_name = filename + "_sample"
    row_count = sum(1 for row in reader)
    f.seek(0)  # reset counter
    chance = sample_size / row_count
    counter = row_counter = 0
    files = []
    data = []

    for row in reader:
        if row_counter == 0:
            data.append(row)  # add labels
        rand = random.random()
        row_counter = row_counter + 1
        if rand <= chance:
            counter = counter + 1
            filename = row[0]
            data.append(row)
            files.append(filename)
    f.close()
    new_file = open(sample_file_name, "w+")
    writer = csv.writer(new_file)
    for row in data:
        writer.writerow(row)
    new_file.close()
    print("Move files to sample.csv:" + str(counter))

    sample_dir = files_dir + "_sample"
    if not os.path.exists(sample_dir):
        os.mkdir(sample_dir)
    for file in files:
        try:
            print("moving file: " + file)
            copy_from = os.path.join(*[os.path.abspath(os.getcwd()), files_dir, file + "." + extension])
            copy_to = os.path.join(*[os.path.abspath(os.getcwd()), sample_dir, file + "." + extension])
            shutil.copy(copy_from, copy_to)
        except Exception as e:
            print(e)


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

if args.csv:
    create_sample_from_csv(args.csv, args.sample)
else:
    create_sample(args.data, args.sample)

