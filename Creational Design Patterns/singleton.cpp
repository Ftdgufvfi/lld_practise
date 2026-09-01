#include <mutex>

std::mutex M;

class Singleton {
private:
    Singleton() = default;

    static Singleton* instance;

public:
    static Singleton* getInstance() {
        std::lock_guard<std::mutex> lock(M);
        if (instance == nullptr) {
            instance = new Singleton();
        }
        return instance;
    }
};

Singleton* Singleton::instance = nullptr;

int main() {
    Singleton* first = Singleton::getInstance();
    Singleton* second = Singleton::getInstance();

    return first == second ? 0 : 1;
}