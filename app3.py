# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 01:13:54 2021

@author: Pranav
"""


import streamlit as st
import random

def main():
    st.title('Design of Springs')
    st.header('Made with :heart: by Pranav Garg')
    
    st.subheader('Input Section')
    
    max_force = st.number_input("Enter the value of maximum force(in N).",min_value=None, max_value=None, value=200.0, step=None,)
    min_force = st.number_input("Enter the value of minimum force(in N).",min_value=None, max_value=None, value=0.0, step=None,)
    disp_max = st.number_input("Enter the displacement(in mm) at maximum force.",1.0,200000.0,step =1.)
    G_values = {'music_wire' : 82.3, 'hard_drawn_wire' : 80.5, 'chrome_vanadium_wire': 77.2, 'chrome_silicon_wire' : 77.2, 'stainless_steel' : 69, 'phoshphor_bronze_wire': 41.4}
    A_values = {'music_wire' : 2211, 'hard_drawn_wire' : 1783, 'chrome_vanadium_wire': 2005, 'chrome_silicon_wire' : 1974, 'stainless_steel' : 2065, 'phoshphor_bronze_wire': 913}
    m_values = {'music_wire' : 0.145, 'hard_drawn_wire' : 0.190, 'chrome_vanadium_wire': 0.168, 'chrome_silicon_wire' : 0.108, 'stainless_steel' : 0.263, 'phoshphor_bronze_wire': 0.028}
    stiffness = abs(max_force - min_force)/disp_max
    if stiffness ==0:
        st.markdown("The input values make the spring stiffness zero which is not possible. Please try again with valid values.")
    else:
        ans = {}
        print('\n')
        max_force = 1.15*abs(max_force)
        for C in range(7,13):
            K = float(4*C-1)/(4*C-4) + 0.615/C
            const = 8*K*max_force*C/3.14
            for d in range(1,101):
                max_shear_stress = const/(d*d)
                if len(ans)==6:
                    break
                for material in G_values:
                    if material in ans:
                        break
                    else:
                        S_s = A_values[material]/(d**(m_values[material]))
                        if max_shear_stress < S_s:
                            ans[material] = (C,d, S_s)
        if not ans:
            st.markdown("No spring found. Please try again with different input conditions.")
        else:
            material, tup = random.choice(list(ans.items()))
            D = tup[0]*tup[1]
            active_turns = int(G_values[material]*tup[1]/(8*tup[0]*stiffness)*100)
            total_turns = active_turns+2
            solid_length = total_turns * tup[0]
            free_length = solid_length + 1.15*disp_max
            buckling_check = free_length/D
            
            st.subheader('Output Section')
            st.markdown("PROPERTIES OF THE SPRING:")
            st.markdown(f"Material : {material}")
            st.markdown(f"Wire Diameter : {tup[1]} mm")
            st.markdown(f"Mean Coil Diameter : {D} mm ")
            st.markdown(f'Total Turns : {total_turns}')
            st.markdown(f'Solid Length : {solid_length} mm')
            st.markdown(f'Free Length : {free_length} mm')
            if buckling_check<2.6:
                st.markdown("The spring does not buckle. Guide is not required.")
            else:
                st.markdown("The spring buckles. Guide is required.")
            F_m = (max_force + min_force)/2.0
            F_a = (max_force - min_force)/2.0
            K_a = float(4*tup[0]-1)/(4*tup[0]-4) + 0.615/tup[0]
            K_m = 1 + 0.5/tup[0]
            tau_m = K_m*8*F_m*D/(3.14*(tup[0]**3))
            tau_a = K_a*8*F_a*D/(3.14*(tup[0]**3))
            S_se = 0.22*tup[2]
            S_sy = 0.45*tup[2]
            const2 = (2*tau_a*(S_sy - 0.5*S_se))/S_se + tau_m
            FoS = S_sy/const2
            st.markdown(f"Factor of safety of the spring for fatigue loading is {round(FoS,2)}")
            

    
if __name__ =="__main__":
    main()