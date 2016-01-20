def process(content):
    return_dict = {}
    process_content = [c.strip() for c in content[3:] if c != "\n"]
    for pc in process_content:
        temp, numbers = pc.split(":")
        file_name, method = temp.strip().split(" ")

        if file_name in return_dict.keys():
            return_dict[file_name][method] = numbers.strip()
        else:
            return_dict[file_name]={}
            return_dict[file_name][method] = numbers.strip()

    return return_dict


def all_results_for_a_model(dict, key_name):
    results = []
    assert(key_name in dict.keys() is not True), "Something is wrong!"
    sampling_policies = dict[key_name].keys()
    for sampling_policy in sampling_policies:
        methods = dict[key_name][sampling_policy].keys()
        for method in methods:
            results.append(sampling_policy + "," + method + "," + dict[key_name][sampling_policy][method].replace("[","").replace("]", "") + "\n")
    results.append("\n\n")
    return "".join(results)


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

policy_names = [content[lineno].strip() for lineno in policy_begin]

policy_begin.append(len(content))
policy_content = []
for lineno in xrange(len(policy_begin)-1):
    start = policy_begin[lineno]
    end = policy_begin[lineno+1]
    policy_content.append(content[start:end])

results = {}
for names, pc in zip(policy_names, policy_content):
    temp = process(pc)
    for key in temp.keys():
        if key in results.keys():results[key][names] = {}
        else:
            results[key] = {}
            results[key][names] = {}
        results[key][names].update(temp[key])


models = results.keys()
output = ""
for model in models:
    output += model + "\n\n"
    output += all_results_for_a_model(results, model)

open("modified_result.txt", "w").write(output)




