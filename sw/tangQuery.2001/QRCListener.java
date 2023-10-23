// Event interface to DbThread
// Brygg Ullmer, MIT Media Lab
// Begun April 28, 2001

// @author  Brygg Ullmer
// @version v0.1

public interface QRCListener {

  public void processParamUpdate(int rackId, int cellId, int tokId, 
                                          int bound1, int bound2);

  public void processReedUpdate(int reedLoc, int reedState);

  public void processAxisUpdate (int rackId, int cellId, int tokId, 
                                          int bound1, int bound2);

}

//// END ////

