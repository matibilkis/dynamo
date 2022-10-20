import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from tqdm import tqdm
from scipy import interpolate

def P(n, alpha, beta):
    p0 =np.exp(-(alpha+beta)**2)
    if n==0:
        return p0
    else:
        return 1-p0

def prob_n(n, alpha, beta,prior):
    p=0.
    for pr,ph in zip([prior, 1-prior], [1,-1]):
        p+=P(n,ph*alpha,beta)*pr
    return p

def postirior(n, alpha, beta, prior):
    pp= prior*P(n,alpha,beta)
    pp/=prob_n(n,alpha,beta, prior)
    return pp

def R(belief):
    return np.max([belief, 1-belief])

def P_1(alpha, beta, prior):
    p=0
    for n in [0,1]:
        p+=prob_n(n, alpha, beta,prior)*R(postirior(n, alpha, beta, prior))
    return 1-p
##

#beta = np.linspace(-10,10,10000)
#plt.plot(beta,[P1(alpha, b, .5) for b in beta])


priors = np.linspace(0,.5,100)
amplitudes = np.linspace(1e-5,2,100)


ps = np.zeros((len(amplitudes),len(priors)))
bopt = np.zeros((len(amplitudes),len(priors)))






give_lim= lambda eta,a : ((-2,2)) if eta>0.01 else ((a-1e-5, a+1e-5))

etas_min = np.linspace(1e-10,.5,100)
whole_etas = np.concatenate([etas_min, (1-etas_min)[::-1]])


L=3
PS = np.zeros((L,2*len(etas_min)))
BOPT = np.zeros((L,2*len(etas_min)))

for el in range(L)[::-1]:
    if el==L-1:
        for ind_eta, eta in enumerate(tqdm(etas_min)):
            optimization = optimize.minimize_scalar(P_1, args=(eta), method="bounded", bounds = give_lim(eta,alpha))#, bonuds= bounds=((-2,2)))#, options={"maxiter":10**9, "xatol":1e-35})
            PS[el,ind_eta]=optimization.fun
            BOPT[el,ind_eta]=optimization.x
        PS[el,len(etas_min):] = PS[el,:len(etas_min)][::-1]
        BOPT[el,len(etas_min):] = -BOPT[el,:len(etas_min)][::-1]

    else:
        model = interpolate.Rbf(whole_etas, PS[el+1], smooth=0.1, epsilon=1e-12)
        for ind_eta, eta in enumerate(tqdm(etas_min)):
            optimization = optimize.minimize_scalar(P_n, args=(eta, model, 1/np.sqrt(L)), method="bounded", bounds = give_lim(eta,alpha))#, bonuds= bounds=((-2,2)))#, options={"maxiter":10**9, "xatol":1e-35})
            PS[el,ind_eta]=optimization.fun
            BOPT[el,ind_eta]=optimization.x
        PS[el,len(etas_min):] = PS[el,:len(etas_min)][::-1]
#         BOPT[el,len(etas_min):] = -BOPT[el,:len(etas_min)][::-1]
#
#
#
#
# for ia,alpha in enumerate(tqdm(amplitudes)):
#     for ie,eta in enumerate(priors):
#         optimization = optimize.minimize_scalar(P1, args=(alpha, eta), method="bounded", bounds=((-2,2)))#, options={"maxiter":10**9, "xatol":1e-35})
#         ps[ia,ie] = 1.-optimization.fun
#         bopt[ia,ie] = optimization.x
#
plt.plot(ps[:,-1])
ps




###
