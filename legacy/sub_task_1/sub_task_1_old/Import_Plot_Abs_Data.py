#def Import_Abs_Data():
#    ''''''
#    # Import libraries
#    import csv
#    import matplotlib.pyplot as plt
#    import numpy as np

#    # Define file path and name to be read
#    filepath_filename='C:\\Users\\tpcheshire\\Downloads\\P Abs.csv'

#    # Initialize variables and arrays
#    count=0;wnm=np.array([]);abs_xsect=np.array([])

#    # Open file and read into arrays
#    with open (filepath_filename,newline='') as csvfile:
#        reader = csv.reader(csvfile)
#        # Loop over lines in *.csv file
#        for row in reader:
#            count=count+1
#            if not count==1 and row:
#                wnm=np.append(wnm,float(row[0]))
#                abs_xsect=np.append(abs_xsect,float(row[1]))
                
#    # Create wavelength array
#    wln=10**7/wnm
    
#    # Plot absorption spectrum v. wavelength
#    #plt.figure(0)
#    #plt.axis([min(wln),max(wln),0,1])#max(abs_xsect)]) # Define axes limits
#    #plt.plot(wln,abs_xsect/max(abs_xsect),'k-',linewidth=4) # Define plot
#    #plt.show() # Show the plot
    
#    return (wln,abs_xsect/max(abs_xsect))