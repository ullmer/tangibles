// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow BldgDbMgr
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;
import java.lang.reflect.*;

//////////////////////////////////////////////////////
/////////////////// Param Wheel /////////////////////
//////////////////////////////////////////////////////

public class BldgDbMgr extends DbMgr implements DbListener {

  String lastQuery = null;

// special coords

//float aLat = 35.31, aLon = -80.7;

  boolean specialCoordsExist = true;
  int numSpecialCoords = 2;

  double  specialCoordPos[][] = {{35.3, -80.7}, 
                                 {35.1, -81}};
  String  specialCoordName[]  = {"A", "B"};
  boolean specialCoordPlot[]  = {true, true};

  float deg2miles = (float) 69.1;

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

  public boolean isVisQueryCompleted() {return visQueryCompleted;}
  public boolean doVisQueryResultsExist() {return visQueryResultsExist;}

//////////////////// methods /////////////////////

  public BldgDbMgr(DbThread dbthread) {

    this.dbthread = dbthread;
  }

//////////////////// getRecsInRange /////////////////////

  public Vector getAllRecs() {
   return records;
  }

//////////////////// getRecsInRange /////////////////////

  public Vector getRecsInRange(String field, float minVal, float maxVal,
                                   float upperThresh) {

    Vector results = new Vector();

    int size = records.size();
    BldgRecord br; 

    br = (BldgRecord) records.elementAt(0);
    Field whichField = br.brGetField(field);

    if (whichField == null) {
      dbg("problem in getRecsInRange (float): field " + field + " not found!");
      return null;
    }

    int numResults = 0;

    for (int i=0; i <size; i++) {

      br        = (BldgRecord) records.elementAt(i);
      float val = br.getFloat(whichField);

      if (val >= minVal && val <= maxVal) {

	results.addElement(br);
	numResults++;

      } else if (upperThresh != -1 && maxVal > upperThresh && 
                val > upperThresh) {
	results.addElement(br);
	numResults++;
      }
    }

//    dbg("calcIdsInRange: " + numResults + " results");

    return results;
  }

//////////////////// getGreaterRecs /////////////////////

  public Vector getGreaterRecs(String field, String minVal) {

   float minValF = Float.parseFloat(minVal);
   return getGreaterRecs(field, minValF);

  }

  public Vector getGreaterRecs(String field, float minVal) {

    Vector results = new Vector();

    int size = records.size();
    BldgRecord br; 

    br = (BldgRecord) records.elementAt(0);
    Field whichField = br.brGetField(field);

    if (whichField == null) {
      dbg("problem in getRecsInRange (float): field " + field + " not found!");
      return null;
    }

    int numResults = 0;

    for (int i=0; i <size; i++) {

      br        = (BldgRecord) records.elementAt(i);
      float val = br.getFloat(whichField);

      if (val >= minVal) {

	results.addElement(br);
	numResults++;

      }
    }

//    dbg("calcIdsInRange: " + numResults + " results");

    return results;
  }
//////////////////// getLesserRecs /////////////////////

  public Vector getLesserRecs(String field, String maxVal) {

   float maxValF = Float.parseFloat(maxVal);
   return getLesserRecs(field, maxValF);

  }

  public Vector getLesserRecs(String field, float maxVal) {

    Vector results = new Vector();

    int size = records.size();
    BldgRecord br; 

    br = (BldgRecord) records.elementAt(0);
    Field whichField = br.brGetField(field);

    if (whichField == null) {
      dbg("problem in getRecsInRange (float): field " + field + " not found!");
      return null;
    }

    int numResults = 0;

    for (int i=0; i <size; i++) {

      br        = (BldgRecord) records.elementAt(i);
      float val = br.getFloat(whichField);

      if (val <= maxVal && val > 0) { // just added > 0 to handle taxes, etc.

	results.addElement(br);
	numResults++;

      }
    }

//    dbg("calcIdsInRange: " + numResults + " results");

    return results;
  }

//////////////////// getRecsDiscrete/////////////////////

  public Vector getRecsDiscrete(String field, String val, boolean boolParam) {

  dbg("gRD val: " + val);

   try {

    if (val == null || val.compareTo("") == 0) {
      dbg("getRecsDiscrete: passed val is null!"); 
      return null;
    }

    Vector results = new Vector();

    int size = records.size();
    BldgRecord br; 

    br = (BldgRecord) records.elementAt(0);

    if (boolParam) {
      field += "_" + val;
    }

    Field whichField = br.brGetField(field);

    if (whichField == null) {
      dbg("problem in getRecsInRange (string): field " + 
           field + " not found!");
      return null;
    }

    String typeStr = whichField.getType().toString();
    int typeInt = 0;
 
    if (typeStr.compareTo("float") == 0) { 
      typeInt = 1;
    }

    if (typeStr.compareTo("boolean") == 0) { 
      typeInt = 2;
    }

    int numResults = 0;

    for (int i=0; i <size; i++) {

      br          = (BldgRecord) records.elementAt(i);

      String  nval = null;
      boolean bval = false;

      switch (typeInt) {
        case 0: nval = br.getString(whichField); break;
        case 1: nval = Float.toString(br.getFloat(whichField)); break;
        case 2: bval = br.getBoolean(whichField); break;
      }
     
      if (typeInt == 2 && bval == true) {
	results.addElement(br);
	numResults++;
	continue;
      } 

      if (nval == null) {
        continue;
      }

      if (val.compareTo(nval) == 0) {

	results.addElement(br);
	numResults++;
      }
    }

    dbg("calcIdsInRange: " + numResults + " results");

    return results;

   } catch (Exception e) {
     dbg("getRecsDiscrete exception: " + e.toString());
   }

   return null;
  }


//////////////////// dist /////////////////////

  public double dist(double a1, double a2, double b1, double b2) {

    double result = Math.sqrt(Math.pow(a1-b1,2) + Math.pow(a2-b2,2));
    return result;
  }


//////////////////// process Result Vector /////////////////////

  public void processResultVector(Vector results, 
                                  String dtype, int resultID) {

    dbg("processResultVector is currently unsupported");
    return;
  }

//////////////////// process Result Set /////////////////////

  public void processResultSet(Statement st, ResultSet rs, int resultID) {

    if (st == null || rs == null) {
      dbg("Problem in processResultSet: st or rs are null.  Aborting...");
      return;
    }

  // Walk through the contents

    if (resultID == 10) { // load full dbase
      int count = 0;
  
      try { 
        while(rs.next()) { 
          //dbg("processing record...");
  
  	BldgRecord br = new BldgRecord();
  
          try {
  	   br.bldg_id    = rs.getInt("bldg_id");
  	   br.mls        = rs.getInt("mls");
  
  	   br.address           = rs.getString("address");
  	   br.floor_descript    = rs.getString("floor_descript");
  	   br.highschool_abbrev = rs.getString("highschool_abbrev");
  	   br.bldg_type         = rs.getString("bldg_type");
  	   br.floorStr          = rs.getString("floorStr");
  
  	   br.area_num       = rs.getInt("area_num");
  	   br.zip            = rs.getInt("zip");
  	   br.listing_price  = rs.getInt("listing_price");
  	   br.ballpark_price = rs.getInt("ballpark_price");
  	   br.sq_foot        = rs.getInt("sq_foot");
  	   br.taxes          = rs.getInt("taxes");
  
  	   br.acreage = rs.getFloat("acreage");
  	   br.floors  = rs.getFloat("floors");
  	   br.lat     = rs.getFloat("lat");
  	   br.lon     = rs.getFloat("lon");

	   br.feature_club       = rs.getBoolean("feature_club");
	   br.feature_golf       = rs.getBoolean("feature_golf");
	   br.feature_pool       = rs.getBoolean("feature_pool");
	   br.feature_porch      = rs.getBoolean("feature_porch");
	   br.feature_waterfront = rs.getBoolean("feature_waterfront");

        // special coords

	   if (specialCoordsExist) {
	     if (numSpecialCoords >= 1) {

	       double a1 = specialCoordPos[0][0];
	       double a2 = specialCoordPos[0][1];

	       br.distToA = (float) dist((double) br.lat, (double) br.lon, 
	         specialCoordPos[0][0],
	         specialCoordPos[0][1]) * deg2miles;
	     }

	     if (numSpecialCoords >= 2) {

	       br.distToB = (float) dist((double) br.lat, (double) br.lon, 
	         specialCoordPos[1][0],
	         specialCoordPos[1][1]) * deg2miles;
	     }
	   }

  	   records.addElement(br);
  
           Integer key = new Integer(br.bldg_id);
           prIdHash.put(key, br);
  
  	   key = new Integer(br.mls);
  	   prMlsHash.put(key, br);

	   //dbg("brs: bldg_id " + bldg_id);
  
          } catch (Exception e) {
            dbg("problem in processResultSet in assigning primary key");
          }
          count++;
        }
      } catch (Exception e) {
        dbg("SQL problem: " + e.getMessage());
      }
      recsLoaded = true;
      dbg("values loaded (" + count + ")");
    }

    if (resultID == 20) { // vis query response

      int count = 0;

        if (visQueryRIncoming == null) {
	  visQueryRIncoming = new Hashtable();
	} else {
	  dbg("processResultSet strangeness: visQueryRIncoming isn't null!");
	}

      synchronized (visQueryRIncoming) {

        try { 
          while(rs.next()) { 
            //dbg("processing record...");

  	    int bldgId = rs.getInt("bldg_id");
	    Integer id = new Integer(bldgId);

	    //visQueryResults.addElement(id);
	    //visQueryResults.put(id, id);
	    visQueryRIncoming.put(id, id);
	    count++;
	  }
        } catch (Exception e) {
           dbg("problems in processResultSet (vis query response): " 
  	     + e.getMessage());
        }

        try {
	  synchronized (visQueryResults) {

            Hashtable oldResults = visQueryResults;
            visQueryResults      = visQueryRIncoming;

	    if (oldResults != null) {
              oldResults.clear();
	    }

            visQueryRIncoming = null;
 
            visQueryCompleted = true;
            visQueryResultsExist = true;
          }
	} catch (Exception e) {
	    dbg("problems in processResultSet (final assignment): " +
	          e.toString());
	}
      //dbg("visQueryResults populated: " + count); 
      }
    }
  }

///////////// visResultsContainEl ///////////////
   // basically, clear flags to life can move on

  public void processPuntedQuery(int resultID) { 

   dbg("processPuntedQuery");

   visQueryCompleted = true;
  }

///////////// visResultsContainEl ///////////////

  public boolean visResultsContainEl(int id) {

    Integer key = new Integer(id);

    if (visQueryResults.containsKey(key)) {
      return true;
    } else {
      return false;
    }
  }

///////////// listBuildings ///////////////

  public void listBuildings() {

    dbg("listing params: ");

    int size = records.size();

    for (int i=0; i<size; i++) {
      BldgRecord el = (BldgRecord) records.elementAt(i);
      //dbg(el.paramName + " " + el.tagId);
    }
  }


///////////// getBldgId ///////////////

  public BldgRecord getBldgId(Integer idKey) {

    if (idKey == null) {return null;}

    BldgRecord result = (BldgRecord) prIdHash.get(idKey);
    return result;
  }

/*
///////////// getImNum ///////////////

  public BldgRecord getMls(Integer key) {

    BldgRecord result = (BldgRecord) brMlsHash.get(key);
    return result;
  }

  public BldgRecord getMls(int tagId) {

    Integer idKey = new Integer(tagId);
    return getImNum(idKey);
  }

  public BldgRecord getId(int tagId) {

    Integer idKey = new Integer(tagId);
    return getId(idKey);
  }
*/


///////////// getVisQueryResults ///////////////

 public Enumeration getVisQueryResults() {

   return visQueryResults.elements();
 }

///////////// submitVisQuery ///////////////

 public void submitVisQuery(String visQuery) {

   lastQuery = visQuery;

   visQueryCompleted = false;
   dbthread.submitQuery(visQuery, this, 20);
 }

///////////// load Vals ///////////////

  public void loadVals() {

    //String query = "select * from building;";

    String query = "select * from building where " + 
                   "lat >  34.9195 and lat <  35.5366 and " + 
		   "lon > -81.1907 and lon < -80.4977;";

    dbthread.submitQuery(query, this, 10);
  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {

    DbThread dbthread = new DbThread("photos", "tmg-internal2");

    BldgDbMgr mgr = new BldgDbMgr(dbthread);
    mgr.loadVals();

    dbg("TEST");
//    mgr.getId(65533).printVals();
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("BldgDbMgr[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
