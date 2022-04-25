import numpy as np 

# Todo se sustenta en que las mediciones tienen una forma 
# (x,+-dx) 
# donde la primera entrada es la magnitud de la medición 
# y la segunda entrada es la incertidumbre de la medición

# ESTRUCTURA DE DATOS
# X = [(x_0,dx_0),...,(x_n,dx_n)]      <------------------------ ¡IMPORTANTE!
# Y = [(y_0,dy_0),...,(y_n,dy_n)]



def obtener_numero_digitos(x,y):
    ind_pto_a  = str(float(x[0])).index(".")
    ind_pto_b  = str(float(y[0])).index(".")
    num_digs_a = len(str(x[0])[ind_pto_a:])-1
    num_digs_b = len(str(y[0])[ind_pto_b:])-1
    return(min([num_digs_a,num_digs_b]))

# convertir todos los numeros a flotantes

def suma_pvdfpcldo_v(x,y):
    return((np.round(x[0]+y[0],3),np.round(x[1]+y[1],3)))

def suma_pvdfpcldo_c(x,y):
    #n = int(x[1]/2)
    return((np.round(x[0]+y[0],15),np.round(x[1]+y[1],12)))

def resta(x,y):
    ind_de_redondeo = obtener_numero_digitos(x,y)
    return((np.round(x[0]-y[0],ind_de_redondeo),x[1]+y[1]))
    
def multiplicacion_dos_mediciones(x,y):
    ind_de_redondeo = obtener_numero_digitos(x,y)
    return((np.round(x[0]*y[0],ind_de_redondeo),x[0]*y[1]+x[1]*y[0]))
    
def division(x,y): #x/y
    ind_de_redondeo = obtener_numero_digitos(x,y)
    return((np.round(x[0]/y[0],ind_de_redondeo),(x[0]*y[1]+y[0]*x[1])/(y[0]**2)))

def constante_entre_medicion(cte,x): #c/x
    return((cte/x[0],np.abs(-cte/(x[0]**2))*x[1]))

def multiplicacion_cte_medicion(cte,x):
    ind_pto_a  = str(float(x[0])).index(".")
    num_digs_a = len(str(x[0])[ind_pto_a:])-1
    return((np.round(x[0]*cte,num_digs_a),x[1]))

def multiplicacion_cte_medicion_c(cte,x):
    return((x[0]*cte,x[1]))

def medicion_a_la_n(x,n):
    ind_pto_a  = str(float(x[0])).index(".")
    num_digs_a = len(str(x[0])[ind_pto_a:])-1
    return((np.round(x[0]**n,np.abs(n)*x[0]**(n-1)*x[1]),x[1]))

def pendiente_min_ord_max(Lp1,Lp2):
    # LP1 = [(x1,dx1),(y1,dy1)]
    # LP2 = [(x2,dx2),(y2,dy2)]
    num1 = (Lp2[1][0]-Lp2[1][1])-(Lp1[1][0]+Lp1[1][1])
    den1 = (Lp2[0][0]+Lp2[0][1])-(Lp1[0][0]-Lp1[0][1])
    #print(num1,den1)
    num2 = (Lp2[1][0]-Lp2[1][1])-(Lp1[1][0]+Lp1[1][1])
    den2 = (Lp2[0][0]-Lp2[0][1])-(Lp1[0][0]+Lp1[0][1])
    #print(num2,den2)
    b1 = (Lp1[1][0]+Lp1[1][1])-(num1/den1)*(Lp1[0][0]-Lp1[0][1])
    b2 = (Lp1[1][0]+Lp1[1][1])-(num2/den2)*(Lp1[0][0]+Lp1[0][1])
    #print("min pendiente y max ord",min([num1/den1,num2/den2]),max([b1,b2]))
    return(min([num1/den1,num2/den2]),max([b1,b2]))

def pendiente_max_ord_min(Lp1,Lp2):
    # LP1 = [(x1,dx1),(y1,dy1)]
    # LP2 = [(x2,dx2),(y2,dy2)]
    num1 = (Lp2[1][0]+Lp2[1][1])-(Lp1[1][0]-Lp1[1][1])
    den1 = (Lp2[0][0]-Lp2[0][1])-(Lp1[0][0]+Lp1[0][1])
    #print(num1/den1)
    num2 = (Lp2[1][0]-Lp2[1][1])-(Lp1[1][0]+Lp1[1][1])
    den2 = (Lp2[0][0]-Lp2[0][1])-(Lp1[0][0]+Lp1[0][1])
    #print(num2/den2)
    b1 = (Lp1[1][0]-Lp1[1][1])-(num1/den1)*(Lp1[0][0]+Lp1[0][1])
    b2 = (Lp1[1][0]+Lp1[1][1])-(num2/den2)*(Lp1[0][0]+Lp1[0][1])
    #print("max pendiente y min ord",max([num1/den1,num2/den2]),min([b1,b2]))
    return(max([num1/den1,num2/den2]),min([b1,b2]))

#flta pendiente max



def calcula_min_y_max_pendiente_y_ordenada(X, Y):
    # X = [(x_0,dx_0),...,(x_n,dx_n)]
    # Y = [(y_0,dy_0),...,(y_n,dy_n)]
    # m = (yf-yi)/(xf-xi) <--- pendiente 
    # b = yi-m*xi <--- ordenada al origen 
    
    tot_meds = len(X)
    Pendientes = []
    Ordenadas  = []
    for i in range(tot_meds): 
        punto = [X[i],Y[i]]
        for j,k in zip(X[i+1:],Y[i+1:]):
            #cambiar la obtencion de la minima pendiente y maxima pendiente y de las ordenadas.
            punto_despues = [j,k]
            #print(punto,punto_despues)
            Pendientes.append(pendiente_min_ord_max(punto,punto_despues)[0])
            Pendientes.append(pendiente_max_ord_min(punto,punto_despues)[0])
            Ordenadas.append(pendiente_max_ord_min(punto,punto_despues)[1])
            Ordenadas.append(pendiente_min_ord_max(punto,punto_despues)[1])
    min_pend,max_pend = min(Pendientes),max(Pendientes)
    min_ord,max_ord   = min(Ordenadas) ,max(Ordenadas)
    return(min_pend,max_pend,min_ord,max_ord)

def calcula_ajuste_lineal(X, Y):
    X_aux = [i[0] for i in X]
    Y_aux = [i[0] for i in Y]
    n = len(X)
    sxy = np.sum([i*j for i,j in zip(X_aux,Y_aux)])
    sx  = np.sum(X_aux)
    sy  = np.sum(Y_aux)
    sxx = np.sum([i*j for i,j in zip(X_aux,X_aux)])
    num_m = n*sxy-(sx)*(sy)
    den_m = n*sxx-(sx)**2
    num_b = (sxx)*(sy)-(sxy)*(sx)
    den_b = n*sxx-(sx)**2
    m = num_m/den_m
    b = num_b/den_b
    RC = 1 - sxy**2/(sx**2*sy**2)
    return(m,b,RC)

def calcula_m_o_inc_m_y_ord(X, Y):
    min_pend, max_pend, min_ord, max_ord = calcula_min_y_max_pendiente_y_ordenada(X,Y)
    m_ajus, o_ajus, rc = calcula_ajuste_lineal(X,Y)
    incerti_pend = max([np.abs(m_ajus-min_pend),np.abs(m_ajus-max_pend)])
    incerti_ord = max([np.abs(o_ajus-min_ord),np.abs(o_ajus-max_ord)])
    return(m_ajus, o_ajus, incerti_pend,incerti_ord, rc)

def promedio_mediciones_v(lista):
    n = len(lista)
    v_prom = (0,0)
    for i in lista:
        v_prom = suma_pvdfpcldo_v(v_prom,i)
    v_prom_div = multiplicacion_cte_medicion(1/n,v_prom)
    return(v_prom_div)

def promedio_mediciones_c(lista):
    n = len(lista)
    v_prom = (0,0)
    for i in lista:
        v_prom = suma_pvdfpcldo_c(v_prom,i)
    v_prom_div = multiplicacion_cte_medicion_c(1/n,v_prom)
    return(v_prom_div)



            
