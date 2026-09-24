from cpu_fan import *

def test_data(test):
    result = []
    for i in range(0,len(test[0])):
        data = {}
        x = test[0][i]
        y = test[1][i]
        data["temp"] = x
        data["cpu"] = y
        data["memberships"] = {}
        dm = data["memberships"] # dm is dictionary too
        dm["temp_membership"] = fuzzify(temperature,x)
        dm["cpu_membership"] = fuzzify(utilization,y)

        data["ruleStrength"] = implementFuzzyRules(fuzzy_rules,dm["temp_membership"],dm["cpu_membership"])
        data["aggregated"] = aggregate_result(speed,data["ruleStrength"])
        data["fanSpeed"] = deffuzify(data["aggregated"])

        result.append(data)
    return result

if __name__ == "__main__":
    temp_test = [30, 55, 75, 95, 20, 50, 80, 90, 70, 100]
    cpu_test = [10, 40, 80, 90, 10, 50, 50, 20, 100, 100]
    test = [temp_test,cpu_test]
    result = test_data(test)
    for i, data in enumerate(result, 1):
        print(f"\nTest Case {i}")
        # print(data)
        print(f"""
        Test Case {i}
        -------------------------
        Temperature      : {data["temp"]}°C
        CPU Utilization  : {data["cpu"]}%
        Fan Speed        : {data["fanSpeed"]:.2f}%
        """)