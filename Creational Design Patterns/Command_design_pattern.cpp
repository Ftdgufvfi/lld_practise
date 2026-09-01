#include <bits/stdc++.h>
using namespace std;

class Command {
    virtual void execute() = 0;
    virtual void undo() = 0;
    virtual ~Command() = default;
};

class Light {
    public:
    void turnOn() {
        cout << "Light is ON" << endl;
    }

    void turnOff() {
        cout << "Light is OFF" << endl;
    }
};

class Fan {
    public:
    void turnOn() {
        cout << "Fan is ON" << endl;
    }

    void turnOff() {
        cout << "Fan is OFF" << endl;
    }
};

class LightOnCommand : public Command {
    Light* light;
    public:
    void execute() override {
        light->turnOn();
    }
    void undo() override {
        light->turnOff();
    }
};


class FanOnCommand : public Command {
    Fan* fan;
    public:
    void execute() override {
        fan->turnOn();
    }
    void undo() override {
        fan->turnOff();
    }
};


class RemoteControl {

    private:
    static const int num_buttons = 2;
    Command* buttons[num_buttons];
    bool isOn[num_buttons];
    public:
    RemoteControl() {
        for (int i = 0; i < num_buttons; ++i) {
            buttons[i] = nullptr;
            isOn[i] = false;
        }
    }
    
    void setcommand(int button, Command* command) {
        if (button >= 0 && button < num_buttons) {
            if(buttons[button] != nullptr) {
                delete buttons[button];
            }
            buttons[button] = command;
        }
    }

    void pressButton(int button) {
        if (button >= 0 && button < num_buttons && buttons[button] != nullptr and isOn[button] = true) {
            buttons[button]->execute();
            isOn[button] = !isOn[button];
        }
        else if(button >= 0 && button < num_buttons && buttons[button] != nullptr and isOn[button] = false) {
            buttons[button]->undo();
            isOn[button] = !isOn[button];
        }
    }
};

int main()
{
    Light light;
    Fan fan;

    RemoteControl remote;

    remote.setcommand(0, new LightOnCommand(&light));
    remote.setcommand(1, new FanOnCommand(&fan));

    remote.pressButton(0); // Turns on the light
    remote.pressButton(1); // Turns on the fan

    remote.pressButton(0); // Turns off the light
    remote.pressButton(1); // Turns off the fan

    return 0;
}



//Note destructor must be virtual is base class to avoid memory leak when deleting derived class object using base class pointer.
// loose coupling between invoker and receiver. Invoker doesn't know about the receiver. It only knows about the command interface. This allows for easy addition of new commands without modifying the invoker or receiver classes.
// Here, the invoker (RemoteControl) is decoupled from the receiver (Light and Fan). The invoker only knows about the command interface, allowing for easy addition of new commands without modifying the invoker or receiver classes.

// Improves Scalability and Maintainability.

/*
Simple UML diagram

                                  +-------------------+
                                  |   RemoteControl   |
                                  |     (Invoker)     |
                                  +-------------------+
                                  | - buttons[]       |
                                  | + setcommand()    |
                                  | + pressButton()   |
                                  +---------+---------+
                                                |
                                                | invokes
                                                v
                                  +-------------------+
                                  |      Command      |
                                  |    <<interface>>  |
                                  +-------------------+
                                  | + execute()       |
                                  | + undo()          |
                                  +---------+---------+
                                                ^
                                 implements |
                             +-------------+-------------+
                             |                           |
              +----------+----------+     +----------+----------+
              |   LightOnCommand    |     |    FanOnCommand     |
              +---------------------+     +---------------------+
              | - light: Light*     |     | - fan: Fan*         |
              | + execute()         |     | + execute()         |
              | + undo()            |     | + undo()            |
              +----------+----------+     +----------+----------+
                             |                           |
                             | delegates                 | delegates
                             v                           v
              +---------------------+     +---------------------+
              |        Light        |     |         Fan         |
              |      (Receiver)     |     |      (Receiver)     |
              +---------------------+     +---------------------+
              | + turnOn()          |     | + turnOn()          |
              | + turnOff()         |     | + turnOff()         |
              +---------------------+     +---------------------+

Client: main() creates the receivers and commands, then configures RemoteControl.
*/

// Benefits:
// - Maintainability: each action is isolated in its own command class.
// - Extensibility: new commands can be added without changing RemoteControl.
// - Testability: commands, receivers, and the invoker can be tested independently.
// - Readability: execute() and undo() provide a consistent interface for all actions.
// - Reusability: the same command can be used by different invokers.
// - Loose coupling: RemoteControl does not depend directly on Light or Fan.
// - Supports undo/redo, command history, queuing, scheduling, and logging.


