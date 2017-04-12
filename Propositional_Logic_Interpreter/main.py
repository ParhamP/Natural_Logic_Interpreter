import re

knowledge_dict = dict()



class Expression:

    def __init__(self, expression):
        self.expression = expression
        self.keywords = ["OR", "AND", "IF", "THEN", "NOT"]
        self.and_regex = r"(\(.*\)) AND (\(.*\))( AND \(.*\))*$"
        self.or_regex = r"(\(.*\)) OR (\(.*\))( OR \(.*\))*$"
        self.conditional_regex = r"IF (\(.*\)) THEN (\(.*\))$"

    def get(self):
        return self.expression

    def set(self, new_expression):
        self.expression = new_expression

    def __eq__(self, other):
        return self.get() == other.get()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.expression)

    def __str__(self):
        return self.expression

    def operator_recognizer(self):

        if re.match(self.or_regex, self.expression):
            return "OR"
        elif re.match(self.and_regex, self.expression):
            return "AND"
        elif re.match(self.conditional_regex, self.expression):
            return "Conditional"
        else:
            flag = True
            for i in self.keywords:
                if i in self.expression:
                    flag = False
                    break
            if flag:
                return "Pure"
            else:
                return "Broken"

    def expression_parser(self):
        if self.operator_recognizer() == "AND":
            parsed_expression = self.expression.split(" AND ")

            for i in parsed_expression:
                if "))" in i and "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:-1]
                    parsed_expression[list_index] = i
                elif "((" in i:
                    list_index = parsed_expression.index(i)
                    double_paren_index = i.index("((")
                    i = i[:double_paren_index] + i[double_paren_index + 1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    double_paren_index = i.index("))")
                    i = i[:double_paren_index + 1] + i[double_paren_index + 2:]
                    parsed_expression[list_index] = i
            parsed_expression_list = []
            for i in parsed_expression:
                new_expression_object = Expression(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list

        elif self.operator_recognizer() == "OR":
            parsed_expression = self.expression.split(" OR ")
            for i in parsed_expression:
                if "))" in i and "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:-1]
                    parsed_expression[list_index] = i
                elif "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    i = i[:-1]
                    parsed_expression[list_index] = i
            parsed_expression_list = []
            for i in parsed_expression:
                new_expression_object = Expression(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list
        elif self.operator_recognizer() == "Conditional":
            conditional_matched = re.match(self.or_regex, self.expression)
            parsed_expression = {"IF": conditional_matched.group(1),
                                 "THEN": conditional_matched.group(2)}
            return parsed_expression

    def is_pure_proposition(self):
        for i in self.expression_parser():
            if i.operator_recognizer() != "Pure":
                return False
        return True

    def resolver(self, knowledge_dict):
        if self.operator_recognizer() == "AND":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                knowledge_dict[expression] = True
            return True

        elif self.operator_recognizer() == "OR":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if expression not in knowledge_dict:
                    knowledge_dict[expression] = None
            print(parsed_expression)
            # count to check if all elements are false
            count = 0
            for expression in parsed_expression:
                if knowledge_dict[expression] is True:
                    return True
                if knowledge_dict[expression] is False:
                    count += 1
            if count == len(parsed_expression):
                return False
            else:
                return None

    def AND_resolver(self, knowledge_dict):
        parsed_expression = self.expression_parser()
        for expression in parsed_expression:
            if expression not in knowledge_dict:
                knowledge_dict[expression] = None
        for expression in parsed_expression:
            if knowledge_dict[expression] is None:
                return None
            if knowledge_dict[expression] is False:
                return False
            else:
                return True

    def and_in_or_checker(self, or_expression_object):
        """
        :param or_expression_object: 
        :return: 
        """

        if self.operator_recognizer() == "AND" and or_expression_object.operator_recognizer() == "OR":
            return True
        else:
            return None

    def and_temp_transform(self):
        return self.expression + "@"


# def is_in_dict(expression, knowledge_dict):
#     for object in knowledge_dict:
#         temp_object = Expression(expression)
#         if temp_object in knowledge_dict:
#             return True
#     return False


def interpreter(expression):

    # Let's check to see if we have an AND operator that was part of an AND
    flag = False
    if expression[-1] == "@":
        flag = True
        # Flag has become True and we can normalize the expression again
        expression = expression[0:-1]

    expression_object = Expression(expression)

    if expression_object.operator_recognizer() == "Pure":
        knowledge_dict[expression_object] = True

    elif expression_object.is_pure_proposition():
        if flag:
            knowledge_dict[expression_object] = expression_object.AND_resolver(
                knowledge_dict)
        else:
            knowledge_dict[expression_object] = expression_object.resolver(knowledge_dict)

    else:
        parsed_expression = expression_object.expression_parser()

        if flag:
            knowledge_dict[expression_object] = expression_object.AND_resolver(
                knowledge_dict)
        else:
            knowledge_dict[expression_object] = expression_object.resolver(knowledge_dict)

        for i in parsed_expression:
            # temp_expression_object = Expression(i)
            expression_type = i.operator_recognizer()

            # Check to see if an AND proposition was par of an OR proposition
            if i.and_in_or_checker(expression_object):
                i.and_temp_transform()

            if expression_type != "Pure" and expression_type != "Broken":
                interpreter(i.expression)


interpreter("(I Think) AND ((I Guess) OR (I play))")

interpreter("(I play)")

interpreter("(I go to school) OR ((I Think) AND (I play))")

interpreter("(I Think) AND ((I Guess) OR (I play))")

interpreter("(I play)")

interpreter("(I go to school) OR ((I Think) AND (I play))")


print(knowledge_dict)

for i,j in enumerate(knowledge_dict):
    print(i, "---->", j, "--->", knowledge_dict[j])