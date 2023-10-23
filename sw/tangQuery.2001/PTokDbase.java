/// Parameter token dbase
/// By Brygg Ullmer, MIT Media Lab
/// Begun October 25, 2001

import java.util.*;
import java.awt.*;
import java.io.*;

///////////////////////////////////////////////////////////
//////////////////  Parameter token ///////////////////////
///////////////////////////////////////////////////////////


  // NOTE: implementing this quickly, partly as a placeholder
  // Eventually, will use a real database to hold information about
  //   the objects.  But meanwhile, let's "get it done"

public class PTokDbase {

/////////////  METHODS ///////////////

// public PTokDbase()

/////////////  MEMBERS ///////////////

  boolean verbose = true;

//  QRack parentRack = null;

  String tokName;

  int currentValue = -1;

  //char dataType = 'b'; // building
  char dataType = 'm'; // mutual fund

  Hashtable issuedPTokHash = null;

  ParamWheelMgr pwMgr = null;
  DbThread dbThread   = null;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

////////////////////  constructor /////////////////////////////

  public PTokDbase (char dataType, DbThread dbThread) {

    this.dataType = dataType;
    issuedPTokHash = new Hashtable();

    this.dbThread = dbThread;
    pwMgr = new ParamWheelMgr();
    pwMgr.loadDefaultWheels(dbThread);
  }

////////////////////  mapId2PTok /////////////////////////////

  public String getSelectStr() {

    String selectStr = "";

    switch (dataType) {
      case 'b': selectStr = "select bldg_id from building"; break;
      case 'm': selectStr = "select fund_id from funds"; break;
    }

    return selectStr;
  }

////////////////////  mapId2PTok /////////////////////////////

  public PTokModel mapId2PTok(int ptokId) {
    switch (dataType) {
      case 'b': return mapBId2PTok(ptokId);
      case 'm': return mapMId2PTok(ptokId);
    }

    return null;
  }

////////////////////  mapBId2PTok /////////////////////////////

  public PTokModel mapBId2PTok(int ptokId) {

   // First, see if we've already cached this ptok

   Integer key = new Integer(ptokId);
   PTokModel ptok = (PTokModel) issuedPTokHash.get(key);

   if (ptok != null) {

     //dbg("mapId2PTok: id " + ptokId + " already stored in hash.  Using it.");
     return ptok;
   }

   // Nope; look it up.

   switch (ptokId) {

//     case 35: 
     case 172: 
//       ptok = new PTokModel("date", 990000000, 1000000000, ptokId, 
//                            Color.blue, "date");

       ptok = new PTokModel("acreage", "acreage", pwMgr.getName("acreage"), 
                              0, 3, ptokId, 
                              //new Color(35, 35, 235),
                              //new Color(0, 150, 0),
                              new Color(253,218,87),
                              new Color(180, 180, 250)); 

//                            new Color(100, 120, 250));
//                            new Color(50, 20, 150));
       ptok.upperThresh = 2.8;
       ptok.invertTok = true;
       break;

     //case 95:
     case 76:
       ptok = new PTokModel("listing_price", "price", 
                           pwMgr.getName("price"), 0, 1200, 
                            //ptokId, new Color(153,25,25),
                            ptokId, new Color(158, 42, 42),
                                    new Color(250,190,190)); 

       ptok.upperThresh = 1150;
       break;

     case 99:

       ptok = new PTokModel("taxes", "taxes", 
                           pwMgr.getName("taxes"), 0, 5000, 
                            ptokId, new Color(119,33,179),
                                    new Color(250,190,190)); 

       ptok.upperThresh = 4800;
       break;

     case 181:
       ptok = new PTokModel("distToB", "distToB", pwMgr.getName("distToB"), 
                            0, 40, 
                            ptokId, new Color(119,33,179),
                                    new Color(250,190,190)); 

       ptok.upperThresh = 40;
       break;

     case 207:
     //case 65:
       ptok = new PTokModel("sq_foot", "sqft", pwMgr.getName("sqfoot"), 
                            0, 4200, ptokId, 
                            //new Color(100, 120, 250),
                            new Color(202, 140, 141),
                            new Color(180, 190, 250));

       //ptok.upperThresh = 3500;
       ptok.upperThresh = 4200;
       ptok.invertTok = true;
       break;

     case 51:

/*       ptok = new PTokModel("floors", "floors", 
                       pwMgr.getName("floors"), ptokId, 
                       //new Color(40, 169, 216), 
                       new Color(15, 44, 92),
                       new Color(143, 197, 216));
*/
/*
       ptok = new PTokModel("floors", "floors", pwMgr.getName("floors"), 
                       1, 3.75, ptokId, 
                       //new Color(40, 169, 216), 
                       new Color(15, 44, 92),
                       new Color(143, 197, 216));
       ptok.invertTok = true;
*/

       ptok = new PTokModel("distToA", "distToA", pwMgr.getName("distToA"), 
                            0, 40, ptokId, 
                            //new Color(100, 120, 250),
                            new Color(202, 140, 141),
                            new Color(180, 190, 250));

       ptok.upperThresh = 40;
       break;
    
     case 190:

       ptok = new PTokModel("bldg type", "bldg_type", 
                       pwMgr.getName("bldg type"), ptokId, 
                       //new Color(169, 40, 216), 
                       new Color(52,86,134),
                       new Color(197, 143, 216)); 
       break;

     case 255:

       ptok = new PTokModel("high school", "highschool_abbrev", 
                       pwMgr.getName("high school"), ptokId, 
                       //new Color(216, 169, 40), 
                       new Color(224, 170, 15),
                       new Color(216, 197, 143)); 
       break;

     case 32:

       ptok = new PTokModel("features", "feature", 
                       pwMgr.getName("features"), ptokId, 
//                       new Color(40, 169, 216), 
                       //new Color(30, 127, 152),
                       new Color(155, 170, 192),
                       new Color(143, 197, 216));
       ptok.boolParam = true;
       break;
    }

    if (ptok != null) {
      issuedPTokHash.put(key, ptok);
    } else {
      dbg("mapId2PTok problem: no valid mapping! (" + ptokId + ")");
    }

    return ptok;
  }
  
////////////////////  mapMId2PTok /////////////////////////////

  public PTokModel mapMId2PTok(int ptokId) {

   // First, see if we've already cached this ptok

   Integer key = new Integer(ptokId);
   PTokModel ptok = (PTokModel) issuedPTokHash.get(key);

   if (ptok != null) {

     //dbg("mapId2PTok: id " + ptokId + " already stored in hash.  Using it.");
     return ptok;
   }

   // Nope; look it up.

   switch (ptokId) {

/*
     case 35: 
       ptok = new PTokModel("risk_cat", "risk", 0, 5, ptokId, 
                            new Color(100, 120, 250),
                            new Color(170, 190, 250));

       ptok.upperThresh = 4.5;
       break;

     case 95:
       ptok = new PTokModel("ytd_return", "ytd_return", -20, 20, 
                            ptokId, new Color(195,85,85),
                                    new Color(250,190,190)); 

       ptok.upperThresh = 15;
       break;
*/
/*
     case 65:
       ptok = new PTokModel("sq_foot", "sqft", 0, 4200, 
                            ptokId, new Color(150, 10, 75)); 

       ptok.upperThresh = 3500;
       break;
*/
    }

    if (ptok != null) {
      issuedPTokHash.put(key, ptok);
    } else {
      dbg("mapId2PTok problem: no valid mapping! (" + ptokId + ")");
    }

    return ptok;
  }
  
 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("PTokDbase." + (dcnt++) + ": " + s);
  } 
}  

//// END ////

