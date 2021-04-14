import re


class SwaVanComparable:

    @classmethod
    def equals(cls, compare_with, value) -> bool:
        return compare_with == value

    @classmethod
    def prefix(cls, compare_with: str, value: str) -> bool:
        if not compare_with:
            return False
        return compare_with.startswith(value)

    @classmethod
    def suffix(cls, compare_with: str, value: str) -> bool:
        if not compare_with:
            return False
        return compare_with.endswith(value)

    @classmethod
    def contains(cls, container: list, value: any) -> bool:
        if not container:
            return False
        return value in container

    @classmethod
    def greater_than(cls, compare_with, value) -> bool:
        if not compare_with:
            return False
        return compare_with > value

    @classmethod
    def less_than(cls, compare_with, value) -> bool:
        if not compare_with:
            return False
        return compare_with < value

    @classmethod
    def wild_card(cls, compare_with, wild_expression) -> bool:
        if not compare_with:
            return False
        return True if re.match(wild_expression, compare_with) else False

    @classmethod
    def action(cls, operator: str, compare_with: any, value: any) -> bool:
        if not operator:
            return False
        elif operator.lower() == "equal":
            return cls.equals(compare_with, value)
        elif operator.lower() == "prefix":
            return cls.prefix(compare_with, value)
        elif operator.lower() == "suffix":
            return cls.suffix(compare_with, value)
        elif operator.lower() == "contains":
            return cls.contains(compare_with, value)
        elif operator.lower() == "greater_than":
            return cls.greater_than(compare_with, value)
        elif operator.lower() == "less_than":
            return cls.less_than(compare_with, value)
        elif operator.lower() == "wildcard":
            return cls.wild_card(compare_with, value)
        return False

