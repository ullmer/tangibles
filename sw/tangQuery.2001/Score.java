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
////////////////////  Score ////////////////////////////
///////////////////////////////////////////////////////////

public class Score {

/////////////  MEMBERS ///////////////

  BldgDbMgr      dbMgr = null;
  Vector   criteriaSet = null;

  private int  numCriteria = 0;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  Score /////////////////////////////

  public Score(BldgDbMgr dbMgr) {

    this.dbMgr = dbMgr;
    criteriaSet = new Vector();
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
      result += crit.evalByCriteria(br);
    }

    return result;
  }

////////////////////  evalByCriteria /////////////////////////////

  public double evalByCriteria() {

    double cumResults = 0;
    int    resultSetSize = dbMgr.numVisQueryResults();

    for (int i=0; i<numCriteria; i++) {

      Criteria crit = (Criteria) criteriaSet.elementAt(i);

      Enumeration queryResults = dbMgr.getVisQueryResults();

      for (; queryResults.hasMoreElements(); ) {

        Integer selBldgId = (Integer) queryResults.nextElement();
        BldgRecord br     = dbMgr.getBldgId(selBldgId);

	cumResults += crit.evalByCriteria(br);
      }
    }

    double normedResults = -1;

    if (resultSetSize != 0) {
      normedResults = cumResults / (numCriteria * resultSetSize);
      normedResults = Math.floor(1000 * normedResults) / 1000;
    }

    return normedResults;
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("Score." + (dcnt++) + ": " + s);
  } 
}

//// END ////

