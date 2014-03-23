#!/usr/bin/env python2

import sys, os
import getopt
import datetime as dt
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

bm_total_face_num = 0
bm_total_male_num = 0
bm_total_female_num = 0

res_total_pos_face_num = 0
res_total_neg_face_num = 0
res_total_pos_male_num = 0
res_total_neg_male_num = 0
res_total_pos_female_num = 0
res_total_neg_female_num = 0

def usage():
    print('----------------------------------------------------------------')
    print('[[Usage]]::evaluate the face detector')
    print('\t./benchmark.py [Paras] benchmark_path_list res_path_list')
    print('[[Paras]]::')
    print('\t--help/-h : Print usage info')
    print('----------------------------------------------------------------')

def is_true_face(bm_face_list, rect):
    return (False, "None")

def cal_detect_ratio(bm_xml_path, res_xml_path):
    global bm_total_face_num 
    global bm_total_male_num 
    global bm_total_female_num

    global res_total_pos_face_num 
    global res_total_neg_face_num 
    global res_total_pos_male_num 
    global res_total_neg_male_num 
    global res_total_pos_female_num 
    global res_total_neg_female_num 

    bm_tree = ET.parse(bm_xml_path)
    bm_root = bm_tree.getroot()
    res_tree = ET.parse(res_xml_path)
    res_root = res_tree.getroot()
    
    ### Get the benchmark first
    
    ### Analyse the res file
    for face in res_root:
        x, y, width, height = 0, 0, 0, 0
        gender = ''
        #get pos first
        for attr in face: 
            if 'postion' != attr.tag:
                continue
            for pos in attr:
                if 'x' == pos.tag:
                    x = eval(pos.text)
                elif 'y' == pos.tag:
                    y = eval(pos.text)
                elif 'width' == pos.tag:
                    width = eval(pos.text)
                elif 'height' == pos.tag:
                    height = eval(pos.text)
            break
                    
        ## Judge if a false detection
                    
        ## get gendet info
        for attr in face: 
            if 'gender' != attr.tag:
                continue
            for gen in attr:
                if 'value' != gen.tag:
                    continue
                gender = gen.text
            break
        ## Judge if a false detection
                    



def main():
    if len(sys.argv) < 2:
        usage()
        return

    try:
        opts, args=getopt.getopt(sys.argv[1:], 
                                 "h", ["help"])  
    except getopt.GetoptError:
        print("ERROR:: Errors occur in getting option Paras")
        usage()
        return 
    
    bIsHelp = False
    
    for op, arg in opts:
        if op in ("--help","-h"):
            bIsHelp = True
        else:
            continue

    if bIsHelp:
        usage()
        return

    try:
        bm_path_list = args[0]
        res_path_list = args[1]
        if not os.path.exists(bm_path_list):
            raise
        if not os.path.exists(res_path_list):
            raise
    except:
        print("ERROR::Please input the right 'benchmark_path_list' and 'jpg_path_list' Paras")
        return 

    bm_file = open(bm_path_list, 'r')
    bm_list = bm_file.readlines()
    res_file = open(res_path_list, 'r')
    res_list = res_file.readlines()
    bm_file.close()
    res_file.close()

    bm_list = list(set(bm_list))
    res_list = list(set(res_list))

    total_bm_face_num = 0
    total_res_face_num = 0
    for bm in bm_list:
        bm = bm.strip()
        bm_path, bm_name = os.path.split(bm)
        bNotFound = True

        for res in res_list:
            res = res.strip()
            res_path, res_name = os.path.split(res)
            if res_name != bm_name:
                continue
            cal_detect_ratio(bm, res)
            bNotFound = False
            
        if bNotFound:
            print("WARNNING::No File Match %s"%(bm))
            

if '__main__' == __name__:
    main()
