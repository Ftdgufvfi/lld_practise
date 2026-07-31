#Here self is passed as an argument to the method bake, which allows the method to access the instance of the class baker. This is a common practice in object-oriented programming, where methods are defined within a class and can operate on the instance's attributes and other methods.

# python allows you to creaate an attribute outside the constructor, but its not a good practice.

# static object in cpp terms means the object whose lifetime is the entire duration of the program. In python, static methods are defined using the @staticmethod decorator and do not require an instance of the class to be called. They can be called on the class itself, rather than on an instance of the class.

# special behaviours in python class definitions.

# __name ( leading double underscore) it triggers name mangling where the interpreter changes the name of the variable in a way that makes it harder to create subclasses that accidentally override the private attributes and methods.
# C++ Actual Access control is enforced by compiler
# but in python, it makes it difficult to access the variable from outside the class, but it is still possible to do so using name mangling. 

# trailing double underscore : no impact in behavior.

# leading and trailing underscore are used for dunder methods __init__, __str__, __len__, etc. which are special methods in python classes that have specific meanings and behaviors.

#Operator overloading in python.

#def __add__(self, other):
    #self.name += other.name

# unlike in cpp bool operator+(Const Vector& other) const {
#     return this->name == other.name
# }  const should be after the function signatature.

class baker:
    bakery_type = "Artisanal"  # class data member / static memeber

    def __init__(self, name):
        self.name = name  # instance data member
        self.ingredients = []  # instance data member
    
    def bake(self, ingredients):
        self.ingredients = ingredients    # attributes
        print(f"Baking with {ingredients}...")

    @staticmethod
    def inventory_manager(baker_instance):
        print(f"Managing inventory for {baker_instance.bakery_type} bakery.")

baker_instance = baker("John's Bakery")
baker_instance.bake("flour, sugar, eggs")