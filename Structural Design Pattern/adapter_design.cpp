#include <bits/stdc++.h>
using namespace std;

class XmlData {
private:
    string data;

public:
    XmlData(string data) {
        this->data = data;
    }

    string getData() {
        return data;
    }
};

class JsonData {
private:
    string data;

public:
    JsonData(string data) {
        this->data = data;
    }

    string getData() {
        return data;
    }
};

class DataConvertor {
protected:
    string data;

public:
    DataConvertor(XmlData data) {
        this->data = data.getData();
    }

    virtual void processData() {
        cout << "Printing data in xml format: " << data << endl;
    }

    virtual ~DataConvertor() = default;
};

class Client {
private:
    DataConvertor* dataConvertor;

public:
    Client(DataConvertor* dataConvertor) {
        this->dataConvertor = dataConvertor;
    }

    void processData() {
        dataConvertor->processData();
    }
};

class Adapter : public DataConvertor {
private:
    JsonData data;

public:
    Adapter(JsonData data)
        : DataConvertor(XmlData("")), data(data) {}

    void processData() override {
        cout << "Printing data in json format: "
             << data.getData() << endl;
    }
};

int main() {
    DataConvertor* jsonData =
        new Adapter(JsonData("{\"name\": \"John\", \"age\": 30}"));

    Client* client1 = new Client(jsonData);
    client1->processData();

    delete client1;
    delete jsonData;

    return 0;
}

// you need to define the data(String) in the constructor initialization rather than body
// because otherwise it wont have empty constructor to call as we already have the constructor defined.
// makes two incompatible interfaces compatible with each other.
// Increases Maintainbility and Scalability.