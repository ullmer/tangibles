// Event interface to DbThread
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

import java.sql.*;
import java.util.*;

public interface SerialPListener {

  public void processPacket(int packetSource, int packetData[], int packetSize);
}

//// END ////

