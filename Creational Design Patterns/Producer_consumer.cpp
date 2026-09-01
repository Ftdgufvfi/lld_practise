#include <mutex>
#include <semaphore>
#include <vector>

class event {
public:
    int x;
};

constexpr int n = 10;

std::vector<event*> event_buffer;

std::counting_semaphore<n> empty(n);
std::counting_semaphore<n> full(0);
std::mutex lock;

class Producer {
public:
    void produceEvent(event* x) {
        empty.acquire();
        lock.lock();
        event_buffer.push_back(x);
        lock.unlock();
        full.release();
    }
};

class Consumer {
public:
    event* consumeEvent() {
        full.acquire();
        lock.lock();
        event* x = event_buffer.back();
        event_buffer.pop_back();
        lock.unlock();
        empty.release();
        return x;
    }
};