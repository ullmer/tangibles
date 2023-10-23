/// Query Rack Model
/// By Brygg Ullmer, MIT Media Lab
///
/// Begun October 25, 2001

import java.util.*;
import java.io.*;

///////////////////////////////////////////////////////////
////////////////////  WRackModel /////////////////////////////
///////////////////////////////////////////////////////////

public class WRackModel implements WRCListener {

/////////////  METHODS ///////////////

//  public WRackModel(PTokDbase ptokDb) 

//  public int getNumToksActive() 
//  public int getNumSensingCells() 

//  public void setCellContents(int whichCell, PTokModel ptok) 

//  public PTokModel getCellContents(int whichCell) 
//  public PTokModel getLastCellContents(int whichCell) 

//  public void printArray() 
//  public void processParamUpdate(int rackId, int cellId, int tokId, 
//  public void processReedUpdate(int reedLoc, int reedState) 

//  public void reedCheckup() 
//  public int untangleCellId(int rackId, int cellId) 
//  public void addListener(WRModelListener newListener) 

//  public void update() 

//  public void updateTokenListeners(PTokModel ptok) 
//  public void updateContainerEntrance(int containerID) 
//  public void updateContainerExit(int containerID) 
//  public void updateTokenExit(PTokModel ptok) 
//  public void updateTokenEntrance(PTokModel ptok) 
//  public void updateWRelListeners(WRackRels wrackRels) 

/////////////  MEMBERS ///////////////

  WRClient wrackClient;

 // Sensing cell information

  private int numSensingCells = 12;

  private PTokModel scCurrentTok[]; // sc = sensing cell; -1 = not present
  private PTokModel scLastTok[];    

  PToksActive ptoksActive = null;
  WRackRels   wrackRels   = null;

  Vector wrModelListeners = null;

  int numCTokWatchdogs = 2;
  TokMWatchdog ctokMWatchdogs[] = new TokMWatchdog[numCTokWatchdogs];
  int lastCTokState[]         = new int[numCTokWatchdogs];


  PTokDbase     ptokDb  = null;

//  int       wrackCellIdMap[]      = {3, 1, 2, 6, 4, 5};  // CHECK THIS!!

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

 ////////////////////  WRackModel /////////////////////////////

  public WRackModel(PTokDbase ptokDb) {

    this.ptokDb = ptokDb;

    wrackClient = new WRClient(this); 
    wrackClient.start();

    ptoksActive = new PToksActive(this);
    wrackRels   = new WRackRels(this);

    // allocate sensing cell trackers

    scCurrentTok = new PTokModel[numSensingCells];
    scLastTok    = new PTokModel[numSensingCells];

    wrModelListeners = new Vector();

    for (int i=0; i<numCTokWatchdogs; i++) {
      ctokMWatchdogs[i] = new TokMWatchdog();
      lastCTokState[i] = 0;
    }
  }

 ////////////////////  describeState /////////////////////////////

  public String describeState() { 

    Vector ptoks = ptoksActive.getActivePToks();
    int numpt = ptoks.size();

    String result = "";

    for (int i=0; i < numpt; i++) {

      PTokModel pt = (PTokModel) ptoks.elementAt(i);
      result += pt.describeState();
      if (i != numpt - 1) { result += " "; }
    }

    return result;
  }

 ////////////////////  set Cell Contents /////////////////////////////

  public int getNumToksActive() { 

     Vector activeToks = ptoksActive.getActivePToks();
     return activeToks.size();
  } 

 ////////////////////  set Cell Contents /////////////////////////////

  public int getNumSensingCells() { return numSensingCells; } 

 ////////////////////  set Cell Contents /////////////////////////////

  public void setCellContents(int whichCell, PTokModel ptok) {
    
    if (whichCell < 0 || whichCell >= numSensingCells) {

      dbg("setCellContents: bad whichCell argument, ignoring");
      return;
    }

    scLastTok[whichCell] = scCurrentTok[whichCell];
    scCurrentTok[whichCell] = ptok;

    wrackRels.adjRelsChanged();
  }

 ////////////////////  get Cell Contents /////////////////////////////
   
   public PTokModel getCellContents(int whichCell) {

     if (whichCell < 0 || whichCell >= numSensingCells) {
       return null;
     }

     return scCurrentTok[whichCell];
   }

 ////////////////////  get Last Cell Contents ///////////////////////

   public PTokModel getLastCellContents(int whichCell) {

     if (whichCell < 0 || whichCell >= numSensingCells) {
       return null;
     }

     return scLastTok[whichCell];
   }

 ////////////////////  print Array ///////////////////////

   public void printArray() {

    String result = "";

    for (int i=0; i < numSensingCells; i++) {

      PTokModel ptok = scCurrentTok[i];
      if (ptok == null) {
        result += "null ";
      } else {
        result += ptok.paramName + " ";
      }
    }
    dbg(result);
   }


 ////////////////////  processTokEntrance /////////////////////////////

  public void processTokEntrance(int whichRack, int whichSlot, int whichId) {
  
    try {

      PTokModel ptok = ptoksActive.tokWitnessed(whichId, whichSlot);

      if (ptok == null) {return;}
      updateTokenListeners(ptok); 

    } catch (Exception e) {
      dbg("processTokEntrance exception: " + e.toString());
    }
  }

 ////////////////////  processTokExit /////////////////////////////

  public void processTokExit(int whichRack, int whichSlot, int whichId) {

    dbg("tokExit: " + whichId);

    //PTokModel ptok = ptoksActive.tokClaimsDeparture(whichId, whichSlot);

     ptoksActive.tokClaimsDeparture(whichId, whichSlot);

//    if (ptok == null) {return;}
//    updateTokenListeners(ptok); 
  }

 ////////////////////  processTokRot/////////////////////////////

  public void processTokRot(int whichRack, int whichCell, int rotVal) {

    PTokModel ptok = ptoksActive.getPTokInCell(whichCell);

    if (ptok == null) {
//      dbg("processTokRot weirdness: null ptok.  Ignoring.");
// not unusual, if no token is there! :-)
      return;
    }

    boolean madeImpact = ptok.updateUpperVal(rotVal);

    if (ptok.discreteParam) {
      ptok.pwheel.setRot(rotVal);
    }

    if (!madeImpact) {return;}

    try {
      updateTokenListeners(ptok); 
    } catch (Exception e) {
      dbg("processValUpdate exception: " + e.getMessage());
    }
  }

  public void processAdjacencies(int tokId, String adjStr) {

    dbg("processAdjacencies not implemented!");
  }

 ////////////////////  processReedUpdate /////////////////////////////

  public void processReedUpdate(int reedLoc, int reedState) {

    dbg("reed: " + reedLoc + " " + reedState);

    // Handle rack adj

    if (reedLoc == 5) {
      int numListeners = wrModelListeners.size();

      for (int i=0; i < numListeners; i++) {
        WRModelListener listener = (WRModelListener) 
	  wrModelListeners.elementAt(i);

        //listener.processWRelUpdate(wrackRels);

        if (reedState == 0) {
          listener.procRackAdj('B');
        } else {
          listener.procRackAdj('C');
        }
        return;
      }    
    }

    // Handle other things
   

    if (reedLoc < 0 || reedLoc >= numCTokWatchdogs) {
      dbg("processReedUpdate: Reed switch loc out of bounds!");
      return;
    }

    TokMWatchdog relWatchdog = ctokMWatchdogs[reedLoc];

    if (reedState == 0) { // magnet detected
      if (relWatchdog.isTokPresent() == false) {
        updateContainerEntrance(reedLoc);
      } 

      relWatchdog.tokWitnessed();
      lastCTokState[reedLoc] = 1;
    }

    if (reedState == 1) { // magnet not detected

      relWatchdog.tokClaimsDeparture();

      if (relWatchdog.isTokPresent() == false) { 
        updateContainerExit(reedLoc);
        lastCTokState[reedLoc] = 0;
      }
    }
  }

 ////////////////////  checkup on reed state/////////////////////////////

  public void reedCheckup() { // hardwired; sorry

    for (int i=0; i < numCTokWatchdogs; i++) {

      if (lastCTokState[i] == 1 && 
          ctokMWatchdogs[i].isTokPresent() == false) {

         lastCTokState[i] = 0;
         updateContainerExit(i);
       }
     }
   }

 ////////////////////  untangle Cell Id /////////////////////////////

  public int untangleCellId(int rackId, int cellId) { // hardwired; sorry

    if (rackId != 0 && rackId != 1) {
      dbg("untangleCellId problem: rackId != 1 or 0!  Aborting...");
      return -1;
    }

    int whichCell = -1;

    switch (cellId) {
//      case 1: whichCell = 0; break;
      case 0: whichCell = 0; break;
      case 2: whichCell = 1; break;
      case 3: whichCell = 2; break;
      case 5: whichCell = 3; break;
      case 4: whichCell = 4; break;
    }

    if (whichCell == -1) {
      dbg("untangleCellId problem: cellId outside of valid range!");
      return -1;
    }

    int result = rackId * 5 + whichCell;

    return result;
  }

 ////////////////////  processAxisUpdate /////////////////////////////

  public void processAxisUpdate (int rackId, int cellId, int tokId, 
                                          int bound1, int bound2) {

    dbg("Warning: processAxisUpdate isn't implemented!");
  }

 ////////////////////  add Listener /////////////////////////////

  public void addListener(WRModelListener newListener) {

    wrModelListeners.addElement(newListener);
  }

 ////////////////////  update /////////////////////////////

  public void update() {

    ptoksActive.update();
    reedCheckup();
  }

 ////////////////////  update Token Listeners /////////////////////////////

  public void updateTokenListeners(PTokModel ptok) {

    int numListeners = wrModelListeners.size();

    for (int i=0; i < numListeners; i++) {
      WRModelListener listener = 
         (WRModelListener) wrModelListeners.elementAt(i);

      if (listener == null) {
        dbg("updateTokenListeners: null listener!"); 
	continue;
      }

      try {
        listener.processPTokUpdate(ptok);
      } catch (Exception e) {
        dbg("updateTokenListeners: ptokUpdate exception: " + e.toString());
	return;
      }
    }
  }

 ////////////////////  update container entrance /////////////////////////////

  public void updateContainerEntrance(int containerID) {

    int numListeners = wrModelListeners.size();

    for (int i=0; i < numListeners; i++) {
      WRModelListener listener = (WRModelListener) wrModelListeners.elementAt(i);
      listener.processCTokEntrance(containerID);
    }
  }

 ////////////////////  update container exit /////////////////////////////

  public void updateContainerExit(int containerID) {

    int numListeners = wrModelListeners.size();

    for (int i=0; i < numListeners; i++) {
      WRModelListener listener = (WRModelListener) wrModelListeners.elementAt(i);
      listener.processCTokExit(containerID);
    }
  }

 ////////////////////  update token exit /////////////////////////////

  public void updateTokenExit(PTokModel ptok) {

    int numListeners = wrModelListeners.size();

    for (int i=0; i < numListeners; i++) {
      WRModelListener listener = (WRModelListener) wrModelListeners.elementAt(i);
      listener.processPTokExit(ptok);
    }
  }



 ////////////////////  update token entrance /////////////////////////////

  public void updateTokenEntrance(PTokModel ptok) {

    int numListeners = wrModelListeners.size();

    for (int i=0; i < numListeners; i++) {
      WRModelListener listener = 
         (WRModelListener) wrModelListeners.elementAt(i);

      if (listener == null) {
        dbg("updateTokEntrance: null listener");
	return;
      }

      listener.processPTokEntrance(ptok);
    }
  }

 ////////////////////  update Relationship Listeners /////////////////////////////

  public void updateWRelListeners(WRackRels wrackRels) {

    int numListeners = wrModelListeners.size();

    for (int i=0; i < numListeners; i++) {
      WRModelListener listener = (WRModelListener) wrModelListeners.elementAt(i);
      listener.processWRelUpdate(wrackRels);
    }
  }


 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("WRackModel." + (dcnt++) + ": " + s);
  } 

}

//// END ////

