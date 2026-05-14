import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint

# Define the system of first-order ODEs
def system(y, t, m, c, k):
    """
    Convert second-order ODE to system of first-order ODEs
    y[0] = x(t)
    y[1] = x'(t)

    The "system" y = 
    """
    x, v = y
    dydt = [v, -(c/m)*v - (k/m)*x]
    return dydt

# Initial parameter values
m0 = 1.0
c0 = 0.5
k0 = 4.0
x0_init = 1.0
v0_init = 0.0

# Time array
t = np.linspace(0, 10, 500)

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Initial solution (damped)
y0 = [x0_init, v0_init]
sol = odeint(system, y0, t, args=(m0, c0, k0))
line_damped, = ax.plot(t, sol[:, 0], 'b-', linewidth=2, label='Damped (with c)')

# Undamped solution (c=0)
sol_undamped = odeint(system, y0, t, args=(m0, 0.0, k0))
line_undamped, = ax.plot(t, sol_undamped[:, 0], 'r--', linewidth=2, label='Undamped (c=0)')

ax.set_xlabel('Time (t)', fontsize=12)
ax.set_ylabel('Displacement x(t)', fontsize=12)
ax.set_title('Solution to m·x"(t) + c·x\'(t) + k·x(t) = 0', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.axhline(y=0, color='black', linewidth=2)

# Create sliders
ax_m = plt.axes([0.15, 0.25, 0.7, 0.02])
ax_c = plt.axes([0.15, 0.20, 0.7, 0.02])
ax_k = plt.axes([0.15, 0.15, 0.7, 0.02])
ax_x0 = plt.axes([0.15, 0.10, 0.7, 0.02])
ax_v0 = plt.axes([0.15, 0.05, 0.7, 0.02])
##test = plt.axes([0.15, 0.00, 0.7, 0.02])

slider_m = Slider(ax_m, 'm (mass)', 0.1, 5.0, valinit=m0, valstep=0.1)
slider_c = Slider(ax_c, 'c (damping)', 0.0, 5.0, valinit=c0, valstep=0.1)
slider_k = Slider(ax_k, 'k (stiffness)', 0.1, 10.0, valinit=k0, valstep=0.1)
slider_x0 = Slider(ax_x0, 'x₀ (initial pos)', -2.0, 2.0, valinit=x0_init, valstep=0.1)
slider_v0 = Slider(ax_v0, 'v₀ (initial vel)', -2.0, 2.0, valinit=v0_init, valstep=0.1)

# Update function for sliders
def update(val):
    m = slider_m.val
    c = slider_c.val
    k = slider_k.val
    x0 = slider_x0.val
    v0 = slider_v0.val
    
    y0 = [x0, v0]
    
    # Update damped solution
    sol = odeint(system, y0, t, args=(m, c, k))
    line_damped.set_ydata(sol[:, 0])
    
    # Update undamped solution (always c=0)
    sol_undamped = odeint(system, y0, t, args=(m, 0.0, k))
    line_undamped.set_ydata(sol_undamped[:, 0])
    
    # Auto-scale y-axis based on both curves
##    y_max = max(np.max(np.abs(sol[:, 0])), np.max(np.abs(sol_undamped[:, 0])))
##    if y_max > 0:
##        ax.set_ylim(-y_max*1.1, y_max*1.1)
##    else:
##        ax.set_ylim(-1, 1)
    
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_m.on_changed(update)
slider_c.on_changed(update)
slider_k.on_changed(update)
slider_x0.on_changed(update)
slider_v0.on_changed(update)

plt.show()
