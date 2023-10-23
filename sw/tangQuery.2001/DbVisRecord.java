// Display server for QueryUI
// By Brygg Ullmer, MIT Media Lab

// Descended from MediaFlow DbVisRecord
// Begun October 9, 2000
// Reworked on May 2, 2001

import java.net.*;
import java.io.*;
import java.util.*;

//////////////////////////////////////////////////////
/////////////////// Dbase Thread /////////////////////
//////////////////////////////////////////////////////

public class DbVisRecord {

//////////////////// members /////////////////////

  // String tableName;

//  public Integer recordId    = -1;
//  public Integer cellPos     = -1;

  public Integer recordId    = null;
  public Integer cellPos     = null;

  public String  recordLabel = null;
  public String  recordImage = null; // 

//////////////////// methods /////////////////////

//  public DbVisRecord() 

/////////////////////////////////////////////////
//////////////////// bodies /////////////////////
/////////////////////////////////////////////////

///////////// constructor ///////////////

  public DbVisRecord() {
  }

/////////////////////// dbg ///////////////////////

  public static int dcnt;
  public static void dbg(String s) {
    System.out.println("DbVisRecord[" + (dcnt++) + "] " + s);
  }
}

/// END ///

 
