// QueryRack pot/switch monitor test
// Brygg Ullmer, MIT Media Lab
// Begun April 29, 2001

// @author  Brygg Ullmer
// @version v0.1

import java.io.*;
import java.util.*;
import javax.comm.*;

//////////////////////////////////////////////////////////
///////////////// Class WRackTest //////////////////////
//////////////////////////////////////////////////////////

public class WRackTest implements WRListener {

////////////////// members //////////////////////

    WRackReader reader = null;

////////////////// methods //////////////////////

//  public WRackTest() 
//  public void potUpdateOccurred(int whichPot, int whichVal); 
//  public void switchUpdateOccurred(); 


///////////////////////////////////////////////
///////////////// bodies //////////////////////
///////////////////////////////////////////////

////////////////// constructor //////////////////////

    public WRackTest () {

      reader = new WRackReader();
      reader.setListener(this);
    }

////////////////// potUpdateOccurred //////////////////////

  public void potUpdateOccurred(int whichPot, int whichVal) {

    dbg("potUpdateOccurred: " + 
         whichPot + " pot, " + 
         whichVal + " val");
  }

////////////////// switchUpdateOccurred //////////////////////

  public void switchUpdateOccurred() {

    dbg("switchUpdateOccurred: switchState " + reader.switchState);
  }

 ///////////////////// Debug ///////////////////////

  public static int dcnt;

  public void dbg(String s) {

    System.out.println("WRackTest." + (dcnt++) + ": " + s);
  } 
}

//// END ////

