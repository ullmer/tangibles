// Event interface to QRackReader
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

public interface WRListener {

  public void potUpdateOccurred(int whichPot, int whichVal); 
  public void switchUpdateOccurred(); 

//  public void switchUpdateOccurred(int whichSwitch, int whichVal); 
}

//// END ////

