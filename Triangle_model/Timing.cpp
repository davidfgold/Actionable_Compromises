#include "global.h"
#include "Timing.h"

using namespace std;

Timing timing;

void Timing::openTimingFile(string filename)
{
	openFile(out, filename);
	return;
}

void Timing::closeTimingFile()
{
	out.close();
	return;
}

void Timing::write(string input)
{
	out << input << " ";
	return;
}

void Timing::write(double input)
{
	out << input;
	return;
}
