// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow QueryResult
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;

//////////////////////////////////////////////////////
/////////////////// Query Result /////////////////////
//////////////////////////////////////////////////////

public class QueryResult implements DbListener {

//////////////////// members /////////////////////

  String baselineQuery;
  DbThread dbthread = null;

  Vector baselineRecordIds = null;
  Vector incomingResult = null;

//  Hashtable recId2Location = null;

  boolean incomingResultReady = false;

//////////////////// methods /////////////////////

//  public QueryResult(DbThread dbthread)

//  public int getNumRecords()
//  public void establishResult(Vector baselineRecordIds)
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
    return incomingResultReady;
  }

  public void clearDataReady() {
    incomingResultReady = false;
  }

  public int size() {
    return incomingResult.size();
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

///////////// getIntAt ///////////////

  public int getIntAt(int id) {
    Integer result = (Integer) incomingResult.elementAt(id);
    return result.intValue();
  }

///////////// process Result Vector ///////////////

  public void processResultVector(Vector results, String dtype, int resultID) {
    incomingResult = results;
    incomingResultReady = true;

    dbg("incoming baseline received");
    dbg("vec length = " + results.size());

    //recId2Location = new Hashtable();
    int numResults = results.size();

    int ndtype = -1;

    if (dtype.startsWith("int")) { 
      ndtype = 0;
    } else if (dtype.startsWith("string")) { 
      ndtype = 1;
      return;
    } else {
      dbg("processResultVector: unsupported type (2)!  Aborting.");
      return;
    }

/*
    for (int i=0; i < numResults; i++) {
      Integer key = (Integer) results.elementAt(i);
      recId2Location.put(key, new Integer(i));
    }
*/
    incomingResultReady = true;
  }

///////////// constructor ///////////////

  public QueryResult(DbThread dbthread) {
    this.dbthread = dbthread;
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("QueryResult[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
