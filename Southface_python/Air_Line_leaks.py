# Base for Air Leaks

n = 1.4
Ecomp = 0.90
Cdischarge = 0.61
T_1 = 297.04
T_line = 305.37
K = 1.4
P1 = 101
P2 = 933
P_line = 305.37
A_leak = 1.356 * 10**-6

R = 0.287


a = (n * R * T_1) 
b = (Ecomp * (n-1)) 
c = (((P2/P1)**(1-(1/n))) - 1)

x = a/b * c

print(a)
print(b)
print(c)
print(x)

