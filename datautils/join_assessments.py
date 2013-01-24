#!/usr/bin/env python
import os,sys
import traceback
import csv

studentevals={}

def clean_dict(dict,key):
  if key in dict:
    return dict[key]
  else:
    return ' '


def main(argv):
  outfile = None
  infile = None 
  stuid_pos = 6
  num_cols = 13
  students={}
  try:
    in1file = open(argv[0],'r')
    in2file = open(argv[1],'r')
    outfile = open(argv[2],'w')
    stuid_pos = int(argv[3]) 
    num_cols = int(argv[4]) 
    print """
      USAGE: python join_assessments.py <pre_input_file> <post_input_file> <combined_ouput_file>
	      <Postion of student ID in the input file i.e column index from 0>
      	      <Total number of header columns counting from 1>
    """
  
    data = csv.reader(in1file,delimiter='|')
    header = '|'.join(data.next())
    for row in data:
      studentid = row[stuid_pos]
      if studentid in students:
        print "duplicate student id"
      else:
        students[studentid] = {"pre" : '|'.join(row) }
        
    print ' Received all pre students....'
    print len(students.keys())
    
    data = csv.reader(in2file,delimiter='|')
    header = header + '|' + '|'.join(data.next()[num_cols-2:])
    for row in data:
      studentid = row[stuid_pos]
      if studentid in students:
        students[studentid]["post"] = '|'.join(row[num_cols-2:])
      else:
        print "Student not found in post test:" + str(studentid)
    outfile.write(header.capitalize() + "\n")
    for stu in students:
      if "post" in students[stu].keys():
        writeline = students[stu]["pre"] + '|' + students[stu]["post"]
        outfile.write(writeline + '\n')
  except:
    print "Unexpected error:", sys.exc_info()
    print "Exception in user code:"
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60
  finally:
    outfile.close()
    in1file.close()
    in2file.close()

if __name__ == "__main__":
   main(sys.argv[1:])
