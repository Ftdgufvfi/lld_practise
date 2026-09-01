// class Shape{

//     private:
//     string Type;
//     string a;
//     string b;
//     string c;

//     public:
//     Calculate Area(){

//         printf("Area of %s is %d", Type, Area);

//     }

// };


// above code violates open closed principle, because any new shape would require modifying the Shape class.

// open closed principle means open for extension but closed for modification.

// open closed principle enhances maintainability and reusability.

class Shape{
    public:
    virtual double area() = 0;
};

class Rectangle : public Shape{
    private:
    double length;
    double breadth;

    public:
    Rectangle(double l, double b) : length(l), breadth(b) {}

    double area() override {
        return length * breadth;
    }
};

class Circle : public Shape{
    private:
    double radius;

    public:
    Circle(double r) : radius(r) {}

    double area() override {
        return 3.14159 * radius * radius;
    }
};


// So, the above code is in open closed principle.
// few additional details about open closed principle:
// Here shape is Abstract class and Rectangle and Circle are concrete classes.

// Yes, private virtual functions do exist in C++, and a derived class can override a private virtual function from the base class.
// Access control (private/public) affects who can call the function; virtual affects runtime dispatch and overriding