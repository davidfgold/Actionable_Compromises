#include "global.h"
#include "ReservoirStorage.h"

using namespace std;

//ReservoirStorage::ReservoirStorage()
//{
//}

void ReservoirStorage::initializeReservoirStorage(double durhamCap, double CCRCap, double StQCap, double ULCap, double lakeWBCap, double fallsLakeSupplyCap, double fallsLakeQualityCap, 
													double jordanSupplyCap, double jordanQualityCap, double CaryTreatmentCap, double DurhamCaryCap, double DurhamOWASACap, 
													double RaleighCaryCap, double raleighJordanAlloc, double durhamJordanAlloc, double owasaJordanAlloc, double caryJordanAlloc)
{
	//Set reservoir capacities and initial storage volumes
	durhamCapacity=durhamCap;//Durham capacity
	durhamStorage=durhamCap;//Initial storage set to capacity
	CCRCapacity = CCRCap;//OWASA Cane Creek reservoir capacity
	CCRStorage = CCRCap;//Initial storage set to capacity
	ULCapacity = ULCap;//OWASA University Lake reservoir capacity
	ULStorage = ULCap;//Initial storage set to capacity
	StQCapacity = StQCap;//OWASA Stone Quarry reservoir capacity
	StQStorage = StQCap;//Initial storage set to capacity
	OWASACapacity = CCRCap+StQCap+ULCap;//OWASA total capacity
	OWASAStorage = OWASACapacity;//Initial storage set to capacity
	lakeWBCapacity = lakeWBCap;//Raleigh Lakes Wheeler and Benson capacity
	fallsLakeSupplyCapacity = fallsLakeSupplyCap;//Capacity of Falls Lake Water Supply allocation
	fallsLakeQualityCapacity = fallsLakeQualityCap;//Capacity of Falls Lake Water Quality allocation
	lakeWBStorage = lakeWBCap;//Initial storage set to capacity
	fallsLakeSupplyStorage = fallsLakeSupplyCap;//Initial storage set to capacity
	fallsLakeQualityStorage = fallsLakeQualityCap;//Initial storage set to capacity
	jordanLakeSupplyCapacity = jordanSupplyCap;
	jordanLakeQualityCapacity = jordanQualityCap;
	jordanLakeSupplyStorage = jordanSupplyCap;
	jordanLakeQualityStorage = jordanQualityCap;
	CaryTreatmentCapacity = CaryTreatmentCap;//Cary WTP capacity
	DurhamCaryCapacity = DurhamCaryCap;//Capacity of the Durham Cary interconnection
	DurhamOWASACapacity = DurhamOWASACap;//Capacity of the Durham OWASA interconnection
	RaleighCaryCapacity = RaleighCaryCap;//Capacity of the Raleigh Cary interconnection
	durhamRequest = 0;//Durham intial transfer request
	owasaRequest = 0;//OWASA initial transfer request
	raleighRequest = 0;//Raleigh initial transfer request
	raleighAllocation = raleighJordanAlloc;
	caryAllocation = caryJordanAlloc;
	durhamAllocation = durhamJordanAlloc;
	owasaAllocation = owasaJordanAlloc;
	caryJordanCapacity = caryJordanAlloc*jordanLakeSupplyCapacity;
	caryJordanStorage = caryJordanCapacity;
	raleighJordanCapacity = raleighJordanAlloc*jordanLakeSupplyCapacity;
	raleighJordanStorage = raleighJordanCapacity;
	durhamJordanCapacity = durhamJordanAlloc*jordanLakeSupplyCapacity;
	durhamJordanStorage = durhamJordanCapacity;
	owasaJordanCapacity = owasaJordanAlloc*jordanLakeSupplyCapacity;
	owasaJordanStorage = owasaJordanCapacity;
	jordanQualityFraction = 94600/(45800+94600);
	jordanRaleighFraction = raleighAllocation*45800/(94600+45800);
	jordanDurhamFraction = durhamAllocation*45800/(94600+45800);
	jordanCaryFraction = caryAllocation*45800/(94600+45800);
	jordanOWASAFraction = owasaAllocation*45800/(94600+45800);
	return;
}

void ReservoirStorage::initializeReservoirStorageROF(double durhamCap, double CCRCap, double StQCap, double ULCap, double lakeWBCap, double fallsLakeSupplyCap, double fallsLakeQualityCap, 
	double durhamStor, double CCRStor, double StQStor, double ULStor, double lakeWBStor, double fallsLakeSupplyStor, double fallsLakeQualityStor, double CaryTreatmentCap, double DurhamCaryCap, 
	double DurhamOWASACap, double RaleighCaryCap)
{
	//Same as above, allowing for variable initial reservoir storage
	durhamCapacity=durhamCap;
	durhamStorage=durhamStor;
	CCRCapacity = CCRCap;
	CCRStorage = CCRStor;
	ULCapacity = ULCap;
	ULStorage = ULStor;
	StQCapacity = StQCap;
	StQStorage = StQStor;
	OWASACapacity = CCRCap+StQCap+ULCap;
	OWASAStorage = CCRStorage+ULStorage+StQStorage;
	lakeWBCapacity = lakeWBCap;
	fallsLakeSupplyCapacity = fallsLakeSupplyCap;
	fallsLakeQualityCapacity = fallsLakeQualityCap;
	lakeWBStorage = lakeWBStor;
	fallsLakeSupplyStorage = fallsLakeSupplyStor;
	fallsLakeQualityStorage = fallsLakeQualityStor;
	CaryTreatmentCapacity = CaryTreatmentCap;
	DurhamCaryCapacity = DurhamCaryCap;
	DurhamOWASACapacity = DurhamOWASACap;
	RaleighCaryCapacity = RaleighCaryCap;
	durhamRequest = 0;
	owasaRequest = 0;
	raleighRequest = 0;
	return;
}
void ReservoirStorage::openResFiles()
{
	openFile(out2, "reservoirOutput2.csv");
	return;
}

void ReservoirStorage::setDemands(double durham, double owasa, double raleigh, double cary, int numberOfDaysInTheWeek)
{
	durhamUse = durham;
	OWASAUse = owasa;
	CaryUse = cary;
	raleighUse = raleigh;
	numdays = numberOfDaysInTheWeek;
	return;
}

void ReservoirStorage::getReturnRatios(double raleighR, double durhamR)
{
	raleighReturn = raleighR;
	durhamReturn = durhamR;
	return;
}

void ReservoirStorage::calcTransfers(double transferDurham, double durhamRisk, double transferOWASA, double owasaRisk, double transferRaleigh, double raleighRisk, double OWASAD)
{
	percentFull_O = OWASAStorage/OWASACapacity;//Actual OWASA reservoir storage
	percentFull_D = durhamStorage/durhamCapacity;//Actual Durham reservoir storage
	percentFull_R = (fallsLakeSupplyStorage)/(fallsLakeSupplyCapacity);//Actual Raleigh reservoir storage
	//Determines how much water each utility needs to request to reach an acceptable risk-of-failure
	if (percentFull_O<transferOWASA)
		owasaRequestInt = (transferOWASA-percentFull_O)*OWASACapacity;
	else
		owasaRequestInt = 0;
			
	if (percentFull_D<transferDurham)
		durhamRequestInt = (transferDurham-percentFull_D)*durhamCapacity;
	else
		durhamRequestInt = 0;
	
	if (percentFull_R<transferRaleigh)
		raleighRequestInt = (transferRaleigh - percentFull_R)*(fallsLakeSupplyCapacity);
	else
		raleighRequestInt = 0;
	
	
	owasaRequest = owasaRequestInt;
	durhamRequest = durhamRequestInt;
	raleighRequest = raleighRequestInt;
	
	caryTreatmentBuffer = 5.0*numdays;
	caryPeakingFactor = .85;
	caryExtraCapacity = (CaryTreatmentCapacity*numdays - caryTreatmentBuffer)*caryPeakingFactor - CaryUse;//Cary WTP spare capacity for transfers
	DurhamOWASACapacity = 7*numdays;//Capacity of Durham/OWASA interconnection
	double OWASAminimumUse = 3*numdays;
	double DCCap = DurhamCaryCapacity*numdays;//Weekly capacity of the Durham-Cary interconnection
	double RCCap = RaleighCaryCapacity*numdays;//Weekly capacity of the Raleigh-Cary interconnection
	double raleighExtra = 0;
	double durhamExtra = 0;
	
	if (OWASAD-DurhamOWASACapacity<OWASAminimumUse)//OWASA WTP needs to process at least 3MGD (transfers cannot reduce OWASAs demand on its own sources to less than 3 MGD)
	{
		DurhamOWASACapacity = OWASAD-OWASAminimumUse;
	}
	if (DurhamOWASACapacity<0)
	{
		DurhamOWASACapacity = 0;
	}
	if (caryExtraCapacity<0)//No transfers if Cary does not have the extra treatment capacity
	{
		caryExtraCapacity=0;
		durhamRequest = 0;
		owasaRequest = 0;
		raleighRequest = 0;
	}
	else if ((durhamRequest+owasaRequest+raleighRequest)>caryExtraCapacity)//Adjust requests to take consideration of Cary's transfer capacity
	{
		if ((raleighRisk+owasaRisk+durhamRisk)==0)
		{
			durhamRequest = 0;
			owasaRequest = 0;
			raleighRequest = 0;
		}
		else
		{
			durhamRequest = caryExtraCapacity*durhamRisk/(raleighRisk+owasaRisk+durhamRisk);
			owasaRequest = caryExtraCapacity*owasaRisk/(raleighRisk+owasaRisk+durhamRisk);
			raleighRequest = caryExtraCapacity*raleighRisk/(raleighRisk+owasaRisk+durhamRisk);
		}
	}
	if (raleighRequest>RCCap)//Make sure Raleigh's request does not exceed its interconnection capacity
	{
		raleighExtra = raleighRequest - RCCap;//If Raleigh can not take all of the water allotted to it, the extra water is available to Durham and OWASA
		raleighRequest = RCCap;
		if ((durhamRequest+owasaRequest+raleighExtra) > DCCap)//Make sure Durham can take all the additional water
		{
			if ((durhamRisk+owasaRisk)==0)
			{
				durhamRequest = 0;
				owasaRequest = 0;
			}
			else
			{
				durhamRequest = DCCap*durhamRisk/(durhamRisk+owasaRisk);
				if (durhamRequest>durhamRequestInt)
				{
					durhamExtra = durhamRequest-durhamRequestInt;
					durhamRequest = durhamRequestInt;
				}
				owasaRequest = DCCap*owasaRisk/(durhamRisk+owasaRisk)+durhamExtra;
				if (owasaRequest>owasaRequestInt)
				{
					owasaRequest = owasaRequestInt;
				}
			}
		}
		if (owasaRequest>DurhamOWASACapacity)//Make sure OWASA can take its allottment of water, if not, Durham can hold on to the extra water
		{
			owasaRequest = DurhamOWASACapacity;
			durhamRequest = durhamRequest + owasaRequest - DurhamOWASACapacity;
		}
	}
	else if ((durhamRequest+owasaRequest) > DCCap)//Make sure Durham/OWASA's request does not exceed ints interconnection capacity
	{	
		if ((durhamRisk+owasaRisk)==0)
		{
			durhamExtra = durhamRequest +owasaRequest;
			durhamRequest = 0;
			owasaRequest = 0;
		}
		else
		{
			durhamExtra = durhamRequest + owasaRequest - DCCap;
			durhamRequest = DCCap*durhamRisk/(durhamRisk+owasaRisk);
			owasaRequest = DCCap*owasaRisk/(durhamRisk+owasaRisk);
		}
		if (raleighRequest+durhamExtra>RCCap)//Make sure Raleigh can take all the additional water
		{
			raleighRequest = RCCap;
		}
	}
	if (owasaRequest>owasaRequestInt)
	{
		owasaRequest = owasaRequestInt;
	}
	if (raleighRequest>raleighRequestInt)
	{
		raleighRequest = raleighRequestInt;
	}
	if (durhamRequest>durhamRequestInt)
	{
		durhamRequest = durhamRequestInt;
	}	
	return;
}

void ReservoirStorage::setInflow(double durham, double ccr, double ul, double stq, double falls, double wb, double clayton, double crabtree, double jordan, double lillington,
									double ralRet, double durRet, double durRet2, double owasaRet, double evaporationf, double evaporationwb, double evaporation)
{
	durhamInflow = durham;//Inflows to Durham Reservoirs
	CCRInflow = ccr;//Inflows to Cane Creek Reservoir
	ULInflow = ul;//Infow to University Lake
	StQInflow = stq;//Inflow to Stone Quarry
	fallsInflow = falls;//Inflow to Falls Lake
	wbInflow = wb;//Inflow to Wheeler Benson
	claytonInflow = clayton;//Inflow to clayton gauge
	crabtreeInflow = crabtree;//Inflow to Crabtree Creek
	jordanInflow = jordan;//Inflow to Jordan Lake
	lillingtonInflow = lillington;//Inflows to lillington Gauge
	raleighReturn = ralRet;//Raleigh WW Returns downstream of Falls Lake
	durhamReturn = durRet;//Durham WW Returns to the Neuse Basin
	durhamReturn2 = durRet2;//Durham WW Returns to the Cape Fear Basin
	owasaReturn = owasaRet;//OWASA WW Returns to Cape Fear Basin
	evapF = evaporationf;//Evaporation from Falls Lake
	evapWB = evaporationwb;//Evaporation from Wheeler and Benson
	evap = evaporation;//Evaporation from Durham and OWASA
	return;
}

void ReservoirStorage::setSpillover(int week)
{
	if (week <21 || week>47)//Spillage rules for Durham Reservoir at Little River
		durhamSpillage = 3.877*numdays;
	else
		durhamSpillage = 9.05;
	return;
}

void ReservoirStorage::updateStorage(int week)
{			
	durhamStorage = durhamStorage + durhamInflow + durhamRequest - durhamUse - evap*1069 - durhamSpillage;//Durham reservoirs modeled as one
	
	if (durhamStorage>durhamCapacity)
	{
		durhamSpillage+=durhamStorage - durhamCapacity;
		durhamStorage=durhamCapacity;
	}
	if (durhamStorage<0)
		durhamStorage = 0;

	double raleighDemand1, raleighDemand2;//Demand from WTP drawing from Lakes Wheeler and Benson (1) and WTP drawing from Falls Lake (2)
	raleighDemand1 = .25*numdays;
	raleighDemand2 = raleighUse-raleighDemand1;
	if (raleighDemand2<36*numdays)//Treatment plant must run at at least 36 MGD
	{
		raleighDemand2 = 36*numdays;
		raleighDemand1 = raleighUse - raleighDemand2;
	}

	if (week< 13 || week>43)
	{
		fallsSpillage = numdays*60/1.547;//Mandatory minimum releases at Falls Lake Reservoir
		if ( (fallsSpillage + raleighReturn + claytonInflow + crabtreeInflow) < 130*numdays)//Mandatory Minimum Flows at Clayton Gauge
		{
			fallsSpillage = 130*numdays - raleighReturn - claytonInflow - crabtreeInflow;
		}
	}
	else
	{
		fallsSpillage = 100*numdays/1.547;//Mandatory minimum releases at Falls Lake Reservoir
		if ( (fallsSpillage + raleighReturn + claytonInflow + crabtreeInflow) < 180*numdays)//Mandatory Minimum Flows at Clayton Gauge
		{
			fallsSpillage = 180*numdays - raleighReturn - claytonInflow - crabtreeInflow;
		}
	}
	claytonGage = fallsSpillage + raleighReturn + claytonInflow + crabtreeInflow;
	if (lakeWBStorage <.3*lakeWBCapacity)//Lake Wheeler and Benson water balance
	{
		lakeWBSpillage = numdays/1.547;
	}
	else if (lakeWBStorage<.6*lakeWBCapacity)
	{
		lakeWBSpillage = 2*numdays/1.547;
	}
	else
	{
		lakeWBSpillage = 3*numdays/1.547;
	}
	lakeWBStorage += wbInflow - raleighDemand1 - lakeWBSpillage - (lakeWBStorage*.3675*evapWB);
	if (lakeWBStorage >lakeWBCapacity)
	{
		lakeWBSpillage = lakeWBStorage - lakeWBCapacity;
		lakeWBStorage = lakeWBCapacity;
	}

	if ((fallsLakeSupplyStorage+fallsLakeQualityStorage+5734)<29000)
	{
		fallsArea = .32*(fallsLakeSupplyStorage+fallsLakeQualityStorage+5734);
	}
	else
	{
		fallsArea = .28*(fallsLakeSupplyStorage+fallsLakeQualityStorage+5734);
	}

	fallsSupplyInflow = (fallsInflow + durhamSpillage - fallsArea*evapF + durhamReturn)*(14.7/34.7) +raleighRequest;//Inflows divided between 'water quality' and 'water supply' storage
	fallsQualityInflow = (fallsInflow + durhamSpillage - fallsArea*evapF + durhamReturn)*(20/34.7);

	fallsLakeQualityStorage += fallsQualityInflow - fallsSpillage;//water quality storage provides water for minimum release/downstream flow releases
	if (fallsLakeQualityStorage > fallsLakeQualityCapacity)
	{
		fallsSupplyInflow += fallsLakeQualityStorage - fallsLakeQualityCapacity;
		fallsQualityInflow += fallsLakeQualityCapacity - fallsLakeQualityStorage;
		fallsLakeQualityStorage = fallsLakeQualityCapacity;
	}
	if (fallsLakeQualityStorage<0)
	{
		fallsLakeQualityStorage = 0;
	}
	fallsLakeSupplyStorage += fallsSupplyInflow - raleighDemand2;//water supply storage provides water for municipal use
	if (fallsLakeSupplyStorage>fallsLakeSupplyCapacity)
	{
		// fallsLakeFloodInflow = fallsLakeSupplyStorage - fallsLakeSupplyCapacity;
		fallsLakeSupplyStorage = fallsLakeSupplyCapacity;
	}
	if (fallsLakeSupplyStorage<0)
	{
		fallsLakeSupplyStorage = 0;
	}
	
	CCRStorage+=owasaRequest;
	//Spillage calculated from Cane Creek Reservoir
	if (CCRInflow > 1.797*7)
		OWASASpillage = 1.797*7;
	else if (CCRInflow < .1422*7)
		OWASASpillage = .1422*7;
	else
		OWASASpillage = CCRInflow;
	//Spillage calculated from Stone Quarry
	if (StQStorage +StQInflow - 10*evap>StQCapacity)
	{
		StQSpillage = StQStorage + StQInflow -10*evap - StQCapacity;
		StQStorage = StQCapacity;
	}
	else
	{
		StQStorage = StQStorage + StQInflow - 10*evap;
		StQSpillage = 0;
	}
	
	//OWASA has three reservoirs, and a long list of how they use water from each reservoir
	//Depending on storage levels.  Its not really important to understand exactly how its done.
	if ((ULStorage + ULInflow + StQSpillage - 212*evap - OWASAUse) > .75*ULCapacity)
	{
		ULStorage = ULStorage + ULInflow + StQSpillage - 212*evap - OWASAUse;
		if (ULStorage > ULCapacity)
		{
			OWASASpillage += ULStorage - ULCapacity;
			ULStorage = ULCapacity;
		}
		
		CCRStorage = CCRStorage +CCRInflow - 500*evap - OWASASpillage;
		if (CCRStorage > CCRCapacity)
		{
			OWASASpillage += CCRStorage - CCRCapacity;
			CCRStorage = CCRCapacity;
		}
	}
	else if ((CCRCapacity - (CCRStorage + CCRInflow -500*evap - OWASASpillage))< .25*ULCapacity)
	{
		if (OWASAUse<70)
		{
			ULStorage = ULStorage + ULInflow + StQSpillage - 212*evap;
			if (ULStorage > ULCapacity)
			{
				OWASASpillage += ULStorage - ULCapacity;
				ULStorage = ULCapacity;
			}
		
			CCRStorage = CCRStorage +CCRInflow - 500*evap - OWASASpillage - OWASAUse;
			if (CCRStorage > CCRCapacity)
			{
				OWASASpillage += CCRStorage - CCRCapacity;
				CCRStorage = CCRCapacity;
			}
		}
		else
		{
			ULStorage = ULStorage + ULInflow + StQSpillage - 212*evap - (OWASAUse - 70);
			if (ULStorage > ULCapacity)
			{
				OWASASpillage += ULStorage - ULCapacity;
				ULStorage = ULCapacity;
			}
		
			CCRStorage = CCRStorage +CCRInflow - 500*evap - OWASASpillage - 70;
			if (CCRStorage > CCRCapacity)
			{
				OWASASpillage += CCRStorage - CCRCapacity;
				CCRStorage = CCRCapacity;
			}
		}
	}
	else if ((ULStorage + ULInflow + StQSpillage - evap*212)> .5*OWASAUse)
	{
		ULStorage = ULStorage + ULInflow + StQSpillage - 212*evap - .5*OWASAUse;
		if (ULStorage > ULCapacity)
		{
			OWASASpillage += ULStorage - ULCapacity;
			ULStorage = ULCapacity;
		}
		
		CCRStorage = CCRStorage +CCRInflow - 500*evap - OWASASpillage - .5*OWASAUse;
		if (CCRStorage > CCRCapacity)
		{
			OWASASpillage += CCRStorage - CCRCapacity;
			CCRStorage = CCRCapacity;
		}
	}
	else if ((CCRStorage + CCRInflow -evap*500 - OWASASpillage)>OWASAUse)
	{
		ULStorage = ULStorage + ULInflow + StQSpillage - 212*evap;
		if (ULStorage > ULCapacity)
		{
			OWASASpillage += ULStorage - ULCapacity;
			ULStorage = ULCapacity;
		}
		
		CCRStorage = CCRStorage +CCRInflow - 500*evap - OWASASpillage - OWASAUse;
		if (CCRStorage > CCRCapacity)
		{
			OWASASpillage += CCRStorage - CCRCapacity;
			CCRStorage = CCRCapacity;	
		}
	}
	else
	{
		ULStorage = ULStorage + ULInflow + StQSpillage - evap*212;
		CCRStorage = CCRStorage + CCRInflow - 500*evap - OWASASpillage;
		CCRStorage = CCRStorage + StQStorage + ULStorage;
		ULStorage = 0;
		StQStorage = 0;
		CCRStorage = CCRStorage - OWASAUse;
	}
	if (CCRStorage<0)
	{
		CCRStorage = 0;
	}
	if (ULStorage<0)
	{
		ULStorage = 0;
	}
	if (StQStorage<0)
	{
		StQStorage = 0;
	}
	OWASAStorage = CCRStorage + ULStorage + StQStorage;
	
	if (jordanLakeQualityStorage/jordanLakeQualityCapacity>.4)
	{
		jordanLakeMinRelease = 25.8527*numdays;
		if (jordanLakeQualityStorage/jordanLakeQualityCapacity>.8)
		{
			if(jordanLakeMinRelease+lillingtonInflow<387.7901*numdays)
			{
				jordanLakeMinRelease = 387.7901*numdays-lillingtonInflow;
			}
		}
		else if(jordanLakeQualityStorage/jordanLakeQualityCapacity>.6)
		{
			if(jordanLakeMinRelease+lillingtonInflow<290.8426*numdays)
			{
				jordanLakeMinRelease = 290.8426*numdays-lillingtonInflow;
			}
		}
		else
		{
			if(jordanLakeMinRelease+lillingtonInflow<193.8951*numdays)
			{
				jordanLakeMinRelease = 193.8951*numdays-lillingtonInflow;
			}
		}
	}
	else if (jordanLakeQualityStorage/jordanLakeQualityCapacity>.2)
	{
		jordanLakeMinRelease = 129.2634*numdays;
	}
	else
	{
		jordanLakeMinRelease = 64.6317*numdays;
	}
	
	jordanLakeQualityStorage += (jordanInflow+durhamReturn2+owasaReturn+OWASASpillage-evap*13940)*jordanQualityFraction-jordanLakeMinRelease;
	raleighJordanStorage += (jordanInflow+durhamReturn2+owasaReturn+OWASASpillage-evap*13940)*jordanRaleighFraction - raleighRequest;
	durhamJordanStorage += (jordanInflow+durhamReturn2+owasaReturn+OWASASpillage-evap*13940)*jordanDurhamFraction - durhamRequest;
	owasaJordanStorage += (jordanInflow+durhamReturn2+owasaReturn+OWASASpillage-evap*13940)*jordanOWASAFraction - owasaRequest;
	caryJordanStorage += (jordanInflow+durhamReturn2+owasaReturn+OWASASpillage-evap*13940)*jordanCaryFraction - CaryUse;
	
	if (jordanLakeQualityStorage>jordanLakeQualityCapacity)
	{
		raleighJordanStorage+=raleighAllocation*(jordanLakeQualityStorage-jordanLakeQualityCapacity);
		durhamJordanStorage+=durhamAllocation*(jordanLakeQualityStorage-jordanLakeQualityCapacity);
		owasaJordanStorage+=owasaAllocation*(jordanLakeQualityStorage-jordanLakeQualityCapacity);
		caryJordanStorage+=caryAllocation*(jordanLakeQualityStorage-jordanLakeQualityCapacity);
		jordanLakeQualityStorage=jordanLakeQualityCapacity;
	}
	if (jordanLakeQualityStorage<0)
	{
		jordanLakeQualityStorage = 0;
	}
	if(raleighJordanStorage<0)
	{
		fallsLakeSupplyStorage+=raleighJordanStorage;
		raleighRequest+=raleighJordanStorage;
		if (fallsLakeSupplyStorage<0)
		{
			fallsLakeSupplyStorage = 0;
		}
		if (raleighRequest<0)
		{
			raleighRequest = 0;
		}
		raleighJordanStorage = 0;
	}
	if(raleighJordanStorage>raleighJordanCapacity)
	{
		raleighJordanStorage = raleighJordanCapacity;
	}
	if(durhamJordanStorage<0)
	{
		durhamStorage+=durhamJordanStorage;
		durhamRequest+=durhamJordanStorage;
		if (durhamRequest<0)
		{
			durhamRequest = 0;
		}
		if (durhamStorage<0)
		{
			durhamStorage = 0;
		}
		durhamJordanStorage = 0;
	}
	if(durhamJordanStorage>durhamJordanCapacity)
	{
		durhamJordanStorage = durhamJordanCapacity;
	}
	if(owasaJordanStorage<0)
	{
		CCRStorage+=owasaJordanStorage;
		OWASAStorage+=owasaJordanStorage;
		owasaRequest+=owasaJordanStorage;
		if (owasaRequest<0)
		{
			owasaRequest = 0;
		}
		if (CCRStorage<0)
		{
			CCRStorage = 0;
		}
		if (OWASAStorage <0)
		{
			OWASAStorage = 0;
		}
		owasaJordanStorage = 0;
	}
	if(owasaJordanStorage>owasaJordanCapacity)
	{
		owasaJordanStorage = owasaJordanCapacity;
	}
	if(caryJordanStorage<0)
	{
		caryJordanStorage = 0;
	}
	if(caryJordanStorage>caryJordanCapacity)
	{
		caryJordanStorage = caryJordanCapacity;
	}
	return;
}
double ReservoirStorage::getDurhamStorage()
{
	return durhamStorage/durhamCapacity;
}
double ReservoirStorage::getOWASAStorage()
{
	return OWASAStorage/OWASACapacity;
}
double ReservoirStorage::getRaleighStorage()
{
	return (fallsLakeSupplyStorage)/(fallsLakeSupplyCapacity);
}
double ReservoirStorage::getCaryStorage()
{
	return (caryJordanStorage)/(caryJordanCapacity);
}
double ReservoirStorage::getDurhamTransfers()
{
	return durhamRequest;
}
double ReservoirStorage::getOWASATransfers()
{
	return owasaRequest;
}
double ReservoirStorage::getRaleighTransfers()
{
	return raleighRequest;
}
double ReservoirStorage::getOWASASpillage()
{
	return OWASASpillage;
}
double ReservoirStorage::getDurhamSpillage()
{
	return durhamSpillage;
}
void ReservoirStorage::upgradeCaryTreatmentPlant(double scaling_factor)
{
	CaryTreatmentCapacity = 56*scaling_factor;
}
void ReservoirStorage::upgradeCaryTreatmentPlant2()
{
	CaryTreatmentCapacity = 64;
}
void ReservoirStorage::upgradeDurhamCaryConnection()
{
	DurhamCaryCapacity = 23;
}
void ReservoirStorage::upgradeDurhamOWASAConnection()
{
	DurhamOWASACapacity = 16;
	

}
