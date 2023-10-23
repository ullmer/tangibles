/// Parameter token adjacency relation
/// By Brygg Ullmer, MIT Media Lab
/// Begun October 25, 2001

import java.util.*;
import java.io.*;

///////////////////////////////////////////////////////////
//////////////////////  PToks active //////////////////////
///////////////////////////////////////////////////////////


  // NOTE: implementing this quickly, partly as a placeholder
  // Eventually, will need to become a more abstract class, with
  // children to handle the bounds types of different parameters


public class PToksActive {

/////////////  METHODS ///////////////

// public PToksActive ()
// public void tokWitnessed(int tokId, int whichCell)

/////////////  MEMBERS ///////////////

  boolean verbose = true;

//  Hashtable activePTokHash = null;
  Vector    activePTokVect = null;

  PTokDbase ptokDbase = null;

  WRackModel parentRack = null;

///////////////////////////////////////////////////////////
////////////////////  BODIES  /////////////////////////////
///////////////////////////////////////////////////////////

 ////////////////////  constructor /////////////////////////////

  public PToksActive(WRackModel parentRack) {

    activePTokVect = new Vector();
    this.parentRack = parentRack;

    ptokDbase = parentRack.ptokDb;

    if (ptokDbase == null) {
      dbg("PToksActive constructor alert: null ptokDbase!");
    }

//  activePTokHash = new Hashtable();
  }
  
 ///////////////////// isPTokPresent /////////////////////

  public boolean isPTokPresent(String visLabel) {

    PTokModel result = getPTok(visLabel);
    if (result == null) {return false;}
    return true;
  }

 ///////////////////// getPTok/////////////////////

  public PTokModel getPTok(String visLabel) {

    int numEls = activePTokVect.size();

    for (int i=0; i < numEls; i++) {

      PTokModel ptok = (PTokModel) activePTokVect.elementAt(i);

      if (visLabel.compareTo(ptok.visLabel) == 0) {
        return ptok;
      }
    }

    return null;
  }

  public PTokModel getPTok(int tokId) {

    PTokModel ptok = ptokDbase.mapId2PTok(tokId); 
    return ptok;
  }

  public PTokModel getPTokInCell(int whichCell) {

    PTokModel ptok = parentRack.getCellContents(whichCell);

    return ptok;
  }
 
///////////////////// tokWitnessed /////////////////////

  public PTokModel tokWitnessed(int tokId, int whichCell) {
    
    PTokModel ptok = null;
    boolean ptokEnters = false;

   try {

    ptok = ptokDbase.mapId2PTok(tokId);

    if (ptok == null) {return null;}

    if (ptok.isTokActive() == false) {
      dbg("ptok " + ptok.paramName + " enters");
      ptokEnters = true;
    } 

    ptok.tokWitnessed();

    if (parentRack.getCellContents(whichCell) != ptok) {
      parentRack.setCellContents(whichCell, ptok);
    }

    ptok.lastCell    = ptok.currentCell;
    ptok.currentCell = whichCell;

    if (ptok.currentCell != ptok.lastCell && ptok.lastCell != -1) {
      dbg("ptok " + ptok.paramName + " moves");

      if (parentRack.getCellContents(ptok.lastCell) == ptok) {
  	  parentRack.setCellContents(ptok.lastCell, null);
      } // only "clear" the old location if we were occupying it
    }


    if (activePTokVect.contains(ptok) == false) {
      activePTokVect.add(ptok);
    }

   } catch (Exception e) {
     dbg("tokWitnessed exception (1) : " + e.toString());
     return null;
   }

   try {
    if (ptokEnters) {
      parentRack.updateTokenEntrance(ptok); // JUST ADDED, 11/05
    }

    return ptok;

   } catch (Exception e) {
     dbg("tokWitnessed exception (2): " + e.toString());
     return null;
   }
  }

 ///////////////////// update /////////////////////

  public void update() {

  //  removeInactivePToks();
  }

 ///////////////////// getActivePToks /////////////////////

  public Vector getActivePToks() {

    //removeInactivePToks();
    return activePTokVect;
  }

///////////////////// tokClaimsDeparture /////////////////////

// fuses removeInactivePToks content

  public void tokClaimsDeparture(int tokId, int whichCell) {

    PTokModel ptok = ptokDbase.mapId2PTok(tokId);

    //if (ptok == null) {return null;}

    if (ptok == null) {
      dbg("tokClaimsDeparture: null token exit event");
      return;
    }

    int len = activePTokVect.size();
    Vector deleteList = null;
  
    // scan for candidates, building a list containing them if necessary

    try {
  
      if (parentRack.getCellContents(ptok.currentCell) == ptok) {
 	parentRack.setCellContents(ptok.currentCell, null);
      } // only "clear" the old location if we were occupying it
  	
      ptok.currentCell = -1;
      activePTokVect.removeElement(ptok);
      parentRack.updateTokenExit(ptok);
  
      dbg("ptok " + ptok.paramName + " exits");

    } catch (Exception e) {
      dbg("removeInactivePToks: " + e.toString());
    }
  }
  
 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("PToksActive." + (dcnt++) + ": " + s);
  } 
}  

//// END ////

