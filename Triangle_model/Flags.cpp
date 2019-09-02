#include "global.h"
#include "Flags.h"

using namespace std;

Flags flags;

void Flags::displayFlags(ostream& out)
{
	out << "Current flags are..." << endl;
	out << "mode: " << mode << endl;
	out << "timing: " << timing << endl;
	return;
}
