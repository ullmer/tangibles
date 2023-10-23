// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow ParamWheel
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.sql.*;
import java.util.*;

//import hb.format.*;

//////////////////////////////////////////////////////
/////////////////// Param Wheel /////////////////////
//////////////////////////////////////////////////////

public class ParamWheel implements DbListener {

//////////////////// fields /////////////////////

  String paramName;

  String projQuery;    // query for retrieving values

  String valsQuery;    // query for retrieving values
  String valsKeyfield; // keyfield name
  String valsName;     // value name

  boolean queryValsMinded = true;

  double min=0, max=1;
  double increment = .05;

  double defaultVal = .5;

  int colorTriple[] = new int[3];
  //int selectedVal = -1;

  int selectedVal = 0;
//  int selectedVal = -1;
  int currentRot  = -1;

  public int tagId;
  int tier; // for result display

  Vector  values = new Vector();
  boolean valsLoaded = false;

  Hashtable valueHash = new Hashtable();

  int lastVal = -1;

  DbThread dbthread = null;

  Vector baselineRecordIds = null;
  Vector incomingResult = null;

  boolean invertTok = false;
  boolean continParam = true;

//  Hashtable recId2Location = null;

  boolean incomingResultReady = false;

//////////////////// methods /////////////////////

//  public ParamWheel(DbThread dbthread) 

//  public int getNumRecords()
//  public void establishResult(Vector baselineRecordIds)
//  public void determineCellNum(int cellId)

//  public void processResultSet(Statement st, ResultSet rs, int resultID)
//  public void processResultVector(Vector results, String dtype, int resultID)

//  public boolean isDataReady() 
//  public void clearDataReady() 

//  public String substStr(String mask, String value) // poor man's hacked single-val sprintf

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// set / get Color ///////////////

  public void setColor(int r, int g, int b) {
    colorTriple[0] = r;
    colorTriple[1] = g;
    colorTriple[2] = b;
  }

  public int[] getColor() {
    return colorTriple;
  }

///////////// isDataReady ///////////////

  public boolean isDataReady() {
    return valsLoaded;
  }

  public void clearDataReady() {
    valsLoaded = false;
  }

  public int size() {
    return values.size();
  }

  public int getSize() {

    return size();
  }

///////////// process Result Set ///////////////

  public void processResultVector(Vector results, 
                                  String dtype, int resultID) {

    dbg("processResultVector is currently unsupported");
    return;
  }

  public void processPuntedQuery(int resultID) {
    dbg("processPuntedQuery is currently unsupported");
    return;
  }

//////////////////// process Result Set /////////////////////

  public void processResultSet(Statement st, ResultSet rs, int resultID) {

    if (st == null || rs == null) {
      dbg("Problem in processResultSet: st or rs are null.  Aborting...");
      return;
    }

  // Walk through the contents
    int count = 0;

    try { 
      while(rs.next()) { 
        //dbg("processing record...");

	ParamWheelVal pwv = new ParamWheelVal();

        try {

           if (resultID != 77) { //... in which case, this won't exist
   	     pwv.id   = rs.getInt(valsKeyfield); 
           }

	   pwv.name = rs.getString(valsName); 
	   values.addElement(pwv);

	   String bname = valsName + "_" + pwv.name;

           valueHash.put(pwv.name, new Integer(count));
           valueHash.put(bname, new Integer(count)); 
	     // just in case we're bool.  really ugly, I know...

        } catch (Exception e) {
          dbg("problem in processResultSet in assigning primary key");
        }
        count++;
      }
    } catch (Exception e) {
      dbg("SQL problem: " + e.getMessage());
    }

    valsLoaded = true;
    dbg("values loaded (" + count + ")");
  }

///////////// cleanupNumber ///////////////

  public String cleanupNumber(double val) {

//  dbg("cleanup called");

   String result = "";

   try {
    double rval = Math.floor(val / increment) * increment;

    rval *= 1000; // trim any pesky trailing digits 
    rval = Math.floor(rval) / 1000.;

    if (rval == Math.floor(rval)) {
      result = Integer.toString((int)rval);
    } else {
      result = Double.toString(rval);
    }

    return result;

   } catch (Exception e) {
     dbg("cleanupNumber exception: " + e.toString());
   }

   return result;
  }

///////////// get val ///////////////

  public String getVal(int i) {

    if (i == -1) {return "";}
    String result;

    lastVal = i;

    try {
      ParamWheelVal pwv = (ParamWheelVal) values.elementAt(i);
      if (pwv == null) {return "";}
      result = pwv.name;

    } catch (Exception e) {
      dbg("getVal exception, ignoring.");
      return "";
    }

    return result;
  }

  public String getBVal(int i) {

    String val = getVal(i);
    String result = valsName + "_" + val;

    return result;
  }


/// reverse listing: string 2 int

  public int getVal(String str) {

    Integer value = (Integer) valueHash.get(str);

    if (value == null) {return -1;}
    return value.intValue();
  }


///////////// set Rot ///////////////

 // basically, compute selectedVal

  public void setRot (int rotVal) {

    int numParams = values.size();
    currentRot    = rotVal;

    double currentVal = (double) rotVal / 255. * (double) (numParams - 1);
    int    intVal     = (int) Math.rint(currentVal);

    selectedVal = intVal;
  }

///////////// get last val ///////////////

  public String getLastVal () {

    return getVal(lastVal);
  }

///////////// load vals///////////////

  public String genQuery (String value) {

//    Parameters p = new Parameters();
//    String result = Format.sprintf(projQuery, p.add(value));

    String result = substStr(projQuery, value);

    return result;
  }

///////////// substitute string ///////////////

  static public String substStr(String mask, String value)  { // poor man's hacked single-val sprintf

    int idx = mask.indexOf("%s");

    if (idx == -1) {return mask;} // %s not found

    String result = mask.substring(0, idx);
    result += value;

    result += mask.substring(idx+2);

    return result;
  }


///////////// load vals///////////////

  public void loadVals() {

    if (queryValsMinded) {
      dbthread.submitQuery(valsQuery, this, 77);
    } else {
      dbg("tok " + paramName + ": loadVals ignored");
    }
  }

///////////// print vals ///////////////

  public void printVals() {

    if (valsLoaded == false) {
      dbg("printVals error: valsLoaded == false");
      return;
    }

    dbg("Listing values for param " + paramName);

    int size = size();

    for (int i=0; i < size; i++) {
      ParamWheelVal val = (ParamWheelVal) values.elementAt(i);
      String name = val.name;
      dbg(name);
    }
  }


///////////// constructor ///////////////

  public ParamWheel(DbThread dbthread) {
    this.dbthread = dbthread;
  }

////////////////////  Main /////////////////////////////

  static public void main(String args[]) {
/*
    DbThread dbthread = new DbThread("pldb", "tmg-internal2");
    ParamWheel group = new ParamWheel(dbthread);

    group.paramName    = "group";
    group.valsQuery    = "select group_id, name from ResearchGroup;";
    group.valsKeyfield = "group_id";
    group.valsName     = "name";

    group.loadVals();
*/

  dbg("substString test:");
  dbg(substStr("yabba%sdoo", "123"));


  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("ParamWheel[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
