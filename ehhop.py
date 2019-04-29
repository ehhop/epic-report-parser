import sys
import os
import re
import math
import operator
import numpy as np
import pandas as pd


def split_problem_list(problemlist):
	try: 
		if len(problemlist) > 1:
			lst = re.split(r'\s*,\s*', problemlist)
		else: 
			lst = problemlist
		return lst
	except:
		return []


def get_month(date):
	try:
		lst = re.split(r'[/ :]+', date)
		month = int(lst[0])
		year = int(lst[2])
		year = 2000 + year if year < 100 else year
		return "{:04d}-{:02d}".format(year, int(month))
	except: 
		return "0000-00"


def retrieve_problem_list(df, date_col, prob_list_col, enc_status_col):
	probdict = {}
	unique_months = df[date_col].unique()
	probdict = dict.fromkeys(unique_months, [])
	for i, row in df.iterrows():
		enc_date = row[date_col]
		if enc_status_col is not None and row[enc_status_col] != GOOD_STATUS:
			next
		probdict[enc_date] = split_problem_list(row[prob_list_col]) + probdict[enc_date]
	return probdict


def print_probdict(probdict):
	for x in probdict: 
		print(x)
		print(probdict[x])
		print("\n")


def write_top_problem_list(top_dict, f, min_count):
	sorted_dict = sorted(top_dict.items(), key=operator.itemgetter(1), reverse=True)
	if min_count == 0:
		for x in sorted_dict:
			f.write("\t" + x[0] + "\t" + str(x[1]) + '\n')
	else: 
		for x in sorted_dict: 
			if x[1] < min_count: 
				continue 
			f.write("\t" + x[0] + "\t" + str(x[1]) + '\n')


def return_problems_per_month(lst): 
	if len(lst) == 0:
		return {}
	newlst = [x.lower() for x in lst]
	uniquelist = list(set(newlst))
	top_dict = dict.fromkeys(uniquelist,0)
	for x in uniquelist: 
		counts = newlst.count(x)
		top_dict[x] = counts 
	return top_dict 


def write_problems(probdict, f):
	for x in sorted(probdict.keys()): 
		dict_per_month = return_problems_per_month(probdict[x])
		f.write(x + '\n')
		write_top_problem_list(dict_per_month, f, 0)
		f.write('\n')


def return_top_problems_per_month(lst): 
	if len(lst) == 0:
		return {}
	newlst = [x.lower() for x in lst]
	uniquelist = list(set(newlst))
	top_dict = dict.fromkeys(uniquelist,0)
	for x in uniquelist: 
		counts = newlst.count(x)
		if counts > 1: 
			top_dict[x] = counts 
	return top_dict 


def write_top_problems(top_dict, f):
	for x in sorted(probdict.keys()): 
		top_dict_per_month = return_top_problems_per_month(probdict[x])
		f.write(x + '\n')
		write_top_problem_list(top_dict_per_month, f, 1)
		f.write('\n')


if __name__ == '__main__':
	ENCOUNTER_FORMAT = os.getenv("ENCOUNTER_FORMAT")
	date_col = 'ENCOUNTER DATE' if ENCOUNTER_FORMAT else 'Last Enc in Dept'
	prob_list_col = 'PROBLEM LIST' if ENCOUNTER_FORMAT else 'Problem List'
	enc_status_col = 'ENCOUNTER STATUS' if ENCOUNTER_FORMAT else None
	GOOD_STATUS = 'Completed'
	
	csv_path = sys.argv[1] if len(sys.argv) > 1 else 'ehhop.csv'
	ehhop = pd.read_csv(csv_path, delimiter = ',')
	ehhop[date_col] = ehhop[date_col].apply(get_month)
	
	raw_probs_file = open('raw_prob.txt', 'w')
	top_probs_file = open('top_prob.txt', 'w')

	probdict = retrieve_problem_list(ehhop, date_col, prob_list_col, enc_status_col)
	write_problems(probdict, raw_probs_file)
	write_top_problems(probdict, top_probs_file)
