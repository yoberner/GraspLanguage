from edu.yu.compilers.intermediate.symtable.Predefined import Predefined


# FIXME This class was converted with ChatGPT so it was not checked so be aware

class TypeChecker:
    @staticmethod
    def isInteger(type):
        """Check if a type specification is integer."""
        return (type is not None) and (type.baseType() == Predefined.integerType)

    @staticmethod
    def areBothInteger(type1, type2):
        """Check if both type specifications are integer."""
        return TypeChecker.isInteger(type1) and TypeChecker.isInteger(type2)

    @staticmethod
    def isReal(type):
        """Check if a type specification is real."""
        return (type is not None) and (type.baseType() == Predefined.realType)

    @staticmethod
    def isIntegerOrReal(type):
        """Check if a type specification is integer or real."""
        return TypeChecker.isInteger(type) or TypeChecker.isReal(type)

    @staticmethod
    def isAtLeastOneReal(type1, type2):
        """Check if at least one of two type specifications is real."""
        return (TypeChecker.isReal(type1) and TypeChecker.isReal(type2)) or (
                    TypeChecker.isReal(type1) and TypeChecker.isInteger(type2)) or (
                    TypeChecker.isInteger(type1) and TypeChecker.isReal(type2))

    @staticmethod
    def isBoolean(type):
        """Check if a type specification is boolean."""
        return (type is not None) and (type.baseType() == Predefined.booleanType)

    @staticmethod
    def areBothBoolean(type1, type2):
        """Check if both type specifications are boolean."""
        return TypeChecker.isBoolean(type1) and TypeChecker.isBoolean(type2)

    @staticmethod
    def isChar(type):
        """Check if a type specification is char."""
        return (type is not None) and (type.baseType() == Predefined.charType)

    @staticmethod
    def isString(type):
        """Check if a type specification is string."""
        return (type is not None) and (type.baseType() == Predefined.stringType)

    @staticmethod
    def areBothString(type1, type2):
        """Check if both type specifications are string."""
        return TypeChecker.isString(type1) and TypeChecker.isString(type2)

    @staticmethod
    def areAssignmentCompatible(targetType, valueType):
        """Check if two type specifications are assignment compatible."""
        if (targetType is None) or (valueType is None):
            return False

        targetType = targetType.baseType()
        valueType = valueType.baseType()

        compatible = False

        # Identical types.
        if targetType == valueType:
            compatible = True

        # real := integer
        elif TypeChecker.isReal(targetType) and TypeChecker.isInteger(valueType):
            compatible = True

        return compatible

    @staticmethod
    def areComparisonCompatible(type1, type2):
        """Check if two type specifications are comparison compatible."""
        if (type1 is None) or (type2 is None):
            return False

        type1 = type1.baseType()
        type2 = type2.baseType()

        if type1.isPascalString() or type2.isPascalString():
            return False

        if type1.isPascalEnumeration() and type2.isPascalEnumeration():
            if type1 == type2:
                return True

            return False

        form1 = type1.getForm
