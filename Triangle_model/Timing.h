#ifndef Timing_h
#define Timing_h

class Timing
{
public:
	clock_t startFileRead, endFileRead;
	clock_t startComm, endComm;
	double timeComm;
	clock_t startRandom, endRandom;
	double timeRandom;	
	void openTimingFile(string filename);
	void closeTimingFile();
	void write(double input);
	void write(string input);

private:
	ofstream out;
};

#endif
