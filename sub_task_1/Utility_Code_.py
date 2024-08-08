#"""
#    Constants
#    Hz_to_fHz
#    J_to_wavenumber
#    Line_Broadening_Function
#    m_to_cm
#    s_to_fs
#    wavenumber_to_J"""

#def Constants(*args):
#    """Constants stores numerous universal constants and returns the 
#        desired values
        
#        kb       :Boltzman constant (J/K)
#        c        :Speed of light (m/s)
#        hbar     :Reduced Planck's constant (Js)
#        eps0     :Permitivity of free space (A^2s^4/kg/m^3)
#        pi       :pi
#        qe       :Fundamental charge of an electron (C)
        
#        """
    
#    import numpy as np
#    # Define values in a searchable dictionary
#    const_dict={
#        'kb':1.38064852e-23,# Boltzman constant (J/K)
#        'c':2.99792458e8,# Speed of light (m/s)
#        'hbar':1.0545718e-34,# Reduced Planck's constant (Js)
#        'eps0':8.85418782e-12,# Permitivity of free space (A^2s^4/kg/m^3)
#        'pi':np.pi,#pi
#        'qe':1.6021765e-19# Fundamental charge of an electron (C)
#        }
        
#    values = tuple([const_dict[query]
#        for query in args if query in const_dict.keys()])
            
#    return values

#def Hz_to_fHz(value):
#    """Hz_to_fHz is a simple conversion"""
    
#    return value*1e-15

#def J_to_wavenumber(value):
#    """J_to_wavenumbers is a conversion incorporating Planck's reduced constant into
#        the object. This conversion reduces hbar to 1 / 2 / pi / c."""
#    import Utility_Code_ as uc
    
#    c,hbar,pi = Constants('c','hbar','pi')
#    c = uc.m_to_cm(uc.Hz_to_fHz(c))
#    hbar = uc.s_to_fs(hbar)
#    return value / 2 / pi / c / hbar 
        
#def Line_Broadening_Function(dk,kT,LAM,lam,Var,wk,t):
#    """Line_Broadening_Function calculates points of Kubo's function for
#        the response function.
        
#        dk:         Dimensionless displacement for mode k
#        kT:         Temperature (cm^-1)
#        LAM:        Inverse time scale of bath (fHz)
#        lam:        Reorganization energy (fHz)
#        Var:        Line width parameter ==> Delta**2 = 2 * lambda * kT / hbar
#                    (fHz^2)
#        wk:         Frequency of mode k
#        t:          time axis (fs)
#    """
#    import Utility_Code_ as uc
#    import numpy as np
    
#    c,hbar,pi = Constants('c','hbar','pi')
#    c = uc.m_to_cm(uc.Hz_to_fHz(c))
#    hbar = uc.J_to_wavenumber(uc.s_to_fs(hbar))
    
    
#    # Compute overdamped contribution to line broadening function
#    gexp = np.exp(-LAM * t) + LAM * t - 1
#    god = (Var / LAM**2 - 1j * lam / LAM) * gexp 
    
#    # Compute underdamped contribution to line broadening function
#    nmode = np.size(wk)
#    gud = 0
#    for k in list(range(0,nmode)):
#        if wk[k]!=0:
#            Sk = dk[k]**2 / 2
#            coth = np.tanh(hbar * wk[k] / 2 / kT)**-1
#            gud = gud + Sk * (coth * (1 - np.cos(wk[k] * t)) + 
#                1j * (np.sin(wk[k] * t) - 0 * wk[k] * t))

#    # Combine overdamped and underdamped contributions to line broadening function
#    g = god + gud
    
#    return g

#def m_to_cm(value):
#    """m_to_cm is a simple conversion"""
#    return value*1e2

#def s_to_fs(value):
#    """s_to_fs is a simple conversion"""
#    return value*1e15

#def wavenumber_to_J(value):
#    """wavenumber_to_J is a conversion removes Planck's reduced constant from
#        the object. This conversion returns hbar to its universal value."""
#    import Utility_Code_ as uc
    
#    c,hbar,pi = Constants('c','hbar','pi')
#    c = uc.m_to_cm(uc.Hz_to_fHz(c))
#    hbar = uc.s_to_fs(hbar)
#    return value * 2 * pi * c * hbar 