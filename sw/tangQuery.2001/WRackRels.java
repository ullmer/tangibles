/// Parameter token adjacency relation
/// By Brygg Ullmer, MIT Media Lab
/// Begun October 25, 2001

import java.util.*;
import java.io.*;

///////////////////////////////////////////////////////////
///////////////  PTok adjacency relation //////////////////
///////////////////////////////////////////////////////////


  // NOTE: implementing this quickly, partly as a placeholder
  // Eventually, will need to become a more abstract class, with
  // children to handle the bounds types of different parameters


public class WRackRels {

/////////////  METHODS ///////////////

// public ParamTok()

/////////////  MEMBERS ///////////////

  boolean verbose = true;

  Vector  adjRelsVect = null;
  boolean relsChanged = true;

  WRackModel parentRack = null;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

 ////////////////////  constructor /////////////////////////////

  public WRackRels(WRackModel parentRack) {

    adjRelsVect = new Vector();

    this.parentRack = parentRack;
  }

 //////////////////// genSqlQuery /////////////////////////////

  public String genSqlQuery(String selectStr) {

    Vector adjRels = getAdjRels();

    String query = selectStr;
    boolean firstRelation = true;

    int numRels = adjRels.size();

    if (numRels == 0) {
      //dbg("genSqlQuery weirdness: no relations found!");
      return "";
    }

    PTokAdjRel adjRel = (PTokAdjRel) adjRels.elementAt(0);
    if (adjRel == null) {return null;}

    String substr = adjRel.genSqlSubstring();

    if (substr != null && substr.compareTo("") != 0) {
      firstRelation = false;
      query += " where " + substr;
    }

    if (numRels == 1) { 
      query += ";";
      return query; 
    }

    for (int i=1; i<numRels; i++) {
      adjRel = (PTokAdjRel) adjRels.elementAt(i);
      substr = adjRel.genSqlSubstring();

      if (substr == null || substr.compareTo("") == 0) {
        break;
      }
      
      if (firstRelation) { 
        query += " where " + substr;
      } else { 
        query += " and " + substr;
      } 

//      query += " or " + adjRel.genSqlSubstring(); // DISABLING OR
    }

    query += ";";

dbg("wrackrel: " + query);

    return query;
  }

 //////////////////// genSqlQuery /////////////////////////////

 public Vector getANDResults(BldgDbMgr dbMgr) {

   try {

    Vector adjRels = getAdjRels();
    int numRels = adjRels.size();

    if (numRels == 1) { // the easiest case

      PTokAdjRel adjRel = (PTokAdjRel) adjRels.elementAt(0);
      Vector substrResults = adjRel.getSubstringANDResults(dbMgr);
      return substrResults;
    }

   // OK, here's the code to AND-fold together multiple vectors of results

    boolean firstRelation = true;
    Hashtable resultsHash = new Hashtable();

    int numNNRels = 0;

    for (int i=0; i<numRels; i++) {
      PTokAdjRel adjRel = (PTokAdjRel) adjRels.elementAt(i);
      Vector substrResults = adjRel.getSubstringANDResults(dbMgr);

      if (substrResults == null) {continue;}
      
      if (firstRelation) { 

        int numEls = substrResults.size();
	for (int j=0; j < numEls; j++) {
	  Object key = substrResults.elementAt(j);
	  resultsHash.put(key, new Integer(1));
	}

      } else { 

        int numEls = substrResults.size();
	for (int j=0; j < numEls; j++) {
	  Object key = substrResults.elementAt(j);

	  if (resultsHash.containsKey(key) == false) {continue;}

	  Integer count = (Integer) resultsHash.get(key);
	  Integer ncount = new Integer(count.intValue() + 1);
	  resultsHash.put(key, ncount);
	}
      } 

      numNNRels++;
    }

    // OK, assemble the results

    Vector result = new Vector();
    Enumeration keys = resultsHash.keys();

    for (; keys.hasMoreElements() ;) {
      Object key = keys.nextElement();

      Integer count = (Integer) resultsHash.get(key);

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

 //////////////////// get Adj Rels /////////////////////////////

  public Vector getAdjRels() {

    if (relsChanged) {
      rebuildAdjRels();

      printRels();
      //parentRack.printArray();
    }

    return adjRelsVect;
  }

 //////////////////// get Adj Rels /////////////////////////////

  public void printRels() {

    int size = adjRelsVect.size();
    String result = "printRels: ";

    for (int i=0; i < size; i++) {

      PTokAdjRel adjRel = (PTokAdjRel) adjRelsVect.elementAt(i);

      if (adjRel == null) {break;}

      String strr = adjRel.strRel();

      if (strr == null) {break;}

      result += adjRel.strRel() + " ";
    }

    dbg(result);
  }

 //////////////////// get Adj Rels /////////////////////////////

  public void adjRelsChanged() {

    relsChanged = true;
  }
 
 //////////////////// rebuild Adj Rels /////////////////////////////

  public void rebuildAdjRels() {

    adjRelsVect.clear();

    PTokModel lastTok = null, lastTok2 = null;
    PTokModel currentTok = null;
    PTokAdjRel currentAdjRel = null;

    int numSensingCells = parentRack.getNumSensingCells();

    for (int i=0; i < numSensingCells; i++) {

      currentTok = parentRack.getCellContents(i);

      if (currentTok != null) {

        if (currentAdjRel == null) { // first one
          currentAdjRel = new PTokAdjRel(parentRack);
          currentAdjRel.leftmostCell = i;
	}

	currentAdjRel.adjPTokVect.add(currentTok);
      }
    }

    adjRelsVect.add(currentAdjRel);
    relsChanged = false;

    return;


/* OLD VERSION THAT REALLY DID SOMETHING! :-)  BAU 4/15/02

    for (int i=0; i < numSensingCells; i++) {

      lastTok2   = lastTok;
      lastTok    = currentTok;
      currentTok = parentRack.getCellContents(i);

      if (currentTok != null && lastTok == null && lastTok2 == null) { 
       // start a new rel

        currentAdjRel = new PTokAdjRel(parentRack);
	currentAdjRel.leftmostCell = i;
	currentAdjRel.adjPTokVect.add(currentTok);

      } else if (currentTok == null && lastTok == null && lastTok2 != null) { 
       // finish last rel

        currentAdjRel.rightmostCell = i - 1;
	adjRelsVect.add(currentAdjRel);
	currentAdjRel = null;

      } else if (currentTok != null && lastTok2 != null) { // existing rel

        currentAdjRel.adjPTokVect.add(currentTok);
      }
    }

    if (currentAdjRel != null) { // final rel adjacent to end of rack

      currentAdjRel.rightmostCell = numSensingCells - 1;
      adjRelsVect.add(currentAdjRel);
    }

    relsChanged = false;
*/
  }
  
 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("WRackRels." + (dcnt++) + ": " + s);
  } 
}  

//// END ////

