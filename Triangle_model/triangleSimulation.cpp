/////////////////////////////////////////////
///  Research Triangle Water Supply Model ///
////////////  For use with MOEA /////////////


#include "global.h"
#include "Simulation.h"
#include "moeaframework.h"

#ifdef PARALLEL
	#include <mpi.h>
	//#include "borgProblemDefinition.h"
	//#include "cborg/borgms.h"
#endif

using namespace std;

void usage(int argc, char* argv[])
{
	cerr << "Usage: " << argv[0] << " [OPTIONS]" << endl;
	cerr << "-m <mode> \t Mode. Options are batch and interactive. REQUIRED." << endl;
	cerr << "-r <realizations> \t Number of realizations. REQUIRED." << endl;
	cerr << "-c <formulation> \t Constraint options.  REQUIRED."<<endl;
	cerr << "-b <BORG Interface toggle> \t BORG interface options or write output to file.  REQUIRED." <<endl;
	cerr << "-t <on/off> \t Timing. (optional, default is off)" << endl;
	cerr << "-s <seed> \t Seed. (optional)." << endl;
	cerr << "-h Help (this screen)." << endl;

	exit(-1);	
	return;
}
//Definition for run types:
// -m batch: batch method, for connection to MOEA
// -m interactive: input decision variables at prompt
// -rX: run model simulations using X number of realizations (different streamflow records)
// -cX: user defined scenario X
//		X = 0; 3 objective formulation
//		X = 1; 4 objective formulation
//		X = 2; 5 objective formulation
//		X = 3; 5 objective formulation
//		X = 4; 5 objective formulation
//		X = 4; 6 objective formulation
// -bX: toggle MOEA on/off
//		X = 0;  on, objectives minimize the maximum individual utility objective
//		X = 1;  on, objectives are additive
//		X = 1; off - requires decision variable file


// Global simulation object
Simulation simulation;

void calculationWrapperFunction(double *xreal, double *obj, double *constr)
{
	simulation.calculation(xreal, obj, constr);
}

int main (int argc, char *argv[])
{

// -----------------------------------------------------------------------------------------------------------
// 				READ COMMAND-LINE PARAMETERS AND INITIALIZE PROGRAM
//------------------------------------------------------------------------------------------------------------
	
	int opt;
	//int seed = (int)time(NULL);
	int seed = 1;
	int numRealizations;
	MPI_Init(&argc,&argv);
	int rank, size; 
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);


	flags.timing = "unset";
	while ((opt = getopt(argc, argv, "m:r:c:b:t:s:z:h")) != -1)
	{
		switch (opt)
		{
			case 'm':
				flags.mode = optarg;
				break;
			case 'r':
				numRealizations = atoi(optarg);
				break;
			case 'c':
				simulation.formulation = atoi(optarg);
				break;
			case 'b':
				simulation.borgToggle = atoi(optarg);
				break;
			case 't':
				flags.timing = optarg;
				break;
			case 's':
				seed = atoi(optarg);
				break;
			case 'z':
				simulation.solutionNumber = atoi(optarg);
				break;
			case 'h':
				usage(argc, argv);
				break;
			case 'p':
				compSolNumber = atoi(optarg);
			default:
				usage(argc, argv);
				break;
		}
	}

	//check required parameters
	if (flags.mode != "batch" && flags.mode != "interactive" && flags.mode != "fromfile")
	{
		cerr << "Error! Mode is wrong." << endl;
		exit(-1);
	} 
	if (numRealizations == 0)
	{
		cerr << "Error! Number of realizations not given." << endl;
		exit(-1);
	}
	
	//set defaults
	simulation.setNumRealizations(numRealizations);
	
	int startYear = 2010;
	int endYear = 2025;
	
	int terminateYear = endYear-startYear+1;
	simulation.setNumYears(terminateYear);

	//seed random number generator
	// NOTE: for model, the seed stays the same. For Borg, the seed comes from command line argument.
	srand(1);
	
	//variables for interfacing with algorithm
	int c_num_dec = 31;
	double *c_xreal; 
	general_1d_allocate(c_xreal, c_num_dec);	
	
	simulation.setNumDecisions(c_num_dec);
	
	// Import historical demand and inflow datasets
	//cout << "import data files" << endl;
	simulation.importDataFiles();
	
	// Set water prices and consumer elasticity, 

	//cout << "write data lists" << endl;
	simulation.writeDataLists();
	
	// 'Whiten' demand and inflow data, generate joint PDFs,	
	//cout << "precondition data" << endl;
	// (Here pass in 1's because we don't want to scale the demand yet).
	simulation.preconditionData(1.0, 1.0, true);

	// Weighted average water prices and consumer surplus losses
	// these functions create water use distribution matricies that show the breakdown of water use into different price tiers/elasticity types as restrictions are implemented
	// output from these functions is used by the simulation.calc_Water_Surcharge functions inside the MOEA to determine:
	
	// 1 - the average revenue each utility aquires per MG of water sold (based on month and restriction stage)
	// 2 - the consumer surplus loss per MG of water sold that would occur during prescribed use restrictions and price increases (based on month and restriction stage)
	// 3 - total reduction in water use from a given combination of restrictions and price increases 
	
	// FOR RDM, these functions need to happen at the beginning of every calculation
	// (Because the underlying variables change)
	
	// cout << "calc water prices" << endl;
	//simulation.calculateWaterPrices();
	//simulation.calculateWaterSurcharges();

	//Generates synthetic streamflows using the autocorrelated bootstrap technique.
	//Streamflows records have weekly values with a length of 52*(terminateYear)
	//there are a number of streamflow records generated equal to (numRealizations)
	//cout << "generate streamflows" << endl;
	simulation.generateStreamflows();
	//simulation.correlateDemandVariations();
	
	//Reservoir risk of failure uses historical streamflow records to determine the probability that reservoir storage will drop below
	//20% of storage capacity within a period of 52 weeks for a given storage level, week of the year, and average consumer demand
	//Risk of failure is used in determining triggers for water transfers
	
	//Function not needed - data is inputted from file
	//simulation.createRiskOfFailure();

	//initialize comm time counter
	timing.timeComm = 0.0;
	timing.timeRandom = 0.0;
	double *c_obj = NULL, *c_constr = NULL;
	//int c_num_obj;
	int c_num_constr;
	/*
	if (simulation.borgToggle < 3)
	{
		if (simulation.formulation == 0)
		{
			c_num_obj = 3;//Number of objective variables
			c_num_constr = 3;//Objective variable formulation
		}
		else if (simulation.formulation == 1)
		{
			c_num_obj = 3;//Number of objective variables
			c_num_constr = 3;//Objective variable formulation
		}
		else if (simulation.formulation == 2)
		{
			c_num_obj = 4;//Number of objective variables
			c_num_constr = 4;//Objective variable formulation
		}
		else if (simulation.formulation == 3)// Five objective formulation, using reliability, restriction frequency, average transfer volume, 
		{								   // mitigation cost, and frequency of mitigation exceedence, using no mitigation						   
			c_num_obj = 5;//Number of objective variables
			c_num_constr = 5;//Objective variable simulation.formulation
		}
		else if (simulation.formulation == 4)// Five objective formulation, using reliability, restriction frequency, average transfer volume, 
		{								   // mitigation cost, and frequency of mitigation exceedence using only contingency funds for mitigation
			c_num_obj = 5;//Number of objective variables
			c_num_constr = 5;//Objective variable formulation
		}
		else if (simulation.formulation == 5)// Five objective formulation, using reliability, restriction frequency, average transfer volume, 
		{								   // mitigation cost, and frequency of mitigation exceedence using contingency funds and third party insurance
			c_num_obj = 5;//Number of objective variables
			c_num_constr = 5;//Objective variable formulation
		}
		else//Six objective formulation, using reliability, restriction frequency, average transfer volume, 
		{								   // mitigation cost, frequency of mitigation exceedence, and drought surcharge burden on consumers
										   //Includes drought surcharges
			c_num_obj = 6;//Number of objective variables
			c_num_constr = 6;//Objective variable formulation
		}
		
		// JDH 11/12: Turning off constraints for now (below here, only for parallel version)
		c_num_constr = 0;
		general_1d_allocate(c_obj, c_num_obj);
		//general_1d_allocate(c_constr, c_num_constr);
		
		simulation.initializeFormulation(c_num_obj, c_num_constr); // number of decisions, objectives, constraints
		
		// Interface with Borg-MS (parallel)
		#ifdef PARALLEL
			
			// BORG_Debug_on();
			// BORG_Algorithm_ms_max_time(0.008);
			// BORG_Algorithm_output_aerovis();
			
			//char runtime[256];
			char outputFilename[256];
			FILE* outputFile = NULL;
			// char timing[256];	
			
			BORG_Algorithm_ms_startup(&argc, &argv);
			BORG_Algorithm_ms_max_evaluations(1000000);
			//BORG_Algorithm_output_frequency(50000);
			BORG_Problem problem = BORG_Problem_create(c_num_dec, c_num_obj, c_num_constr, calculationWrapperFunction);
			
			// Set all the parameter bounds and epsilons
			setProblemDefinition(problem, simulation.formulation);
			
			// This is set up to run only one seed at a time.
			
			//sprintf(runtime, "./output/O%d_F%d/CBorg_NCTriangle_O%d_F%d_S%d.runtime", simulation.borgToggle, simulation.formulation, simulation.borgToggle, simulation.formulation, seed);
			sprintf(outputFilename, "./output/O%d_F%d/CBorg_NCTriangle_O%d_F%d_S%d.set", simulation.borgToggle, simulation.formulation, simulation.borgToggle, simulation.formulation, seed);
			//sprintf(timing, "timing_%d_%%d.txt", params.filename_base.c_str(), i); // %%d is replaced with rank
			
			//BORG_Algorithm_output_runtime(runtime);
			//BORG_Algorithm_output_timing(timing);

			BORG_Random_seed(seed);
			BORG_Archive result = BORG_Algorithm_ms_run(problem);
			
			// If this is the master node, print out the final archive
			if (result != NULL) { 
				outputFile = fopen(outputFilename, "w");
				BORG_Archive_print(result, outputFile);
				BORG_Archive_destroy(result);
				fclose(outputFile);
			}
			
			BORG_Algorithm_ms_shutdown();
			BORG_Problem_destroy(problem);
		
		#else // Interface with MOEA Framework
			
			MOEA_Init(c_num_obj, c_num_constr); // pass number of objectives and formulation to MOEA
			
			while (MOEA_Next_solution() == MOEA_SUCCESS)
			{
				MOEA_Read_doubles(c_num_dec, c_xreal);//Input decision variables
				simulation.calculation(c_xreal, c_obj, c_constr); // Run simulation iteration
				MOEA_Write(c_obj, c_constr);//write new objective functions
			}
			
		#endif
					
	}
	*/

	//else // If running from parameter input file (no constraints here)
	//{
	int c_num_obj = 24;
	general_1d_allocate(c_obj, c_num_obj);
	simulation.initializeFormulation(c_num_obj, 0);
	
	//cout << "running simulations" << endl;
	
	// Read a certain number of parameter sets from a file (8, 9, 215, 84)
	//int formulationSolutions[] = {-1, 8, 9, -1, 215, 84, -1};
	//int formulationSolutions[] = {-1, 8, 9, -1, 215, 2957, -1};
	//int numSolutions = formulationSolutions[simulation.formulation];
	//int numSolutions = 8;
	int numSolutions = 1;
	char paramfilebuffer[1024];
	//int compSolNumber = 1113;
	// sprintf(paramfilebuffer, "./inputfiles/parameterInputFile_O0_F%d.csv", simulation.formulation);
	//sprintf(paramfilebuffer, "./Compromise_sols_reevaluation.reference");

	//sprintf(paramfilebuffer, "./Triangle_13_DV.csv");


	//sprintf(paramfilebuffer, "./Perturbed_DVs/all_perturbations%d.csv", rank);
	sprintf(paramfilebuffer, "./Perturbed_DVs/Solution_%d/sample_%d.csv", compSolNumber, rank);
	//sprintf(paramfilebuffer, "./Perturbed_DVs_2018/original/Solution_%d.csv", rank);
	readFile(simulation.parameterInput, paramfilebuffer, numSolutions, c_num_dec);
	//readFile(simulation.parameterInput, "./Compromise_sols_reevaluation.csv", numSolutions, c_num_dec+1);
	//sprintf(paramfilebuffer, "./Bsols.csv", simulation.formulation);	
	//readFile(simulation.parameterInput, paramfilebuffer, numSolutions, c_num_dec);

	// Read RDM factors from file
	readFile(simulation.RDMInput, "./RDMSamples_1000.csv", 1000, simulation.num_rdm_factors);
	
	// Set up the output stream for objective values
	ofstream out1;
	char outfilebuffer[1024];
	
	//int compSolNumber = simulation.parameterInput[0][0];

	for (int i = 0; i < numSolutions; i++)
	{
	sprintf(outfilebuffer, "./output/DU/Solution_%d/sample_%d_sol.rdm", compSolNumber, rank);
	//sprintf(outfilebuffer, "./output_2018/DU/original/Solution_%d.rdm", compSolNumber);
	openFile(out1, outfilebuffer);
	//	cout << i << endl;
	simulation.solutionNumber = i;
	
	//cout<< "Input read for rank: " << rank << endl;
	//cout << "parameter input for rank " << rank << endl;
	/*for (int i =1; i < c_num_dec+1; i++)
	{
		cout << simulation.parameterInput[simulation.solutionNumber][i] << " ";
	}
	cout << endl;
	*/

	//sprintf(outfilebuffer, "./output/WCU/Solution_%d.rdm", rank);
	//openFile(out1, outfilebuffer);
	//cout << "Running calcs solution " << compSolNumber << endl;
	for (int r = 0; r < 1000; r++)
	{
		simulation.rdmNumber = r;
		
		simulation.calculation(c_xreal, c_obj, c_constr);
		for (int x = 0; x < c_num_obj; x++)
		{
			out1 << c_obj[x] << " ";
		}
		out1 << endl;
	}
	
	out1.close();
		}
	//out1.close();
	//}

	MPI_Finalize();
	zap(c_obj);
	zap(c_xreal);
	zap(c_constr);

	return 0;
}
