import re

knowledge_dict = dict()


class Expression:

    def __init__(self, expression):
        self.expression = expression
        self.keywords = ["OR", "AND", "IF", "THEN", "NOT"]
        self.and_regex = r"(\(.*\)) AND (\(.*\))( AND \(.*\))*$"
        self.or_regex = r"(\(.*\)) OR (\(.*\))( OR \(.*\))*$"
        self.conditional_regex = r"IF (\(.*\)) THEN (\(.*\))$"

    def operator_recognizer(self):

        keywords = ["OR", "AND", "IF", "THEN", "NOT"]
        and_regex = r"(\(.*\)) AND (\(.*\))( AND \(.*\))*$"
        or_regex = r"(\(.*\)) OR (\(.*\))( OR \(.*\))*$"
        conditional_regex = r"IF (\(.*\)) THEN (\(.*\))$"

        if re.match(and_regex, self.expression):
            return "AND"
        elif re.match(or_regex, self.expression):
            return "OR"
        elif re.match(conditional_regex, self.expression):
            return "Conditional"
        else:
            flag = True
            for i in keywords:
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
            return parsed_expression

        elif self.operator_recognizer() == "OR":
            parsed_expression = self.expression.split(" OR ")
            for i in parsed_expression:
                if "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    i = i[:-1]
                    parsed_expression[list_index] = i
            return parsed_expression
        elif self.operator_recognizer() == "Conditional":
            conditional_matched = re.match(self.or_regex, self.expression)
            parsed_expression = {"IF": conditional_matched.group(1),
                                 "THEN": conditional_matched.group(2)}
            return parsed_expression

    def is_pure_proposition(self):
        for i in self.expression_parser():
            new_expression = Expression(i)
            if new_expression.operator_recognizer() != "Pure":
                return False
        return True

    def resolver(self, knowledge_dict):
        if self.operator_recognizer() == "AND":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if expression not in knowledge_dict:
                    knowledge_dict[expression] = None
            for expression in parsed_expression:
                if knowledge_dict[expression] is None:
                    return None
            for expression in parsed_expression:
                if knowledge_dict[expression]:
                    return True
            return False
        elif self.operator_recognizer() == "OR":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if expression not in knowledge_dict:
                    knowledge_dict[expression] = None
            # count to check if all elements are false
            count = True
            for expression in parsed_expression:
                if knowledge_dict[expression] is True:
                    return True
                if knowledge_dict[expression] is False:
                    count += 1
            if count == len(parsed_expression):
                return False
            else:
                return None



    # def or_resolver(self, knowledge_dict):
    #     parsed_expression = self.expression_parser()
    #     for expression in parsed_expression:
    #         if expression not in knowledge_dict:
    #             knowledge_dict[expression] = None
    #     for expression in parsed_expression:
    #         if knowledge_dict[expression] is None:
    #             return None
    #     for expression in parsed_expression:
    #         if knowledge_dict[expression]:
    #             return True
    #     return False
    #
    # def and_resolver(self, knowledge_dict):
    #     parsed_expression = self.expression_parser()
    #     for expression in parsed_expression:
    #         if expression not in knowledge_dict:
    #             knowledge_dict[expression] = None
    #     for expression in parsed_expression:
    #         if expression is True:
    #             return True
    #     return False


def interpreter(expression):
    expression_object = Expression(expression)
    if expression_object.operator_recognizer() == "Pure":
        knowledge_dict[expression] = True
    elif expression_object.is_pure_proposition():
        knowledge_dict[expression] = expression_object.resolver(knowledge_dict)
    else:
        parsed_expression = expression_object.expression_parser()
        # if expression not in knowledge_dict:
        #     knowledge_dict[expression] = None
        for i in parsed_expression:
            if i not in knowledge_dict:
                knowledge_dict[i] == None
        knowledge_dict[expression] = expression_object.resolver(knowledge_dict)
        for i in parsed_expression:
            temp_expression_object = Expression(i)
            expression_type = temp_expression_object.operator_recognizer()
            if expression_type != "Pure" and expression_type != "Broken":
                interpreter(i)

interpreter("(I study)")


interpreter("(I go to school) OR ((I play football) OR ((I Dance)) OR (I study))")

print(knowledge_dict)