/// Parameter token adjacency relation
/// By Brygg Ullmer, MIT Media Lab
/// Begun October 25, 2001

import java.util.*;
import java.awt.*;
import java.io.*;

///////////////////////////////////////////////////////////
///////////////  PTok adjacency relation //////////////////
///////////////////////////////////////////////////////////


  // NOTE: implementing this quickly, partly as a placeholder
  // Eventually, will need to become a more abstract class, with
  // children to handle the bounds types of different parameters


public class PTokAdjRel {

/////////////  METHODS ///////////////

// public ParamTok()

/////////////  MEMBERS ///////////////

  boolean verbose = true;

  Vector adjPTokVect = null;
  WRackModel parentRack = null;

  int leftmostCell   = -1;
  int rightmostCell  = -1;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

 ////////////////////  constructor /////////////////////////////

  public PTokAdjRel(WRackModel parentRack) {

    adjPTokVect = new Vector();
    this.parentRack = parentRack;
  }
  
 ////////////////  size /////////////

  public int size() {

    return adjPTokVect.size();
  }

 ////////////////  genSqlSubstring /////////////

  public String genSqlSubstring() {

    boolean firstRelation = true;
    String result = "";

    int numEls = size();

    if (numEls == 0) { 
      dbg("genSqlSubstring strangeness: no elements found!");
      return "";
    }

    PTokModel ptok = (PTokModel) adjPTokVect.elementAt(0);

    String sql = ptok.genSqlSubstring();

    if (numEls == 1) { // if it's just a single element...
      return sql;
    } 

    if (sql != null && sql.compareTo("") != 0) {

       result = "(" + sql;
       firstRelation = false;
    } 

    for (int i=1; i<numEls; i++) {

      ptok = (PTokModel) adjPTokVect.elementAt(i);
      sql = ptok.genSqlSubstring();

      if (sql == null || sql.compareTo("") == 0) {
        break;
      } 

      if (firstRelation) {
        result += "(";
	firstRelation = false;
      } else {
        result += " and ";
      }

      result += sql;
    }

    if (firstRelation) {
      return ""; // no content
    }

    result += ")";

    return result;
  }

 ////////////////  convert Relation to string /////////////

   // directly generate AND results for this AdjRel

  public Vector getSubstringANDResults(BldgDbMgr dbMgr) {

   try {

    boolean firstRelation = true;

    int numRels = size();

    Hashtable resultHash = new Hashtable();

    int numNNRels = 0; // number non-null relations

    for (int i=0; i<numRels; i++) {
      PTokModel ptok = (PTokModel) adjPTokVect.elementAt(i);
      if (ptok == null) {continue;}

      Vector fieldResults = ptok.getResults(dbMgr);
      if (fieldResults == null) {continue;}

      if (firstRelation) {
	firstRelation = false;
        int numEls = fieldResults.size();

	for (int j=0; j<numEls; j++) {

	  Object key= fieldResults.elementAt(j);
	  resultHash.put(key, new Integer(1));
	}

      } else { // not first time through

        int numEls = fieldResults.size();

	for (int j=0; j<numEls; j++) {

	  Object key= fieldResults.elementAt(j);

	  if (resultHash.containsKey(key)) {
	    Integer val = (Integer) resultHash.get(key);
	    Integer nval = new Integer(val.intValue() + 1);
	    resultHash.put(key, nval);
	  }
	}
      }

      numNNRels++; // number non-null relations
    }

    Vector result = new Vector();
    Enumeration keys = resultHash.keys();

    for (; keys.hasMoreElements() ;) {
      Object key = keys.nextElement();

      Integer count = (Integer) resultHash.get(key);

      if (count != null && count.intValue() == numNNRels) {
        result.addElement(key);
      }
    }

    return result;
   } catch (Exception e) {
     dbg("genSubstringANDResults exception: " + e.toString());
     e.printStackTrace();
   }

   return null;
 }

 ////////////////  convert Relation to string /////////////

  public String strRel() {

   try {
    int size = adjPTokVect.size();
    String result = "(";

    for (int i=0; i < size; i++) {
      PTokModel ptok = (PTokModel) adjPTokVect.elementAt(i);

      if (ptok == null) {
        dbg("problem in strRel: ptok is null!");
      } else {

        if (result.length() != 1) {result += " ";}
        result += ptok.paramName;
      }
    }
    result += ")";

    return result;
   } catch (Exception e) {
     dbg("strRel exception: " + e.toString());
     e.printStackTrace();
   }
   return null;
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("PTokAdjRel." + (dcnt++) + ": " + s);
  } 
}  

//// END ////

