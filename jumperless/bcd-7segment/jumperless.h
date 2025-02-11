// jumperless.h
#ifndef JUMPERLESS_h
#define JUMPERLESS_h

#include <Arduino.h>
#include <Array.h>

const int CONNECTIONS_MAX_COUNT = 100;

struct connection {
  String source;
  String dest;
};

class Jumperless {
  public:
    Jumperless(int baud);
    void AddConnection(connection connection);
    void MakeConnections();
  private:
    Array<connection,CONNECTIONS_MAX_COUNT> connections;
};

#endif