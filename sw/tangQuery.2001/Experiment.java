/// Plot test
/// By Brygg Ullmer, MIT Media Lab
/// Begun November 1, 2001
///
/// Based on threading template by Ben Fry (fry@media.mit.edu),
/// 4/18/2001, and WinHelp Java Tutorial: AnimatorApplication.java,
/// Arthur van Hoff

import java.util.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.awt.image.*;

import javax.swing.*;
import java.io.*;

///////////////////////////////////////////////////////////
/////////////////  Experiment /////////////////////////
///////////////////////////////////////////////////////////

public class Experiment { // experiment set

/////////////  MEMBERS ///////////////

  BldgDbMgr      dbMgr = null;
  Vector   criteriaSet = null;

  Logger logger = null;

  int experimentNum = -1;
  double expectedScore = .15;
//  double expectedScore = 1.5;

  private int  numCriteria = 0;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  Experiment /////////////////////////////

  public Experiment(BldgDbMgr dbMgr, int experimentNum) {

    this.dbMgr = dbMgr;
    this.experimentNum = experimentNum;

    criteriaSet = new Vector();
  }

//    Criteria lowPrice = new Criteria("listing_price", 1, 0, 1200.);
//    Criteria bigSqft  = new Criteria("sq_foot", 1, 4300, 4300.);


////////////////////  setLogger /////////////////////////////

  public void setLogger(Logger logger) {
    this.logger = logger;
  }

////////////////////  addCriteria /////////////////////////////

  public int getId() {
    return experimentNum;
  }

////////////////////  genCriteriaStr /////////////////////////////

  public String genCriteriaStr() {

    String result = "";

    for (int i=0; i<numCriteria; i++) {

      Criteria crit = (Criteria) criteriaSet.elementAt(i);

      result += crit.dispStr;

      if (i != numCriteria-1) {result += ", ";}
    } 

    return result;
  }

////////////////////  addCriteria /////////////////////////////

  public void addCriteria(Criteria newCriteria) {
    criteriaSet.addElement(newCriteria);
    numCriteria++;
  }

////////////////////  evalByCriteria /////////////////////////////

  public double evalByCriteria(BldgRecord br) {

    double result = 0;

    for (int i=0; i < numCriteria; i++) {

      Criteria crit = (Criteria) criteriaSet.elementAt(i);
      double score = crit.evalByCriteria(br);

      if (score == -1) {return -1;}

      result += score;
    }

    return result;
  }

////////////////////  evalByCriteria /////////////////////////////

  public double evalByCriteria() {

   double normedResults = -1;

   try {

    double cumResults = 0;

    int numResults = dbMgr.numVisQueryResults();
    int count = 0;

    for (int i=0; i<numCriteria; i++) {

      Criteria crit = (Criteria) criteriaSet.elementAt(i);

      Enumeration queryResults = dbMgr.getVisQueryResults();

      for (; queryResults.hasMoreElements(); ) {

        Integer selBldgId = (Integer) queryResults.nextElement();
        BldgRecord br     = dbMgr.getBldgId(selBldgId);

	double score = crit.evalByCriteria(br);

	if (score != -1) {
	  cumResults += score;
	  count++;
	}
      }
    }

    if (numResults != 0 && count != 0) {
//      normedResults = cumResults / (numCriteria * count);
      normedResults = cumResults / (numCriteria * numResults);
      normedResults = Math.floor(1000 * normedResults) / 1000;
    }

    String debugStr = "result: " + normedResults + 
                 // " / cum: " + cumResults);
                  " / count: " + count +
                  " / numRes : " + numResults;

    if (logger != null) {
      logger.logStr(debugStr);
    } else {
      dbg("evalByCriteria problem: logger is null!");
    }

    dbg(debugStr);

   } catch (Exception e) {
     dbg("evalByCriteria exception: " + e.toString());
     e.printStackTrace();
   }
   return normedResults;
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("Experiment." + (dcnt++) + ": " + s);
  } 
}

//// END ////

