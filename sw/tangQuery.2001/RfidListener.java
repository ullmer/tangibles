// Event interface to RfidReader
// Brygg Ullmer, MIT Media Lab
// Begun April 30, 2001

// @author  Brygg Ullmer
// @version v0.1

public interface RfidListener {

  public void rfidUpdateOccurred(int whichCell, boolean whatState, int whatVal);
}

//// END ////

