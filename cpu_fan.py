def triangular(x, tup):
    a,b,c = tup
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        if(a == b): return 1
        return (x-a)/(b-a)
    else:
        if(c == b): return 1
        return (c-x)/(c-b)

def trapezoid(x,tup):
    a,b,c,d = tup
    if x < a or x > d:
        return 0
    elif x <= b:
        if(a == b): return 1
        return (x-a)/(b-a)
    elif x <= c:
        return 1
    else:
        if(c == d): return 1
        return (d-x)/(d-c)
    

def fuzzify(dic, x):
    fuzzify_result = {}
    for k in dic:
        # print(k,dic[k])
        if len(dic[k]) == 3:
            fuzzify_result[k] = triangular(x,dic[k])
        elif len(dic[k]) == 4:
            fuzzify_result[k] = trapezoid(x,dic[k])
    return fuzzify_result

def display(dic):
    for k in dic:
        # ADD THIS DEBUG LINE:
        print(f"Key: {k} | Value: {dic[k]} | Type: {type(dic[k])}")

def implementFuzzyRules(fuzzyRules,input1,input2):
    result = {}
    for t in fuzzyRules:
        if(t[2] not in result): result[t[2]] = 0
        result[t[2]] =  max(min(input1[t[0]],input2[t[1]]),result[t[2]])
    return result

def aggregate_result(speed,speed_res_cap):
    aggregate_membership = []
    for x in range(0,101):
        function_op = 0
        max_res = 0
        for k,v in fuzzify(speed,x).items():
            m = speed_res_cap[k]
            function_op = min(v,m)
            max_res = max(max_res,function_op)
        aggregate_membership.append((x,max_res))
    return aggregate_membership

def deffuzify(lst):
    n = 0
    m = 0
    for x,ux in lst:
        # x = tup[0]
        # ux = tup[1]
        n += x*ux
        m += ux
    if(m == 0): return None
    return n/m

# global parameters
temperature = {"low":0,"normal":0,"high":0,"critical":0}
temperature["low"] = (0, 0, 25, 40)
temperature["normal"] = (30, 50, 70)
temperature["high"] = (60, 80, 95)
temperature["critical"] = (85, 95, 100, 100)

utilization = {"low":0,"medium":0,"high":0}
utilization["low"] = (0, 0, 20, 40)
utilization["medium"] = (25, 50, 70)
utilization["high"] = (60, 80, 100, 100)

speed = {"slow":0,"medium":0,"fast":0,"maximum":0}
speed["slow"] = (0, 0, 25, 35)
speed["medium"] = (25, 50, 70)
speed["fast"] = (60, 75, 90)
speed["maximum"] = (80, 90, 100, 100)

# global fuzzy rules
fuzzy_rules = [
    ("low", "low", "slow"),
    ("low", "medium", "slow"),
    ("low", "high", "medium"),
    ("normal", "low", "slow"),
    ("normal", "medium", "medium"),
    ("normal", "high", "fast"),
    ("high", "low", "medium"),
    ("high", "medium", "fast"),
    ("high", "high", "fast"),
    ("critical", "low", "maximum"),
    ("critical", "medium", "maximum"),
    ("critical", "high", "maximum")
]


if __name__ == "__main__":
    # phase - 1 : input
    x= int(input("enter the temperature: "))
    y = int(input("enter the cpu utilization:"))



    # phase - 2 : define fuzzy sets

    # temperature = {"low":0,"normal":0,"high":0,"critical":0}
    # temperature["low"] = (0, 0, 25, 40)
    # temperature["normal"] = (30, 50, 70)
    # temperature["high"] = (60, 80, 95)
    # temperature["critical"] = (85, 95, 100, 100)

    # utilization = {"low":0,"medium":0,"high":0}
    # utilization["low"] = (0, 0, 20, 40)
    # utilization["medium"] = (25, 50, 70)
    # utilization["high"] = (60, 80, 100, 100)

    # speed = {"slow":0,"medium":0,"fast":0,"maximum":0}
    # speed["slow"] = (0, 0, 25, 35)
    # speed["medium"] = (25, 50, 70)
    # speed["fast"] = (60, 75, 90)
    # speed["maximum"] = (80, 90, 100, 100)


    # phase - 4 : implement fuzzification
    temperature = fuzzify(temperature,x)
    utilization = fuzzify(utilization,y)
    # display(temperature,x)
    # display(utilization,x)
    # print(temperature)
    # print(utilization)


    # phase - 5 : designing the rule base
    # temperature and utilization -> speed  == one tuple
    # fuzzy_rules = [
    # ("low", "low", "slow"),
    # ("low", "medium", "slow"),
    # ("low", "high", "medium"),
    # ("normal", "low", "slow"),
    # ("normal", "medium", "medium"),
    # ("normal", "high", "fast"),
    # ("high", "low", "medium"),
    # ("high", "medium", "fast"),
    # ("high", "high", "fast"),
    # ("critical", "low", "maximum"),
    # ("critical", "medium", "maximum"),
    # ("critical", "high", "maximum")
    # ]

    # phase - 6 : evaluate the rules
    speed_res_cap = implementFuzzyRules(fuzzy_rules,temperature,utilization)

    # phase - 7 : implications -> aggregate rule outputs

    aggregate_res_list = aggregate_result(speed,speed_res_cap)

    # phase - 8 : defuizzication

    ans = deffuzify(aggregate_res_list)
    print(ans)

