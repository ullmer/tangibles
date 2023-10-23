/// Tile database functions (SQL wrappers)
// Conversion of stp_funcs.tcl 
// Conversion begun August 2, 2000
//
// @author Brygg Ullmer
// @version v0.5

import java.io.*;
import java.sql.*;
import java.util.*;

//////////////////////////////////////////////////
/////////// CLASS Tile data base functions ///////
//////////////////////////////////////////////////

public class DbFuncs {

//// methods ////

//  public DbFuncs ()
//  public DbFuncs(String dbaseName)
//  public DbFuncs(String dbaseName, String dbaseHost)

//  public Connection getDbase();

//  public void connect()                  //Connect to database
//  public int exec(String command)        //returns result
//  public String buildList(Vector values, boolean quote) 
//  public String buildInsertion(String table, 
//       Vector fields, Vector values, Vector noquote)

//  public int findLastInstance(String table, String queryField, 
//       String queryVal, String keyfield, boolean quoteVal) 

//  public void dbg(String s);

//// fields ////

  public String dbaseName;
  public String dbaseHost = "strata.media.mit.edu";

  public String dbaseType     = "postgresql";
  public String dbaseUser     = "nsadmin";
  public String dbasePassword = "snarf-it";

  public String driverName = "org.postgresql.Driver";

  //public String pgsqlDriverName = "org.postgresql.Driver";
  //public String mysqlDriverName = "org.gjt.mm.mysql.Driver";
  //String driverName = "symantec.itools.db.jdbc.Driver";

  public String dbaseURL;
  Connection dbase;

////////////////////////////////////////////////////
/////////////////// BODIES /////////////////////////
////////////////////////////////////////////////////
 
///////////////////// Constructors /////////////////
 
  public DbFuncs () {}

  public DbFuncs(String dbaseName) {
    this();
    this.dbaseName = dbaseName;
  }

  public DbFuncs(String dbaseName, String dbaseHost) {
    this(dbaseName);
    this.dbaseHost = dbaseHost;
  }

////////////////////// Connect, getDbase /////////////////////

  public void connect() {

    if (dbaseName == null && dbaseURL == null) {
      throw new IllegalArgumentException("dbaseName is null");
    }

    //Register PostgreSQL with system

    Properties systemProperties = System.getProperties();

    if (dbaseType.startsWith("mysql")) { // MySQL driver
      dbg("Loading MySQL drivers...");
      try {
        Class.forName("org.gjt.mm.mysql.Driver").newInstance(); 
      } catch (Exception e) {dbg("problem loading mysql driver"); return;}

    } else if (driverName.startsWith("org.postgresql")) {

      dbg("Loading PostgreSQL drivers...");
      systemProperties.put("jdbc.drivers", driverName);

    } else {
      dbg("Strange state; inspect...");
    }

    if (dbaseURL == null) {
      dbaseURL = "jdbc:" + dbaseType + "://" + dbaseHost + "/" + dbaseName;
      //dbaseURL = "jdbc." + dbaseType + ":" + dbaseHost + "/" + dbaseName;
      try {
        dbase = DriverManager.getConnection(dbaseURL, dbaseUser, dbasePassword);
      } catch ( SQLException e ) {
      dbg("Init error: " + e.getMessage());
      dbg("dbaseURL : " + dbaseURL);
      }

    } else {
      try {
        dbg("dbase URL: " + dbaseURL);
        dbase = DriverManager.getConnection(dbaseURL);
      } catch (SQLException e) {
        dbg("Init error: " + e.getMessage());
      }
    }
  }

  public Connection getDbase() {return dbase;}

/////////////////////// Execute /////////////////////////

  public int exec(String command) {

    int result = -1;

    try {
      Statement st = dbase.createStatement();
      result = st.executeUpdate(command);
      st.close();

    } catch ( SQLException e ) {

      dbg("Execute error: " + e.getMessage());
    }

    return result;
  }

/////////////////////// Build List /////////////////////////

  public String buildList(Vector values, boolean quote) {

    String result = "";

    if (values.size() == 0) {return "";}

    for (int i=0; i < values.size(); i++) {
      if (i > 0) {result += ", ";}

      if (quote) { 
        result += "\'" + values.get(i) + "\'"; 
      } else { 
        result += values.get(i); 
      }
    }

    return result;
  }

/////////////////////// Build Insertion /////////////////////////

  public String buildInsertion(String table, Vector fields, 
                               Vector values, Vector noquote) {

   //List noquote contains the list of values which shouldn't be quoted.
   //Maybe fields and values should also be of class List; I'm still
   // getting a feeling for these classes.  --BAU, Aug 2, 2000

    String result;

  /// Check arguments ///

    if (fields.size() == 0 || values.size() == 0) {
      throw new IllegalArgumentException("Fields or Values is empty");
    }

    if (fields.size() != values.size()) {
      throw new IllegalArgumentException(
        "Number of fields and values does not match!");  
    }

  /// Start things out ///

    result = "insert into " + table + " (";

  /// process fields ///

    for (int i=0; i < fields.size(); i++) {
      if (i > 0) { result += ", "; }
      result += fields.get(i);
    }

  /// transition ///

    result += ") values (";

  /// process values ///

    for (int i=0; i < values.size(); i++) {
      if (i > 0) { result += ", "; }

      if (noquote.contains(fields.get(i))) { //don't quote it 
        result += values.get(i); 
      } else { 
        result += "\'" + quoteStr((String) values.get(i)) + "\'"; 
      }
    }

    result += ")";

    return result;
  }

/////////////////////// quoteIt /////////////////////////

  public String quoteStr(String str) { // deals with SQL quotes

    if (str == null) {return str;}

    String result;
    // for the moment... hack it.  Sigh.

    result = str.replace('\'', ' '); // as a quick hack, replace with space
    return result;
  }

/////////////////////// findLastInstance /////////////////////////

  public int findLastInstance(String table, String queryField, 
       String queryVal, String keyfield, boolean quoteVal) {

    int result = -1, count = 0;

    try {
      Statement st = dbase.createStatement();
      String query = 
        "select " + keyfield + " from " + table + 
	" where " + queryField + " = ";

      if (quoteVal) {
        query += "'" + queryVal + "';";
      } else {
        query += queryVal + ";";
      }

      ResultSet rs = st.executeQuery(query);

      while(rs.next()) {
        result = rs.getInt(keyfield);
	count++;
      }

      rs.close();
      st.close();

    } catch ( SQLException e ) {

      dbg(e.getMessage());
    }

    if (count > 1) {
      dbg("warning on findLastInstance: " + count + 
          " instances of " + table + ": " + queryField + " = " + 
	  queryVal + " were found.");
    }

    return result;
  }

/////////////////////// Test /////////////////////////

  public void test() { // assumes baseball database

    try {
      Statement st = dbase.createStatement();
      ResultSet rs = st.executeQuery("select * from Team");
      while(rs.next()) {

        String str = rs.getString(1) + " " + rs.getString("name");
	dbg(str);
      }
      rs.close();
      st.close();

    } catch ( SQLException e ) {

      dbg(e.getMessage());
    }
  }


//////////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("DbFuncs." + (dcnt++) + ": " + s);
  }
}

///////////////// END /////////////////
  
 
