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
  has_int_header = 0 
  stuid_pos = 6
  num_cols = 13
  students={}
  try:
    infile = open(argv[0],'r')
    outfile = open(argv[1],'w')
    has_int_header = int(argv[2]) 
    stuid_pos = int(argv[3]) 
    num_cols = int(argv[4]) 
    print """
      USAGE: python clean_assessment.py <pre_or_post_input_file> <pre_post_cleaned_output_file>
                        <1 if the questions are integers as in Anganwadi assessment>
      			<Postion of student ID in the input file i.e column index from 0>
      			<Total number of header columns counting from 1>
    """
    data = csv.reader(infile,delimiter='|')
    header = '|'.join(data.next()[:-2])
    for row in data:
      studentid = row[stuid_pos]
      if studentid in students:
        students[studentid]["data"][row[num_cols]]=row[num_cols+1]
      else:
        if len(students) > 0:
          students[studentid] = {"meta":'|'.join(row[0:stuid_pos+1])+'|'+'|'.join(row[stuid_pos+1:num_cols])}
        else:
          students = {studentid: {"meta":'|'.join(row[0:stuid_pos+1])+'|'+'|'.join(row[stuid_pos+1:num_cols])}}
        students[studentid]["data"]={row[num_cols]:row[num_cols+1]}
        
    print ' Received all students....'
    print len(students.keys())
    append = ''
    header_set = False
    qkeys = []
    for stu in students:
      writeline = students[stu]["meta"]
      if len(append) == 0:
        if has_int_header:
          qkeys = sorted(map(int,students[stu]["data"].keys()))
        else:
          qkeys = sorted(students[stu]["data"].keys())
        append = header + '|' + '|'.join(map(str,qkeys))
      for key in qkeys: 
        writeline = writeline + '|' + clean_dict(students[stu]["data"],str(key))
      if header_set == False:
      	outfile.write(append.capitalize() + "\n")
        header_set = True
      outfile.write(writeline + '\n')
  except:
    print "Unexpected error:", sys.exc_info()
    print "Exception in user code:"
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60
  finally:
    outfile.close()
    infile.close()

if __name__ == "__main__":
   main(sys.argv[1:])
