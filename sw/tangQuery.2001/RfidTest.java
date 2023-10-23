// Rfid reader monitor test
// Brygg Ullmer, MIT Media Lab
// Begun April 30, 2001

// @author  Brygg Ullmer
// @version v0.1

import java.io.*;
import java.util.*;
import javax.comm.*;

//////////////////////////////////////////////////////////
///////////////// Class RfidTest //////////////////////
//////////////////////////////////////////////////////////

public class RfidTest implements RfidListener {

////////////////// members //////////////////////

    RfidReader reader = null;

////////////////// methods //////////////////////

// public RfidTest() 
// public void rfidUpdateOccurred(int whichCell, boolean whatState, int whatVal)
// public void switchUpdateOccurred(); 


///////////////////////////////////////////////
///////////////// bodies //////////////////////
///////////////////////////////////////////////

////////////////// constructor //////////////////////

    public RfidTest () {

      reader = new RfidReader();
      reader.setListener(this);
    }

////////////////// rfidUpdateOccurred //////////////////////

 public void rfidUpdateOccurred(int whichCell, boolean whatState, int whatVal) {

    dbg("rfidUpdateOccurred: " + 
         whichCell + " cell, " + 
         whatState + " state, " + 
         whatVal   + " val");
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("RfidTest." + (dcnt++) + ": " + s);
  } 
}

//// END ////

