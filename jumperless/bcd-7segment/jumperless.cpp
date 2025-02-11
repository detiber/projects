// JUMPERLESS.cpp
#include "jumperless.h"
#include <Array.h>

Jumperless::Jumperless(int baud) {
    Serial.println("Initializing Jumperless UART Connection");
    delay(3500);
    // UART Connection to Jumperless
    Serial1.begin(115200);
    delay(500);

    // Ensure UART Connections are included
    // connections.push_back({"UART_TX", "D0"});
    // connections.push_back({"UART_RX", "D1"});
    connections.push_back({"117", "71"});
    connections.push_back({"116", "70"});
}

void Jumperless::MakeConnections() {
    Serial.print("nodelist: ");
    String nodes = String("f ");

    for (connection connection : connections) {
      nodes.concat(connection.source + "-" + connection.dest + ",");
    }

    Serial.println("nodelist: " + nodes);
    Serial1.write(nodes.c_str());
}

void Jumperless::AddConnection(connection connection) {
    String out = String("Adding connection: " + connection.source+ "-" + connection.dest);
    Serial.println(out);

    connections.push_back(connection);
}

