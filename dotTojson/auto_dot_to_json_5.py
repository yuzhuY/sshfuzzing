from __future__ import with_statement

import json
import re
import time
import os

############################################################
#Author: Yuzhu Yan(TU Delft) Master thesis project

# This script can convert .dot file to .json file
# Only suitable for learnlib generated dot file

# This script must work together with the following files:
#   newlearnresult.dot(The .dot file needs to be converted)
#   data1.txt(Temporary file to save all states)
#   data2.json(Temporary file to save all transitions )
#   final_result.json(Converted .json file)

# To use this script, just use your .dot file to replace newlearnresult.dot,
# then run the script
############################################################




# define find between function
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def write_node():
    writefile = open('data1.txt', 'w')
    # with open("auto_data.dot", "r") as f:
    with open("newlearnresult.dot", "r") as f:

        lines = f.readlines()  # Read to end

        lines = lines[2:26]

        for line in lines:
            if line != 's0 [label="s0"];\n':
                writefile.write(line)
            else:
                break

    writefile.close()
    f.close()


def write_relation():
    # writefile = open('data2.json', 'r+')
    writefile = open('data2.json', 'w')
    # writefile.read()

    # with open("auto_data.dot", "r") as f:
    with open("newlearnresult.dot", "r") as f:
        writefile.write("[")

        # Skips text before the beginning of the interesting block:
        for line in f:
            if line.strip() == 's0 [label="s0"];':  # Or whatever test is needed
                break
                # Reads text until the end of the block:
        for line in f:  # This keeps reading the file
            if line.strip() == '}':
                break
                # print line  # Line is extracted (or block_of_lines.append(line), etc.)
            # print line
            a = (re.match(r's\d\s.label', line))  # use regular expression to filter out unnecessary line
            print a
            if a != None:
                print "pass"
            else:
                c = '{"source":' + find_between(line, "s", " -> ") + ", " + '"target":' + find_between(line, "-> s",
                                                                                                       "[") + ", " + '"l_label":' + '"' + find_between(
                    line, "><tr><td>", "</td><td>/</td><td>") + "/" + find_between(line, "</td><td>/</td><td>",
                                                                                   "</td></tr></table>>]") + '"' + '},' + "\n"

                writefile.write(c)

    writefile.close()
    f.close()

    with open("data2.json", 'rb+') as filehandle:
        filehandle.seek(-2, os.SEEK_END)
        filehandle.truncate()

        filehandle.write("]")



def create_json():
    import json

# handle all the states, transform to json

    with open("data1.txt") as f:
        content = f.readlines()

    list1 = []

    for line in content:
        data1 = {'name': line.strip()}
        list1.append(data1)




    complete_json = {'nodes': list1, 'edges': ''}


# handle all the transition, and append result to edges
    with open('data2.json') as data_file:
        data = json.load(data_file)

    complete_json['edges'] = data

    print json.dumps(complete_json)


    a=json.dumps(complete_json,indent=4, sort_keys=True)
#write the converted json to final_result.json file
    dumpjson = open('final_result.json', 'w')
    with open("final_result.json", "r") as f:
        dumpjson.write(a)





write_node()
write_relation()
create_json()
