/// Query Rack Interp
/// By Brygg Ullmer, MIT Media Lab
///
/// Begun November 3, 2001

import java.util.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  WRackInterp /////////////////////////////
///////////////////////////////////////////////////////////

public class QRackInterp implements WRModelListener {

/////////////  METHODS ///////////////

//  public QRackInterp(WRackMgr mgr, char whichData) 

//  public DbMgr       getDbMgr() 
//  public PTokDbase   getPTokDb() 
//  public WRackModel  getModel() 
//  public Enumeration getPTokResults() 

//  public void addVis(WRackVis qrackVis) 
//  public void updateSql() 

//  public PTokResults mapPTok2Results(PTokModel ptok) 
//  public boolean      isPTokActive(PTokModel ptok) 

//  public void processCTokEntrance(int containerID) 
//  public void processCTokExit(int containerID) 
//  public void processPTokEntrance(PTokModel ptok) 
//  public void processPTokExit(PTokModel ptok) 
//  public void processPTokUpdate (PTokModel ptok) 
//  public void processQRelUpdate(WRackRels qrackRels) 

/////////////  MEMBERS ///////////////

  boolean verbose = true;

  QRackMgr   qrackMgr;
  WRackModel qrackModel = null;

  DbThread   dbthread = null;

  DbMgr      dbMgr  = null;
  PTokDbase ptokDb  = null;

  Vector qrackVisList = new Vector();

  private Hashtable ptok2results = null;

  //char dataType = 'b'; // building
  char dataType = 'm';  // mutual

  String lastQuery = "";
  String currentQuery = "";

  // FOLLOWING VARIABLE IS POWERFUL; BE CAREFUL!
  boolean isInterpActive = true; // allows us to disable certain interps

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

  public DbMgr     getDbMgr() {return dbMgr;}
  public PTokDbase getPTokDb() {return ptokDb;}
  public WRackModel getModel() {return qrackModel;}

 ////////////////////  QRackInterp /////////////////////////////

//  public QRackInterp(CircTest mgr, WRackModel qrModel) {

  public QRackInterp(QRackMgr mgr, char whichData) {

    dataType = whichData;

    switch (dataType) {
      case 'b': dbthread   = new DbThread("realestate", "tmg-internal2");
                dbMgr     = new BldgDbMgr(dbthread);
                dbMgr.loadVals();

		break;

      case 'm': dbthread   = new DbThread("mutual", "tmg-internal2");
//                dbMgr     = new MutualDbMgr(dbthread);
                dbMgr.loadVals();
		break;
    }

    ptokDb = new PTokDbase(dataType, dbthread);

    qrackMgr   = mgr;
    qrackModel = new WRackModel(ptokDb);

    ptok2results = new Hashtable();
    qrackModel.addListener(this);
  }

 ////////////////////  add Vis /////////////////////////////

  public void addVis(QRackVis qrackVis) {

    if (qrackVis == null) {return;}

//    dbg("addVis: adding " + qrackVis);

    qrackVisList.addElement(qrackVis);
  }

 ////////////////////  updateSql /////////////////////////////

  public void updateSql() {
    if (isInterpActive == false) {return;}

    try {
  
      // if we're already in the midst of a query, don't start a new one
  
//      if (dbMgr.isVisQueryCompleted() == false) {return;}

  // but -- should we queue the final query, to make sure we went up
  // reflecting the final state?
  
      lastQuery = currentQuery;
      currentQuery = null;
  
      qrackMgr.getModel().update(); // poll thing, just in case tokens changed

      String selectStr = ptokDb.getSelectStr();
 

// still use generation of SQL query -- now, as method for calculating 
// whether we need to repeat our internal numerical query
 
      try {
        currentQuery = qrackMgr.getModel().wrackRels.genSqlQuery(selectStr);

      } catch (Exception e) { 
        dbg("updateSql: problems generating Sql query: " + e.toString());
	e.printStackTrace();
        return;
      }
  
      if (currentQuery == null) {return;} // IS THIS ENOUGH; OR "CLEAR"?
  
      if (lastQuery == null || (currentQuery.compareTo(lastQuery) != 0 && 
          currentQuery.length() != 0)) {
  
//        dbg("QUERY: " + currentQuery + "\n");
      //  dbMgr.submitVisQuery(currentQuery);

        BldgDbMgr bdm = (BldgDbMgr) dbMgr;

        Vector results = qrackMgr.getModel().wrackRels.getANDResults(bdm);

        setQueryResults(results); 

      }
    } catch (Exception e) {
      dbg("updateSql exception: " + e.toString());
      e.printStackTrace();
    }
  }

 ////////////////////  setQueryResults /////////////////////////////

  public void setQueryResults(Vector results) {

  // basically, we're trying to rebuild the queryResults hash of bldgIDs
  // this replicates process of resultID==20 in BldgDbMgr::processResultSet

    if (results == null) {

      dbg("setQueryResults bogosity: results = null!");
      return;
    }

    Hashtable QResultIncoming = new Hashtable();

    int numEls = results.size();

    for (int i=0; i < numEls; i++) {
      BldgRecord br = (BldgRecord) results.elementAt(i);
      Integer key = new Integer(br.bldg_id);

      QResultIncoming.put(key, key);
    }

    // OK, swap over to new results

    dbMgr.visQueryResults = QResultIncoming;
    dbMgr.visQueryCompleted = true;
    dbMgr.visQueryResultsExist = true;

  }

 ////////////////////  isPTokActive /////////////////////////////

  public PTokResults mapPTok2Results(PTokModel ptok) {

    PTokResults ptokr = (PTokResults) ptok2results.get(ptok);
    return ptokr;
  }

 ////////////////////  isPTokActive /////////////////////////////

  public boolean isPTokActive(PTokModel ptok) {
    if (ptok2results.containsKey(ptok)) {
      return true;
    }

    return false;
  }

 ////////////////////  getPTokrEnum /////////////////////////////

  public Enumeration getPTokResults() {

    return ptok2results.elements();
  }
 
////////////////////  rack adj /////////////////////////////

  public void procRackAdj(char state) {
    IBase ib = (IBase) qrackMgr;

//    ib.rrelVis.currentState = state;
  }

////////////////////  CTok Entrance /////////////////////////////

  public void processCTokEntrance(int containerID) {

    qrackMgr.deiconify(containerID);
  }

////////////////////  CTok Exit /////////////////////////////

  public void processCTokExit(int containerID) {

    qrackMgr.iconify(containerID);
  }

////////////////////  PTok Entrance /////////////////////////////

  public void processPTokEntrance(PTokModel ptok) {

   if (ptok == null) {
     dbg("processPTokEntrance passed null ptok!");
     return;
   }

   try {

    if (isInterpActive == false) {return;}

    if (verbose) {dbg("TOK ENTRANCE: " + ptok.paramName);}

    if (ptok2results.containsKey(ptok)) {
      dbg("strangeness in processPTokEntrance: handle already exists!");
      return;
    }

    // OK, create the handle

    PTokResults ptokr = new PTokResults(dataType);

    if (ptokr == null) {
      dbg("procesPTokEntrance: null ptokr!");
      return;
    }

    ptokr.ptokModel   = ptok;

    ptok2results.put(ptok, ptokr);

    updateSql();

    // Send command to qrackVis

    int numEls = qrackVisList.size();

    for (int i=0; i < numEls; i++) {
      QRackVis qrackVis = (QRackVis) qrackVisList.elementAt(i);

      if (qrackVis == null) {
        dbg("processPTokEntrance: null qrackVis!");
        break;
      }

      qrackVis.ptokEnters(ptok);
    }
   } catch (Exception e) { 

     dbg("processPTokEntrance exception: " + e.toString());
   }
  }

////////////////////  PTok Exit /////////////////////////////

  public void processPTokExit(PTokModel ptok) {

    if (isInterpActive == false) {return;}

    if (verbose) {dbg("TOK EXIT: " + ptok.paramName);}

    if (ptok2results.containsKey(ptok) == false) {
      dbg("strangeness in processPTokExit: handle doesn't exist!");
      return;
    }

    updateSql();

    // OK, remove the handle

    // ptok2results.remove(ptok); // MAY NEED TO UNDO COMMENT!
  }
 ////////////////////  PTok Update /////////////////////////////

  public void processPTokUpdate (PTokModel ptok) {

    if (isInterpActive == false) {return;}

//    if (verbose) {dbg("processPTokUpdate: ptok " + ptok.paramName);}

    if (ptok == null) {
      dbg("processPTokUpdate: passed null ptok!");
      return;
    }

  PTokResults ptokr = null;

  try {
    if (ptok2results.containsKey(ptok) == false) {
      dbg("strangeness in processPTokUpdate: handle doesn't exist!" +
           " Creating.");
      processPTokEntrance(ptok);
      dbg("processPTokUpdate: processPTokEntrance complete");
    }

    ptokr = (PTokResults) ptok2results.get(ptok);

    if (ptokr == null) {
      dbg("processPTokUpdate: ptok2results returns null!");
      return;
    }
   } catch (Exception e) {
     dbg("processPTokUpdate exception (1): " + e.getMessage());
     return;
   }

   float lower, upper, upperThresh;
   Vector ptokResults;

   try {

     if (ptok.discreteParam == true) {

       if (ptok == null) {
         dbg("processPTokUpdate(d) problem: ptok is null!");
	 return;
       }
   
       if (ptok.pwheel == null) {
         dbg("processPTokUpdate(d) problem: ptok.pwheel is null!");
	 return;
       }
   

       String field = ptok.pwheel.getVal(ptok.pwheel.selectedVal);
       ptokResults = 
          dbMgr.getRecsDiscrete(ptok.pwheel.valsName, field, ptok.boolParam);

     } else {

       lower = (float) ptok.getScaledLower();
       upper = (float) ptok.getScaledUpper();
 
       upperThresh = (float) ptok.getUpperThresh();

       ptokResults = dbMgr.getRecsInRange(ptok.paramName, 
                                          lower, upper, upperThresh);
     }
 
    } catch (Exception e) {
      dbg("processPTokUpdate exception (2): " + 
          e.toString() + " : " + e.getMessage() + e.toString());
      return;
    }

   try {
 
     ptokr.setRecs(ptokResults);
     updateSql();
 
     //dbg("vals: " + lower + " | " + upper);

     if (qrackVisList == null) {
       dbg("processPTokUpdate oddity: qrackVisList is null");
       return;
     }
    } catch (Exception e) {
      dbg("processPTokUpdate exception (3): " + 
          e.toString() + " : " + e.getMessage() + e.toString());
    }
 
   try {
     // Send command to qrackVis
 
     int numEls = qrackVisList.size();
 
     for (int i=0; i < numEls; i++) {
       QRackVis qrackVis = (QRackVis) qrackVisList.elementAt(i);

       if (qrackVis == null) {
//         dbg("processPTokUpdate oddity: qrackVis is null / " + 
//	     + i + "/" + numEls);
	 break;
       }
       qrackVis.ptokChanges(ptok);
     }
 
    } catch (Exception e) {
      dbg("processPTokUpdate exception (4): " + 
          e.toString() + " : " + e.getMessage() + e.toString());
    }
  }

//////////////////  Query Relation Update //////////////////////////

  public void processWRelUpdate(WRackRels qrackRels) {}

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("QRackInterp." + (dcnt++) + ": " + s);
  } 

}

//// END ////

