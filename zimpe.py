import shutil
import sys

# usage python zimpe.py "absolute path"
shutil.make_archive('dataset', 'zip', sys.argv[1])
