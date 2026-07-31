#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>

using namespace std;

/*

What is hashing?

Hashing is a process in which we map the keys to a specific index in a data structure.

You can define your own hash function sauch as key % n but it should be designed well to avoid
collisions.

The hash value is calculated using a hash function. The hash function takes an input (or 'key') and returns an integer, which is used as an index in the hash table.

bucket index = hash value = Each index in the array is called a bucket as it is having a bucket of liked list

Rehashing:

Rehashing is used to avoid collisions in a hash table, whenever the size of the hash table is
increased, then size of the hash table is increased to twice and the existing elements are inserted 
into the new hash table using the updated hash function. (Rehashing generally occurs when the load factor is greater than 0.5)

Load factor = Total number of elements/ Total number of buckets


*/

/*
Types of hashing:

1. Division Method: The hash function is key % table_size.
2. Multiplication Method: The hash function is floor(table_size * (key * A % 1)), where 0 < A < 1.
3. Universal Hashing: A random hash function is chosen from a family of hash functions. h(k)=((a * k + b) mod p) mod m 
4. Cryptographic Hashing: Uses cryptographic algorithms like SHA-256.
*/

// Two type of techniques to handle collision in hashing;

/*
one is linear probing = h(k, i) = (h(k) + i) mod m, where i = 0, 1, 2, ..., m-1;
another is chaining = each bucket contains a linked list of elements that hash to the same index;

another technique is quadratic probing = h(k, i) = (h(k) + c1 * i + c2 * i^2) mod m, where c1 and c2 are constants.

Linear probing suffers from primary clustering,

whereas quadratic probing suffers from secondary clustering.

chaining is a better technique to handle collisions in handle.

*/

/*
l value, r value referencing.

U& means returning a reference to a value of type U. This allows you to modify the value directly through the reference.

U&& means returning an rvalue reference to a value of type U. This is typically used for move semantics, allowing you to transfer ownership of resources from one object to another without making a copy.

copy constructor

Example(const Example& other)
{
    // Copy the data from the other object to this object
    this->data = other.data;
}

Example & Operator = (Example & other)
{
    // Copy the data from the other object to this object
    this->data = other.data;
    return *this; // Return a reference to this object
}

Example && Operator = (Example && other)
{
    // Move the data from the other object to this object
    this->data = std::move(other.data);
    return *this; // Return a reference to this object
}

Example A = B; // copy assignement

Example A = std::move(B); // Move assignment

*/

// Implementation of hashmap using Rehashing.

template <typename T, typename U>
struct Node{
    T key;
    U value;
    struct Node<T, U>* next;
};

template <typename T, typename U>
class Hashmap_open_addressing{

    private:

    int max_capacity = 100;

    vector<Node<T, U>*> table = vector<Node<T, U>*>(max_capacity, nullptr);

    int hash_function_universal(T key, int max_capacity) 
    {
        const long long p = 10000019;
        const long long a = 31;
        const long long b = 7;

        if constexpr (is_same_v<T, string>)
        {
            long long hash = b;
            for (char c : key) {
                hash = (hash * a + c) % p;
            }
            return static_cast<int>(hash % max_capacity);
        }

        else if constexpr (is_same_v<T, float>)
        {
            long long hash = b;
            int intPart = static_cast<int>(key);
            float fracPart = key - intPart;

            hash = (hash * a + intPart) % p;
            hash = (hash * a + static_cast<long long>(fracPart * 1000000)) % p; // Scale fractional part

            return static_cast<int>(hash % max_capacity);
        }

        else if constexpr (is_same_v<T, char>)
        {
            long long hash = b;
            hash = (hash * a + static_cast<long long>(key)) % p;
            return static_cast<int>(hash % max_capacity);
        }

        else {
        long long hash = (a * static_cast<long long>(key) + b) % p;

        // Handle negative keys.
        if (hash < 0)
            hash += p;

        return static_cast<int>(hash % max_capacity);
        }
    }

    public :

    U& operator[](T key){

        int index = hash_function_universal(key, max_capacity);
        if(table[index] == NULL){
            table[index] = new Node<T, U>();
            table[index]->key = key;
            table[index]->value = U();  // Initialize the value to the default constructor of U
            table[index]->next = nullptr;
            return table[index]->value;
        }
        if(table[index]->key == key){
            return table[index]->value;
        }
        else{
            // Handle collision using linear probing
            int originalIndex = index;
            do {
                index = (index + 1) % max_capacity;
                if (table[index] == NULL) {
                    table[index] = new Node<T, U>();
                    table[index]->key = key;
                    table[index]->value = U();  // Initialize the value to the default constructor of U
                    return table[index]->value;
                }
                if (table[index]->key == key) {
                    return table[index]->value;
                }
            } while (index != originalIndex);
        }

        // If we reach here, the table is full and the key was not found.
        throw std::overflow_error("Hashmap is full");  // otherwise we can implement rehashing.
    }
    




};

template <typename T, typename U>
class hashmap_chaining{

    private:

    int max_capacity = 100;

    vector<Node<T, U>*> table = vector<Node<T, U>*>(max_capacity, nullptr);

    int hash_function(T key, int max_capacity){
    
    const int factor = 31;
    if constexpr (is_integral_v<T>){
        return (key % max_capacity + (factor*(key % max_capacity))%max_capacity)%max_capacity;
       }
    return 0;
    }

    public :

    U& operator[](T key){

        int index = hash_function(key, max_capacity);

        if(table[index] == NULL){
            table[index] = new Node<T, U>();
            table[index]->key = key;
            table[index]->value = U();  // Initialize the value to the default constructor of U
            table[index]->next = nullptr;
            return table[index]->value;
        }
        else
        {
            Node<T, U>* temp = table[index];
            Node<T, U>* prev = NULL;
            while(temp != NULL)
            {
                if(temp->key == key){
                    return temp->value;
                }
                prev = temp;
                temp = temp->next;
            }

            // If key not found, add a new node at the beginning of the chain
            Node<T, U>* newNode = new Node<T, U>();
            prev->next = newNode;
            newNode->key = key;
            newNode->value = U();  // Initialize the value to the default constructor of U
            newNode->next = NULL;
            return newNode->value;
        }
    }
};

int main()
{
    hashmap_chaining<int, string> map;

    map[1] = "One";
    map[2] = "Two";
    map[3] = "Three";

    cout << "Key: 1, Value: " << map[1] << endl;
    cout << "Key: 2, Value: " << map[2] << endl;
    cout << "Key: 3, Value: " << map[3] << endl;

    return 0;
}
