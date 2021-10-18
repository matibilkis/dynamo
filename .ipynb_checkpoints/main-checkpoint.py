import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from tqdm import tqdm
from scipy import interpolate
import argparse
import os

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--alpha", type=float, default=0.4)
parser.add_argument("--L", type=int, default=3)
parser.add_argument("--path", type=str, default="/data/uab-giq/scratch/matias/dynamo/")

args = parser.parse_args()
alpha = args.alpha
L=args.L

def P_0(eta):
    return np.max([eta, 1-eta])


def Prob(n,alpha,beta):
    p0 = np.exp(-(alpha+beta)**2)
    if n==0:
        return p0
    else:
        return 1-p0
    
def Prob_Outcome(n, alpha, beta, eta):
    q=0
    for a,et in zip([alpha, -alpha], [eta, 1-eta]):
       q+= et*Prob(n,a,beta)
    return q

def Postirior(n, alpha, beta, eta):
    po = Prob(n, alpha, beta)*eta
    po /= Prob_Outcome(n, alpha, beta, eta)
    return po

def P_1(beta, eta, alpha):
    p=0
    beta = beta[0]
    alpha = alpha[0]
    eta = eta[0]
    for n in [0,1]:
        p+= Prob_Outcome(n, alpha, beta,eta)*P_0(Postirior(n, alpha, beta,eta))
    return 1-p



def P_n(beta, eta,  model, at=1):
    p=0
    for n in [0,1]:
        p+=Prob_Outcome(n, at*alpha, beta, eta)*model(Postirior(n, at*alpha, beta, eta))
    return p


def give_bounds(eta, alpha):
    if alpha < 1:
        return [((-1.5,1.5))]
    else:
        return [((-1.5*alpha,1.5*alpha))]

    
etas_min = np.linspace(0,.5,100)
whole_etas = np.concatenate([etas_min, (1-etas_min)[::-1]])

PS = np.zeros((L,2*len(etas_min)))
BOPT = np.zeros((L,2*len(etas_min)))

for el in range(L)[::-1]:
    print(el, alpha)
    if el==L-1:
        for ind_eta, eta in enumerate(tqdm(etas_min)):
            if ind_eta == 0:
                PS[el, ind_eta] = 0
                BOPT[el,ind_eta]= alpha
            else:
                optimization = optimize.dual_annealing(P_1, x0=np.array([ BOPT[el, ind_eta-1]]), args=([eta], [alpha/np.sqrt(L)]), bounds=give_bounds(eta, alpha))
                PS[el,ind_eta]=optimization.fun
                BOPT[el,ind_eta]=optimization.x
        PS[el,len(etas_min):] = PS[el,:len(etas_min)][::-1]
        BOPT[el,len(etas_min):] = -BOPT[el,:len(etas_min)][::-1]

    else:
        model = interpolate.Rbf(whole_etas, PS[el+1], smooth=0.01, epsilon=1e-2)
        for ind_eta, eta in enumerate(tqdm(etas_min)):
            
            if ind_eta == 0:
                PS[el, ind_eta] = 0
                BOPT[el,ind_eta]= alpha
            else:
                optimization  = optimize.dual_annealing(P_n, x0=np.array([ BOPT[el, ind_eta-1]]), args=(eta, model, 1/np.sqrt(L)), bounds=give_bounds(eta, alpha))
                PS[el,ind_eta]=optimization.fun
                BOPT[el,ind_eta]=optimization.x
        PS[el,len(etas_min):] = PS[el,:len(etas_min)][::-1]
        BOPT[el,len(etas_min):] = -BOPT[el,:len(etas_min)][::-1]
    print("LAYER {}/{} DONE! \n".format(el+1, L))
    
name = args.path+"/{}/{}".format(L,alpha)
os.makedirs(name, exist_ok=True)
np.save(name+"/Ps", PS)
np.save(name+"/Bo", BOPT)

