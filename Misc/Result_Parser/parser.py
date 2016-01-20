def process(content):
    return_dict = {}
    process_content = [c.strip() for c in content[3:] if c != "\n"]
    for pc in process_content:
        temp, numbers = pc.split(":")
        print temp
        file_name, method = temp.strip().split(" ")
        print file_name, method, numbers

        if file_name in return_dict.keys():


    import pdb
    pdb.set_trace()



content = open("result.txt", "r").readlines()

# find lines with policies
policy_begin = []
last = False
for line_no, line in enumerate(content):
    if line == "\n" and last is True:
        policy_begin.append(line_no-2)
        last = False
    elif line == "\n" and last is not True:
        last = True
    else:
        last = False
        pass

print "The policies are ", [content[lineno].strip() for lineno in policy_begin]

policy_begin.append(len(content))
policy_content = []
for lineno in xrange(len(policy_begin)-1):
    start = policy_begin[lineno]
    end = policy_begin[lineno+1]
    policy_content.append(content[start:end])

for pc in policy_content:
    process(pc)
import pdb
pdb.set_trace()

