#!/bin/bash

JAVA_ARGS="-Xmx1g -classpath MOEAFramework-1.16-Executable.jar"
NUM_SAMPLES=1008
METHOD=latin

compSols=('598' '629' '1077' '1079' '1427' '1494' '1599' '1709' '1713' '1864' '1939' '2074' '2191' '2841')

for i in ${compSols[@]}
do
	RANGES_FILENAME=LHSSampleRanges/${i}ranges.txt
	OUTPUT_FILENAME=Solution${i}_Samples.txt
	CSV_FILENAME=LHSSamples/Solution${i}_Samples.csv
	java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.SampleGenerator -m ${METHOD} -n ${NUM_SAMPLES} -p ${RANGES_FILENAME} -o ${OUTPUT_FILENAME}

	sed 's/ /,/g' ${OUTPUT_FILENAME} > ${CSV_FILENAME}
done