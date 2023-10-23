// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow DbThread
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;

//////////////////////////////////////////////////////
/////////////////// Dbase Thread /////////////////////
//////////////////////////////////////////////////////

public class DbThread extends Thread {

//////////////////// members /////////////////////

  static final String DBHOST_DEF = "tmg-internal2";
  static final String DBNAME_DEF = "pldb";

  String dbhost, dbname;

  DbFuncs dbhandle = null;

//////////////////// methods /////////////////////

//  public DbThread() 
//  public DbThread(String dburl) 
//  public DbThread(String dbname, String dbhost) 
//  public DbThread(String dbname, String dbhost, 
//                    String dbtype, String dbuser, String dbpasswd) {
//  public void run() 

//  public void submitQuery(String query, DbListener callback, int queryID)
//  public void submitQuery(String query, DbListener callback)

//  public void submitKVQuery(String query, String keyfield, String dtype,
//                             DbListener callback, int queryID = 0) {
//  public void submitKVQuery(String query, String keyfield, String dtype,
//                             DbListener callback) 

     // KV = keyed vector.  Will respond with processResultVector

//  public void submitExec (String exec,  int execID) = 0;

//  public DbFuncs getDbHandle();

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// get Db Handle ///////////////

  public DbFuncs getDbHandle() {
    return dbhandle;
  }

///////////// submit KV Query ///////////////

  public void submitKVQuery(String query, String keyfield, String dtype,
                             DbListener callback, int queryID) {

/*
    if (dbname == null) {
      dbg("Problem in submitKVQuery: dbname == null.  Returning...");
      return;
    }
 */
    if (callback == null) { 
      dbg("Problem in submitKVQuery:  callback == null.  Returning...");
      return;
    }

    Vector result = new Vector();

    try { 
      Statement st = dbhandle.getDbase().createStatement(); 
      ResultSet rs = st.executeQuery(query); 


      // Which kind of data are we to retrieve?
      int    ddtype;

      if        (dtype.compareTo("int") == 0) {
	ddtype = 0;

      } else if (dtype.compareTo("string") == 0) {
	ddtype = 1;

      } else {
	dbg("submitKVQuery called with unsupported dtype: " + dtype);
	dbg("Returning...");
	return;
      }
        
      // Do the query, and build our results vector

      while(rs.next()) { 

	switch (ddtype) {
	  case 0: // int
	    Integer val = new Integer(rs.getInt(keyfield));
	    result.addElement(val);
	    break;

	  case 1: // string
	    String str = rs.getString(keyfield);
	    result.addElement(str);
	    break;

	  default: 
            dbg("Bogus condition in submitKVQuery (1)");
        } 
        
        rs.close(); 
        st.close(); 
        
      } 
    } catch ( SQLException e ) { 
      dbg("submitKVQuery error: " + e.getMessage() + "; returning"); 
      return;
    }
 
    // fire callback

    try {
      callback.processResultVector(result, dtype, queryID);

    } catch (Exception e) {
	dbg("Failure in submitKVQuery callback: " + e.toString()); 
    }
  }

  public void submitKVQuery(String query, String keyfield, String dtype,
                             DbListener callback) {
    submitKVQuery(query, keyfield, dtype, callback, 0);
  }

///////////// submit Query ///////////////

  public void submitQuery(String query, DbListener callback, int queryID) {

/*
    if (dbname == null) {
      dbg("Problem in submitKVQuery: dbname == null.  Returning...");
      return;
    }
 */
    if (query == null) {
      dbg("submitQuery bogosity: query == null!");
      return;
    }

    if (callback == null) { 
      dbg("Problem in submitQuery:  callback == null.  Returning...");
      return;
    }

    Statement st = null;
    ResultSet rs = null;
   
    boolean querySuccessful = false;

    try { 
      st = dbhandle.getDbase().createStatement(); 
      rs = st.executeQuery(query); 

      querySuccessful = true;

      //rs.close(); 
      //st.close(); 
        
    } catch ( SQLException e ) { 
      dbg("submitQuery error: " + e.toString() + "; returning"); 
      dbg(">> query: " + query);
    }
 
    // handle bogosity

    if (querySuccessful == false) {

      try {
        callback.processPuntedQuery(queryID);

      } catch (Exception e) {
  	dbg("Failure in processPuntedQuery callback: " + e.toString()); 
      }
      return;
    }
    

    // fire callback

    try {
      callback.processResultSet(st, rs, queryID);

    } catch (Exception e) {
	dbg("Failure in submitQuery callback: " + e.toString()); 
    }

    // warning: callback is expected to close statement and result set!
  }

  public void submitQuery(String query, DbListener callback) {
    submitQuery(query, callback, 0);
  } 

///////////// constructor ///////////////

  public DbThread(String dbname, String dbhost) {
    super("DbThread");

    this.dbname = dbname;
    this.dbhost = dbhost;

    dbhandle = new DbFuncs(dbname, dbhost);
    dbhandle.connect();

    dbg("started");
  }

  public DbThread(String dbname, String dbhost, 
                    String dbtype, String dbuser, String dbpasswd) {
    super("DbThread");

    this.dbname = dbname;
    this.dbhost = dbhost;

    dbhandle = new DbFuncs(dbname, dbhost);
    dbhandle.dbaseType     = dbtype;
    dbhandle.dbaseUser     = dbuser;
    dbhandle.dbasePassword = dbpasswd;

    dbhandle.connect();

    dbg("started");
  }

  public DbThread(String dburl) {
    super("DbThread");

    dbhandle = new DbFuncs();
    dbhandle.dbaseURL = dburl;
    dbhandle.dbaseType = "mysql"; // THIS IS A HACK

    dbg("warning: DbThread hacked to use mysql...");

    dbhandle.connect();

    dbg("started");
  }

  public DbThread() {
    this(DBNAME_DEF, DBHOST_DEF);
  }

///////////// run ///////////////

  public void run() {
    dbg("running");
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("DbThread[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
