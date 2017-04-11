import re


def operator_recognizer(expression):
    """
    :param expression: user's entered expression            str
    :return: name of the operator used in the expression    str
    """

    keywords = ["OR", "AND", "IF", "THEN", "NOT"]
    and_regex = r"(\(.*\)) AND (\(.*\))( AND \(.*\))*$"
    or_regex = r"(\(.*\)) OR (\(.*\))( OR \(.*\))*$"
    conditional_regex = r"IF (\(.*\)) THEN (\(.*\))$"

    if re.match(and_regex, expression):
        return "AND"
    elif re.match(or_regex, expression):
        return "OR"
    elif re.match(conditional_regex, expression):
        return "Conditional"
    else:
        flag = True
        for i in keywords:
            if i in expression:
                flag = False
        if flag:
            return "Pure"
        else:
            return "Broken"
