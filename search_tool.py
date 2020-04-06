import os
import time
import re
import datetime as kctime
import sys
import thread
from time import sleep

path = 'C:\\'
count = 0
match_file = 0
dir_count = 0
dir_list=[]
file_list=[]
path_list=[]
filepath = r'C:\test_directory\kc_search_log.txt'


result_dict = {'Total Directory Searched':0,
			   'Total Files Searched':0,
			   'Matching Files':0,
			   'Matching Directory':0,
			   'Search String':'',
			   'Elapsed Time (In Seconds)':''
			   }


def search_files(search_str):
	# Record time before starting search operation

	start = time.time()
	fh = open(filepath,'r')
	
	pattern = r'[\w\W]%s.*' % search_str 
	for file in fh.readlines():
		#result_dict['Total Files Searched'] += 1fp
		match = re.search(pattern, file.lower())
		if match:
			print file
			result_dict['Matching Files'] += 1
	fh.close()
	end = time.time()
	
	#print "Time took to read entry from indexd file\t - %f" % (end-start)
	#print "Total searched files \t\t\t%s" %result_dict['Total Files Searched']
	#print "Total matching files found \t\t%s" %result_dict['Matching Files']
	#print 'Search String %s' %result_dict['Search String']

def print_result():
	'''
	This function display the file search statisticks
	'''
	
	for key in result_dict:
		print key,':',result_dict[key]
	return True

def display_counter(name,data):
	'''
	Display number of files searched 
	
	'''
	global result_dict
	#print 'Thread Name %s' %name
	while not search_completed:
		time.sleep(0.01)
		print 'File Searched {}\r'.format(result_dict['Total Files Searched']),
	return True 
	

# Main function 
# Record time before starting search operation

def my_doc():
        '''
        Usage : python my_search_tool.py <directory path> <pattern to search> 

        Example:
                # python my_search_tool.py C:\ data"
        '''
try:
        pattern = sys.argv[2]
        path = sys.argv[1]
except IndexError:
        print my_doc.__doc__
        exit(1)

search_completed = False

result_dict['Search String'] = 'Pattern to search {} in a path {}'.format(pattern,path)
start_time = time.time()

thread.start_new_thread(display_counter,("counterhandler",1))

fh = open(filepath,'w')

for p,d,f in os.walk(path):
	for di in d:
		dir_list.append(di)
		result_dict['Total Directory Searched'] +=1
	for fn in f:
		count+=1
		result_dict['Total Files Searched'] += 1
		file_list.append(fn)
		path_list.append(os.path.join(p,fn))

# Record time of completion.
end_time = time.time()
search_completed = True

for dd in path_list:
	fh.write(dd+'\n')

fh.close()
search_files(pattern)

result_dict['Elapsed Time (In Seconds)'] = str(end_time - start_time)
print_result()

#print 'Total Directory Searched files \t\t-%s' %dir_count
#print 'Time took to index files is\t- %f Seconds' %t

