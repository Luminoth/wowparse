#! /bin/sh

echo "Removing compiled python code..."
find . -name \*.pyc | xargs rm -f
find . -name \*.pyo | xargs rm -f

#echo "Removing configuration files..."
#rm -f etc/*.conf

echo "Removing log files..."
rm -f *.log
rm -f *.log-psyco

#echo "Removing profiling files..."
#rm -f *.profile
#rm -f *.kgrind
