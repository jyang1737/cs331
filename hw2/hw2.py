import random

numset = [1,3,6,5]
target = 12
signs = ["+","-","*","/"]

def swap(n1, n2, nums):
    temp = nums[n1]
    nums[n1] = nums[n2]
    nums[n2] = temp

def changeSign(n1, sign, signset):
    signset[n1] = sign

def printEq(nums, signset):
    s = str(nums[0])
    for i in range(1,4):
        s += signset[i-1]
        s += str(nums[i])
    print(s)

def eval(nums, signset):
    final = nums[0]
    for i in range(1,4):
        sign = signset[i-1]
        if (sign == '+'):
            final += nums[i]
        elif (sign == '-'):
            final -= nums[i]
        elif (sign == '*'):
            final *= nums[i]
        else:
            #if there is a divide by 0, make result 0, evaluate rest of equation
            if (nums[i] == 0):
                final = 0
                continue
            final /= nums[i]
    return final

def diff(nums, signset):
    cur = eval(nums, signset)
    return abs(target - cur)

def new(nums):
    random.shuffle(nums)
    signset = []
    for i in range(0,3):
        signset.append(random.choice(['+','-','*','/']))
    
def rrhc(nums, signset, difference):
    current = eval(nums, signset)
    while True:
        tempnums = list(nums)
        for i in range(0,4):
            for j in range(i+1,4):
                tempnums = list(nums)
                swap(i, j, tempnums)
                printEq(tempnums, signset)
                if (diff(tempnums, signset) < difference):
                    break
            else:
                continue
            break
        if (diff(tempnums, signset) < difference):
            nums = list(tempnums)
            difference = diff(nums, signset)
            current = eval(nums, signset)
            if (difference == 0):
                print("number changeD")
                return True
            continue

        tempsigns = list(signset)
        print(str(tempsigns))
        for i in range(0,3):
            for j in range(0,4):
                sign = signs[j]
                tempsigns = list(signset)
                changeSign(i, sign, tempsigns)
                printEq(nums, tempsigns)
                if (diff(nums, signset) < difference):
                    break
            else:
                continue
            break
        if (diff(nums, signset) < difference):
            signset = list(tempsigns)
            difference = diff(nums, signset)
            current = eval(nums, signset)
            if (difference == 0):
                print("sign changedd")
                return True
            continue
        return False

        
        
    
def main():
    nums = random.sample(numset, 4)
    signset = []
    #default set and target already set
    #for i in range(0,100):
        #numset.append(random.randint(0,9))
    for i in range(0,3):
        signset.append(random.choice(['+','-','*','/']))
    #target = random.randint(1000,9999)
    print("Target: " + str(target))
    printEq(nums, signset)
    best = eval(nums, signset)
    print("Evaluated: " + str(best))
    bestdiff = diff(nums, signset)
    print("Difference: " + str(bestdiff))

    if (rrhc(nums, signset, bestdiff)):
        print("Found optimal solution")
        print("Target: " + str(target))
        printEq(nums, signset)
        print("Evaluated: " + str(eval(nums, signset)))
        print("Difference: " + str(diff(nums, signset)))

                      

if '__main__' == __name__:
    main()
