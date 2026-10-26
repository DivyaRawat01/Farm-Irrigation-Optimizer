# 🌾 Farm Irrigation Optimizer

A Python-based farm irrigation planning application that uses graph algorithms and greedy scheduling to optimize water distribution across multiple fields while minimizing pipe network costs.

## 📌 Project Overview

The Farm Irrigation Optimizer helps users plan irrigation by considering soil moisture levels, field areas, available water, pipe connections, and flow rate.

The application uses **Dijkstra’s Algorithm** to find minimum-cost water routes, **Greedy Scheduling** to prioritize fields with greater moisture deficits, and **Prim’s Algorithm** to calculate the minimum spanning tree (MST) cost of the pipe network.

The project provides an interactive interface built using Streamlit, allowing users to enter farm details and view the resulting irrigation plan.

## ✨ Features

- 💧 Calculate estimated water requirements for individual fields.
- 🌱 Prioritize fields based on soil moisture deficit.
- 🛣️ Find minimum-cost routes from the water source.
- 📅 Generate an irrigation schedule based on available water and flow rate.
- 💰 Calculate the minimum spanning tree cost of the pipe network.
- 📊 Visualize the pipe network and selected MST edges.
- 🖥️ Interactive web interface using Streamlit.
- ✅ Input validation for reliable operation.

## 🛠️ Technologies Used

- **Python** — Core programming language
- **Streamlit** — Web interface
- **Pandas** — Tabular input and data handling
- **Heapq** — Priority queue operations
- **SVG** — Pipe network visualization

## 🧠 Algorithms Implemented

### 1. Dijkstra’s Algorithm
Finds the minimum-cost path from the water source to each field in the pipe network.

### 2. Greedy Scheduling
Prioritizes fields with the largest soil moisture deficit and allocates water according to availability.

### 3. Prim’s Minimum Spanning Tree
Calculates a minimum-cost spanning network connecting the source and fields, where the graph is connected.

## 📂 Project Structure

```text
Farm-Irrigation-Optimizer/
│
├── app.py                 # Streamlit user interface
├── irrigation_core.py     # Core logic and algorithms
└── README.md              # Project documentation
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.9 or newer
- pip package manager

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd Farm-Irrigation-Optimizer
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, create one containing:

```text
streamlit
pandas
```

Then run the installation command again.

### Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🚀 How to Use

1. Enter the available water in litres.
2. Specify the number of fields and pipes.
3. Enter each field’s current soil moisture, target moisture, and area.
4. Define pipe connections using `Source` and field labels such as `A`, `B`, or `C`.
5. Enter the pipe costs, water flow rate, and irrigation start time.
6. Click **Optimize** to calculate the irrigation routes, schedule, and network cost.
7. Enable **View Graph** to visualize the pipe network.

## 📥 Inputs

| Input | Description |
|---|---|
| Available Water | Total water available for irrigation, in litres |
| Number of Fields | Number of farm fields |
| Number of Pipes | Number of pipe connections |
| Soil Moisture | Current moisture percentage of a field |
| Target Moisture | Desired moisture percentage |
| Field Area | Area of the field in square metres |
| Pipe Cost | Cost assigned to a pipe connection |
| Flow Rate | Water flow in litres per hour |
| Start Time | Starting time for irrigation scheduling |

## 📊 Outputs

- **Water Routing:** Calculated route and route cost for scheduled fields.
- **Irrigation Schedule:** Field, allocated water quantity, and planned start time.
- **Infrastructure Cost:** Total cost of the minimum spanning tree.
- **Network Visualization:** Graph showing pipe connections and selected MST edges.

## ⚠️ Limitations

- Water requirements are estimated from moisture deficit and field area.
- The application does not use live weather data or physical soil sensors.
- Pipe pressure, capacity, and water losses are not modeled.
- Scheduling is based on moisture deficit rather than a complete crop-specific irrigation model.
- Results depend on the accuracy of the user-provided data.

## 🎯 Future Enhancements

- Integrate live weather forecasts.
- Add crop-specific water requirements.
- Model pipe capacity, pressure, and water loss.
- Integrate IoT soil moisture sensors.
- Add downloadable irrigation reports.
- Improve scheduling using advanced optimization algorithms.

## 🎓 Project Purpose

This project demonstrates the practical application of graph algorithms, greedy techniques, and priority queues to a real-world resource optimization problem.

## 👩‍💻 Author

**Divya Rawat**

## 📄 License

This project is available for educational and learning purposes. Add a specific open-source license if you intend to distribute it under particular reuse terms.
