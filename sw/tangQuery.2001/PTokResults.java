/// Parameter token results
/// By Brygg Ullmer, MIT Media Lab
/// Begun Novebmer 2, 2001

import java.util.*;
import java.awt.*;
import java.io.*;

///////////////////////////////////////////////////////////
///////////////  Parameter tok results ////////////////////
///////////////////////////////////////////////////////////

public class PTokResults {

/////////////  METHODS ///////////////

// public PTokResults()

/////////////  MEMBERS ///////////////

  boolean verbose = true;

  PTokModel ptokModel;
  int bitFlag; // bit flag associated with this token 

  double lowerBound = -1;
  double upperBound = -1;

  char dataType;

  private Vector    currentRecs = null;
  private Hashtable recHash     = new Hashtable();

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  constructor /////////////////////////////

  public PTokResults (char whichDataType) {
    dataType = whichDataType;
  }

////////////////////  setRecs /////////////////////////////

  public void setRecs(Vector newrecs) { 

    try {
  
      currentRecs = newrecs;
  
      if (currentRecs == null) {return;}
  
      int numEls = currentRecs.size();
      recHash.clear();

      switch (dataType) {

        case 'b': 
  
          for (int i=0; i < numEls; i++) {
            // DataRecord el = (DataRecord)...

            BldgRecord el = (BldgRecord) currentRecs.elementAt(i);
            Integer key = new Integer(el.bldg_id);
  
            recHash.put(key, el);
          }

 	  break;

        case 'm': 
  
          for (int i=0; i < numEls; i++) {
            // DataRecord el = (DataRecord)...

//            MutualRecord el = (MutualRecord) currentRecs.elementAt(i);
//            Integer key = new Integer(el.fund_id);
//            recHash.put(key, el);
          }

 	  break;
      }
    } catch (Exception e) {dbg("setRecs exception: " + e.toString());}
  }
  
 ////////////////////  getRecs /////////////////////////////

  public Vector getRecs() { 

    return currentRecs;
  }

 /////////////////  containsBldgId -> //////////////////  
 ////////////////////  containsKey    //////////////////  

  public boolean containsKey(int id) { 

    Integer key = new Integer(id);

    if (recHash.containsKey(key)) {
      return true;
    }

    return false;
  }
 
 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("PTokResults." + (dcnt++) + ": " + s);
  } 
}  

//// END ////


