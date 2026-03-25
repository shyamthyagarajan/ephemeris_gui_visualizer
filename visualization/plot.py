import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Source: https://acme.byu.edu/00000179-d3f1-d7a6-a5fb-ffff6a210001/animation-pdf#:~:text=Saving%20Animations,solution%20is%20to%20use%20the

def plot_trajectories(data_map):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([0],[0],[0], color='yellow', s=250, label='Sun')
    lines = {}
    body_data = {}

    for satellite in data_map:
        t, x, y, z = data_map[satellite]
        body, = ax.plot([], [], [], marker='o', label=satellite)
        traj, = ax.plot([], [], [], alpha=0.5)
        lines[satellite] = (body, traj)
        body_data[satellite] = (x, y, z)

    first_sat = list(body_data.values())[0]
    num_frames = len(first_sat[0])

    def update(i):
        for satellite in body_data:
            x, y, z = body_data[satellite]
            body, traj = lines[satellite]
            body.set_data([x[i]], [y[i]])
            body.set_3d_properties([z[i]])
            traj.set_data(x[:i+1], y[:i+1])
            traj.set_3d_properties(z[:i+1])
        return [lines[s][j] for s in lines for j in range(2)]
    
    all_x = np.concatenate([body_data[s][0] for s in body_data])
    all_y = np.concatenate([body_data[s][1] for s in body_data])
    all_z = np.concatenate([body_data[s][2] for s in body_data])
    ax.set_xlim([all_x.min(), all_x.max()])
    ax.set_ylim([all_y.min(), all_y.max()])
    ax.set_zlim([all_z.min(), all_z.max()])

    ani = FuncAnimation(fig, update, frames=num_frames, interval=25)
    ax.legend()
    ax.set_xlabel('x (AU)')
    ax.set_ylabel('y (AU)')
    ax.set_zlabel('z (AU)')
    plt.show()

if __name__ == "__main__":
    from ephemeris.horizons import fetch_horizons_data
    data_map = fetch_horizons_data(['99942', '-64'], '2028-02-20', '2029-04-14', '60h')
    plot_trajectories(data_map)
