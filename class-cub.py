import json
import re
import urllib3

HTTP = urllib3.PoolManager()
DEPT_FILTER = 'EL ENG'
# TODO arg parsing

def main():
    with open('request.json', 'r') as req_input:
        req = HTTP.request(
            'POST', 
            'https://berkeleytime.com/api/graphql', 
            body=json.dumps(json.load(req_input)), 
            headers={'Content-Type': 'application/json'}
        )

    resp_obj = json.loads(req.data.decode('utf-8'))
    resp_obj = resp_obj['data']['allCourses']['edges']
    resp_obj = [node for node in resp_obj if node['node']['abbreviation'] == DEPT_FILTER]
    for node in resp_obj:
        node['node']['prerequisites'] = filter_prereqs(node['node']['prerequisites'])


    with open('response.json', 'w') as resp_output:
        resp_output.write(json.dumps(resp_obj, indent=4))


def filter_prereqs(prereq_str):
    matches = re.findall(r'([A-Z]+[A-Za-z ]* [0-9]+[A-Z]*)', prereq_str)
    return matches if matches else []

if __name__ == "__main__":
    main()
