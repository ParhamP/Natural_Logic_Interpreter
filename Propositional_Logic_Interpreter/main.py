import re


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


knowledge_dict = dict()

def interpreter(expression):
    expression_object = Expression(expression)
    parsed_object = expression_object.expression_parser()
