import argparse
from bs4 import BeautifulSoup as b
import json
import argparse
import os
import os.path as osp
import requests
import hashlib



def get_url_content(url, cache_dir):
    #cache_dir = osp.join(osp.dirname(__file__), 'cache')
    fname = hashlib.sha1(url.encode('utf-8')).hexdigest()
    full_fname = osp.join(cache_dir, fname)

    #print(full_fname)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)



    contents = None
    if (osp.exists(full_fname)):
        print("Loading from cache")
        contents = open(full_fname, 'r').read()
    else:
        print("Loading from source")
        r = requests.get(url)
        contents = r.text
        
        #     fh.write(contents)
        f = open(full_fname, 'w')
        f.write(contents)

    return full_fname


def find_candidate(candidate, person_url):
    relationships = []
    for links in candidate:
        if 'href' not in links.attrs:
            continue
        href = links['href']
        if(href.startswith('/dating') and href != person_url):
            x = ""
            for i, v in enumerate(href): 
                if (i < 8):
                    continue
                else:
                    x +=v
            #print(x)
            relationships.append(x)
            #relationships.append(href)
    return relationships

def extract_relationships(cache, url,person_url):
    """
    Extract all the relationships of the mensioned celev
    """
    relationships = []
    new_url = "https://www.whosdatedwho.com/dating/"+url
    filename = get_url_content(new_url,cache)
    soup = b(open(filename, 'r'), 'html.parser')

    ##grab the h4 class
    status_h4 = soup.find('h4', 'ff-auto-status') #always the tag type
    
    #grab the net sibling
    key_div = status_h4.next_sibling

    candidate = key_div.find_all('a')
    
    #we need all that start with dating
    relationships.extend(find_candidate(candidate, person_url))

    ##get all prior relationships
    prev_h4 = soup.find('h4', 'ff-auto-relationships')

    div_past_relationships = prev_h4.next_sibling
    while div_past_relationships is not None and div_past_relationships.name=='p':
        candidate = div_past_relationships.find_all('a')
        relationships.extend(find_candidate(candidate, person_url))
        div_past_relationships= div_past_relationships.next_sibling

    return relationships

def relationships_output(cache_dir, input_dicts):

    mydict = input_dicts

    x = input_dicts
    new_dict = {}
    for i in range(len(x)):
        new_dict[x[i]] = extract_relationships(cache_dir, x[i], '/dating/'+x[i])

    return new_dict

def main():

    ##parser = argparse.ArgumentParser()
    # parser.add_argument("-c","--directory")
    # parser.add_argument('pagenumber')

    #args = parser.parse_args()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configfile")
    parser.add_argument("-o", "--outputfile")

    args = parser.parse_args()

    configfile = args.configfile
    outputfile= args.outputfile
    args = parser.parse_args()

    with open (configfile, "r") as f:
        line_per_json_file = f.readline()
        jsonfile = json.loads(line_per_json_file)


    cache_dir = jsonfile["cache"]
    target_audience = jsonfile["target_audience"]
    #print(handsomefile)
    #relationships = extract_relationships(args.config-file, '/dating/jennifer-aniston')
    #relationships_output()
    f = open(outputfile, "w")
    f.write(json.dumps(relationships_output(cache_dir, target_audience)))


if __name__ == '__main__':
    main()