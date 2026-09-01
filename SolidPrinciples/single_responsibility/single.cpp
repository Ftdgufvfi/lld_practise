#include <bits/stdc++.h>
using namespace std;

// here baker class is doing two things, baking and checking inventory. This violates the single responsibility principle. We can refactor this code by creating two separate classes, one for baking and another for inventory management. 

// improves maintainability and readability
class baker {
    public:
    void bake(){
        cout << "Baking bread" << endl;
    }
    void inventory(){
        cout << "checking inventory" << endl;
    }
};

class baker_refactored {
    public:
    void bake(){
        cout << "Baking bread" << endl;
    }
};

class inventory_manager {
    public:
    void inventory(){
        cout << "checking inventory" << endl;
    }
};

int main() {
    baker b;
    b.bake();
    b.inventory();

    baker_refactored br;
    br.bake();

    inventory_manager im;
    im.inventory();

}