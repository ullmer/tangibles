// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow QueryBaseline
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;

//////////////////////////////////////////////////////
/////////////////// Query Baseline /////////////////////
//////////////////////////////////////////////////////

public class QueryBaseline implements DbListener {

//////////////////// members /////////////////////

  String baselineQuery;
  DbThread dbthread = null;

  Vector baselineRecordIds = null;
  Vector incomingBaseline = null;

  Hashtable recId2Location = null;

  boolean incomingBaselineReady = false;

//////////////////// methods /////////////////////

//  public QueryBaseline(DbThread dbthread) 

//  public int getNumRecords()
//  public void establishBaseline(Vector baselineRecordIds)
//  public void determineCellNum(int cellId)

//  public void processResultSet(Statement st, ResultSet rs, int resultID)
//  public void processResultVector(Vector results, String dtype, int resultID)

//  public boolean isDataReady() 
//  public void clearDataReady() 

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// isDataReady ///////////////

  public boolean isDataReady() {
    return incomingBaselineReady;
  }

  public void clearDataReady() {
    incomingBaselineReady = false;
  }

  public int size() {
    return incomingBaseline.size();
  }

///////////// process Result Set ///////////////

  public void processResultSet(Statement st, ResultSet rs, int resultID) {
    dbg("processResultSet is currently unsupported");
    return;
  }

  public void processPuntedQuery(int resultID) {
    dbg("processPuntedQuery is currently unsupported");
    return;
  }

///////////// process Result Vector ///////////////

  public void processResultVector(Vector results, String dtype, int resultID) {
    incomingBaseline = results;
    incomingBaselineReady = true;

    dbg("incoming baseline received");
    dbg("vec length = " + results.size());

    recId2Location = new Hashtable();
    int numResults = results.size();

    int ndtype = -1;

    if (dtype.startsWith("int")) { 
      ndtype = 0;
    } else if (dtype.startsWith("string")) { 
      ndtype = 1;
      dbg("processResultVector: unsupported type (1)!  Aborting.");
      return;
    } else {
      dbg("processResultVector: unsupported type (2)!  Aborting.");
      return;
    }

    for (int i=0; i < numResults; i++) {
      Integer key = (Integer) results.elementAt(i);
      recId2Location.put(key, new Integer(i));
    }

    incomingBaselineReady = true;
  }


///////////// determine Cell Num ///////////////

  public int determineCellNum(int cellId) {

    Integer result = (Integer) recId2Location.get(new Integer(cellId));

    if (result == null) {
      //dbg("determineCellNum: received null result for cellId " + cellId);
      return -1;
    }

    return  result.intValue();
  }

///////////// constructor ///////////////

  public QueryBaseline(DbThread dbthread) {
    this.dbthread = dbthread;
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("QueryBaseline[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
