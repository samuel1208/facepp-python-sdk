#!/usr/bin/env python2

from facepp import API , File
import sys, os
import getopt
import datetime as dt
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom import minidom

API_KEY = 'f6dc9651b27bce2d54ce01945c1f7b83'
API_SECRET = 'mPl3uedPiLohaMuxSF0DQgEdrZw-cBkz'

facePP = API(API_KEY, API_SECRET)

def usage():
    print('----------------------------------------------------------------')
    print('[[Usage]]:: Get face info by facepp')
    print('\t./%s [Paras]  jpg_path_list'%(sys.argv[0]))
    print('[[Paras]]::')
    print('\t--help/-h : Print usage info')
    print('----------------------------------------------------------------')

def saveRes(xml_path, res):
            ### Save the result
    dateStr=dt.datetime.now().strftime("%G-%m-%d")
    root= ET.Element("facePP_res",    
                     date=dateStr)
    img_width = res['img_width']
    img_height = res['img_height']
    faces = res['face']
    
    for f in faces:
        face_sub = ET.SubElement(root,'face')
        ### write positions
        face_pos = ET.SubElement(face_sub,'position')
        x_c = f['position']['center']['x']*img_width/100
        y_c = f['position']['center']['y']*img_height/100
        width = f['position']['width']*img_width/100
        height = f['position']['height']*img_height/100

        tag_x = ET.SubElement(face_pos,'x')
        tag_x.text = repr(int(round(x_c-width/2)))
        tag_y = ET.SubElement(face_pos,'y')
        tag_y.text = repr(int(round(y_c-height/2)))
        tag_width = ET.SubElement(face_pos,'width')
        tag_width.text = repr(int(round(width)))
        tag_height = ET.SubElement(face_pos,'height')
        tag_height.text = repr(int(round(height)))
        ### write attribute
        attr = f['attribute']
        gender = ET.SubElement(face_sub,'gender')
        gender_val = ET.SubElement(gender,'value')
        gender_val.text = attr['gender']['value']
        gender_con = ET.SubElement(gender,'confidence')
        gender_con.text = repr(attr['gender']['confidence'])

        age = ET.SubElement(face_sub,'age')
        age_val = ET.SubElement(age,'value')
        age_val.text = repr(attr['age']['value'])
        age_range = ET.SubElement(age,'range')
        gender_con.text = repr(attr['age']['range'])
    
    ### Save to file
    xmlStr=ET.tostring(root,encoding='utf-8',method='xml') 
    xmlStr=minidom.parseString(xmlStr).toprettyxml() 
    xmlFile=open(xml_path, 'w')
    xmlFile.write(xmlStr)
    xmlFile.close()
    return


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
        jpg_path_list=args[0]
        if not os.path.exists(jpg_path_list):
            raise
    except:
        print("ERROR::Please input the right 'jpg_path_list' Para")
        return 

    path_file = open(jpg_path_list, 'r')
    path_list = path_file.readlines()
    path_file.close()

    for p in path_list:
        p = p.strip()
        file_name, ext = os.path.splitext(p)
        if ext.upper() not in ['.JPG','.JPEG',
                               '.BMP','.TIFF','.PNG']:
            continue
        try:
            res=facePP.detection.detect(img = File(p))
        except:
            print("ERROR::Processing %s Failed"%(p))

        xml_path = "%s_facepp.xml"%(file_name)    
        saveRes(xml_path, res)

if '__main__' == __name__:
    main()
