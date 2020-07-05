# A small tool to make making easier
# 20/06/2020
# Written by Junjun(Joseph) Pan, z5141460@ad.unsw.edu.au

import os
import sys
import shutil
import zipfile
import tarfile

class Config:
    defalt_path = './lab1'
    debug = False

class Extractor():
    _path = ''
    _dest = ''
    _sub_name = ''
    _excluded_dirs = ['__MACOSX']
    def __init__(self, path = './', dest = './result', submission_name = '/submission.tar'):
        self._path = path
        self._dest = dest
        self._sub_name = submission_name

        if self._path[-1] != '/':
            self._path = self._path + '/'

        if self._dest is not None:
            if self._dest[-1] != '/':
                self._dest = self._dest + '/'
        else:
            self._dest = self._path

    def get_submission(self, file_name, submission_tar_path):
        if file_name != self._path + file_name:
            file_name = self._path + file_name
        onedrive_zip = zipfile.ZipFile(file_name)
        onedrive_zip.extract(submission_tar_path, self._dest)
        return onedrive_zip

    def extract_submission(self, submission_tar_path, dest_path):
        submission_tar = tarfile.open(submission_tar_path)
        task_names = submission_tar.getnames()
        submission_tar.extractall(dest_path)

        return submission_tar

    def extract_code(self, student_path, task_names, dest_path = _dest):
        if dest_path is None:
            dest_path = student_path
        # Extract student's submission
        for task_name in task_names:
            # print("Extracting: ", task_name, "to", dest_path)
            task_path = student_path + '/' + task_name
            student_zip = zipfile.ZipFile(task_path)
           #  print("Contents of ", task_name, ":", student_zip.namelist())
            # Suppress extraction of MACOSX folders
            for content in student_zip.namelist(): 
                if content.split('/')[0].rstrip('/') in self._excluded_dirs: 
                    continue
                else: 
                    student_zip.extract(content, dest_path)
            
            # student_zip.extractall(dest_path)
            # Delete task.zip
            student_zip.close()
            os.remove(task_path)

    def run(self):
        file_list = os.listdir(self._path)
        # Traverse zip files (which downloaded from OneDrive) under current directory.
        for file_name in file_list:
            student_id = ''
            if os.path.isdir(self._path + file_name):
                # print("Directory: " + str(file_name))
                student_id = file_name
                if not os.path.isdir(self._dest + student_id): 
                    os.mkdir(self._dest + student_id)
                shutil.copyfile(self._path + file_name + self._sub_name, self._dest + student_id + self._sub_name)
            else:
                file_name_split = os.path.splitext(file_name)
                if file_name_split[1] == '.zip':
                    student_id = file_name_split[0]
                    # Get the submission.tar
                    self.get_submission(file_name, student_id + self._sub_name)
                else:
                    # Add additional file formats in future
                    continue

            # student_path = self._path + student_id
            dest_path = self._dest + student_id
            submission_tar_path = self._dest + student_id + self._sub_name

            if os.path.isfile(submission_tar_path):

                submission_tar = self.extract_submission(submission_tar_path, dest_path)
                task_names = submission_tar.getnames()
                # Wrapping this in except block to skip bad files. Will build in some kind of repair
                try:
                    self.extract_code(dest_path, task_names, dest_path = dest_path)
                except zipfile.BadZipFile:
                    print("File corrupted or does not exist")
                # Finshed. Close submission.tar
                submission_tar.close()
                # Delete submission.tar
                os.remove(submission_tar_path)
                
                # If submission enclosed in a folder, extract to root level
                dest_contents = os.listdir(dest_path)
                if len(dest_contents) == 1 and os.path.isdir(dest_path + '/' + dest_contents[0]): 
                    # print("Folder: ", dest_contents)
                    for enclose_content in os.listdir(dest_path + '/' + dest_contents[0]): 
                        os.rename(dest_path + '/' + dest_contents[0] + '/' + enclose_content, \
                                    dest_path + '/' + enclose_content)
                    os.rmdir(dest_path + '/' + dest_contents[0])
                else: 
                    # print("Everything at root")
                    pass
            else: 
                print(submission_tar_path, 'none')
                pass

# https://stackoverflow.com/questions/3083235/unzipping-file-results-in-badzipfile-file-is-not-a-zip-file
def fixBadZipfile(zipFile):
     f = open(zipFile, 'r+b')
     data = f.read()
     pos = data.find(b'\x50\x4b\x05\x06') # End of central directory signature
     if (pos > 0):
         self._log("Truncating file at location " + str(pos + 22)+ ".")
         f.seek(pos + 22)   # size of 'ZIP end of central directory record'
         f.truncate()
         f.close()
     else:
         # raise error, file is truncated
         raise Exception('File is truncated')



if __name__ == '__main__':
    argv = sys.argv
    path = Config.defalt_path
    if len(argv) < 2:
        print('Extract students\'s files from default path: \'{}\''.format(Config.defalt_path))
    else:
        print('Extract students\'s files from ' + '\'{}\''.format(argv[1]))
        path = argv[1]
    print('Extracting...')
    # extract_students_submissions(path, dest = './result')
    extractor = Extractor(path = path)
    extractor.run()
    print('Done! ')
