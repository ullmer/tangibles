// Event interface to DbThread
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

import java.sql.*;
import java.util.*;

public interface DbListener {

  public void processResultSet(Statement st, ResultSet rs, int resultID);
  public void processResultVector(Vector results, String dtype, int resultID);
  public void processPuntedQuery(int resultID);
}

//// END ////

