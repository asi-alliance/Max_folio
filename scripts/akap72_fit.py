import numpy as np
from scipy.optimize import curve_fit
data = np.array([[1.78,0.031,0],[6.32,0.064,0],[18.75,0.134,13],[41.41,0.134,0],[40.15,0.195,90],[113.28,0.664,0]])
kd=data[:,0]; ratio=data[:,1]; theta=data[:,2]
def model(X, L, k, kd0, alpha):
    kd_v,t=X; return L/(1+np.exp(-k*(kd_v-kd0)))*(1+alpha*np.sin(t*np.pi/180))
p0=[0.7,0.1,30,0.46]; bounds=([0,0,0,0],[2,1,200,2])
popt,pcov=curve_fit(model,(kd,theta),ratio,p0=p0,bounds=bounds,maxfev=10000)
preds=model((kd,theta),*popt); ss_res=np.sum((ratio-preds)**2); ss_tot=np.sum((ratio-np.mean(ratio))**2); r2=1-ss_res/ss_tot
print(f"Logistic+theta: L={popt[0]:.4f} k={popt[1]:.4f} kd0={popt[2]:.4f} alpha={popt[3]:.4f}")
print(f"R2={r2:.4f} SSR={ss_res:.6f}")
for i in range(6): print(f" kd={kd[i]:.2f} th={theta[i]:.0f} act={ratio[i]:.3f} pred={preds[i]:.3f} err={ratio[i]-preds[i]:.4f}")