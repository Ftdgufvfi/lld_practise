// Resource Acquisition is initialization.
// The wrapper class is responsible for managing the resource, and it ensures that the resource is properly released 
//when the wrapper object goes out of scope. This helps prevent memory leaks and other resource management issues.
// more improvement is explicit for no typecasting.


#include <bits/stdc++.h>
using namespace std;
template <typename T>
class uniqueptr {
    private:
    T* res;
    public:

    //Constructor
    uniqueptr(T* a = nullptr): res(a){cout << "Constructor called" << endl;}

    // copy constructor
    uniqueptr(const uniqueptr& other) = delete; // deleted copy constructor

    // move constructor
    uniqueptr(uniqueptr && other)
    {
        if(this != &other)
        {
            if(res != nullptr)
            {
                delete res;
            }
            res = other.res;
            other.res = nullptr;
        }
    }

    // copy assignment operator
    uniqueptr& operator=(uniqueptr& other) = delete; // deleted copy assignment operator

    // move assignment Operator
    uniqueptr& operator=(uniqueptr&& other)
    {
        if(this != &other)
        {
            delete res;
            res = other.res;
            other.res = nullptr;
        }
        return *this;
    }

    T& operator*()
    {
        return *res;
    }

    T* operator->()
    {
        return res;
    }
    T* get()
    {
        return res;
    }

    void reset(T* a = nullptr)
    {
        delete res;
        res = a;
    }

    reset(){

    }
    // destructor
    ~uniqueptr()
    {
        delete res;
    }
};

int main() {
    uniqueptr<int> ptr1(new int(10)); constructoe
    // uniqueptr<int> ptr2(ptr1); // Error: Copy constructor is deleted
    uniqueptr<int> ptr3(std::move(ptr1)); // Move constructor

    uniqueptr<int> ptr4 = ptr1 // Error: Copy assignment is deleted
    uniqueptr<int> ptr5 = std::move(ptr3); // Move assignment

    cout<< *ptr5 << endl; // Output: 10  // impementation of * operator
    //cout<< ptr->func() <<endl; // Output: 10  // impementation of -> operator
}

