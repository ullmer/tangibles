// Interface to DbMgr
// Brygg Ullmer, MIT Media Lab
// Interface sprouted on November 13, 2001

// @author  Brygg Ullmer
// @version v0.1

import java.util.*;

abstract public class DbMgr {

 ////////////// FIELDS ///////////////////////

  Vector    records          = new Vector();

  Hashtable visQueryResults   = new Hashtable();
  Hashtable visQueryRIncoming = null;

  Hashtable prIdHash     = new Hashtable();
  Hashtable prMlsHash    = new Hashtable();

  boolean   recsLoaded   = false;

  boolean   visQueryCompleted    = true;
  boolean   visQueryResultsExist = false;

  DbThread  dbthread;

 //////////////////// METHODS ///////////////////

  abstract public void   loadVals();
  abstract public Vector getAllRecs();
  abstract public Vector getRecsInRange(String field, 
                              float minVal, float maxVal, float upperThresh);

  abstract public Vector getRecsDiscrete(String field, String val, 
                                         boolean boolParam);

  abstract public boolean visResultsContainEl(int id);

  abstract public Enumeration getVisQueryResults();
  abstract public void submitVisQuery(String visQuery);

  abstract public boolean isVisQueryCompleted();
  abstract public boolean doVisQueryResultsExist();

  public int   numVisQueryResults() {return visQueryResults.size();}
}

//// END ////

