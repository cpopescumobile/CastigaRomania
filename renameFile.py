import os
import sys

# rename first file with extension .mp4, with the name received as argv[1]
# also put the original file name into a file for reference

if len(sys.argv) <= 1:
    print ('Please specify the new name for the .mp4 file')
    exit()

# iterate over files in current directory
for filename in os.listdir(os.getcwdb()):
    f = os.path.join(os.getcwdb(), filename)
    newF = os.path.join(os.getcwdb(), sys.argv[1].encode('UTF-8'))
    
    titleFileName = sys.argv[1] + ".Title.txt"
    
    # checking if it is a file
    if os.path.isfile(f):
        split_tup = os.path.splitext(filename)
        if len(split_tup) >= 2:
            if str(split_tup[1].decode('UTF-8')) == ".mp4":
                os.rename(f, newF)
                print (f)
                print (sys.argv[1])
                print ("renamed")
                
                originalFileName = split_tup[0].decode('UTF-8', 'ignore')
                
                print (originalFileName)
           
                # put the original file name into a file
                with open(titleFileName, 'a', encoding="utf-8") as the_file:
                    the_file.write(originalFileName)
                exit()


        
