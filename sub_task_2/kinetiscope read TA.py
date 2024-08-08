# Import libraries
import datetime
import decimal
import matplotlib.pyplot as mplot
import numpy as np
import os


# What day shall we use
carpe_diem = False
if carpe_diem:
    # Gather today's date
    now = datetime.datetime.now()
    today = now.strftime("%B") + " " + str(now.day) + " " + str(now.year)
    today_folder = now.strftime("%B") + " " + str(now.year) + "\\" + today
    today_nums = str(now.month) + "-" + str(now.day) + "-" + str(now.year)
else:
    # Use another date
    now = datetime.datetime.now()
    today = "November" + " " + str(1) + " " + str(now.year)
    today_folder = "November" + " " + str(now.year) + "\\" + today
    today_nums = str(11) + "-" + str(1) + "-" + str(now.year)


# Define file path to write
filepath_prefix = "C:\\Users\\tpcheshire\\Documents\\Kinetiscope Results\\"
filepath_pu_pr = filepath_prefix + today_folder + "\\Results\\Pump On"
filepath_pr = filepath_prefix + today_folder + "\\Results\\Pump Off"

#os.makedirs(filepath_pu_pr,exist_ok = True)
#os.makedirs(filepath_pr,exist_ok = True)
file_prefix = "\\"
suffix_pump_on_switch = {
        1   :   " fs Pump On " + today_nums + ".txt",
        2   :   " ps Pump On " + today_nums + ".txt",
        3   :   " ns Pump On " + today_nums + ".txt"
        }
suffix_pump_off_switch = {
        1   :   " fs Pump Off " + today_nums + ".txt",
        2   :   " ps Pump Off " + today_nums + ".txt",
        3   :   " ns Pump Off " + today_nums + ".txt"
        }
#delays = np.array([0,10,50,100,500,1000,5000,10000,50000,100000,500000,1000000])
delays = np.array([-500,-400,-300,-200,-100,0,10,20,30,40,50,60,70,80,90,
                   100,200,300,400,500,600,700,800,900,
                   1000,2000,3000,4000,5000,10000,100000,1000000])
time = np.arange(0, 1.0105e-9, 1e-14)
time = np.append(time,np.arange(2.0e-9, 5e-6, 1e-8))
ese_dOD = np.array([])
gsb_dOD = np.array([])
dems = np.array([])
ds0 = np.array([])
ds1 = np.array([])
dt1 = np.array([])
for delay in delays:
    if delay < 1e3: case = 1
    elif delay < 1e6: case = 2;delay /= 1e3
    else: case = 3;delay /= 1e6

    file_suffix_pump_on = suffix_pump_on_switch[case] 
    file_suffix_pump_off = suffix_pump_off_switch[case] 
    
    file_pu_pr = filepath_pu_pr + file_prefix + str(int(delay)) + file_suffix_pump_on
    file_pr = filepath_pr + file_prefix + str(int(delay)) + file_suffix_pump_off

    #data_pu_pr 
    time_on, ems_on, ese_on, gsb_on, s0_on, s1_on, t1_on \
        = np.genfromtxt(file_pu_pr, skip_header = 11, skip_footer = 1,
                        unpack = True, usecols = (1,2,3,4,5,6,7))
    if delay == -500:
        time_off, ems_off, ese_off, gsb_off, s0_off, s1_off, t1_off \
            = np.genfromtxt(file_pr, skip_header = 11, skip_footer = 1,
                                   unpack = True, usecols = (1,2,3,4,5,6,7))
        to = time_off
    #print((ems_off[-1],ese_off[-1],gsb_off[-1],s0_off[-1],s1_off[-1],t1_off[-1]))
    
    if delay == -500:
    #    ems_off_mat = np.interp(time, time_off,ems_off)
    #    ems_on_mat = np.interp(time, time_on,ems_on)
        s0_off_mat = np.interp(time, to,s0_off)
        s0_on_mat = np.interp(time, time_on,s0_on)
        s1_off_mat = np.interp(time, to,s1_off)
        s1_on_mat = np.interp(time, time_on,s1_on)
        t1_off_mat = np.interp(time, to,t1_off)
        t1_on_mat = np.interp(time, time_on,t1_on)
    else:
    #    ems_off_mat = np.vstack((ems_off_mat, np.interp(time, time_off,ems_off)))
    #    ems_on_mat = np.vstack((ems_on_mat, np.interp(time, time_on,ems_on)))
        s0_off_mat = np.vstack((s0_off_mat, np.interp(time, to,s0_off)))
        s0_on_mat = np.vstack((s0_on_mat, np.interp(time, time_on,s0_on)))
        s1_off_mat = np.vstack((s1_off_mat, np.interp(time, to,s1_off)))
        s1_on_mat = np.vstack((s1_on_mat, np.interp(time, time_on,s1_on)))
        t1_off_mat = np.vstack((t1_off_mat, np.interp(time, to,t1_off)))
        t1_on_mat = np.vstack((t1_on_mat, np.interp(time, time_on,t1_on)))
    #ems_off = np.interp(time, time_off,ems_off)
    #ems_on = np.interp(time, time_on,ems_on)
    #s0_off = np.interp(time, time_off,s0_off)
    #s0_on = np.interp(time, time_on,s0_on)
    #s1_off = np.interp(time, time_off,s1_off)
    #s1_on = np.interp(time, time_on,s1_on)
    #t1_off = np.interp(time, time_off,t1_off)
    #t1_on = np.interp(time, time_on,t1_on)
    dems = np.append(dems, ems_off[-1]--ems_on[-1])
    ds0 = np.append(ds0, s0_off[-1]-s0_on[-1])
    ds1 = np.append(ds1, s1_off[-1]-s1_on[-1])
    dt1 = np.append(dt1, t1_off[-1]-t1_on[-1])

    if time_off[-1] > time_on[-1]:
        time_on = np.append(time_on,time_off[-1])
        ese_on = np.append(ese_on, ese_on[-1])
        gsb_on = np.append(gsb_on, gsb_on[-1])
    elif time_off[-1] < time_on[-1]:
        time_off = np.append(time_off,time_on[-1])
        ese_off = np.append(ese_off, ese_off[-1])
        gsb_off = np.append(gsb_off, gsb_off[-1])
    elif time_off[-1] < 1.0105e-9:
        time_on = np.append(time_on,1.0105e-9)
        time_off = np.append(time_off,1.0105e-9)
        ese_on = np.append(ese_on, ese_on[-1])
        ese_off = np.append(ese_off, ese_off[-1])
        gsb_on = np.append(gsb_on, gsb_on[-1])
        gsb_off = np.append(gsb_off, gsb_off[-1])

    #ese_on = np.interp(time, time_on, ese_on)
    #ese_off = np.interp(time, time_off, ese_off)
    #gsb_on = np.interp(time, time_on, gsb_on)
    #gsb_off = np.interp(time, time_off, gsb_off)
    ndec_off = -decimal.Decimal(str(ese_off[-1])).as_tuple().exponent
    ndec_on = -decimal.Decimal(str(ese_on[-1])).as_tuple().exponent
    if ndec_off < ndec_on: ndec = ndec_off
    else: ndec = ndec_on
    ese_dOD = np.append(ese_dOD,-np.around(0*ese_off[-1], ndec) + np.around(ese_on[-1], ndec))

    ndec_off = -decimal.Decimal(str(gsb_off[-1])).as_tuple().exponent
    ndec_on = -decimal.Decimal(str(gsb_on[-1])).as_tuple().exponent
    if ndec_off < ndec_on: ndec = ndec_off
    else: ndec = ndec_on
    gsb_dOD = np.append(gsb_dOD,np.around(0*gsb_off[-1], ndec) - np.around(gsb_on[-1], ndec))


#print((ems_off[-1],ese_off[-1],gsb_off[-1],s0_off[-1],s1_off[-1],t1_off[-1]))

mplot.figure("GSB fsTA")
mplot.subplot(331)
mplot.plot(delays*1e-3,gsb_dOD*1e3,'b-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\Delta$mOD')
#mplot.xlim(0,0.01)
mplot.legend(("GSB",))
#mplot.show('GSB fsTA')
#mplot.figure("log GSB fsTA")
mplot.subplot(333)
mplot.semilogx(delays*1e-3,gsb_dOD*1e3,'b-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'log|$\tau/\tau_0$|')
mplot.ylabel(r'$\Delta$mOD')
#mplot.xlim(0,0.01)
mplot.legend(("GSB",))
mplot.subplot(337)
mplot.plot(delays*1e-3,gsb_dOD*1e3,'b-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\Delta$mOD')
mplot.xlim(-0.5,1.5)
mplot.legend(("GSB",))
mplot.subplot(339)
mplot.plot(delays*1e-3,gsb_dOD*1e3,'b-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\Delta$mOD')
mplot.ylim(-0.3309,-0.33085)
mplot.legend(("GSB",))
mplot.show('GSB fsTA')

mplot.figure("ESE fsTA")
mplot.subplot(331)
mplot.plot(delays*1e-3,ese_dOD*1e3,'r-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\Delta$mOD')
#mplot.xlim(0,0.01)
mplot.legend(("ESE",))
#mplot.show('GSB fsTA')
#mplot.figure("log GSB fsTA")
mplot.subplot(333)
mplot.semilogx(delays*1e-3,ese_dOD*1e3,'r-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'log|$\tau/\tau_0$|')
mplot.ylabel(r'$\Delta$mOD')
#mplot.xlim(0,0.01)
mplot.legend(("ESE",))
mplot.subplot(337)
mplot.plot(delays*1e-3,ese_dOD*1e3,'r-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\Delta$mOD')
mplot.xlim(-0.5,1.5)
mplot.legend(("ESE",))
mplot.subplot(339)
mplot.plot(delays*1e-3,ese_dOD*1e3,'r-')#delays*1e-3,ese_dOD,'r-',
mplot.xlabel(r'$\tau$ (ps)')
mplot.ylabel(r'$\Delta$mOD')
mplot.ylim(0.195,0.1955)
mplot.legend(("ESE",))
mplot.show('ESE fsTA')

#mplot.figure("populations")
#mplot.semilogx(delays*1e-3,ds0,'b-',delays*1e-3,ds1,'r-',delays*1e-3,dt1,'k-')
#mplot.xlabel(r'$\tau$ (ps)')
#mplot.ylabel(r'population')
##mplot.xlim(0,0.01)
#mplot.legend(("s0","s1","t1"))
#mplot.show("populations")

#mplot.figure("ems")
#mplot.plot(time_on * 1e12 , np.max(ems_on)-ems_on)
##mplot.xlim(0,1)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'count')
#mplot.show("ems")
#logtime=np.log10(time[time>0] * 1e12)
#logtime=np.append(logtime, np.log10(5.001e6))
#mplot.figure("S0 fsTA")
#mplot.contourf(logtime , delays * 1e-3, np.log10(s0_on_mat/(s1_on_mat+t1_on_mat+s0_on_mat)),20)
##mplot.xlim(0,10)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'$\tau$ (ps)')
#mplot.set_cmap('jet')
#mplot.colorbar()
#mplot.grid()
#mplot.show("S0 fsTA")

#mplot.figure("S1 fsTA")
#mplot.contourf(logtime , delays * 1e-3, s1_on_mat/(s1_on_mat+t1_on_mat+s0_on_mat),20)
##mplot.xlim(0,1)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'$\tau$ (ps)')
#mplot.set_cmap('jet')
#mplot.colorbar()
#mplot.show("S1 fsTA")

#mplot.figure("T1 fsTA")
#mplot.contourf(logtime , delays * 1e-3, t1_on_mat/(s1_on_mat+t1_on_mat+s0_on_mat),20)
##mplot.xlim(0,1)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'$\tau$ (ps)')
#mplot.set_cmap('jet')
#mplot.colorbar()
#mplot.show("T1 fsTA")

#mplot.figure("dS0 fsTA")
#mplot.contourf(time * 1e12 , delays * 1e-3, (s0_off_mat - s0_on_mat))#\
##    /(s1_off_mat - s1_on_mat+t1_off_mat - t1_on_mat + s0_off_mat - s0_on_mat),20)
##mplot.xlim(0,10)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'$\tau$ (ps)')
#mplot.set_cmap('jet')
#mplot.colorbar()
#mplot.grid()
#mplot.show("dS0 fsTA")

#mplot.figure("dS1 fsTA")
#mplot.contourf(time * 1e12 , delays * 1e-3, (s1_off_mat - s1_on_mat))#\
##    /(s1_off_mat - s1_on_mat+t1_off_mat - t1_on_mat + s0_off_mat - s0_on_mat),20)
##mplot.xlim(0,10)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'$\tau$ (ps)')
#mplot.set_cmap('jet')
#mplot.colorbar()
#mplot.grid()
#mplot.show("dS1 fsTA")

#mplot.figure("dT1 fsTA")
#mplot.contourf(time * 1e12 , delays * 1e-3, (t1_off_mat - t1_on_mat))#\
##mplot.xlim(0,10)
#mplot.xlabel(r't (ps)')
#mplot.ylabel(r'$\tau$ (ps)')
#mplot.set_cmap('jet')
#mplot.colorbar()
#mplot.grid()
#mplot.show("dT1 fsTA")
