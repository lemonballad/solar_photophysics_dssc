"""constants
   find_index"""

def constants(*args):
    """Constants stores numerous universal constants and returns the 
        desired values
        
        kb       :Boltzman constant (J/K)
        c        :Speed of light (m/s)
        hbar     :Reduced Planck's constant (Js)
        eps0     :Permitivity of free space (A^2s^4/kg/m^3)
        pi       :pi
        qe       :Fundamental charge of an electron (C)
        
        """
    
    import numpy as np
    # Define values in a searchable dictionary
    const_dict={
        'kb':1.38064852e-23,# Boltzman constant (J/K)
        'c':2.99792458e8,# Speed of light (m/s)
        'hbar':1.0545718e-34,# Reduced Planck's constant (Js)
        'eps0':8.85418782e-12,# Permitivity of free space (A^2s^4/kg/m^3)
        'pi':np.pi,#pi
        'qe':1.6021765e-19# Fundamental charge of an electron (C)
        }
        
    values = tuple([const_dict[query]
        for query in args if query in const_dict.keys()])
            
    return values


def find_index(array,query):
    """Find the index of an array
        
        array       :The data set to be searched
        query       :The value being sought
        
        """
    
    # Import any needed libraries
    import numpy as np

    index = (np.abs(array - query)).argmin()
    return index

