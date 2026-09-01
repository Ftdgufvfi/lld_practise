// Pass-by-value / reference quick notes:
// 1) C++: arguments are pass-by-value by default. To mutate caller state, pass by reference (&)
//    or pointer (*).
// 2) Java: always pass-by-value. For objects, the value copied is the reference.
// 3) Python: call-by-sharing (object reference is passed). Rebinding is local; mutating a
//    mutable object is visible to caller.

// Nested class quick notes:
// 1) A nested class is a class declared inside another class.
// 2) It helps with logical grouping, readability, and encapsulation.
// 3) Creating an outer object does not automatically create an inner object.

// Access rules by language (important):
// 1) Java:
//    - Non-static inner class is tied to an outer instance and can access outer private members.
//    - Outer class can also access inner private members.
//    - Static nested class has no implicit outer instance.
// 2) C++:
//    - Nested class is mostly a scoped type (no implicit outer object like Java non-static inner).
//    - If needed, friendship can be used for explicit private-member access direction.
// 3) Python:
//    - Mostly namespacing; inner class needs explicit outer object if outer instance data is needed.

// Static vs non-static inner class in Java:
// - Non-static usage:
//     Outer outer = new Outer();
//     Outer.Inner inner = outer.new Inner();
// - Static nested usage:
//     Outer.Inner inner = new Outer.Inner();

// Nested class usage syntax in C++ and Python:
// - C++:
//     Outer::Inner inner = Outer::Inner();
// - Python:
//     outer = Outer()
//     inner = Outer.Inner()  # or use outer reference explicitly if required by design

// Builder pattern note:
// - Useful when constructor overloading becomes difficult because of many parameters.
// - Lets you build an object in a flexible, readable, and maintainable way.

#include <iostream>
#include <string>

using namespace std;

class car {
private:
    string carType;
    string color;
    string num_of_wheels;
    string engineType;

public:
    class carBuilder;

    void printCarDetails() const {
        std::cout << "Car Type: " << carType << std::endl;
        std::cout << "Color: " << color << std::endl;
        std::cout << "Number of Wheels: " << num_of_wheels << std::endl;
        std::cout << "Engine Type: " << engineType << std::endl;
    }

    class carBuilder {
    private:
        friend class car;
        string carType = "Sedan";
        string color = "Red";
        string num_of_wheels = "4";
        string engineType = "V6";

    public:
        carBuilder() {
        }

        carBuilder* setCarType(const string& carType) {
            this->carType = carType;
            return this;
        }

        carBuilder* setColor(const string& color) {
            this->color = color;
            return this;
        }

        carBuilder* setNumOfWheels(const string& num_of_wheels) {
            this->num_of_wheels = num_of_wheels;
            return this;
        }

        carBuilder* setEngineType(const string& engineType) {
            this->engineType = engineType;
            return this;
        }

        car* build() {
            return new car(this);
        }
    };

private:
    car(carBuilder* builder);
};

car::car(carBuilder* builder) {
    this->carType = builder->carType;
    this->color = builder->color;
    this->num_of_wheels = builder->num_of_wheels;
    this->engineType = builder->engineType;
}

int main() {
    car::carBuilder* builder = new car::carBuilder();
    car* myCar = builder->setCarType("SUV")->setColor("Blue")->setNumOfWheels("4")->setEngineType("V8")->build();

    myCar->printCarDetails();
    delete myCar;
    delete builder;
}
