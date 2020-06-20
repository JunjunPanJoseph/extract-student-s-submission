# A small tool to make making easier
# 20/06/2020
# Written by Junjun(Joseph) Pan, z5141460@ad.unsw.edu.au

import os
import sys
import zipfile
import tarfile

class Config:
    defalt_path = './lab1'
    debug = False


def extract_students_submissions(path = './'):
    if path[-1] != '/':
        path = path + '/'
    file_list = os.listdir(path)
    # Traverse zip files (which downloaded from OneDrive) under current directory.
    for file_name in file_list:
        file_name_split = os.path.splitext(file_name)
        if file_name_split[1] == '.zip':
            file_name = path + file_name
            student_id = file_name_split[0]
            student_path = path + student_id
            onedrive_zip = zipfile.ZipFile(file_name)
            # Get the submission.tar
            submission_tar_path = student_id + '/submission.tar'
            onedrive_zip.extract(submission_tar_path, path)
            # Extract submission.tar
            submission_tar_path = path + submission_tar_path
            submission_tar = tarfile.open(submission_tar_path)
            task_names = submission_tar.getnames()
            submission_tar.extractall(path + student_id)
            # Extract student's submission
            for task_name in task_names:
                task_path = student_path + '/' + task_name
                student_zip = zipfile.ZipFile(task_path)
                student_zip.extractall(student_path)
                # Delete task.zip
                student_zip.close()
                os.remove(task_path)
            # Finshed. Close submission.tar
            submission_tar.close()
            # Delete submission.tar
            os.remove(submission_tar_path)
        if Config.debug:
            break

if __name__ == '__main__':
    argv = sys.argv
    path = Config.defalt_path
    if len(argv) < 2:
        print('Extract students\'s files from default path: \'{}\''.format(Config.defalt_path))
    else:
        print('Extract students\'s files from ' + '\'{}\''.format(argv[1]))
        path = argv[1]
    print('Extracting...')
    extract_students_submissions(path)
    print('Done! ')
