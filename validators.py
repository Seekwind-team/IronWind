from django.core.exceptions import ValidationError

# checks every number in soft_skills, raises Error if on Number is not in range of min and max
# soft_skills: SoftSkillsArguments Object, containing arguments 
# min: minimal allowed value
# max: maximal allowed value
def soft_skills_validator(soft_skills, max, min):
    soft_skills_str = str(soft_skills).replace(",","")    
    # extracts numbers from soft_skills
    numbers = [int(n) for n in soft_skills_str.split() if n.lstrip('-').isdigit()]

    for n in numbers:
        min_int_val(min, n)
        max_int_val(max, n)
 
# checks if input is an Integer-Type and its value is above cap. If one check fails an ValidationError is raises
# cap: minimal value input is allowed to store
# input: value to check
def min_int_val(cap, input):
    if not isinstance(input, int):
        raise ValidationError("{} not a Number".format(input))

    if input > cap:
        return True
    else:
        raise ValidationError("{} too small.".format(input))

def max_int_val(cap, input):
    if not isinstance(input, int):
        raise ValidationError("{} not a Number".format(input))

    if input < cap:
        return True
    else:
        raise ValidationError("{} too big.".format(input))
