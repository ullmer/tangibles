// Event interface to DbThread
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

import java.sql.*;
import java.util.*;

public interface SerialRPListener { // for reed relay

  public void processRPacket(int packetData[], int packetSize);
}

//// END ////

